"""
Streamlit Cloud Fix - Handle missing models gracefully
"""

import streamlit as st
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_model_availability():
    """Check if models are available and provide fallback information."""
    
    # Check for model directories
    model_dirs = [
        'models/task_specific_survival',
        'models/task_specific_symptom', 
        'models/task_specific_classification'
    ]
    
    available_models = []
    missing_models = []
    
    for model_dir in model_dirs:
        if os.path.exists(model_dir):
            available_models.append(model_dir)
        else:
            missing_models.append(model_dir)
    
    return available_models, missing_models

def display_model_status():
    """Display model status in the Streamlit app."""
    
    available_models, missing_models = check_model_availability()
    
    if available_models:
        st.success(f"✅ {len(available_models)} model(s) loaded successfully")
        for model in available_models:
            st.info(f"📁 {model}")
    
    if missing_models:
        st.warning(f"⚠️ {len(missing_models)} model(s) not found - using fallback predictions")
        for model in missing_models:
            st.error(f"❌ {model}")
        
        # Show fallback information
        st.info("""
        **Fallback System Active** 🔄
        
        The application is using rule-based predictions instead of trained ML models. 
        This ensures the app remains functional while providing reasonable estimates.
        
        **What this means:**
        - Predictions are based on clinical guidelines and statistical patterns
        - Results are still useful for educational and informational purposes
        - All features remain available (confidence intervals, recommendations, etc.)
        """)

def get_fallback_message():
    """Get a user-friendly message about the fallback system."""
    
    return """
    <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                padding: 1.5rem; border-radius: 10px; margin: 1rem 0; 
                border-left: 4px solid #8B4513;">
        <h4 style="color: #8B4513; margin-top: 0;">🔄 Fallback Prediction System Active</h4>
        <p style="color: #8B4513; margin: 0; line-height: 1.6;">
            We're currently using our intelligent fallback system to provide predictions. 
            This ensures you get helpful insights based on clinical guidelines and statistical patterns, 
            even when the full ML models aren't available. All features remain fully functional!
        </p>
    </div>
    """

def show_model_loading_info():
    """Show information about model loading status."""
    
    st.markdown("### 🔍 Model Status Information")
    
    # Check current directory
    current_dir = os.getcwd()
    st.info(f"**Current Directory:** `{current_dir}`")
    
    # List all directories
    try:
        dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
        st.info(f"**Available Directories:** {', '.join(dirs[:10])}")  # Show first 10
    except Exception as e:
        st.error(f"Error listing directories: {e}")
    
    # Check for models directory
    if os.path.exists('models'):
        st.success("✅ Models directory found")
        try:
            model_contents = os.listdir('models')
            st.info(f"**Model Contents:** {', '.join(model_contents)}")
        except Exception as e:
            st.error(f"Error reading models directory: {e}")
    else:
        st.warning("⚠️ Models directory not found")
    
    # Show fallback message
    st.markdown(get_fallback_message(), unsafe_allow_html=True)

if __name__ == "__main__":
    st.title("🔍 Model Status Checker")
    show_model_loading_info()
