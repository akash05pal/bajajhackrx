import asyncio
import time
from typing import List, Dict, Any
from app.document_processor import DocumentProcessor
from app.vector_store import VectorStore
from app.llm_processor import LLMProcessor
from app.models import QueryRequest, QueryResponse
from config import settings

class QueryEngine:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.llm_processor = LLMProcessor()
        self.document_cache = {}
    
    async def process_query_request(self, request: QueryRequest) -> QueryResponse:
        """Process a query request with optimized performance"""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = request.documents
            if cache_key in self.document_cache:
                print("✅ Using cached document")
                chunks = self.document_cache[cache_key]
            else:
                # Process document with smaller chunks for faster processing
                print("📄 Processing document...")
                chunks = await self.document_processor.process_document(request.documents)
                self.document_cache[cache_key] = chunks
                print(f"✅ Document processed: {len(chunks)} chunks")
            
            # Store documents in vector store
            await self.vector_store.store_documents(chunks)
            
            # Process questions in parallel for faster response
            answers = []
            contexts = []
            
            # Get contexts for all questions first
            for question in request.questions:
                search_results = await self.vector_store.search_similar(question, top_k=3)  # Reduced from 5 to 3
                context = "\n\n".join([result.content for result in search_results])
                contexts.append(context)
            
            # Generate answers in parallel
            if len(request.questions) <= 3:
                # For small number of questions, process sequentially for better quality
                for i, question in enumerate(request.questions):
                    answer = await self.llm_processor.generate_answer(question, contexts[i])
                    answers.append(answer)
            else:
                # For multiple questions, use batch processing
                answers = await self.llm_processor.generate_answers_batch(request.questions, contexts)
            
            processing_time = time.time() - start_time
            print(f"⏱️ Total processing time: {processing_time:.2f} seconds")
            
            # Return only answers as required by competition
            return QueryResponse(answers=answers)
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            return QueryResponse(
                answers=["Error processing request"] * len(request.questions)
            )
    
    async def process_single_query(self, question: str, document_url: str) -> str:
        """Process a single query for faster response"""
        try:
            # Check cache
            if document_url in self.document_cache:
                chunks = self.document_cache[document_url]
            else:
                chunks = await self.document_processor.process_document(document_url)
                self.document_cache[document_url] = chunks
            
            await self.vector_store.store_documents(chunks)
            search_results = await self.vector_store.search_similar(question, top_k=2)  # Reduced for speed
            context = "\n\n".join([result.content for result in search_results])
            
            return await self.llm_processor.generate_answer(question, context)
            
        except Exception as e:
            print(f"❌ Error in single query: {e}")
            return f"Error: {str(e)}"
    
    async def health_check(self) -> Dict[str, Any]:
        """Check system health"""
        return {
            "status": "healthy",
            "llm_available": self.llm_processor.client is not None or self.llm_processor.groq_client is not None,
            "vector_store_available": self.vector_store.index is not None or self.vector_store.fallback_search is not None,
            "cache_size": len(self.document_cache)
        } 