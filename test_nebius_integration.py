#!/usr/bin/env python3
"""
Test script for Nebius AI integration
"""

import os
import sys
sys.path.append('src')

# Set the API key as environment variable for testing
os.environ['NEBIUS_AI_API_KEY'] = 'eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDExNzkyNzY2ODY2MDc4NDUyOTg4OSIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTkxODg2MTM0MiwidXVpZCI6IjAxOWEwZTk2LTk0YTMtNzExMS1hN2E5LWVhODIxZGEzNjdmOSIsIm5hbWUiOiJVbm5hbWVkIGtleSIsImV4cGlyZXNfYXQiOiIyMDMwLTEwLTIyVDAxOjAyOjIyKzAwMDAifQ.SaCHoSTSGj22KGjxHMeIrWgmXbha9ezbfeFr2_UOMJA'

from chatbot_nebius import get_nebius_service

def test_nebius_integration():
    """Test Nebius AI integration."""
    print("Testing Nebius AI Integration...")
    
    # Get the service
    nebius_service = get_nebius_service()
    
    # Test 1: Check if API key is loaded
    print(f"[OK] API Key loaded: {nebius_service.api_key is not None}")
    print(f"[OK] Base URL: {nebius_service.base_url}")
    
    # Test 2: Test chat functionality
    print("\nTesting chat functionality...")
    try:
        response = nebius_service.chat(
            "Hello, I'm experiencing hot flashes during menopause. What can I do?",
            context={"session_id": "test_session"}
        )
        print(f"✓ Chat response received: {response[:100]}...")
    except Exception as e:
        print(f"⚠ Chat test failed (expected if API is not accessible): {e}")
    
    # Test 3: Test recommendations generation
    print("\nTesting recommendations generation...")
    try:
        health_data = {
            "age": 45,
            "bmi": 24.5,
            "predictions": {
                "classification": {"stage": "Peri-menopause"},
                "symptom": {"overall_severity": 6.5}
            }
        }
        recommendations = nebius_service.generate_recommendations(health_data)
        print(f"✓ Recommendations generated: {len(recommendations)} recommendations")
        for rec in recommendations[:2]:  # Show first 2
            print(f"  - {rec['title']}: {rec['description'][:50]}...")
    except Exception as e:
        print(f"⚠ Recommendations test failed: {e}")
    
    # Test 4: Test educational content generation
    print("\nTesting educational content generation...")
    try:
        content = nebius_service.generate_educational_content("menopause symptoms")
        print(f"✓ Educational content generated: {content['title']}")
        print(f"  Content: {content['content'][:100]}...")
    except Exception as e:
        print(f"⚠ Educational content test failed: {e}")
    
    print("\nNebius AI integration test completed!")
    print("Note: Some tests may fail if the API endpoint is not accessible, but fallback responses should work.")

if __name__ == "__main__":
    test_nebius_integration()