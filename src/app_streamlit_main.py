"""
MenoBalance AI - Main Streamlit Application
Comprehensive menopause prediction and wellness management platform.
"""

import os
import sys
from datetime import datetime

import streamlit as st

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="MenoBalance AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Custom CSS for beautiful, empathetic design
def load_custom_css():
    """Load custom CSS for styling."""
    st.markdown(
        """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #9B59B6 0%, #E8DAEF 50%, #5DADE2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(155, 89, 182, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #E8DAEF 0%, #F8F4FF 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #E8DAEF 0%, #F8F4FF 100%);
        display: block !important;
        visibility: visible !important;
        width: 300px !important;
        min-width: 300px !important;
    }
    
    /* Navigation Styles */
    .nav-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    .nav-item:hover {
        background: rgba(155, 89, 182, 0.1);
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: linear-gradient(90deg, #9B59B6, #E8DAEF);
        color: white;
        box-shadow: 0 4px 15px rgba(155, 89, 182, 0.3);
    }
    
    /* Card Styles */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid rgba(155, 89, 182, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(155, 89, 182, 0.2);
    }
    
    .card-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #9B59B6;
        margin-bottom: 1rem;
        font-size: 1.3rem;
        text-decoration: none !important;
    }
    
    .card-title::after {
        content: none !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(45deg, #9B59B6, #E8DAEF);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(155, 89, 182, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(155, 89, 182, 0.4);
    }
    
    /* Form Styles */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    
    /* Metric Styles */
    .metric-card {
        background: linear-gradient(135deg, #F8F4FF 0%, #E8DAEF 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        border: 2px solid rgba(155, 89, 182, 0.2);
    }
    
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        color: #9B59B6;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Progress Bar Styles */
    .progress-container {
        background: rgba(155, 89, 182, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Alert Styles */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #9B59B6;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(90deg, #E8F5E8, #F0F8F0);
        border: 1px solid #4CAF50;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Info Message */
    .info-message {
        background: linear-gradient(90deg, #E3F2FD, #F0F8FF);
        border: 1px solid #2196F3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Warning Message */
    .warning-message {
        background: linear-gradient(90deg, #FFF8E1, #FFFBF0);
        border: 1px solid #FF9800;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .card {
            padding: 1rem;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(155, 89, 182, 0.3);
        border-radius: 50%;
        border-top-color: #9B59B6;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    """Initialize session state variables."""
    if "privacy_consent" not in st.session_state:
        st.session_state.privacy_consent = False

    if "health_data" not in st.session_state:
        st.session_state.health_data = {}

    if "predictions" not in st.session_state:
        st.session_state.predictions = None

    if "sidebar_visible" not in st.session_state:
        st.session_state.sidebar_visible = True

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "wellness_scores" not in st.session_state:
        st.session_state.wellness_scores = []

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"


def show_privacy_consent():
    """Show privacy consent modal."""
    if not st.session_state.privacy_consent:
        # Create a single aligned privacy consent box
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
                padding: 3rem;
                border-radius: 25px;
                margin: 2rem 0;
                border: 3px solid #FF4757;
                box-shadow: 0 20px 60px rgba(255, 71, 87, 0.4);
                position: relative;
                z-index: 10;
                width: 100%;
                box-sizing: border-box;
            ">
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <h2 style="color: white; font-family: 'Poppins', sans-serif; margin-bottom: 1rem; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                🔒 Privacy & Data Protection
            </h2>
            <p style="font-family: 'Inter', sans-serif; line-height: 1.6; margin-bottom: 1.5rem; text-align: center; color: white; font-size: 1.1rem;">
                Your privacy is our top priority. Please review our data protection practices before continuing.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.95); padding: 2rem; border-radius: 20px; margin-bottom: 1.5rem; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
                <h4 style="color: #FF4757; margin-bottom: 1rem; text-align: center; font-size: 1.2rem;">🔐 Your Data Protection Promise:</h4>
                <ul style="font-family: 'Inter', sans-serif; margin: 0; line-height: 2; color: #333;">
                    <li>✅ <strong>Local Processing:</strong> Your health data stays on your device</li>
                    <li>✅ <strong>No Data Sharing:</strong> We never share your personal information</li>
                    <li>✅ <strong>AI Chat Only:</strong> Nebius AI is used only for chatbot conversations</li>
                    <li>✅ <strong>Full Control:</strong> You can delete your data anytime</li>
                    <li>✅ <strong>Educational Purpose:</strong> Predictions are for guidance only</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Add consent buttons
        st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)

        col_accept, col_decline = st.columns(2)
        with col_accept:
            if st.button(
                "✅ I Accept & Continue",
                use_container_width=True,
                type="primary",
                key="accept_privacy",
            ):
                st.session_state.privacy_consent = True
                st.rerun()

        with col_decline:
            if st.button("❌ Decline", use_container_width=True, key="decline_privacy"):
                st.error(
                    "Privacy consent is required to use MenoBalance AI. Please accept to continue."
                )
                st.stop()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():
    """Render the navigation sidebar."""
    with st.sidebar:
        st.markdown("**SIDEBAR IS WORKING!**")
        st.markdown(
            """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #9B59B6; font-family: 'Poppins', sans-serif; margin-bottom: 0;">
                🌸 MenoBalance AI
            </h2>
            <p style="color: #666; font-family: 'Inter', sans-serif; margin: 0;">
                Your compassionate health companion
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Navigation menu
        pages = {
            "🏠 Home": "Home",
            "📝 Health Input": "Health Input",
            "🔮 Predictions": "Predictions",
            "📊 Wellness Dashboard": "Wellness Dashboard",
            "⌚ Wearables": "Wearables",
            "📈 Symptom Timeline": "Symptom Timeline",
            "💬 AI Chatbot": "AI Chatbot",
            "📚 Education": "Education",
            "📊 Model Evaluation": "Model Evaluation",
            "🔍 Explainability": "Explainability",
            "⚖️ Ethics & Bias": "Ethics & Bias",
            "📄 Export Summary": "Export Summary",
        }

        st.markdown("### Navigation")

        for page_name, page_id in pages.items():
            if st.button(page_name, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.current_page = page_id
                st.rerun()

        st.markdown("---")

        # Privacy status
        if st.session_state.privacy_consent:
            st.success("✅ Privacy consent given")
        else:
            st.warning("⚠️ Privacy consent required")

        # Session info
        st.markdown("### Session Info")
        st.markdown(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
        st.markdown(f"**Time:** {datetime.now().strftime('%I:%M %p')}")


def render_header():
    """Render the main header."""
    st.markdown(
        """
    <div class="main-header">
        <h1>🌸 MenoBalance AI</h1>
        <p>Empowering women through AI-driven menopause prediction and wellness management</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_home_page():
    """Render the home page."""
    st.markdown(
        """
    <div class="card">
        <h2 class="card-title" style="text-decoration: none; color: #9B59B6;">Welcome to Your Health Journey</h2>
        <p style="font-family: 'Inter', sans-serif; font-size: 1.1rem; line-height: 1.6;">
            MenoBalance AI is designed to provide compassionate support and evidence-based insights 
            during your menopause transition. Our AI-powered platform helps you understand your body's 
            changes and make informed decisions about your health and wellness.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Feature overview
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "🔮 AI Predictions\n\nGet personalized predictions about menopause stage, timeline, and symptom severity with confidence intervals.\n\nClick to explore →",
            key="ai_predictions_card",
            help="Click to go to AI Predictions page",
            use_container_width=True,
        ):
            st.session_state.current_page = "Predictions"
            st.rerun()

    with col2:
        if st.button(
            "📊 Wellness Tracking\n\nMonitor your daily wellness score and track progress with interactive visualizations and insights.\n\nClick to explore →",
            key="wellness_tracking_card",
            help="Click to go to Wellness Dashboard page",
            use_container_width=True,
        ):
            st.session_state.current_page = "Wellness Dashboard"
            st.rerun()

    with col3:
        if st.button(
            "💬 AI Support\n\nChat with our empathetic AI assistant for personalized recommendations and educational content.\n\nClick to explore →",
            key="ai_support_card",
            help="Click to go to AI Chatbot page",
            use_container_width=True,
        ):
            st.session_state.current_page = "AI Chatbot"
            st.rerun()

    # Quick start guide
    st.markdown(
        """
    <div class="card">
        <h3 style="color: #9B59B6;">🚀 Quick Start Guide</h3>
        <ol style="font-family: 'Inter', sans-serif; line-height: 1.8;">
            <li><strong>Health Input:</strong> Complete your health information form</li>
            <li><strong>Get Predictions:</strong> View your personalized menopause predictions</li>
            <li><strong>Track Wellness:</strong> Monitor your daily wellness score</li>
            <li><strong>Chat with AI:</strong> Get personalized support and recommendations</li>
            <li><strong>Export Summary:</strong> Download your health summary report</li>
        </ol>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Credits and acknowledgments
    st.markdown(
        """
    <div class="card">
        <h3 style="color: #9B59B6; text-align: center;">🙏 Special Thanks</h3>
        <p style="font-family: 'Inter', sans-serif; text-align: center; margin-bottom: 2rem;">
            MenoBalance AI is made possible through the support and collaboration of amazing organizations.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Partner logos and credits
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card" style="text-align: center;">
                <h4 style="color: #9B59B6; margin-bottom: 1rem;">OpenLongevity</h4>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
                    <h4 style="color: #9B59B6; margin: 0;">OpenLongevity</h4>
                </div>
                <p style="font-family: 'Inter', sans-serif; font-size: 0.9rem;">
                    Thanks to OpenLongevity for Hackaging AI - providing the platform and resources 
                    that made this project possible.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card" style="text-align: center;">
                <h4 style="color: #9B59B6; margin-bottom: 1rem;">Nebius.ai</h4>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
                    <h4 style="color: #9B59B6; margin: 0;">Nebius.ai</h4>
                </div>
                <p style="font-family: 'Inter', sans-serif; font-size: 0.9rem;">
                    Powered by Nebius.ai for AI capabilities and intelligent chatbot functionality 
                    that enhances user experience.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card" style="text-align: center;">
                <h4 style="color: #9B59B6; margin-bottom: 1rem;">AthenaDAO</h4>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
                    <h4 style="color: #9B59B6; margin: 0;">AthenaDAO</h4>
                </div>
                <p style="font-family: 'Inter', sans-serif; font-size: 0.9rem;">
                    Grateful to AthenaDAO for guidance and support in developing ethical AI 
                    solutions for women's health.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Additional acknowledgment
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <p style="font-family: 'Inter', sans-serif; font-style: italic; color: #666;">
                "Empowering women through AI-driven health solutions, made possible by the collaborative 
                spirit of the open-source community and our dedicated partners."
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Privacy notice
    if not st.session_state.privacy_consent:
        st.markdown(
            """
        <div class="warning-message">
            <h4>🔒 Privacy Consent Required</h4>
            <p>Please provide your privacy consent to access all features of MenoBalance AI.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Provide Privacy Consent", use_container_width=True):
                st.session_state.privacy_consent = True
                st.rerun()


def main():
    """Main application function."""
    # Load custom CSS
    load_custom_css()

    # Initialize session state
    initialize_session_state()

    # Render sidebar navigation
    render_sidebar()

    # Show privacy consent if needed
    show_privacy_consent()

    # Render header
    render_header()

    # Route to appropriate page
    current_page = st.session_state.current_page

    if current_page == "Home":
        render_home_page()
    elif current_page == "Health Input":
        from pages.health_input import render_health_input_page

        render_health_input_page()
    elif current_page == "Predictions":
        from pages.predictions import render_predictions_page

        render_predictions_page()
    elif current_page == "Wellness Dashboard":
        from pages.wellness_dashboard import render_wellness_dashboard

        render_wellness_dashboard()
    elif current_page == "Wearables":
        from pages.wearables import render_wearables_page

        render_wearables_page()
    elif current_page == "Symptom Timeline":
        from pages.symptom_timeline import render_symptom_timeline_page

        render_symptom_timeline_page()
    elif current_page == "AI Chatbot":
        from pages.chatbot import render_chatbot_page

        render_chatbot_page()
    elif current_page == "Education":
        from pages.education import render_education_page

        render_education_page()
    elif current_page == "Model Evaluation":
        from pages.model_evaluation import render_model_evaluation_page

        render_model_evaluation_page()
    elif current_page == "Explainability":
        from pages.model_explainability import render_explainability_page

        render_explainability_page()
    elif current_page == "Ethics & Bias":
        from pages.ethics_bias import render_ethics_page

        render_ethics_page()
    elif current_page == "Export Summary":
        from pages.export import render_export_page

        render_export_page()
    else:
        render_home_page()


if __name__ == "__main__":
    main()
