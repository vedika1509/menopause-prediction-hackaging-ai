"""
Simple deployment test script for MenoBalance AI
Tests all components without emoji characters
"""

import json
import os
import sys
from datetime import datetime


def check_requirements():
    """Check if all required files exist."""
    required_files = [
        "menobalance/src/app_streamlit_main.py",
        "menobalance/src/api_integration.py",
        "menobalance/requirements.txt",
        "menobalance/Dockerfile",
        "menobalance/.streamlit/config.toml",
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"Missing required files: {missing_files}")
        return False

    print("All required files present")
    return True


def test_api_integration():
    """Test the API integration."""
    print("Testing API integration...")

    try:
        # Import and test the API integration
        sys.path.insert(0, "menobalance/src")
        from api_integration import predict_menopause_streamlit

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
            "thyroid": False,
        }

        # Test prediction
        result = predict_menopause_streamlit(test_data)

        if "survival" in result and "symptoms" in result and "classification" in result:
            print("API integration working correctly")
            print(f"   Method: {result.get('method', 'unknown')}")
            print(f"   Timestamp: {result.get('timestamp', 'unknown')}")
            return True
        else:
            print("API integration returned incomplete results")
            return False

    except Exception as e:
        print(f"Error testing API integration: {e}")
        return False


def test_streamlit_imports():
    """Test that all Streamlit imports work."""
    print("Testing Streamlit imports...")

    try:
        import numpy as np
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        import streamlit as st

        print("All Streamlit dependencies available")
        return True
    except ImportError as e:
        print(f"Missing dependencies: {e}")
        return False


def create_deployment_summary():
    """Create deployment summary."""
    print("Creating deployment summary...")

    try:
        summary = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "status": "ready_for_deployment",
            "components": {
                "streamlit_app": "src/app_streamlit_main.py",
                "api_integration": "src/api_integration.py",
                "prediction_service": "src/prediction_service.py",
                "fallback_service": "src/prediction_service_fallback.py",
                "model_explainability": "src/pages/model_explainability.py",
                "health_input": "src/pages/health_input.py",
                "ethics_bias": "src/pages/ethics_bias.py",
            },
            "features": [
                "Confidence Intervals",
                "Model Explainability",
                "Ethics Documentation",
                "API Integration",
                "Health Input Forms",
                "Model Analysis Dashboard",
            ],
            "deployment": {
                "platform": "Streamlit Cloud",
                "dockerfile": "Dockerfile",
                "requirements": "requirements.txt",
                "config": ".streamlit/config.toml",
            },
        }

        with open("deployment_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        print("Deployment summary created")
        return True

    except Exception as e:
        print(f"Error creating deployment summary: {e}")
        return False


def main():
    """Main test function."""
    print("MenoBalance AI Deployment Test")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        print("Deployment test failed: Missing required files")
        return False

    # Test Streamlit imports
    if not test_streamlit_imports():
        print("Deployment test failed: Missing dependencies")
        return False

    # Test API integration
    if not test_api_integration():
        print("Deployment test failed: API integration test failed")
        return False

    # Create deployment summary
    if not create_deployment_summary():
        print("Deployment test failed: Could not create summary")
        return False

    print("\n" + "=" * 50)
    print("Deployment test completed successfully!")
    print("\nNext Steps:")
    print("1. Push code to GitHub repository")
    print("2. Connect repository to Streamlit Cloud")
    print("3. Deploy from Streamlit Cloud dashboard")
    print("4. Test deployed application")

    print("\nStreamlit Cloud Deployment:")
    print("   - Repository: https://github.com/yourusername/menobalance")
    print("   - App URL: https://menobalance-ai.streamlit.app")
    print("   - Documentation: https://docs.streamlit.io/streamlit-community-cloud")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
