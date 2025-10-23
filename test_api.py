"""
Test script for MenoBalance AI API
Tests the /predict endpoint locally
"""

import requests
import json
import time

def test_api_endpoint():
    """Test the API endpoint locally."""
    base_url = "http://localhost:8000"
    
    # Test data
    test_data = {
        "age": 45,
        "bmi": 25.5,
        "fsh": 15.2,
        "amh": 1.5,
        "estradiol": 50.0,
        "last_period_months": 6,
        "hot_flashes": 3,
        "mood_changes": 4,
        "sleep_quality": 6,
        "stress_level": 5,
        "smoking": False,
        "exercise": "Moderate",
        "family_history": False,
        "diabetes": False,
        "hypertension": False,
        "thyroid": False
    }
    
    print("🧪 Testing MenoBalance AI API...")
    print(f"📡 Base URL: {base_url}")
    print(f"📊 Test Data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Test health endpoint
        print("\n1️⃣ Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {health_response.json()}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return False
        
        # Test root endpoint
        print("\n2️⃣ Testing root endpoint...")
        root_response = requests.get(f"{base_url}/", timeout=10)
        if root_response.status_code == 200:
            print("✅ Root endpoint passed")
            print(f"   Response: {root_response.json()}")
        else:
            print(f"❌ Root endpoint failed: {root_response.status_code}")
        
        # Test prediction endpoint
        print("\n3️⃣ Testing prediction endpoint...")
        start_time = time.time()
        
        predict_response = requests.post(
            f"{base_url}/predict",
            json=test_data,
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if predict_response.status_code == 200:
            print("✅ Prediction endpoint passed")
            print(f"   Response time: {response_time:.2f} seconds")
            
            result = predict_response.json()
            
            # Display results
            print("\n📊 Prediction Results:")
            print(f"   Survival: {result['survival']['time_to_menopause_years']:.1f} years")
            print(f"   Symptoms: {result['symptoms']['severity_score']:.1f}/10")
            print(f"   Classification: {result['classification']['predicted_class']}")
            print(f"   Method: {result['method']}")
            print(f"   Timestamp: {result['timestamp']}")
            
            # Display confidence intervals
            print("\n📈 Confidence Intervals:")
            print(f"   Survival: {result['survival']['confidence_interval']}")
            print(f"   Symptoms: {result['symptoms']['confidence_interval']}")
            print(f"   Classification: {result['classification']['confidence_interval']}")
            
            # Display recommendations
            print("\n💡 Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                print(f"   {i}. {priority_emoji} {rec['title']}: {rec['description']}")
            
            return True
        else:
            print(f"❌ Prediction endpoint failed: {predict_response.status_code}")
            print(f"   Error: {predict_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the API server is running on localhost:8000")
        print("   Start the server with: python src/api_endpoint.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The server might be slow or unresponsive.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MenoBalance AI API Test Suite")
    print("=" * 50)
    
    success = test_api_endpoint()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("💥 Some tests failed. Check the errors above.")
