#!/usr/bin/env python3
"""
Render Deployment Helper Script
Verifies system is ready for deployment
"""

import os
import sys
import requests
import json

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        'main.py',
        'config.py',
        'requirements.txt',
        'app/__init__.py',
        'app/auth.py',
        'app/models.py',
        'app/document_processor.py',
        'app/vector_store.py',
        'app/llm_processor.py',
        'app/query_engine.py',
        'app/fallback_search.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_requirements():
    """Check requirements.txt"""
    print("\n🔍 Checking requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'openai',
        'groq',
        'pinecone-client',
        'pypdf2',
        'python-docx',
        'requests',
        'pydantic-settings'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        return False
    else:
        print("✅ All required packages in requirements.txt")
        return True

def check_config():
    """Check configuration"""
    print("\n🔍 Checking configuration...")
    
    try:
        from config import settings
        print("✅ Configuration loaded successfully")
        
        # Check API keys
        if settings.groq_api_key:
            print("✅ Groq API key configured")
        else:
            print("⚠️ Groq API key not set")
        
        if settings.openai_api_key:
            print("✅ OpenAI API key configured")
        else:
            print("⚠️ OpenAI API key not set")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_local_server():
    """Test if local server starts correctly"""
    print("\n🔍 Testing local server...")
    
    try:
        import subprocess
        import time
        
        # Start server in background
        process = subprocess.Popen([sys.executable, 'main.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test health endpoint
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                print("✅ Local server working")
                process.terminate()
                return True
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                process.terminate()
                return False
        except:
            print("❌ Could not connect to local server")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def generate_deployment_commands():
    """Generate deployment commands"""
    print("\n📋 Deployment Commands:")
    print("=" * 50)
    
    print("1. Initialize Git (if not done):")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit - HackRx 6.0 system'")
    print()
    
    print("2. Create GitHub repository:")
    print("   - Go to github.com")
    print("   - Create new repository: hackrx-6-0-system")
    print("   - Make it public")
    print()
    
    print("3. Push to GitHub:")
    print("   git remote add origin https://github.com/yourusername/hackrx-6-0-system.git")
    print("   git push -u origin main")
    print()
    
    print("4. Deploy on Render:")
    print("   - Go to render.com")
    print("   - Create new Web Service")
    print("   - Connect GitHub repository")
    print("   - Set environment variables")
    print("   - Deploy")
    print()
    
    print("5. Environment Variables to set in Render:")
    print("   GROQ_API_KEY=your_groq_api_key_here")
    print("   OPENAI_API_KEY=your_openai_api_key_here")
    print("   PINECONE_API_KEY=your_pinecone_api_key_here")
    print("   PINECONE_ENVIRONMENT=us-east-1-aws")
    print("   PINECONE_INDEX_NAME=bajaj-documents")
    print("   HOST=0.0.0.0")
    print("   PORT=10000")
    print("   DEBUG=False")
    print()

def main():
    """Main deployment check"""
    print("🚀 HackRx 6.0 - Render Deployment Check")
    print("=" * 50)
    
    checks = [
        check_files(),
        check_requirements(),
        check_config(),
        test_local_server()
    ]
    
    print(f"\n{'='*50}")
    print("📊 Deployment Readiness Results")
    print(f"{'='*50}")
    
    if all(checks):
        print("✅ System is ready for deployment!")
        print("✅ All checks passed")
        print("✅ Local server working")
        print("✅ Configuration correct")
        print("✅ Dependencies complete")
        
        generate_deployment_commands()
        
        print("🎉 Ready to deploy on Render!")
        print("\nNext steps:")
        print("1. Follow the deployment commands above")
        print("2. Use RENDER_DEPLOYMENT.md for detailed steps")
        print("3. Test your deployed URL")
        print("4. Submit to HackRx 6.0 competition")
        
    else:
        print("❌ System needs fixes before deployment")
        print("❌ Please fix the issues above")
        print("❌ Then run this script again")

if __name__ == "__main__":
    main() 