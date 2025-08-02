#!/usr/bin/env python3
"""
Setup script for HackRx 6.0 LLM-Powered Intelligent Query–Retrieval System
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    print("\n🔧 Creating .env file...")
    env_content = """# HackRx 6.0 Configuration

# Required - OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Pinecone Configuration (for vector search)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=hackrx-documents

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Model Configuration
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-4
MAX_TOKENS=4000
TEMPERATURE=0.1
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please update the API keys in .env file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    try:
        import fastapi
        import uvicorn
        import openai
        import pinecone
        import PyPDF2
        import docx
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running basic tests...")
    try:
        # Test the main application
        from main import app
        print("✅ FastAPI app created successfully")
        
        # Test query engine
        from app.query_engine import QueryEngine
        print("✅ Query engine imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 HackRx 6.0 Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the API keys in .env file")
    print("2. Run: python main.py")
    print("3. Visit: http://localhost:8000/docs")
    print("4. Test with: python test_api.py")
    print("\n📚 Documentation: README.md")

if __name__ == "__main__":
    main() 