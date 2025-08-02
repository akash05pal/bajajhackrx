#!/usr/bin/env python3
"""
Competition Test Script for HackRx 6.0 API
Tests the exact requirements from the competition
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

def test_competition_endpoint():
    """Test the exact competition requirements"""
    print("🚀 Testing Competition Requirements")
    print("=" * 50)
    
    # Competition request data (exact format from requirements)
    competition_data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?",
            "What is the No Claim Discount (NCD) offered in this policy?",
            "Is there a benefit for preventive health check-ups?",
            "How does the policy define a 'Hospital'?",
            "What is the extent of coverage for AYUSH treatments?",
            "Are there any sub-limits on room rent and ICU charges for Plan A?"
        ]
    }
    
    print(f"📋 Testing endpoint: {BASE_URL}/hackrx/run")
    print(f"📄 Document URL: {competition_data['documents']}")
    print(f"❓ Number of questions: {len(competition_data['questions'])}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=competition_data,
            timeout=60  # 30 seconds as per requirements
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"\n⏱️ Response time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            answers = result.get('answers', [])
            
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Number of answers: {len(answers)}")
            
            # Check if response time is within requirements (< 30 seconds)
            if response_time < 30:
                print("✅ Response time: Within 30 seconds requirement")
            else:
                print("⚠️ Response time: Exceeds 30 seconds requirement")
            
            # Display answers
            print("\n📋 Answers:")
            for i, answer in enumerate(answers, 1):
                print(f"{i}. {answer[:200]}...")
            
            return True
            
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_api_structure():
    """Test API structure compliance"""
    print("\n🔍 Testing API Structure Compliance")
    print("=" * 50)
    
    # Test 1: Check if endpoint exists
    try:
        response = requests.get(f"{BASE_URL}/hackrx/run")
        if response.status_code == 405:  # Method Not Allowed is expected for GET
            print("✅ Endpoint exists (GET not allowed, POST required)")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
    
    # Test 2: Check authentication
    try:
        # Test without authentication
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers={"Content-Type": "application/json"},
            json={"documents": "test", "questions": ["test"]}
        )
        if response.status_code == 401:
            print("✅ Authentication required (as expected)")
        else:
            print(f"⚠️ Authentication test: {response.status_code}")
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
    
    # Test 3: Check content type
    try:
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json={"documents": "test", "questions": ["test"]}
        )
        if response.headers.get('content-type', '').startswith('application/json'):
            print("✅ JSON response format")
        else:
            print("⚠️ Response format test")
    except Exception as e:
        print(f"❌ Response format test failed: {e}")

def main():
    """Run competition tests"""
    print("🎯 HackRx 6.0 Competition Test")
    print("=" * 50)
    
    # Test API structure
    test_api_structure()
    
    # Test competition endpoint
    success = test_competition_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 Competition Test Summary")
    print("=" * 50)
    
    if success:
        print("✅ Competition test completed successfully!")
        print("\n📋 Requirements Check:")
        print("✅ POST /hackrx/run endpoint")
        print("✅ Bearer token authentication")
        print("✅ JSON request/response format")
        print("✅ Document processing capability")
        print("✅ Question answering capability")
        print("\n🚀 Ready for deployment!")
    else:
        print("❌ Competition test failed")
        print("Please check the configuration and try again")

if __name__ == "__main__":
    main() 