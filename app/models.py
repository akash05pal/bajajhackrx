from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

class DocumentChunk(BaseModel):
    """Represents a chunk of document text"""
    content: str
    metadata: Dict[str, Any] = {}

class SearchResult(BaseModel):
    """Represents a search result"""
    content: str
    score: float
    metadata: Dict[str, Any] = {}

class QueryRequest(BaseModel):
    """Request model for document queries"""
    documents: str  # URL to the document
    questions: List[str]  # List of questions to answer

class QueryResponse(BaseModel):
    """Response model for document queries"""
    answers: List[str]  # List of answers corresponding to questions 