#!/usr/bin/env python3
"""
Demo script for HackRx 6.0 LLM-Powered Intelligent Query–Retrieval System
"""

import asyncio
import time
from app.query_engine import QueryEngine
from app.models import QueryRequest

async def demo():
    """Run a demonstration of the system"""
    print("🚀 HackRx 6.0 - LLM-Powered Intelligent Query–Retrieval System")
    print("=" * 70)
    
    # Initialize query engine
    print("🔧 Initializing query engine...")
    query_engine = QueryEngine()
    
    # Health check
    print("\n🏥 Performing health check...")
    health_status = await query_engine.health_check()
    print(f"Health Status: {health_status}")
    
    # Sample request
    print("\n📄 Processing sample document and queries...")
    
    request = QueryRequest(
        documents="https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        questions=[
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?"
        ]
    )
    
    # Process request
    start_time = time.time()
    response = await query_engine.process_query_request(request)
    end_time = time.time()
    
    print(f"\n⏱️ Processing time: {end_time - start_time:.2f} seconds")
    print(f"📝 Number of answers: {len(response.answers)}")
    
    # Display results
    print("\n📋 Results:")
    print("-" * 50)
    for i, (question, answer) in enumerate(zip(request.questions, response.answers)):
        print(f"\nQ{i+1}: {question}")
        print(f"A{i+1}: {answer}")
        print("-" * 50)
    
    # Cache info
    print("\n💾 Cache information:")
    cache_info = query_engine.get_cache_info()
    print(f"Cached documents: {cache_info['cached_documents']}")
    print(f"Document URLs: {cache_info['document_urls']}")
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(demo()) 