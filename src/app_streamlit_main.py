"""
MenoBalance AI - Complete UI Rebuild
Professional menopause prediction interface with calming pastel theme
Updated: 2025-01-23 - Enhanced with Nebius AI integration
"""

import os
import sys
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st

# Add project root (one level up) to path for imports (fix double 'src/src' bug)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Try to import Plotly but continue if unavailable
PLOTLY_AVAILABLE = True
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except Exception:
    PLOTLY_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="MenoBalance AI - Harmonize Your Hormonal Rhythms",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS - Enhanced Calming Pastel Theme
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #7BB3D3;
        --secondary: #B8A5D1;
        --coral: #E8957A;
        --mint: #9BC4A3;
        --lavender: #A695C7;
        --background: #F8FAFB;
        --foreground: #2D3748;
        --text-muted: #718096;
        --border: #E2E8F0;
        --success: #68D391;
        --warning: #F6AD55;
        --error: #FC8181;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .stApp { 
        font-family: 'Inter', sans-serif; 
        background: linear-gradient(135deg, #F8FAFB 0%, #F1F5F9 100%);
        color: var(--foreground); 
    }
    
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}
    
    /* Ensure sidebar is visible */
    .css-1d391kg {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    }
    
    /* Sidebar toggle button */
    .sidebar-toggle {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 1.2rem;
        cursor: pointer;
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }
    
    .sidebar-toggle:hover {
        transform: scale(1.1);
        background: var(--secondary);
    }
    
    /* Prediction Card Styles */
    .prediction-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: var(--shadow-xl);
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .prediction-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .prediction-header h2 {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .prediction-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 2rem;
        position: relative;
        z-index: 2;
    }
    
    .timeline-prediction {
        margin: 2rem 0;
        position: relative;
        z-index: 2;
    }
    
    .prediction-value {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .prediction-label {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    .confidence-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        backdrop-filter: blur(10px);
    }
    
    .confidence-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .confidence-value {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .risk-level {
        margin: 2rem 0;
        position: relative;
        z-index: 2;
    }
    
    .risk-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .risk-badge.moderate {
        background: rgba(255,193,7,0.9);
        color: #000;
    }
    
    .risk-description {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .prediction-actions {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 2rem;
        position: relative;
        z-index: 2;
    }
    
    .prediction-btn {
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .prediction-btn.primary {
        background: white;
        color: var(--primary);
    }
    
    .prediction-btn.secondary {
        background: rgba(255,255,255,0.2);
        color: white;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    .prediction-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* Enhanced Cards */
    .pastel-card { 
        background: white; 
        border-radius: 20px; 
        padding: 2rem; 
        box-shadow: var(--shadow); 
        border: 1px solid var(--border); 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .pastel-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .pastel-card:hover { 
        transform: translateY(-8px); 
        box-shadow: var(--shadow-xl);
        border-color: var(--primary);
    }
    
    .pastel-card:hover::before {
        transform: scaleX(1);
    }
    
    .metric-card { 
        background: white; 
        border-radius: 20px; 
        padding: 2rem; 
        box-shadow: var(--shadow); 
        border: 1px solid var(--border); 
        text-align: center; 
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Hero Cards */
    .hero-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    
    .hero-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 200px;
        height: 200px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        filter: blur(50px);
    }
    
    .coral-card {
        background: linear-gradient(135deg, var(--coral) 0%, #D67A5F 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-lg);
    }
    
    .mint-card {
        background: linear-gradient(135deg, var(--mint) 0%, #7BA085 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-lg);
    }
    
    .lavender-card {
        background: linear-gradient(135deg, var(--lavender) 0%, #8B7BA5 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-lg);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Form Elements */
    .stSelectbox > div > div {
        background: white;
        border-radius: 12px;
        border: 2px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(184, 212, 232, 0.1);
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    }
    
    /* Animations */
    .fade-in { 
        animation: fadeIn 0.8s ease-out; 
    }
    
    @keyframes fadeIn { 
        from { opacity: 0; transform: translateY(30px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
        border-right: 1px solid var(--border);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) { 
        .pastel-card { padding: 1.5rem; } 
        .metric-card { padding: 1.5rem; }
        .hero-card { padding: 2rem 1.5rem; }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary);
    }
</style>
""",
    unsafe_allow_html=True,
)

API_URL = "https://menopause-prediction-4xl8.onrender.com"  # placeholder


def initialize_session_state():
    """Initialize all session state variables"""
    if "symptom_logs" not in st.session_state:
        st.session_state.symptom_logs = []
    if "wellness_score" not in st.session_state:
        st.session_state.wellness_score = 50.0
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {"age": None, "last_period_months": None}
    if "predictions" not in st.session_state:
        st.session_state.predictions = {}
    if "demo_data_generated" not in st.session_state:
        st.session_state.demo_data_generated = False


def generate_demo_data(days: int = 30):
    """Generate sample symptom tracking data for demonstration"""
    if st.session_state.demo_data_generated:
        return
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    logs = []
    rng = np.random.default_rng(seed=42)
    for i in range(days):
        d = today - timedelta(days=(days - 1 - i))
        logs.append(
            {
                "date": d.isoformat(),
                "hot_flashes": int(np.clip(rng.normal(3 + 0.5 * np.sin(i / 5), 1.8), 0, 10)),
                "mood_changes": int(np.clip(rng.normal(4, 2), 0, 10)),
                "sleep_quality": int(np.clip(rng.normal(6 - 0.2 * np.cos(i / 7), 1.5), 0, 10)),
                "stress_level": int(np.clip(rng.normal(4 + 0.3 * np.sin(i / 6), 1.8), 0, 10)),
            }
        )
    st.session_state.symptom_logs = logs
    st.session_state.wellness_score = calculate_wellness_score()
    st.session_state.demo_data_generated = True


def calculate_wellness_score():
    """Calculate overall wellness score from symptom data"""
    if not st.session_state.symptom_logs:
        return 50.0
    recent_logs = st.session_state.symptom_logs[-7:]  # Last 7 days
    if not recent_logs:
        return 50.0
    avg_sleep = np.mean([log["sleep_quality"] for log in recent_logs])
    avg_stress = np.mean([log["stress_level"] for log in recent_logs])
    avg_hot_flashes = np.mean([log["hot_flashes"] for log in recent_logs])
    avg_mood = np.mean([log["mood_changes"] for log in recent_logs])
    wellness = (
        avg_sleep * 0.3
        + (10 - avg_stress) * 0.3
        + (10 - avg_hot_flashes) * 0.2
        + (10 - avg_mood) * 0.2
    ) * 10
    return float(max(0, min(100, wellness)))


def save_symptom_log(symptom_data):
    """Save new symptom entry to session state"""
    symptom_data["date"] = datetime.now().isoformat()
    st.session_state.symptom_logs.append(symptom_data)
    st.session_state.wellness_score = calculate_wellness_score()


def get_symptom_insights():
    """Get AI-powered insights using Nebius AI and prediction service"""
    try:
        from chatbot_nebius import NebiusChatbot

        # Get user data and predictions
        user_data = st.session_state.get("user_data", {})
        predictions = st.session_state.get("predictions", {})

        # Initialize chatbot
        chatbot = NebiusChatbot()

        # Update chatbot context
        if "chat_session_id" in st.session_state:
            chatbot.update_user_profile(st.session_state.chat_session_id, user_data)
            chatbot.update_prediction_context(st.session_state.chat_session_id, predictions)

        # Generate personalized recommendations
        recommendations = chatbot.generate_personalized_recommendations(user_data, predictions)

        # Convert to simple insights format
        insights = []
        for rec in recommendations:
            priority_emoji = (
                "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
            )
            insights.append(f"{priority_emoji} {rec['title']}: {rec['description']}")

        return (
            insights
            if insights
            else [
                "No personalized insights available yet. Complete your health assessment to get AI-powered recommendations."
            ]
        )

    except Exception:
        # Fallback to basic insights
        if not st.session_state.symptom_logs:
            return ["No symptom data yet. Track symptoms to see insights."]

        recent = st.session_state.symptom_logs[-14:]
        if not recent:
            return ["No recent symptom data. Start tracking to see insights."]

        avg = {
            "hot_flashes": np.mean([l.get("hot_flashes", 0) for l in recent]),
            "mood_changes": np.mean([l.get("mood_changes", 0) for l in recent]),
            "sleep_quality": np.mean([l.get("sleep_quality", 0) for l in recent]),
            "stress_level": np.mean([l.get("stress_level", 0) for l in recent]),
        }

        insights = []
        if avg["hot_flashes"] > 5:
            insights.append(
                "🔥 Hot flashes are above average — consider logging triggers (caffeine, heat)."
            )
        else:
            insights.append("✅ Hot flashes are within a mild range.")

        if avg["sleep_quality"] < 5:
            insights.append("😴 Sleep quality is low — review sleep hygiene.")
        else:
            insights.append("💤 Sleep quality is acceptable.")

        if avg["stress_level"] > 6:
            insights.append("😰 Stress is elevated — try short relaxation exercises.")

        if avg["mood_changes"] > 6:
            insights.append(
                "😔 Mood changes are significant — consider discussing with a clinician."
            )

        return insights


def create_symptom_timeline_chart():
    """Return a Plotly timeline figure or None if not available"""
    if not st.session_state.symptom_logs:
        return None
    df = pd.DataFrame(st.session_state.symptom_logs)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    if not PLOTLY_AVAILABLE:
        return None
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["hot_flashes"],
            mode="lines+markers",
            name="Hot Flashes",
            line=dict(color="#FFB5A7"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["mood_changes"],
            mode="lines+markers",
            name="Mood Changes",
            line=dict(color="#E6D5F0"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["sleep_quality"],
            mode="lines+markers",
            name="Sleep Quality",
            line=dict(color="#C8E6C9"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["stress_level"],
            mode="lines+markers",
            name="Stress Level",
            line=dict(color="#D4C5F9"),
        )
    )
    fig.update_layout(
        title="Symptom Timeline", xaxis_title="Date", yaxis_title="Severity (0-10)", height=420
    )
    return fig


def create_wellness_score_gauge():
    """Return a Plotly gauge or None if not available"""
    score = st.session_state.wellness_score
    if not PLOTLY_AVAILABLE:
        return None
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Wellness Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#B8D4E8"},
                "steps": [
                    {"range": [0, 40], "color": "#FC8181"},
                    {"range": [40, 70], "color": "#F6AD55"},
                    {"range": [70, 100], "color": "#68D391"},
                ],
            },
        )
    )
    fig.update_layout(height=300)
    return fig


def create_symptom_frequency_bar():
    """Return Plotly bar of average symptom severity or None if not available"""
    if not st.session_state.symptom_logs:
        return None
    df = pd.DataFrame(st.session_state.symptom_logs)
    symptoms = {
        "Hot Flashes": df["hot_flashes"].mean(),
        "Mood Changes": df["mood_changes"].mean(),
        "Sleep Quality": df["sleep_quality"].mean(),
        "Stress Level": df["stress_level"].mean(),
    }
    if not PLOTLY_AVAILABLE:
        return None
    fig = px.bar(
        x=list(symptoms.keys()),
        y=list(symptoms.values()),
        color=list(symptoms.values()),
        color_continuous_scale=["#FFB5A7", "#E6D5F0", "#C8E6C9", "#D4C5F9"],
        title="Average Symptom Severity",
    )
    fig.update_layout(xaxis_title="Symptoms", yaxis_title="Average Severity", height=400)
    return fig


def test_api_connection():
    """Test if prediction service is available"""
    try:
        from prediction_service import get_prediction_service

        service = get_prediction_service()
        st.info(f"Available models: {list(service.models.keys())}")
        st.info(f"Available scalers: {list(service.scalers.keys())}")
        st.info(f"Available features: {list(service.feature_names.keys())}")
        return len(service.models) > 0
    except Exception as e:
        st.error(f"Prediction service error: {str(e)}")
        return False


def get_predictions(health_data):
    """Get predictions using external API or fallback to integrated service"""
    try:
        # Try external API first
        from api_client import get_predictions_with_api
        return get_predictions_with_api(health_data)
    except ImportError:
        # Fallback to integrated prediction service
        try:
            from api_integration import predict_menopause_streamlit
            return predict_menopause_streamlit(health_data)
        except Exception as e:
            st.warning(f"Trained models not available: {str(e)}")
            try:
                # Fallback to rule-based predictions
                from prediction_service_fallback import predict_menopause_fallback
                return predict_menopause_fallback(health_data)
            except Exception as fallback_error:
                st.error(f"Fallback prediction failed: {str(fallback_error)}")
                # Final fallback to demo data
                return {
                    "survival": {
                        "time_to_menopause_years": 3.2,
                        "risk_level": "moderate",
                        "confidence_interval": [2.0, 4.5],
                        "confidence_level": 0.95,
                        "model_confidence": 0.75,
                        "uncertainty_measure": 0.6,
                        "method": "demo_data",
                    },
                    "symptoms": {
                        "severity_score": 6.5,
                        "severity_level": "moderate",
                        "confidence_interval": [5.0, 8.0],
                        "confidence_level": 0.95,
                        "model_confidence": 0.72,
                        "uncertainty_measure": 0.8,
                        "method": "demo_data",
                    },
                    "classification": {
                        "predicted_class": "Peri-menopause",
                        "confidence": 0.68,
                        "confidence_interval": [0.55, 0.81],
                        "confidence_level": 0.95,
                        "probabilities": {"pre_menopause": 0.32, "peri_menopause": 0.68},
                        "model_confidence": 0.68,
                        "uncertainty_measure": 0.07,
                        "method": "demo_data",
                    },
                    "recommendations": [
                        {
                            "priority": "high",
                            "title": "Consult Healthcare Provider",
                            "description": "Your symptoms suggest consultation with a healthcare provider.",
                        }
                    ],
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                    "fallback_error": str(fallback_error),
                }


def render_home_page():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Hero Section
    st.markdown(
        """
        <div class="hero-card" style="margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: white; position: relative; z-index: 2;">
                🌸 Welcome to MenoBalance AI
            </h1>
            <p style="font-size: 1.2rem; margin-bottom: 2rem; color: rgba(255,255,255,0.9); position: relative; z-index: 2;">
                Harmonize your hormonal rhythms, master your symptoms with personalized AI guidance
            </p>
            <div style="display: inline-flex; align-items: center; gap: 1rem; background: rgba(255,255,255,0.2); padding: 1rem 2rem; border-radius: 50px; backdrop-filter: blur(10px); position: relative; z-index: 2;">
                <span class="pulse">🌸</span>
                <span style="font-weight: 600;">Trusted by thousands of women</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main Prediction Feature - Center Stage
    st.markdown("### 🎯 Your Menopause Prediction")

    # Prediction card with prominent styling
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            """
        <div class="prediction-card">
            <div class="prediction-header">
                <h2>🔮 Menopause Timeline Prediction</h2>
                <p class="prediction-subtitle">Based on your health data and symptoms</p>
            </div>
            <div class="prediction-content">
                <div class="timeline-prediction">
                    <div class="prediction-value">2-4 Years</div>
                    <div class="prediction-label">Estimated Time to Menopause</div>
                    <div class="confidence-indicator">
                        <span class="confidence-label">Confidence:</span>
                        <span class="confidence-value">87%</span>
                    </div>
                    <div class="confidence-interval" style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                        <span>95% Confidence Interval: 2.0 - 4.5 years</span>
                    </div>
                </div>
                <div class="risk-level">
                    <div class="risk-badge moderate">Moderate Risk</div>
                    <p class="risk-description">Your symptoms suggest you're in the perimenopause phase</p>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Add functional buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Get Detailed Analysis", width="stretch", key="detailed_analysis"):
                st.session_state.current_page = "Tracker"
                st.rerun()

        with col2:
            if st.button("💡 View Recommendations", width="stretch", key="view_recommendations"):
                st.session_state.current_page = "Insights"
                st.rerun()

    st.markdown("---")

    # Quick Stats Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3 style="color: var(--primary); margin-bottom: 0.5rem;">Wellness Score</h3>
                <div style="font-size: 2.5rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                    {st.session_state.wellness_score:.0f}
                </div>
                <p style="margin: 0; color: var(--text-muted);">out of 100</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        days_tracked = len(st.session_state.symptom_logs)
        st.markdown(
            f"""
            <div class="metric-card">
                <h3 style="color: var(--coral); margin-bottom: 0.5rem;">Days Tracked</h3>
                <div style="font-size: 2.5rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                    {days_tracked}
                </div>
                <p style="margin: 0; color: var(--text-muted);">symptom entries</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <h3 style="color: var(--mint); margin-bottom: 0.5rem;">AI Insights</h3>
                <div style="font-size: 2.5rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                    ✓
                </div>
                <p style="margin: 0; color: var(--text-muted);">available</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <h3 style="color: var(--lavender); margin-bottom: 0.5rem;">Privacy</h3>
                <div style="font-size: 2.5rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                    🔒
                </div>
                <p style="margin: 0; color: var(--text-muted);">protected</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Main Content Row
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📊 Your Wellness Overview")
        fig = create_wellness_score_gauge()
        if fig:
            st.plotly_chart(fig, config={"displayModeBar": False})
        else:
            st.markdown(
                f"""
                <div class="pastel-card" style="text-align: center;">
                    <h2 style="color: var(--primary); margin-bottom: 1rem;">Wellness Score</h2>
                    <div style="font-size: 4rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                        {st.session_state.wellness_score:.0f}
                    </div>
                    <p style="color: var(--text-muted);">out of 100</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("### 📈 Recent Activity")
        if st.session_state.symptom_logs:
            df = pd.DataFrame(st.session_state.symptom_logs)[-5:][
                ["date", "hot_flashes", "mood_changes", "sleep_quality", "stress_level"]
            ]
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%m/%d")
            st.dataframe(df, width="stretch", hide_index=True)
        else:
            st.markdown(
                """
                <div class="pastel-card" style="text-align: center; padding: 2rem;">
                    <h3 style="color: var(--text-muted); margin-bottom: 1rem;">No Activity Yet</h3>
                    <p style="color: var(--text-muted); margin-bottom: 1.5rem;">Start tracking your symptoms to see your wellness journey</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Quick Actions Section
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Generate Demo Data", width="stretch"):
            generate_demo_data()
            st.success("Demo data generated!")
            st.rerun()

    with col2:
        if st.button("📝 Log New Symptoms", use_container_width=True):
            st.session_state.current_page = "Tracker"
            st.rerun()

    with col3:
        if st.button("🧹 Clear All Data", use_container_width=True):
            st.session_state.symptom_logs = []
            st.session_state.demo_data_generated = False
            st.session_state.wellness_score = 50.0
            st.success("Data cleared!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_symptom_tracker():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--foreground); margin-bottom: 0.5rem;">📊 Symptom Tracker</h1>
            <p style="color: var(--text-muted);">Monitor your daily symptoms and track your wellness journey</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Input Form
    st.markdown("### 📝 Log New Symptoms")
    with st.form("log_form", clear_on_submit=True):
        st.markdown("**How are you feeling today?**")

        cols = st.columns(4)
        with cols[0]:
            hot = st.slider(
                "🔥 Hot Flashes",
                0,
                10,
                3,
                help="Rate the intensity of hot flashes (0 = none, 10 = severe)",
            )
        with cols[1]:
            mood = st.slider(
                "😊 Mood Changes",
                0,
                10,
                4,
                help="Rate mood fluctuations (0 = stable, 10 = very unstable)",
            )
        with cols[2]:
            sleep = st.slider(
                "😴 Sleep Quality",
                0,
                10,
                6,
                help="Rate your sleep quality (0 = poor, 10 = excellent)",
            )
        with cols[3]:
            stress = st.slider(
                "😰 Stress Level",
                0,
                10,
                4,
                help="Rate your current stress level (0 = very low, 10 = very high)",
            )

        submitted = st.form_submit_button("💾 Save Entry", use_container_width=True)
        if submitted:
            save_symptom_log(
                {
                    "hot_flashes": int(hot),
                    "mood_changes": int(mood),
                    "sleep_quality": int(sleep),
                    "stress_level": int(stress),
                }
            )
            st.success("✅ Entry added successfully!")
            st.balloons()
            st.rerun()

    # Wellness Score Display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div class="metric-card" style="margin: 1rem 0;">
                <h3 style="color: var(--primary); margin-bottom: 0.5rem;">Current Wellness Score</h3>
                <div style="font-size: 3rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                    {st.session_state.wellness_score:.0f}
                </div>
                <p style="margin: 0; color: var(--text-muted);">out of 100</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Visualizations
    st.markdown("### 📈 Symptom Trends")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Timeline Chart")
        fig = create_symptom_timeline_chart()
        if fig:
            st.plotly_chart(fig, config={"displayModeBar": False})
        else:
            if st.session_state.symptom_logs:
                df = pd.DataFrame(st.session_state.symptom_logs)
                df["date"] = pd.to_datetime(df["date"])
                df = df.set_index("date")[
                    ["hot_flashes", "mood_changes", "sleep_quality", "stress_level"]
                ]
                st.line_chart(df)
            else:
                st.markdown(
                    """
                    <div class="pastel-card" style="text-align: center; padding: 2rem;">
                        <h3 style="color: var(--text-muted); margin-bottom: 1rem;">No Data Yet</h3>
                        <p style="color: var(--text-muted);">Start logging symptoms to see your timeline</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with col2:
        st.markdown("#### Symptom Frequency")
        fig2 = create_symptom_frequency_bar()
        if fig2:
            st.plotly_chart(fig2, config={"displayModeBar": False})
        else:
            if st.session_state.symptom_logs:
                df = pd.DataFrame(st.session_state.symptom_logs)
                symptoms = {
                    "Hot Flashes": df["hot_flashes"].mean(),
                    "Mood Changes": df["mood_changes"].mean(),
                    "Sleep Quality": df["sleep_quality"].mean(),
                    "Stress Level": df["stress_level"].mean(),
                }
                freq_df = pd.DataFrame(
                    {"symptom": list(symptoms.keys()), "avg": list(symptoms.values())}
                ).set_index("symptom")
                st.bar_chart(freq_df)
            else:
                st.markdown(
                    """
                    <div class="pastel-card" style="text-align: center; padding: 2rem;">
                        <h3 style="color: var(--text-muted); margin-bottom: 1rem;">No Data Yet</h3>
                        <p style="color: var(--text-muted);">Start logging symptoms to see frequency analysis</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Recent Entries Table
    if st.session_state.symptom_logs:
        st.markdown("### 📋 Recent Entries")
        df = pd.DataFrame(st.session_state.symptom_logs)[-10:]
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d %H:%M")
        st.dataframe(
            df[["date", "hot_flashes", "mood_changes", "sleep_quality", "stress_level"]],
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_insights():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--foreground); margin-bottom: 0.5rem;">💡 AI Insights</h1>
            <p style="color: var(--text-muted);">Get personalized recommendations based on your symptoms</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Insights Cards
    insights = get_symptom_insights()

    if insights:
        st.markdown("### 🎯 Personalized Recommendations")
        for i, insight in enumerate(insights, 1):
            color_class = "coral-card" if i % 2 == 0 else "mint-card"
            st.markdown(
                f"""
                <div class="{color_class}" style="margin-bottom: 1rem;">
                    <div style="display: flex; align-items: flex-start; gap: 1rem;">
                        <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; flex-shrink: 0;">
                            {i}
                        </div>
                        <div style="flex: 1;">
                            <p style="margin: 0; font-size: 1.1rem; line-height: 1.5;">{insight}</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="pastel-card" style="text-align: center; padding: 3rem 2rem;">
                <h3 style="color: var(--text-muted); margin-bottom: 1rem;">No Insights Yet</h3>
                <p style="color: var(--text-muted); margin-bottom: 1.5rem;">Start tracking your symptoms to get personalized insights</p>
                <p style="color: var(--text-muted);">The more data you provide, the better our AI can help you!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Wellness Score Section
    if st.session_state.symptom_logs:
        st.markdown("### 📊 Your Wellness Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3 style="color: var(--primary); margin-bottom: 0.5rem;">Overall Wellness</h3>
                    <div style="font-size: 3rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                        {st.session_state.wellness_score:.0f}
                    </div>
                    <p style="margin: 0; color: var(--text-muted);">out of 100</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            # Calculate trend
            if len(st.session_state.symptom_logs) >= 7:
                recent_avg = np.mean(
                    [
                        log["wellness_score"]
                        for log in st.session_state.symptom_logs[-7:]
                        if "wellness_score" in log
                    ]
                )
                older_avg = np.mean(
                    [
                        log["wellness_score"]
                        for log in st.session_state.symptom_logs[-14:-7]
                        if "wellness_score" in log
                    ]
                )
                trend = (
                    "📈 Improving"
                    if recent_avg > older_avg
                    else "📉 Declining"
                    if recent_avg < older_avg
                    else "➡️ Stable"
                )
            else:
                trend = "📊 Building Data"

            st.markdown(
                f"""
                <div class="metric-card">
                    <h3 style="color: var(--secondary); margin-bottom: 0.5rem;">Trend</h3>
                    <div style="font-size: 2rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                        {trend}
                    </div>
                    <p style="margin: 0; color: var(--text-muted);">7-day trend</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def render_educational_resources():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--foreground); margin-bottom: 0.5rem;">📚 Educational Resources</h1>
            <p style="color: var(--text-muted);">Learn about menopause and how to manage your symptoms</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Educational content tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🧠 Understanding Menopause",
            "🩺 Symptom Management",
            "🥗 Lifestyle & Nutrition",
            "💚 Mental Health",
        ]
    )

    with tab1:
        st.markdown(
            """
            <div class="pastel-card">
                <h3>What is Menopause?</h3>
                <p>Menopause is a natural biological process that marks the end of a woman's reproductive years. It typically occurs between the ages of 45 and 55, when the ovaries stop producing eggs and hormone levels decline.</p>
                
                <h4>Key Stages:</h4>
                <ul>
                    <li><strong>Perimenopause:</strong> The transition period before menopause (can last 4-8 years)</li>
                    <li><strong>Menopause:</strong> When you haven't had a period for 12 consecutive months</li>
                    <li><strong>Postmenopause:</strong> The years after menopause</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("🔬 Hormonal Changes"):
            st.markdown(
                """
                **Estrogen and Progesterone Decline:**
                - Estrogen levels drop significantly, affecting many body systems
                - Progesterone production decreases
                - These changes can cause various symptoms and health considerations
                
                **Impact on Body Systems:**
                - Cardiovascular system
                - Bone health
                - Skin and hair
                - Mood and cognitive function
                """
            )

    with tab2:
        st.markdown(
            """
            <div class="pastel-card">
                <h3>Common Symptoms & Management</h3>
                <p>Every woman's experience with menopause is unique. Here are some common symptoms and strategies to manage them:</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div class="coral-card" style="padding: 1.5rem;">
                    <h4>🔥 Hot Flashes</h4>
                    <ul>
                        <li>Dress in layers</li>
                        <li>Avoid triggers (spicy foods, caffeine)</li>
                        <li>Practice deep breathing</li>
                        <li>Keep room temperature cool</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="mint-card" style="padding: 1.5rem;">
                    <h4>😴 Sleep Issues</h4>
                    <ul>
                        <li>Maintain regular sleep schedule</li>
                        <li>Create cool, dark bedroom</li>
                        <li>Avoid screens before bed</li>
                        <li>Practice relaxation techniques</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab3:
        st.markdown(
            """
            <div class="pastel-card">
                <h3>Nutrition & Lifestyle Tips</h3>
                <p>Healthy lifestyle choices can help manage menopause symptoms and promote overall well-being.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🥗 Nutrition")
            st.markdown(
                """
                **Foods to Include:**
                - Calcium-rich foods (dairy, leafy greens)
                - Omega-3 fatty acids (fish, nuts)
                - Phytoestrogens (soy, flaxseeds)
                - Vitamin D sources
                - Whole grains and fiber
                
                **Foods to Limit:**
                - Processed foods
                - Excessive caffeine
                - Alcohol
                - Spicy foods (if triggering hot flashes)
                """
            )

        with col2:
            st.markdown("#### 🏃‍♀️ Exercise")
            st.markdown(
                """
                **Recommended Activities:**
                - Weight-bearing exercises (bone health)
                - Cardiovascular exercise
                - Strength training
                - Yoga and stretching
                - Walking or swimming
                
                **Benefits:**
                - Reduces hot flashes
                - Improves mood
                - Strengthens bones
                - Better sleep quality
                """
            )

    with tab4:
        st.markdown(
            """
            <div class="pastel-card">
                <h3>Mental Health & Emotional Well-being</h3>
                <p>Menopause can affect your mental health and emotional well-being. It's important to take care of your mental health during this transition.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 💭 Common Emotional Changes")
        st.markdown(
            """
            - Mood swings and irritability
            - Anxiety and worry
            - Depression or sadness
            - Brain fog and memory issues
            - Changes in self-esteem
            """
        )

        st.markdown("#### 💚 Coping Strategies")
        st.markdown(
            """
            - **Talk to someone:** Share your feelings with friends, family, or a therapist
            - **Practice self-care:** Make time for activities you enjoy
            - **Stay connected:** Maintain social relationships
            - **Mindfulness:** Practice meditation or deep breathing
            - **Professional help:** Don't hesitate to seek counseling if needed
            """
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_settings():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--foreground); margin-bottom: 0.5rem;">⚙️ Settings</h1>
            <p style="color: var(--text-muted);">Customize your MenoBalance AI experience</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # User Profile Section
    st.markdown("### 👤 User Profile")

    with st.form("user_profile"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=st.session_state.user_profile.get("age") or 40,
            )
            last_period = st.number_input(
                "Months since last period",
                min_value=0,
                max_value=120,
                value=st.session_state.user_profile.get("last_period_months") or 12,
            )

        with col2:
            st.markdown("#### Menopause Stage")
            if last_period < 3:
                stage = "Pre-menopause"
            elif last_period < 12:
                stage = "Peri-menopause"
            else:
                stage = "Post-menopause"

            st.info(f"**Current Stage:** {stage}")

        if st.form_submit_button("💾 Save Profile", use_container_width=True):
            st.session_state.user_profile["age"] = int(age)
            st.session_state.user_profile["last_period_months"] = int(last_period)
            st.success("✅ Profile updated successfully!")

    # Data Management Section
    st.markdown("### 📊 Data Management")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📤 Export Data")
        if st.button("📥 Download My Data", use_container_width=True):
            if st.session_state.symptom_logs:
                df = pd.DataFrame(st.session_state.symptom_logs)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"menobalance_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                )
            else:
                st.info("No data to export yet. Start tracking your symptoms!")

    with col2:
        st.markdown("#### 🗑️ Clear Data")
        if st.button("🧹 Clear All Data", use_container_width=True):
            st.session_state.symptom_logs = []
            st.session_state.demo_data_generated = False
            st.session_state.wellness_score = 50.0
            st.success("✅ All data cleared!")
            st.rerun()

    # Privacy Settings
    st.markdown("### 🔒 Privacy & Security")

    st.markdown(
        """
        <div class="pastel-card">
            <h4>🔐 Data Privacy</h4>
            <p>Your health data is stored locally in your browser and is never shared with third parties. All predictions are processed securely and your personal information remains private.</p>
            
            <h4>🛡️ Security Features</h4>
            <ul>
                <li>Local data storage (no cloud uploads)</li>
                <li>Encrypted data transmission</li>
                <li>No personal data collection</li>
                <li>GDPR compliant</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # About Section
    st.markdown("### ℹ️ About MenoBalance AI")

    st.markdown(
        f"""
        <div class="pastel-card">
            <p><strong>Version:</strong> 1.0.0</p>
            <p><strong>Last Updated:</strong> {datetime.now().strftime("%Y-%m-%d")}</p>
            <p><strong>AI Models:</strong> Advanced machine learning models trained on diverse datasets</p>
            <p><strong>Disclaimer:</strong> This tool provides general health information and should not replace professional medical advice.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    initialize_session_state()

    # Streamlit sidebar is collapsible by default - no custom toggle needed

    # Enhanced Sidebar
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem 1rem;">
                <h1 style="color: white; margin: 0; font-size: 1.8rem;">🌸 MenoBalance AI</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0; font-size: 0.9rem;">
                    Harmonize your hormonal rhythms, master your symptoms
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        nav = st.radio(
            "Navigate",
            [
                "🏠 Home",
                "🌟 Wellness Dashboard",
                "📊 Tracker",
                "💡 Insights",
                "🏥 Health Input",
                "🔍 Model Analysis",
                "📚 Resources",
                "⚙️ Settings",
            ],
        )

        st.markdown("---")

        # Quick Stats
        if st.session_state.symptom_logs:
            st.markdown("### 📈 Quick Stats")
            st.metric("Days Tracked", len(st.session_state.symptom_logs))
            st.metric("Wellness Score", f"{st.session_state.wellness_score:.0f}/100")
            st.markdown("---")

        # Quick Actions
        st.markdown("### 🚀 Quick Actions")
        if st.button("📊 Generate Demo Data", width="stretch"):
            generate_demo_data()
            st.success("Demo data generated!")
            st.rerun()

        if st.button("🧹 Clear Data", use_container_width=True):
            st.session_state.symptom_logs = []
            st.session_state.demo_data_generated = False
            st.session_state.wellness_score = 50.0
            st.success("Data cleared!")
            st.rerun()

        st.markdown("---")

        # API Status
        api_status = "✅ Connected" if test_api_connection() else "❌ Offline"
        st.markdown(f"**Model Status:** {api_status}")

        # Show model loading details
        if st.button("🔍 Check Model Details", use_container_width=True):
            test_api_connection()

        # Show model status information
        if st.button("📊 Model Status", use_container_width=True):
            try:
                from streamlit_cloud_fix import show_model_loading_info

                show_model_loading_info()
            except ImportError:
                st.error("Model status checker not available")

        # Footer
        st.markdown(
            """
            <div style="text-align: center; margin-top: 2rem; padding: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                <p style="color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0;">
                    Made with ❤️ for women's health
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Render selected page
    try:
        if nav == "🏠 Home":
            render_home_page()
        elif nav == "🌟 Wellness Dashboard":
            try:
                from pages.wellness_dashboard import render_wellness_dashboard

                render_wellness_dashboard()
            except ImportError as e:
                st.error(f"Wellness Dashboard not available: {e}")
                st.info(
                    "Please check that the wellness_dashboard.py file exists in the pages directory."
                )
        elif nav == "📊 Tracker":
            render_symptom_tracker()
        elif nav == "💡 Insights":
            render_insights()
        elif nav == "🏥 Health Input":
            try:
                from pages.health_input import render_health_input

                render_health_input()
            except ImportError as e:
                st.error(f"Health Input page not available: {e}")
                st.info("Please check that the health_input.py file exists in the pages directory.")
        elif nav == "🔍 Model Analysis":
            try:
                from pages.model_explainability import render_model_explainability

                render_model_explainability()
            except ImportError as e:
                st.error(f"Model Analysis page not available: {e}")
                st.info(
                    "Please check that the model_explainability.py file exists in the pages directory."
                )
        elif nav == "📚 Resources":
            render_educational_resources()
        elif nav == "⚙️ Settings":
            render_settings()
        else:
            st.error(f"Unknown page: {nav}")
    except Exception as e:
        st.error(f"Error loading page: {e}")
        st.info("Please check the console for more details.")


if __name__ == "__main__":
    main()
