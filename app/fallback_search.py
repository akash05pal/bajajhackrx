import re
from typing import List
from app.models import DocumentChunk, SearchResult

class FallbackSearch:
    def __init__(self):
        self.documents = []
    
    def add_documents(self, chunks: List[DocumentChunk]):
        """Add document chunks to the search index"""
        self.documents = chunks
    
    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for relevant content using simple text matching"""
        if not self.documents:
            return []
        
        # Convert query to lowercase for better matching
        query_lower = query.lower()
        
        # Define search terms for common insurance queries
        search_terms = {
            'grace period': ['grace period', 'grace', 'payment grace', 'thirty days', '30 days'],
            'premium payment': ['premium payment', 'premium', 'payment'],
            'waiting period': ['waiting period', 'waiting', 'period'],
            'maternity': ['maternity', 'pregnancy', 'delivery'],
            'hospital': ['hospital', 'hospitalization'],
            'coverage': ['coverage', 'cover', 'benefit'],
            'exclusion': ['exclusion', 'exclude', 'not covered'],
            'claim': ['claim', 'claiming', 'claimant'],
            'renewal': ['renewal', 'renew', 'continue'],
            'policy': ['policy', 'insurance', 'mediclaim']
        }
        
        # Find relevant search terms
        relevant_terms = []
        for category, terms in search_terms.items():
            if any(term in query_lower for term in terms):
                relevant_terms.extend(terms)
        
        # If no specific terms found, use the original query
        if not relevant_terms:
            relevant_terms = [query_lower]
        
        # Score each document chunk
        scored_chunks = []
        for chunk in self.documents:
            content_lower = chunk.content.lower()
            score = 0
            
            # Calculate score based on term frequency and relevance
            for term in relevant_terms:
                if term in content_lower:
                    # Count occurrences
                    count = content_lower.count(term)
                    score += count * 0.5
                    
                    # Bonus for exact phrase matches
                    if term in query_lower and term in content_lower:
                        score += 2.0
                    
                    # Bonus for proximity to important words
                    if any(word in content_lower for word in ['grace', 'period', 'premium', 'payment']):
                        score += 1.0
                    
                    # Special bonus for grace period specific terms
                    if 'grace period' in content_lower and 'grace period' in query_lower:
                        score += 5.0
                    
                    # Bonus for exact definitions
                    if 'means' in content_lower and any(term in content_lower for term in ['grace', 'period']):
                        score += 3.0
            
            if score > 0:
                scored_chunks.append((chunk, score))
        
        # Sort by score and return top results
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for chunk, score in scored_chunks[:top_k]:
            # Normalize score to 0-1 range
            normalized_score = min(score / 10.0, 1.0)
            results.append(SearchResult(
                content=chunk.content,
                score=normalized_score,
                metadata=chunk.metadata
            ))
        
        return results 