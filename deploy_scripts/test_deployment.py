#!/usr/bin/env python3
"""
Deployment Test Script for HackRx 6.0
Tests all critical components before deployment
"""

import asyncio
import sys
import os
from pathlib import Path

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import groq
        print("✅ Groq imported successfully")
    except ImportError as e:
        print(f"❌ Groq import failed: {e}")
        return False
    
    try:
        import pinecone
        print("✅ Pinecone imported successfully")
    except ImportError as e:
        print(f"❌ Pinecone import failed: {e}")
        return False
    
    try:
        import httpx
        print("✅ HTTPX imported successfully")
    except ImportError as e:
        print(f"❌ HTTPX import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import settings
        print("✅ Configuration loaded successfully")
        print(f"   - API Key: {'Set' if settings.api_key else 'Not set'}")
        print(f"   - OpenAI: {'Set' if settings.openai_api_key else 'Not set'}")
        print(f"   - Groq: {'Set' if settings.groq_api_key else 'Not set'}")
        print(f"   - Pinecone: {'Set' if settings.pinecone_api_key else 'Not set'}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_app_components():
    """Test app components"""
    print("\n🏗️ Testing app components...")
    
    try:
        from app.models import QueryRequest, QueryResponse
        print("✅ Models imported successfully")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from app.auth import verify_api_key
        print("✅ Auth imported successfully")
    except Exception as e:
        print(f"❌ Auth import failed: {e}")
        return False
    
    try:
        from app.query_engine import QueryEngine
        print("✅ QueryEngine imported successfully")
    except Exception as e:
        print(f"❌ QueryEngine import failed: {e}")
        return False
    
    try:
        from app.document_processor import DocumentProcessor
        print("✅ DocumentProcessor imported successfully")
    except Exception as e:
        print(f"❌ DocumentProcessor import failed: {e}")
        return False
    
    try:
        from app.vector_store import VectorStore
        print("✅ VectorStore imported successfully")
    except Exception as e:
        print(f"❌ VectorStore import failed: {e}")
        return False
    
    try:
        from app.llm_processor import LLMProcessor
        print("✅ LLMProcessor imported successfully")
    except Exception as e:
        print(f"❌ LLMProcessor import failed: {e}")
        return False
    
    return True

def test_deployment_files():
    """Test deployment files exist"""
    print("\n📁 Testing deployment files...")
    
    required_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        "Procfile",
        "runtime.txt",
        "README.md",
        ".gitignore"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    return True

def test_app_structure():
    """Test app directory structure"""
    print("\n📂 Testing app structure...")
    
    required_app_files = [
        "app/__init__.py",
        "app/models.py",
        "app/auth.py",
        "app/query_engine.py",
        "app/document_processor.py",
        "app/vector_store.py",
        "app/llm_processor.py",
        "app/fallback_search.py"
    ]
    
    for file in required_app_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    return True

async def test_basic_functionality():
    """Test basic functionality"""
    print("\n⚡ Testing basic functionality...")
    
    try:
        from app.query_engine import QueryEngine
        engine = QueryEngine()
        print("✅ QueryEngine initialized successfully")
        
        # Test health check
        health = await engine.health_check()
        print(f"✅ Health check: {health}")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 HackRx 6.0 Deployment Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_app_components,
        test_deployment_files,
        test_app_structure,
        lambda: asyncio.run(test_basic_functionality())
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test failed: {test.__name__}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment.")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 