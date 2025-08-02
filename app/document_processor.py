import requests
import PyPDF2
import io
from docx import Document
from typing import List, Dict, Any
import re
import mimetypes
from app.models import DocumentChunk
from config import settings

class DocumentProcessor:
    def __init__(self):
        self.supported_extensions = ['.pdf', '.docx', '.doc']
    
    async def download_document(self, url: str) -> bytes:
        """Download document from URL"""
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' in content_type or 'application/octet-stream' in content_type:
                return response.content
            elif 'word' in content_type or 'document' in content_type:
                return response.content
            else:
                # Try to determine from URL
                if any(ext in url.lower() for ext in self.supported_extensions):
                    return response.content
                else:
                    raise Exception(f"Unsupported content type: {content_type}")
                    
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to download document: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to download document: {str(e)}")
    
    def extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF content"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_text_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX content"""
        try:
            doc = Document(io.BytesIO(content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text or text.strip() == "":
            raise Exception("No text content found in document")
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}]', '', text)
        return text.strip()
    
    def chunk_text(self, text: str) -> List[DocumentChunk]:
        """Split text into chunks for processing"""
        if not text or len(text.strip()) == 0:
            raise Exception("No text content available for chunking")
            
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > settings.chunk_size:
                if current_chunk:
                    chunk_text = " ".join(current_chunk)
                    chunks.append(DocumentChunk(
                        content=chunk_text,
                        metadata={
                            "chunk_id": len(chunks),
                            "word_count": len(current_chunk),
                            "char_count": len(chunk_text)
                        }
                    ))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        # Add the last chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(DocumentChunk(
                content=chunk_text,
                metadata={
                    "chunk_id": len(chunks),
                    "word_count": len(current_chunk),
                    "char_count": len(chunk_text)
                }
            ))
        
        if not chunks:
            raise Exception("No valid chunks created from document")
            
        return chunks
    
    async def process_document(self, url: str) -> List[DocumentChunk]:
        """Process document from URL and return chunks"""
        try:
            # Download document
            content = await self.download_document(url)
            
            # Determine file type and extract text
            if url.lower().endswith('.pdf') or 'pdf' in url.lower():
                text = self.extract_text_from_pdf(content)
            elif url.lower().endswith(('.docx', '.doc')) or 'word' in url.lower():
                text = self.extract_text_from_docx(content)
            else:
                # Try to detect from content
                if content.startswith(b'%PDF'):
                    text = self.extract_text_from_pdf(content)
                else:
                    raise Exception("Unsupported document format. Please provide a PDF or DOCX file.")
            
            # Clean text
            text = self.clean_text(text)
            
            # Chunk text
            chunks = self.chunk_text(text)
            
            return chunks
            
        except Exception as e:
            raise Exception(f"Document processing failed: {str(e)}") 