import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    api_key: str = "d809808918dd2a7d6b11fa5b23fa01e3abf9814dd225582d4d5674dc2138be0b"
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None  # Added Groq support
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "bajaj-documents"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Model Configuration
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-3.5-turbo"  # Changed from gpt-4 to gpt-3.5-turbo
    max_tokens: int = 2000  # Reduced for faster responses
    temperature: float = 0.1
    
    # Document Processing - Optimized for speed
    chunk_size: int = 800  # Reduced from 1000
    chunk_overlap: int = 100  # Reduced from 200
    max_document_size: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 