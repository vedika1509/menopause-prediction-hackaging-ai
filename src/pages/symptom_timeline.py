"""
Symptom Timeline Page for MenoBalance AI
Interactive timeline for tracking menopause symptoms over time.
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_symptom_timeline_page():
    """Render the symptom timeline page."""
    st.markdown(
        """
    <div class="card">
        <h2 class="card-title">📈 Symptom Timeline</h2>
        <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            Track your menopause symptoms over time and identify patterns to better understand your health journey.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize symptom data if not exists
    if "symptom_timeline" not in st.session_state:
        st.session_state.symptom_timeline = generate_sample_symptom_data()

    # Symptom input form
    render_symptom_input_form()

    # Timeline visualization
    render_symptom_timeline()

    # Pattern analysis
    render_pattern_analysis()


def render_symptom_input_form():
    """Render the symptom input form."""
    st.markdown("### 📝 Add Today's Symptoms")

    with st.form("symptom_form"):
        col1, col2 = st.columns(2)

        with col1:
            hot_flashes = st.slider(
                "Hot Flashes (0-10)",
                min_value=0,
                max_value=10,
                value=0,
                help="Rate the severity of hot flashes today",
            )

            night_sweats = st.slider(
                "Night Sweats (0-10)",
                min_value=0,
                max_value=10,
                value=0,
                help="Rate the severity of night sweats today",
            )

            mood_changes = st.slider(
                "Mood Changes (0-10)",
                min_value=0,
                max_value=10,
                value=0,
                help="Rate the severity of mood changes today",
            )

        with col2:
            sleep_disturbance = st.slider(
                "Sleep Disturbance (0-10)",
                min_value=0,
                max_value=10,
                value=0,
                help="Rate the severity of sleep disturbances today",
            )

            fatigue = st.slider(
                "Fatigue (0-10)",
                min_value=0,
                max_value=10,
                value=0,
                help="Rate the severity of fatigue today",
            )

            joint_pain = st.slider(
                "Joint Pain (0-10)",
                min_value=0,
                max_value=10,
                value=0,
                help="Rate the severity of joint pain today",
            )

        # Additional notes
        notes = st.text_area(
            "Additional Notes",
            placeholder="Any additional symptoms or observations...",
            height=100,
        )

        if st.form_submit_button("💾 Save Today's Symptoms", use_container_width=True):
            # Save today's symptom data
            today_data = {
                "date": datetime.now().date(),
                "hot_flashes": hot_flashes,
                "night_sweats": night_sweats,
                "mood_changes": mood_changes,
                "sleep_disturbance": sleep_disturbance,
                "fatigue": fatigue,
                "joint_pain": joint_pain,
                "notes": notes,
                "overall_severity": (hot_flashes + night_sweats + mood_changes + sleep_disturbance + fatigue + joint_pain) / 6,
            }

            # Update or add today's data
            today = datetime.now().date()
            st.session_state.symptom_timeline = [
                data
                for data in st.session_state.symptom_timeline
                if pd.to_datetime(data["date"]).date() != today
            ] + [today_data]

            st.success("✅ Today's symptoms saved!")
            st.rerun()


