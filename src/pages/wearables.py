"""
Wearables Page for MenoBalance AI
Simulates wearable device data and sync functionality.
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import warnings

# Suppress Plotly deprecation warnings
warnings.filterwarnings("ignore", message="The keyword arguments have been deprecated")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="plotly")


def render_wearables_page():
    """Render the wearables sync page."""
    st.markdown(
        """
    <div class="card">
        <h2 class="card-title">⌚ Wearable Device Sync</h2>
        <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            Sync your wearable devices to get comprehensive health insights and track your wellness journey.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Device connection section
    render_device_connection()

    # Data sync section
    render_data_sync()

    # Health metrics visualization
    render_health_metrics()


def render_device_connection():
    """Render device connection interface."""
    st.markdown("### 📱 Connected Devices")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="card">
            <h4 style="color: #9B59B6;">Apple Watch</h4>
            <p>Status: <span style="color: #4CAF50;">Connected</span></p>
            <p>Last sync: 2 minutes ago</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="card">
            <h4 style="color: #9B59B6;">Fitbit</h4>
            <p>Status: <span style="color: #FF9800;">Disconnected</span></p>
            <p>Last sync: 1 hour ago</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="card">
            <h4 style="color: #9B59B6;">Oura Ring</h4>
            <p>Status: <span style="color: #4CAF50;">Connected</span></p>
            <p>Last sync: 5 minutes ago</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Sync button
    if st.button("🔄 Sync All Devices", width="stretch", type="primary"):
        with st.spinner("Syncing devices..."):
            # Simulate sync delay
            import time

            time.sleep(2)
        st.success("✅ All devices synced successfully!")


def render_data_sync():
    """Render data synchronization interface."""
    st.markdown("### 📊 Data Synchronization")

    # Generate sample wearable data
    wearable_data = generate_sample_wearable_data()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Activity Data")
        activity_df = pd.DataFrame(wearable_data["activity"])
        st.dataframe(activity_df, width="stretch")

    with col2:
        st.markdown("#### 💤 Sleep Data")
        sleep_df = pd.DataFrame(wearable_data["sleep"])
        st.dataframe(sleep_df, width="stretch")

    # Heart rate data
    st.markdown("#### ❤️ Heart Rate Data")
    hr_df = pd.DataFrame(wearable_data["heart_rate"])
    st.dataframe(hr_df, width="stretch")


def render_health_metrics():
    """Render health metrics visualizations."""
    st.markdown("### 📊 Health Metrics Overview")

    # Generate sample data for the last 7 days
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq="D")

    # Create tabs for different metrics
    tab1, tab2, tab3 = st.tabs(["🏃‍♀️ Activity", "💤 Sleep", "❤️ Heart Rate"])

    with tab1:
        render_activity_charts(dates)

    with tab2:
        render_sleep_charts(dates)

    with tab3:
        render_heart_rate_charts(dates)


def render_activity_charts(dates):
    """Render activity charts."""
    # Generate sample activity data
    steps = [random.randint(8000, 15000) for _ in dates]
    calories = [random.randint(1800, 2500) for _ in dates]
    active_minutes = [random.randint(20, 60) for _ in dates]

    # Steps chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=steps,
            mode="lines+markers",
            name="Steps",
            line=dict(color="#4CAF50", width=3),
            marker=dict(size=8),
        )
    )

    fig.update_layout(
        title="Daily Steps (Last 7 Days)",
        xaxis_title="Date",
        yaxis_title="Steps",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, config={"displayModeBar": False})

    # Activity summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Steps", f"{np.mean(steps):,.0f}")
    with col2:
        st.metric("Average Calories", f"{np.mean(calories):,.0f}")
    with col3:
        st.metric("Average Active Minutes", f"{np.mean(active_minutes):.0f}")


