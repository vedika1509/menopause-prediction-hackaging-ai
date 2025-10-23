"""
Enhanced Wellness Dashboard with UX improvements, wearable sync, and educational content
"""

import os
import random
import sys
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def get_empathetic_messages():
    """Get empathetic and supportive messages for different situations."""
    return {
        "welcome": [
            "Welcome to your personal menopause journey companion 💜",
            "You're taking an important step in understanding your health - we're here to support you",
            "Every woman's journey is unique, and yours matters deeply to us",
        ],
        "encouragement": [
            "You're doing great by tracking your symptoms - knowledge is power!",
            "Remember, you're not alone in this journey - millions of women are navigating similar experiences",
            "Your health data helps us provide better insights - thank you for sharing",
        ],
        "support": [
            "If you're feeling overwhelmed, that's completely normal - take it one day at a time",
            "Your symptoms are valid, and seeking help is a sign of strength",
            "Remember to be kind to yourself - this transition is a natural part of life",
        ],
        "celebration": [
            "Great job on maintaining your wellness routine! 🌟",
            "Your dedication to tracking your health is inspiring",
            "Small steps lead to big changes - you're making progress",
        ],
    }


def get_educational_tips():
    """Get educational tips about menopause and wellness."""
    return {
        "hormones": {
            "title": "Understanding Your Hormones",
            "tips": [
                "FSH (Follicle Stimulating Hormone) levels typically rise during perimenopause",
                "AMH (Anti-Müllerian Hormone) indicates ovarian reserve - lower levels are normal with age",
                "Estradiol levels fluctuate during the transition - this is completely normal",
                "Hormone levels can vary day-to-day, so single measurements may not tell the whole story",
            ],
        },
        "symptoms": {
            "title": "Managing Common Symptoms",
            "tips": [
                "Hot flashes often peak in the first 2 years of menopause transition",
                "Sleep quality can be improved with consistent bedtime routines and cool room temperatures",
                "Mood changes are often related to hormone fluctuations - they're temporary",
                "Regular exercise can help reduce symptom severity and improve overall wellbeing",
            ],
        },
        "lifestyle": {
            "title": "Lifestyle Support",
            "tips": [
                "A balanced diet rich in calcium and vitamin D supports bone health during menopause",
                "Stress management techniques like meditation can help with mood and sleep",
                "Regular physical activity, even gentle walks, can improve energy and mood",
                "Staying hydrated and limiting caffeine can help with hot flashes and sleep",
            ],
        },
        "wellness": {
            "title": "Daily Wellness Practices",
            "tips": [
                "Start your day with 5 minutes of deep breathing or gentle stretching",
                "Keep a gratitude journal - focusing on positive moments can improve mood",
                "Connect with friends or support groups - social support is crucial during this time",
                "Prioritize sleep - aim for 7-9 hours of quality rest each night",
            ],
        },
    }


def simulate_wearable_data():
    """Simulate wearable device data sync."""
    # Simulate realistic wearable data
    base_date = datetime.now() - timedelta(days=7)

    wearable_data = []
    for i in range(7):
        date = base_date + timedelta(days=i)

        # Simulate realistic patterns
        steps = random.randint(6000, 12000)
        heart_rate_avg = random.randint(65, 85)
        sleep_hours = random.uniform(6.5, 8.5)
        sleep_quality = random.randint(6, 9)
        stress_level = random.randint(3, 7)

        # Calculate wellness score based on multiple factors
        wellness_score = calculate_wellness_score(
            {
                "steps": steps,
                "heart_rate": heart_rate_avg,
                "sleep_hours": sleep_hours,
                "sleep_quality": sleep_quality,
                "stress_level": stress_level,
            }
        )

        wearable_data.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "steps": steps,
                "heart_rate_avg": heart_rate_avg,
                "sleep_hours": round(sleep_hours, 1),
                "sleep_quality": sleep_quality,
                "stress_level": stress_level,
                "wellness_score": wellness_score,
            }
        )

    return wearable_data


