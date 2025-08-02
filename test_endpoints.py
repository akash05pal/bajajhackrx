#!/usr/bin/env python3
"""
Comprehensive Endpoint Testing for HackRx 6.0
Tests all API endpoints locally
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

def test_root_endpoint():
    """Test root endpoint"""
    print("🔍 Testing Root Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_endpoint():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config_endpoint():
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

def test_cache_info_endpoint():
    """Test cache info endpoint"""
    print("\n🔍 Testing Cache Info Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/cache/info", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_main_endpoint_single_question():
    """Test main endpoint with single question"""
    print("\n🔍 Testing Main Endpoint (Single Question)")
    print("=" * 40)
    
    data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
        ]
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=data,
            timeout=30
        )
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response Time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Check if answer is meaningful
            answers = result.get('answers', [])
            if answers and not answers[0].startswith("LLM service not available"):
                print("✅ Answer is meaningful")
                return True
            else:
                print("❌ Answer is not meaningful")
                return False
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_main_endpoint_multiple_questions():
    """Test main endpoint with multiple questions"""
    print("\n🔍 Testing Main Endpoint (Multiple Questions)")
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
            
            # Check if answers are meaningful
            meaningful_answers = 0
            for i, answer in enumerate(result.get('answers', []), 1):
                if answer and not answer.startswith("LLM service not available"):
                    meaningful_answers += 1
                    print(f"✅ Answer {i}: Meaningful")
                else:
                    print(f"❌ Answer {i}: {answer[:100]}...")
            
            print(f"\n✅ {meaningful_answers}/{len(result.get('answers', []))} meaningful answers")
            return meaningful_answers >= 2  # At least 2 meaningful answers
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_authentication():
    """Test authentication"""
    print("\n🔍 Testing Authentication")
    print("=" * 40)
    
    # Test without authentication
    try:
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers={"Content-Type": "application/json"},
            json={"documents": "test", "questions": ["test"]},
            timeout=10
        )
        print(f"Without auth - Status: {response.status_code}")
        if response.status_code in [401, 403]:  # Both 401 and 403 are acceptable
            print("✅ Authentication required")
        else:
            print("❌ Authentication not working properly")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test with wrong authentication
    try:
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers={
                "Authorization": "Bearer wrong-key",
                "Content-Type": "application/json"
            },
            json={"documents": "test", "questions": ["test"]},
            timeout=10
        )
        print(f"Wrong auth - Status: {response.status_code}")
        if response.status_code in [401, 403]:  # Both 401 and 403 are acceptable
            print("✅ Wrong authentication rejected")
        else:
            print("❌ Wrong authentication not rejected")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    """Run all endpoint tests"""
    print("🚀 HackRx 6.0 Endpoint Testing")
    print("=" * 50)
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Endpoint", test_health_endpoint),
        ("Config Endpoint", test_config_endpoint),
        ("Cache Info Endpoint", test_cache_info_endpoint),
        ("Authentication", test_authentication),
        ("Main Endpoint (Single Question)", test_main_endpoint_single_question),
        ("Main Endpoint (Multiple Questions)", test_main_endpoint_multiple_questions)
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
    print("📊 Endpoint Test Results Summary")
    print(f"{'='*50}")
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL ENDPOINT TESTS PASSED! Ready for deployment!")
        print("\n📋 Deployment Checklist:")
        print("✅ All endpoints working")
        print("✅ Authentication working")
        print("✅ LLM responses meaningful")
        print("✅ Response time acceptable")
        print("✅ JSON format correct")
    else:
        print("\n⚠️ Some endpoint tests failed. Please check the issues.")

if __name__ == "__main__":
    main() 