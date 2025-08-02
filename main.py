import os
import time
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.models import QueryRequest, QueryResponse
from app.query_engine import QueryEngine
from app.auth import verify_api_key
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="HackRx 6.0 - LLM-Powered Document Query System",
    description="Intelligent Query-Retrieval System for large documents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy initialization for QueryEngine
_query_engine = None

def get_query_engine():
    global _query_engine
    if _query_engine is None:
        _query_engine = QueryEngine()
    return _query_engine

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "HackRx 6.0 - LLM-Powered Document Query System",
        "version": "1.0.0",
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    query_engine = get_query_engine()
    health_status = await query_engine.health_check()
    return health_status

# Main competition endpoint
@app.post("/hackrx/run", response_model=QueryResponse)
async def run_query(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Main endpoint for HackRx 6.0 competition
    Processes documents and answers questions
    """
    try:
        query_engine = get_query_engine()
        response = await query_engine.process_query_request(request)
        
        # Return response with only answers
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

# Configuration endpoint
@app.get("/api/v1/config")
async def get_config(api_key: str = Depends(verify_api_key)):
    """Get system configuration"""
    return {
        "llm_model": settings.llm_model,
        "embedding_model": settings.embedding_model,
        "chunk_size": settings.chunk_size,
        "max_tokens": settings.max_tokens,
        "has_openai_key": bool(settings.openai_api_key),
        "has_groq_key": bool(settings.groq_api_key),
        "has_pinecone_key": bool(settings.pinecone_api_key)
    }

# Cache info endpoint
@app.get("/api/v1/cache/info")
async def get_cache_info(api_key: str = Depends(verify_api_key)):
    """Get cache information"""
    query_engine = get_query_engine()
    return {
        "cache_size": len(query_engine.document_cache),
        "cached_documents": list(query_engine.document_cache.keys())
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get("PORT", settings.port))
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=port,
        reload=settings.debug
    ) 