def calculate_wellness_score(data):
    """Calculate daily wellness score based on multiple metrics."""
    # Normalize metrics to 0-100 scale
    steps_score = min(100, (data["steps"] / 10000) * 100)
    heart_rate_score = max(0, 100 - abs(data["heart_rate"] - 70) * 2)
    sleep_score = min(100, (data["sleep_hours"] / 8) * 100)
    sleep_quality_score = (data["sleep_quality"] / 10) * 100
    stress_score = max(0, 100 - (data["stress_level"] / 10) * 100)

    # Weighted average
    wellness_score = (
        steps_score * 0.2
        + heart_rate_score * 0.15
        + sleep_score * 0.25
        + sleep_quality_score * 0.25
        + stress_score * 0.15
    )

    return round(wellness_score, 1)


def create_wellness_progress_chart(data):
    """Create a wellness progress chart."""
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    fig = go.Figure()

    # Add wellness score line
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["wellness_score"],
            mode="lines+markers",
            name="Wellness Score",
            line=dict(color="#4CAF50", width=3),
            marker=dict(size=8, color="#4CAF50"),
        )
    )

    # Add target line
    fig.add_hline(
        y=75,
        line_dash="dash",
        line_color="orange",
        annotation_text="Target: 75",
        annotation_position="top right",
    )
    
    fig.update_layout(
        title="7-Day Wellness Progress",
        xaxis_title="Date",
        yaxis_title="Wellness Score",
        height=400,
        showlegend=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_metrics_dashboard(data):
    """Create a comprehensive metrics dashboard."""
    latest = data[-1]  # Most recent data

    # Create subplot with multiple metrics
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Steps", "Heart Rate", "Sleep Quality", "Stress Level"),
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}],
            [{"type": "indicator"}, {"type": "indicator"}],
        ],
    )

    # Steps gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=latest["steps"],
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Steps Today"},
            gauge={
                "axis": {"range": [None, 15000]},
                "bar": {"color": "#4CAF50"},
                "steps": [
                    {"range": [0, 5000], "color": "lightgray"},
                    {"range": [5000, 10000], "color": "yellow"},
                    {"range": [10000, 15000], "color": "green"},
                ],
            },
        ),
        row=1,
        col=1,
    )

    # Heart rate gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=latest["heart_rate_avg"],
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Avg Heart Rate"},
            gauge={
                "axis": {"range": [50, 100]},
                "bar": {"color": "#FF5722"},
                "steps": [
                    {"range": [50, 60], "color": "lightblue"},
                    {"range": [60, 80], "color": "green"},
                    {"range": [80, 100], "color": "orange"},
                ],
            },
        ),
        row=1,
        col=2,
    )

    # Sleep quality gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=latest["sleep_quality"],
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Sleep Quality"},
            gauge={
                "axis": {"range": [0, 10]},
                "bar": {"color": "#2196F3"},
                "steps": [
                    {"range": [0, 4], "color": "red"},
                    {"range": [4, 7], "color": "yellow"},
                    {"range": [7, 10], "color": "green"},
                ],
            },
        ),
        row=2,
        col=1,
    )

    # Stress level gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=latest["stress_level"],
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Stress Level"},
            gauge={
                "axis": {"range": [0, 10]},
                "bar": {"color": "#9C27B0"},
                "steps": [
                    {"range": [0, 3], "color": "green"},
                    {"range": [3, 7], "color": "yellow"},
                    {"range": [7, 10], "color": "red"},
                ],
            },
        ),
        row=2,
        col=2,
    )

    fig.update_layout(height=600, showlegend=False)

    return fig


