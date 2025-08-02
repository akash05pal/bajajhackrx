#!/usr/bin/env python3
"""
Test Pinecone connection
"""

import os
from pinecone import Pinecone

def test_pinecone():
    """Test Pinecone connection"""
    try:
        # Get API key from environment
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            print("❌ PINECONE_API_KEY not set in environment")
            print("Please set your Pinecone API key:")
            print("export PINECONE_API_KEY=your_api_key_here")
            return False
        
        print("🔍 Testing Pinecone connection...")
        
        # Initialize Pinecone
        pc = Pinecone(api_key=api_key)
        print("✅ Pinecone client initialized successfully")
        
        # List indexes
        indexes = pc.list_indexes()
        index_names = [idx.name for idx in indexes]
        print(f"📋 Available indexes: {index_names}")
        
        # Test with a specific index
        test_index_name = "bajaj-documents"
        if test_index_name in index_names:
            print(f"✅ Index '{test_index_name}' exists")
            index = pc.Index(test_index_name)
            print("✅ Successfully connected to index")
            return True
        else:
            print(f"⚠️ Index '{test_index_name}' not found")
            print("Creating test index...")
            pc.create_index(
                name=test_index_name,
                dimension=1536,
                metric="cosine"
            )
            print(f"✅ Created index '{test_index_name}'")
            return True
            
    except Exception as e:
        print(f"❌ Pinecone test failed: {e}")
        return False

if __name__ == "__main__":
    test_pinecone() 