def render_sleep_charts(dates):
    """Render sleep charts."""
    # Generate sample sleep data
    sleep_duration = [random.uniform(6.5, 8.5) for _ in dates]
    sleep_quality = [random.randint(70, 95) for _ in dates]
    deep_sleep = [random.uniform(1.5, 2.5) for _ in dates]

    # Sleep duration chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=sleep_duration,
            mode="lines+markers",
            name="Sleep Duration",
            line=dict(color="#2196F3", width=3),
            marker=dict(size=8),
        )
    )

    fig.update_layout(
        title="Sleep Duration (Last 7 Days)",
        xaxis_title="Date",
        yaxis_title="Hours",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, config={"displayModeBar": False})

    # Sleep summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Sleep Duration", f"{np.mean(sleep_duration):.1f} hours")
    with col2:
        st.metric("Average Sleep Quality", f"{np.mean(sleep_quality):.0f}%")
    with col3:
        st.metric("Average Deep Sleep", f"{np.mean(deep_sleep):.1f} hours")


def render_heart_rate_charts(dates):
    """Render heart rate charts."""
    # Generate sample heart rate data
    resting_hr = [random.randint(55, 75) for _ in dates]
    max_hr = [random.randint(160, 180) for _ in dates]
    avg_hr = [random.randint(70, 90) for _ in dates]

    # Heart rate chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=resting_hr,
            mode="lines+markers",
            name="Resting HR",
            line=dict(color="#F44336", width=3),
            marker=dict(size=8),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=max_hr,
            mode="lines+markers",
            name="Max HR",
            line=dict(color="#FF5722", width=3),
            marker=dict(size=8),
        )
    )

    fig.update_layout(
        title="Heart Rate Trends (Last 7 Days)",
        xaxis_title="Date",
        yaxis_title="BPM",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, config={"displayModeBar": False})

    # Heart rate summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Resting HR", f"{np.mean(resting_hr):.0f} BPM")
    with col2:
        st.metric("Average Max HR", f"{np.mean(max_hr):.0f} BPM")
    with col3:
        st.metric("Average HR", f"{np.mean(avg_hr):.0f} BPM")


def generate_sample_wearable_data():
    """Generate sample wearable device data."""
    return {
        "activity": [
            {
                "Date": "2024-01-15",
                "Steps": 12450,
                "Calories": 2150,
                "Active Minutes": 45,
                "Distance (km)": 8.2,
            },
            {
                "Date": "2024-01-16",
                "Steps": 9870,
                "Calories": 1890,
                "Active Minutes": 32,
                "Distance (km)": 6.5,
            },
            {
                "Date": "2024-01-17",
                "Steps": 15680,
                "Calories": 2380,
                "Active Minutes": 58,
                "Distance (km)": 10.3,
            },
        ],
        "sleep": [
            {
                "Date": "2024-01-15",
                "Duration (hours)": 7.5,
                "Quality (%)": 85,
                "Deep Sleep (hours)": 2.1,
                "REM Sleep (hours)": 1.8,
            },
            {
                "Date": "2024-01-16",
                "Duration (hours)": 6.8,
                "Quality (%)": 78,
                "Deep Sleep (hours)": 1.9,
                "REM Sleep (hours)": 1.5,
            },
            {
                "Date": "2024-01-17",
                "Duration (hours)": 8.2,
                "Quality (%)": 92,
                "Deep Sleep (hours)": 2.3,
                "REM Sleep (hours)": 2.0,
            },
        ],
        "heart_rate": [
            {
                "Date": "2024-01-15",
                "Resting HR": 62,
                "Max HR": 175,
                "Average HR": 78,
                "HR Variability": 45,
            },
            {
                "Date": "2024-01-16",
                "Resting HR": 65,
                "Max HR": 168,
                "Average HR": 82,
                "HR Variability": 42,
            },
            {
                "Date": "2024-01-17",
                "Resting HR": 58,
                "Max HR": 182,
                "Average HR": 75,
                "HR Variability": 48,
            },
        ],
    }