def render_wellness_dashboard():
    """Render the enhanced wellness dashboard."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Empathetic header
    messages = get_empathetic_messages()
    welcome_msg = random.choice(messages["welcome"])
        
        st.markdown(
            f"""
        <div style="text-align: center; margin-bottom: 2rem; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h1 style="color: white; margin-bottom: 1rem;">💜 Your Wellness Journey</h1>
            <p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">{welcome_msg}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Wearable sync simulation
    st.markdown("### 📱 Wearable Device Sync")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.info("🔄 Syncing data from your connected devices...")

    with col2:
        if st.button("🔄 Sync Now", width="stretch"):
            with st.spinner("Syncing wearable data..."):
                time.sleep(2)  # Simulate sync time
                st.success("✅ Sync complete!")

    with col3:
        if st.button("📊 View History", width="stretch"):
            st.session_state.show_history = True

    # Simulate wearable data
    wearable_data = simulate_wearable_data()
    latest_data = wearable_data[-1]

    # Daily wellness score with progress bar
    st.markdown("### 🌟 Today's Wellness Score")

    wellness_score = latest_data["wellness_score"]
    progress_color = (
        "green" if wellness_score >= 75 else "orange" if wellness_score >= 50 else "red"
    )
    
    st.markdown(
        f"""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: #333;">Your Wellness Score</h3>
                <span style="font-size: 2rem; font-weight: bold; color: {progress_color};">{
            wellness_score
        }/100</span>
            </div>
            <div style="background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 50%, #FFC107 100%); height: 100%; width: {
            wellness_score
        }%; transition: width 0.5s ease;"></div>
            </div>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                {
            "🎉 Excellent! Keep up the great work!"
            if wellness_score >= 75
            else "👍 Good progress! Small improvements make a big difference"
            if wellness_score >= 50
            else "💪 Every step counts! Focus on one small improvement today"
        }
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics dashboard
    st.markdown("### 📊 Health Metrics Overview")

    metrics_fig = create_metrics_dashboard(wearable_data)
    st.plotly_chart(metrics_fig, config={"displayModeBar": False})

    # Wellness progress chart
    st.markdown("### 📈 7-Day Wellness Trend")

    progress_fig = create_wellness_progress_chart(wearable_data)
    st.plotly_chart(progress_fig, config={"displayModeBar": False})

    # Educational tips section
    st.markdown("### 💡 Educational Tips & Insights")

    tips = get_educational_tips()

    # Create tabs for different tip categories
    tip_tabs = st.tabs(["🧬 Hormones", "😌 Symptoms", "🏃‍♀️ Lifestyle", "🌟 Wellness"])

    with tip_tabs[0]:
        st.markdown(f"#### {tips['hormones']['title']}")
        for tip in tips["hormones"]["tips"]:
            st.markdown(f"• {tip}")

    with tip_tabs[1]:
        st.markdown(f"#### {tips['symptoms']['title']}")
        for tip in tips["symptoms"]["tips"]:
            st.markdown(f"• {tip}")

    with tip_tabs[2]:
        st.markdown(f"#### {tips['lifestyle']['title']}")
        for tip in tips["lifestyle"]["tips"]:
            st.markdown(f"• {tip}")

    with tip_tabs[3]:
        st.markdown(f"#### {tips['wellness']['title']}")
        for tip in tips["wellness"]["tips"]:
            st.markdown(f"• {tip}")

    # Supportive messages
    st.markdown("### 💜 Support & Encouragement")

    encouragement_msg = random.choice(messages["encouragement"])
    support_msg = random.choice(messages["support"])

    col1, col2 = st.columns(2)

    with col1:
    st.markdown(
        f"""
            <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: #8B4513; margin-top: 0;">💪 Encouragement</h4>
                <p style="color: #8B4513; margin: 0;">{encouragement_msg}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with col2:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: #6B46C1; margin-top: 0;">🤗 Support</h4>
                <p style="color: #6B46C1; margin: 0;">{support_msg}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Quick actions
    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Log Symptoms", width="stretch"):
            st.session_state.current_page = "Health Input"
            st.rerun()
    
    with col2:
        if st.button("📊 View Analysis", width="stretch"):
            st.session_state.current_page = "Model Analysis"
            st.rerun()

    with col3:
        if st.button("💡 Get Tips", width="stretch"):
            st.info("💡 Check out the educational tips above for personalized insights!")

    with col4:
        if st.button("🔄 Refresh Data", width="stretch"):
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render_wellness_dashboard()
