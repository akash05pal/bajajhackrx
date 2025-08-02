import pinecone
import openai
from typing import List, Dict, Any
from app.models import DocumentChunk, SearchResult
from config import settings
import asyncio
import time

class VectorStore:
    def __init__(self):
        self.index = None
        self.fallback_search = None
        self.initialize_pinecone()
    
    def initialize_pinecone(self):
        """Initialize Pinecone connection"""
        try:
            if settings.pinecone_api_key:
                # Try new Pinecone API first
                try:
                    from pinecone import Pinecone
                    pc = Pinecone(api_key=settings.pinecone_api_key)
                    
                    # Check if index exists
                    indexes = pc.list_indexes()
                    index_names = [idx.name for idx in indexes]
                    
                    if settings.pinecone_index_name in index_names:
                        print(f"✅ Using existing Pinecone index: {settings.pinecone_index_name}")
                        self.index = pc.Index(settings.pinecone_index_name)
                    else:
                        print(f"⚠️ Index '{settings.pinecone_index_name}' not found. Using fallback search.")
                        self.index = None
                        
                except (ImportError, AttributeError):
                    # Fallback to legacy API
                    print("Using legacy Pinecone API")
                    pinecone.init(
                        api_key=settings.pinecone_api_key,
                        environment=settings.pinecone_environment
                    )
                    
                    if settings.pinecone_index_name in pinecone.list_indexes():
                        print(f"✅ Using existing Pinecone index: {settings.pinecone_index_name}")
                        self.index = pinecone.Index(settings.pinecone_index_name)
                    else:
                        print(f"⚠️ Index '{settings.pinecone_index_name}' not found. Using fallback search.")
                        self.index = None
            else:
                print("Warning: Pinecone API key not provided. Using fallback search.")
        except Exception as e:
            print(f"Warning: Pinecone initialization failed: {e}. Using fallback search.")
    
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for text using OpenAI"""
        try:
            if not settings.openai_api_key:
                raise Exception("OpenAI API key not provided")
            
            client = openai.OpenAI(api_key=settings.openai_api_key)
            
            embeddings = []
            for text in texts:
                response = client.embeddings.create(
                    model=settings.embedding_model,
                    input=text
                )
                embeddings.append(response.data[0].embedding)
            
            return embeddings
        except Exception as e:
            raise Exception(f"Failed to get embeddings: {str(e)}")
    
    async def store_documents(self, chunks: List[DocumentChunk]) -> bool:
        """Store document chunks in vector database"""
        try:
            if not self.index:
                print("Warning: Using fallback storage (no vector database)")
                # Initialize fallback search
                from app.fallback_search import FallbackSearch
                self.fallback_search = FallbackSearch()
                self.fallback_search.add_documents(chunks)
                return True
            
            # Get embeddings for chunks
            texts = [chunk.content for chunk in chunks]
            embeddings = await self.get_embeddings(texts)
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector = {
                    "id": f"chunk_{i}_{int(time.time())}",
                    "values": embedding,
                    "metadata": {
                        "content": chunk.content,
                        **chunk.metadata
                    }
                }
                vectors.append(vector)
            
            # Upsert to Pinecone
            self.index.upsert(vectors=vectors)
            print(f"✅ Stored {len(vectors)} chunks in Pinecone")
            return True
            
        except Exception as e:
            print(f"Warning: Vector storage failed: {e}")
            # Initialize fallback search
            from app.fallback_search import FallbackSearch
            self.fallback_search = FallbackSearch()
            self.fallback_search.add_documents(chunks)
            return False
    
    async def search_similar(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for similar documents using vector similarity"""
        try:
            if not self.index:
                return await self._fallback_search(query, top_k)
            
            # Get query embedding
            query_embedding = await self.get_embeddings([query])
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding[0],
                top_k=top_k,
                include_metadata=True
            )
            
            # Convert to SearchResult objects
            search_results = []
            for match in results.matches:
                search_results.append(SearchResult(
                    content=match.metadata.get("content", ""),
                    score=match.score,
                    metadata=match.metadata
                ))
            
            return search_results
            
        except Exception as e:
            print(f"Warning: Vector search failed: {e}")
            return await self._fallback_search(query, top_k)
    
    async def _fallback_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Fallback search using simple text matching"""
        from app.fallback_search import FallbackSearch
        
        # Use fallback search if available
        if hasattr(self, 'fallback_search') and self.fallback_search:
            return self.fallback_search.search(query, top_k)
        
        # Return empty results if no fallback available
        return []
    
    def clear_index(self):
        """Clear all vectors from the index"""
        try:
            if self.index:
                # Delete all vectors (this is a simple approach)
                # In production, you might want to keep track of vector IDs
                print("Warning: Index clear not implemented for Pinecone")
        except Exception as e:
            print(f"Warning: Failed to clear index: {e}") 