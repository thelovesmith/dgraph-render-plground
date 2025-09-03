#!/usr/bin/env python3
"""
Test script for the Sentence Transformer API
Run this script to test both local and deployed versions of the API
"""

import requests
import json
import time

def test_health_endpoint(base_url):
    """Test the health check endpoint"""
    print(f"Testing health endpoint: {base_url}/health")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_embedding_map_format(base_url, api_key=None):
    """Test embedding endpoint with map format"""
    print(f"\nTesting embedding endpoint (map format): {base_url}/embedding")
    
    payload = {
        "text1": "This is a sample sentence.",
        "text2": "Here is another example text.",
        "text3": "Machine learning is fascinating."
    }
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/embedding",
            json=payload,
            headers=headers,
            timeout=30
        )
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Number of embeddings: {len(result)}")
            
            # Show first few dimensions of first embedding
            for key in result:
                embedding = json.loads(result[key])
                print(f"Embedding for '{key}': [{embedding[0]:.6f}, {embedding[1]:.6f}, ...] (length: {len(embedding)})")
                break
                
        else:
            print(f"Error response: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_embedding_kserve_format(base_url, api_key=None):
    """Test embedding endpoint with KServe format"""
    print(f"\nTesting embedding endpoint (KServe format): {base_url}/embedding")
    
    payload = {
        "instances": [
            "This is a sample sentence.",
            "Here is another example text.",
            "Machine learning is fascinating."
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/embedding",
            json=payload,
            headers=headers,
            timeout=30
        )
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            predictions = result["predictions"]
            print(f"Number of predictions: {len(predictions)}")
            
            # Show first few dimensions of first prediction
            if predictions:
                embedding = predictions[0]
                print(f"First embedding: [{embedding[0]:.6f}, {embedding[1]:.6f}, ...] (length: {len(embedding)})")
                
        else:
            print(f"Error response: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_api_key_info(base_url):
    """Get API key information from the server"""
    print(f"\nGetting API key info from: {base_url}/api-key-info")
    try:
        response = requests.get(f"{base_url}/api-key-info", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            api_key = data.get('api_key')
            if api_key:
                print(f"🔑 API Key: {api_key}")
                return api_key
            else:
                print("ℹ️  API key is hidden. Set SHOW_API_KEY_INFO=true to display it.")
                return None
        else:
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error getting API key info: {e}")
        return None

def test_api_key_protection(base_url):
    """Test that API key protection is working"""
    print(f"\n🔒 Testing API key protection: {base_url}/embedding")
    
    payload = {"test": "This should fail without API key"}
    
    try:
        # Test without API key
        response = requests.post(
            f"{base_url}/embedding",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status without API key: {response.status_code}")
        if response.status_code == 401:
            print("✅ API key protection is working correctly")
            return True
        else:
            print("❌ API key protection may not be working")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing API key protection: {e}")
        return False

def main():
    """Run all tests"""
    print("Sentence Transformer API Test Suite (with API Key Protection)")
    print("=" * 65)
    
    # Test local development server
    local_url = "http://localhost:5000"
    print(f"\n🧪 Testing LOCAL server: {local_url}")
    print("-" * 35)
    
    local_health = test_health_endpoint(local_url)
    local_api_key_protection = test_api_key_protection(local_url) if local_health else False
    local_api_key = get_api_key_info(local_url) if local_health else None
    
    local_map = False
    local_kserve = False
    
    if local_health and local_api_key:
        local_map = test_embedding_map_format(local_url, local_api_key)
        local_kserve = test_embedding_kserve_format(local_url, local_api_key)
    elif local_health:
        print("⚠️  Could not retrieve API key. Testing without authentication...")
        local_map = test_embedding_map_format(local_url)
        local_kserve = test_embedding_kserve_format(local_url)
    
    print(f"\n📊 LOCAL Results:")
    print(f"  Health: {'✅ PASS' if local_health else '❌ FAIL'}")
    print(f"  API Key Protection: {'✅ PASS' if local_api_key_protection else '❌ FAIL'}")
    print(f"  API Key Retrieved: {'✅ PASS' if local_api_key else '❌ FAIL'}")
    print(f"  Map Format: {'✅ PASS' if local_map else '❌ FAIL'}")
    print(f"  KServe Format: {'✅ PASS' if local_kserve else '❌ FAIL'}")
    
    # Test deployed version if URL provided as argument
    import sys
    if len(sys.argv) > 1:
        deployed_url = sys.argv[1]
        print(f"\n🚀 Testing DEPLOYED server: {deployed_url}")
        print("-" * 45)
        
        deployed_health = test_health_endpoint(deployed_url)
        deployed_api_key_protection = test_api_key_protection(deployed_url) if deployed_health else False
        deployed_api_key = get_api_key_info(deployed_url) if deployed_health else None
        
        deployed_map = False
        deployed_kserve = False
        
        if deployed_health and deployed_api_key:
            deployed_map = test_embedding_map_format(deployed_url, deployed_api_key)
            deployed_kserve = test_embedding_kserve_format(deployed_url, deployed_api_key)
        elif deployed_health:
            print("⚠️  Could not retrieve API key. Testing without authentication...")
            deployed_map = test_embedding_map_format(deployed_url)
            deployed_kserve = test_embedding_kserve_format(deployed_url)
        
        print(f"\n📊 DEPLOYED Results:")
        print(f"  Health: {'✅ PASS' if deployed_health else '❌ FAIL'}")
        print(f"  API Key Protection: {'✅ PASS' if deployed_api_key_protection else '❌ FAIL'}")
        print(f"  API Key Retrieved: {'✅ PASS' if deployed_api_key else '❌ FAIL'}")
        print(f"  Map Format: {'✅ PASS' if deployed_map else '❌ FAIL'}")
        print(f"  KServe Format: {'✅ PASS' if deployed_kserve else '❌ FAIL'}")
    else:
        print("\n💡 To test deployed version, run:")
        print("   python test_api.py https://your-app-name.onrender.com")
        
    print("\n🔐 API Key Usage Examples:")
    if local_api_key:
        print(f"   curl -H 'X-Api-Key: {local_api_key}' -X POST {local_url}/embedding -d '{{\"text\":\"test\"}}'")
        print(f"   curl -H 'Authorization: Bearer {local_api_key}' -X POST {local_url}/embedding -d '{{\"text\":\"test\"}}'")
    else:
        print("   curl -H 'X-Api-Key: YOUR_API_KEY' -X POST http://localhost:5000/embedding -d '{\"text\":\"test\"}'")
        print("   curl -H 'Authorization: Bearer YOUR_API_KEY' -X POST http://localhost:5000/embedding -d '{\"text\":\"test\"}'")
        print("   💡 Set SHOW_API_KEY_INFO=true environment variable to display the actual API key")

if __name__ == "__main__":
    main()
