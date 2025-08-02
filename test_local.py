#!/usr/bin/env python3
"""
Local Test Script for HackRx 6.0 API
Tests the API locally with various scenarios
"""

import requests
import time
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "d809808918dd2a7d6b11fa5b23fa01e3abf9814dd225582d4d5674dc2138be0b"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def test_health():
    """Test health endpoint"""
    print("🔍 Testing Health Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config():
    """Test config endpoint"""
    print("\n🔍 Testing Config Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/config", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_competition_document():
    """Test with the competition document"""
    print("\n🔍 Testing Competition Document")
    print("=" * 40)
    
    data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?"
        ]
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=data,
            timeout=60
        )
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response Time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Number of Answers: {len(result.get('answers', []))}")
            for i, answer in enumerate(result.get('answers', []), 1):
                print(f"\nAnswer {i}:")
                print(f"  {answer}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sample_document():
    """Test with a sample PDF document"""
    print("\n🔍 Testing Sample Document")
    print("=" * 40)
    
    data = {
        "documents": "https://www.africau.edu/images/default/sample.pdf",
        "questions": [
            "What is this document about?",
            "What are the main topics covered?",
            "Is this a technical or general document?"
        ]
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=data,
            timeout=60
        )
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response Time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Number of Answers: {len(result.get('answers', []))}")
            for i, answer in enumerate(result.get('answers', []), 1):
                print(f"\nAnswer {i}:")
                print(f"  {answer}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_questions():
    """Test with simple questions"""
    print("\n🔍 Testing Simple Questions")
    print("=" * 40)
    
    data = {
        "documents": "https://www.africau.edu/images/default/sample.pdf",
        "questions": [
            "What is the title of this document?",
            "How many pages does this document have?"
        ]
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=data,
            timeout=60
        )
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response Time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Number of Answers: {len(result.get('answers', []))}")
            for i, answer in enumerate(result.get('answers', []), 1):
                print(f"\nAnswer {i}:")
                print(f"  {answer}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 HackRx 6.0 Local API Testing")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Config Check", test_config),
        ("Competition Document", test_competition_document),
        ("Sample Document", test_sample_document),
        ("Simple Questions", test_simple_questions)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {name}")
        print(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((name, False))
    
    print(f"\n{'='*50}")
    print("📊 Test Results Summary")
    print(f"{'='*50}")
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your API is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Test with Postman (see instructions below)")
        print("2. Deploy to get a public HTTPS URL")
    else:
        print("\n⚠️ Some tests failed. Please check the configuration.")

if __name__ == "__main__":
    main() 