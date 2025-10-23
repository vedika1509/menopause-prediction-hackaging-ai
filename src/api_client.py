"""
API Client for MenoBalance AI
Handles communication with external FastAPI backend
"""

import requests
import streamlit as st
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MenoBalanceAPIClient:
    """Client for MenoBalance AI API"""
    
    def __init__(self, api_url: str = None):
        """Initialize API client"""
        self.api_url = api_url or st.secrets.get("API_URL", "http://localhost:8000")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "MenoBalance-Streamlit/1.0"
        })
    
    def health_check(self) -> bool:
        """Check if API is available"""
        try:
            response = self.session.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def predict_menopause(self, health_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get menopause predictions from API"""
        try:
            response = self.session.post(
                f"{self.api_url}/predict",
                json=health_data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Get model information from API"""
        try:
            response = self.session.get(f"{self.api_url}/", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return None

def get_api_client() -> MenoBalanceAPIClient:
    """Get configured API client"""
    return MenoBalanceAPIClient()

def test_api_connection() -> bool:
    """Test API connection"""
    client = get_api_client()
    return client.health_check()

def get_predictions_with_api(health_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get predictions using external API"""
    client = get_api_client()
    
    # Check if API is available
    if not client.health_check():
        st.warning("🌐 API backend not available. Using fallback predictions.")
        # Fallback to integrated prediction service
        try:
            from api_integration import predict_menopause_streamlit
            return predict_menopause_streamlit(health_data)
        except Exception as e:
            st.error(f"Fallback failed: {e}")
            return get_demo_predictions()
    
    # Use external API
    predictions = client.predict_menopause(health_data)
    if predictions:
        return predictions
    else:
        st.warning("⚠️ API request failed. Using fallback predictions.")
        try:
            from api_integration import predict_menopause_streamlit
            return predict_menopause_streamlit(health_data)
        except Exception as e:
            st.error(f"Fallback failed: {e}")
            return get_demo_predictions()

def get_demo_predictions() -> Dict[str, Any]:
    """Get demo predictions when API is unavailable"""
    return {
        "survival": {
            "time_to_menopause_years": 3.2,
            "risk_level": "moderate",
            "confidence_interval": [2.0, 4.5],
            "confidence_level": 0.95,
            "model_confidence": 0.75,
            "uncertainty_measure": 0.6,
            "method": "demo_data"
        },
        "symptoms": {
            "severity_score": 6.5,
            "severity_level": "moderate",
            "confidence_interval": [5.0, 8.0],
            "confidence_level": 0.95,
            "model_confidence": 0.72,
            "uncertainty_measure": 0.8,
            "method": "demo_data"
        },
        "classification": {
            "predicted_class": "Peri-menopause",
            "confidence": 0.68,
            "confidence_interval": [0.55, 0.81],
            "confidence_level": 0.95,
            "probabilities": {"pre_menopause": 0.32, "peri_menopause": 0.68},
            "model_confidence": 0.68,
            "uncertainty_measure": 0.07,
            "method": "demo_data"
        },
        "recommendations": [
            {
                "priority": "high",
                "title": "Consult Healthcare Provider",
                "description": "Your symptoms suggest consultation with a healthcare provider."
            }
        ],
        "timestamp": "2025-01-23T00:00:00Z",
        "method": "demo_data"
    }
