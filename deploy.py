"""
Deployment script for MenoBalance AI
Handles Streamlit Cloud deployment and testing
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime

import requests


def check_requirements():
    """Check if all required files exist."""
    required_files = [
        "src/app_streamlit_main.py",
        "src/api_integration.py",
        "requirements.txt",
        "Dockerfile",
        ".streamlit/config.toml",
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


def test_local_app():
    """Test the Streamlit app locally."""
    print("Testing Streamlit app locally...")

    try:
        # Start Streamlit in background
        process = subprocess.Popen(
            [
                "streamlit",
                "run",
                "src/app_streamlit_main.py",
                "--server.port=8501",
                "--server.headless=true",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for app to start
        time.sleep(10)

        # Test health endpoint
        try:
            response = requests.get("http://localhost:8501", timeout=10)
            if response.status_code == 200:
                print("✅ Streamlit app is running locally")
                return True
            else:
                print(f"❌ Streamlit app returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to Streamlit app: {e}")
            return False
        finally:
            # Kill the process
            process.terminate()
            process.wait()

    except Exception as e:
        print(f"❌ Error testing Streamlit app: {e}")
        return False


def test_api_integration():
    """Test the API integration."""
    print("🧪 Testing API integration...")

    try:
        # Import and test the API integration
        sys.path.insert(0, "src")
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
            print("✅ API integration working correctly")
            print(f"   Method: {result.get('method', 'unknown')}")
            print(f"   Timestamp: {result.get('timestamp', 'unknown')}")
            return True
        else:
            print("❌ API integration returned incomplete results")
            return False

    except Exception as e:
        print(f"❌ Error testing API integration: {e}")
        return False


def create_deployment_package():
    """Create deployment package for Streamlit Cloud."""
    print("📦 Creating deployment package...")

    try:
        # Create deployment info
        deployment_info = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": [
                "Streamlit Frontend",
                "API Integration",
                "Model Loading",
                "Confidence Intervals",
                "Explainability",
                "Ethics Documentation",
            ],
            "endpoints": [
                "Home",
                "Health Input",
                "Model Analysis",
                "Insights",
                "Resources",
                "Settings",
            ],
        }

        with open("deployment_info.json", "w") as f:
            json.dump(deployment_info, f, indent=2)

        print("✅ Deployment package created")
        return True

    except Exception as e:
        print(f"❌ Error creating deployment package: {e}")
        return False


def main():
    """Main deployment function."""
    print("MenoBalance AI Deployment Script")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        print("💥 Deployment failed: Missing required files")
        return False

    # Test API integration
    if not test_api_integration():
        print("💥 Deployment failed: API integration test failed")
        return False

    # Create deployment package
    if not create_deployment_package():
        print("💥 Deployment failed: Could not create deployment package")
        return False

    print("\n" + "=" * 50)
    print("🎉 Deployment preparation completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Push code to GitHub repository")
    print("2. Connect repository to Streamlit Cloud")
    print("3. Deploy from Streamlit Cloud dashboard")
    print("4. Test deployed application")

    print("\n🔗 Streamlit Cloud Deployment:")
    print("   - Repository: https://github.com/yourusername/menobalance")
    print("   - App URL: https://menobalance-ai.streamlit.app")
    print("   - Documentation: https://docs.streamlit.io/streamlit-community-cloud")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