def render_symptom_timeline():
    """Render the symptom timeline visualization."""
    st.markdown("### 📊 Symptom Timeline")

    if not st.session_state.symptom_timeline:
        st.info("No symptom data available yet. Please add your daily symptoms above.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.symptom_timeline)
    df["date"] = pd.to_datetime(df["date"])

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 Overall Trend", "🔥 Hot Flashes", "😴 Sleep & Mood"])

    with tab1:
        render_overall_trend_chart(df)

    with tab2:
        render_hot_flash_chart(df)

    with tab3:
        render_sleep_mood_chart(df)


def render_overall_trend_chart(df):
    """Render overall symptom trend chart."""
    fig = go.Figure()

    # Add overall severity line
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["overall_severity"],
            mode="lines+markers",
            name="Overall Severity",
            line=dict(color="#9B59B6", width=3),
            marker=dict(size=8),
        )
    )

    # Add trend line
    if len(df) > 1:
        z = np.polyfit(range(len(df)), df["overall_severity"], 1)
        p = np.poly1d(z)
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=p(range(len(df))),
                mode="lines",
                name="Trend",
                line=dict(color="#E8DAEF", width=2, dash="dash"),
            )
        )

    fig.update_layout(
        title="Overall Symptom Severity Trend",
        xaxis_title="Date",
        yaxis_title="Severity (0-10)",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Trend interpretation
    if len(df) > 1:
        trend = df["overall_severity"].iloc[-1] - df["overall_severity"].iloc[0]
        if trend > 1:
            st.warning("📈 Your symptoms are increasing. Consider consulting with your healthcare provider.")
        elif trend < -1:
            st.success("📉 Your symptoms are decreasing. Keep up the good work!")
        else:
            st.info("📊 Your symptoms are relatively stable.")


def render_hot_flash_chart(df):
    """Render hot flash specific chart."""
    fig = go.Figure()

    # Add hot flashes and night sweats
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["hot_flashes"],
            mode="lines+markers",
            name="Hot Flashes",
            line=dict(color="#F44336", width=3),
            marker=dict(size=8),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["night_sweats"],
            mode="lines+markers",
            name="Night Sweats",
            line=dict(color="#FF5722", width=3),
            marker=dict(size=8),
        )
    )

    fig.update_layout(
        title="Hot Flashes & Night Sweats",
        xaxis_title="Date",
        yaxis_title="Severity (0-10)",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Hot flash insights
    avg_hot_flashes = df["hot_flashes"].mean()
    if avg_hot_flashes > 6:
        st.warning("🔥 You're experiencing frequent hot flashes. Consider cooling strategies and discuss with your healthcare provider.")
    elif avg_hot_flashes > 3:
        st.info("🌡️ Moderate hot flash activity. Try layering clothes and keeping cool.")
    else:
        st.success("❄️ Low hot flash activity. Great job managing your symptoms!")


def render_sleep_mood_chart(df):
    """Render sleep and mood chart."""
    fig = go.Figure()

    # Add sleep disturbance and mood changes
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["sleep_disturbance"],
            mode="lines+markers",
            name="Sleep Disturbance",
            line=dict(color="#2196F3", width=3),
            marker=dict(size=8),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["mood_changes"],
            mode="lines+markers",
            name="Mood Changes",
            line=dict(color="#FF9800", width=3),
            marker=dict(size=8),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["fatigue"],
            mode="lines+markers",
            name="Fatigue",
            line=dict(color="#607D8B", width=3),
            marker=dict(size=8),
        )
    )

    fig.update_layout(
        title="Sleep, Mood & Fatigue",
        xaxis_title="Date",
        yaxis_title="Severity (0-10)",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Sleep and mood insights
    avg_sleep = df["sleep_disturbance"].mean()
    avg_mood = df["mood_changes"].mean()
    avg_fatigue = df["fatigue"].mean()

    col1, col2, col3 = st.columns(3)
    with col1:
        if avg_sleep > 6:
            st.error("😴 High sleep disturbance. Consider sleep hygiene strategies.")
        else:
            st.success("😴 Sleep quality is manageable.")

    with col2:
        if avg_mood > 6:
            st.error("😰 High mood changes. Consider stress management techniques.")
        else:
            st.success("😊 Mood is relatively stable.")

    with col3:
        if avg_fatigue > 6:
            st.error("😴 High fatigue levels. Consider energy management strategies.")
        else:
            st.success("⚡ Energy levels are manageable.")


def render_pattern_analysis():
    """Render pattern analysis section."""
    st.markdown("### 🔍 Pattern Analysis")

    if not st.session_state.symptom_timeline:
        st.info("No symptom data available for pattern analysis.")
        return

    df = pd.DataFrame(st.session_state.symptom_timeline)
    df["date"] = pd.to_datetime(df["date"])

    # Symptom correlation matrix
    st.markdown("#### 📊 Symptom Correlations")
    symptom_cols = ["hot_flashes", "night_sweats", "mood_changes", "sleep_disturbance", "fatigue", "joint_pain"]
    correlation_matrix = df[symptom_cols].corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale="RdBu",
            zmid=0,
        )
    )

    fig.update_layout(
        title="Symptom Correlation Matrix",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Pattern insights
    st.markdown("#### 💡 Pattern Insights")

    # Find strongest correlations
    correlations = []
    for i in range(len(symptom_cols)):
        for j in range(i + 1, len(symptom_cols)):
            corr = correlation_matrix.iloc[i, j]
            if abs(corr) > 0.5:  # Strong correlation
                correlations.append((symptom_cols[i], symptom_cols[j], corr))

    if correlations:
        st.markdown("**Strong symptom correlations found:**")
        for symptom1, symptom2, corr in correlations:
            st.markdown(f"• {symptom1.replace('_', ' ').title()} & {symptom2.replace('_', ' ').title()}: {corr:.2f}")
    else:
        st.info("No strong correlations found between symptoms. This is normal - symptoms can vary independently.")

    # Weekly patterns
    if len(df) >= 7:
        st.markdown("#### 📅 Weekly Patterns")
        df["weekday"] = df["date"].dt.day_name()
        weekday_avg = df.groupby("weekday")["overall_severity"].mean()

        fig = go.Figure(
            data=go.Bar(
                x=weekday_avg.index,
                y=weekday_avg.values,
                marker_color="#9B59B6",
            )
        )

        fig.update_layout(
            title="Average Symptom Severity by Day of Week",
            xaxis_title="Day of Week",
            yaxis_title="Average Severity",
            height=400,
            template="plotly_white",
        )

        st.plotly_chart(fig, use_container_width=True)


def generate_sample_symptom_data():
    """Generate sample symptom data for demonstration."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=14), end=datetime.now(), freq="D")

    symptom_data = []
    for i, date in enumerate(dates):
        # Generate realistic symptom scores with some variation
        base_severity = 3 + (i % 7) * 0.5  # Slight weekly pattern

        symptom_data.append({
            "date": date,
            "hot_flashes": max(0, min(10, base_severity + random.uniform(-2, 2))),
            "night_sweats": max(0, min(10, base_severity + random.uniform(-2, 2))),
            "mood_changes": max(0, min(10, base_severity + random.uniform(-2, 2))),
            "sleep_disturbance": max(0, min(10, base_severity + random.uniform(-2, 2))),
            "fatigue": max(0, min(10, base_severity + random.uniform(-2, 2))),
            "joint_pain": max(0, min(10, base_severity + random.uniform(-2, 2))),
            "notes": "",
            "overall_severity": 0,  # Will be calculated
        })

    # Calculate overall severity
    for data in symptom_data:
        data["overall_severity"] = (
            data["hot_flashes"] + data["night_sweats"] + data["mood_changes"] + 
            data["sleep_disturbance"] + data["fatigue"] + data["joint_pain"]
        ) / 6

    return symptom_data
