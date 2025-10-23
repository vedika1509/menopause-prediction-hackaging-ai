"""
Wellness Dashboard Page for MenoBalance AI
Daily wellness scoring, progress tracking, and interactive health metrics.
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_wellness_dashboard():
    """Render the wellness dashboard page."""
    st.markdown(
        """
    <div class="card">
        <h2 class="card-title">📊 Wellness Dashboard</h2>
        <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            Track your daily wellness score and monitor your health journey with interactive visualizations.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize wellness data if not exists
    if "wellness_scores" not in st.session_state:
        st.session_state.wellness_scores = generate_sample_wellness_data()

    # Today's wellness input
    render_today_wellness_input()

    # Dashboard metrics
    render_wellness_metrics()

    # Progress charts
    render_progress_charts()

    # Goal setting
    render_goal_setting()


def generate_sample_wellness_data():
    """Generate sample wellness data for demonstration."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq="D")

    wellness_data = []
    base_score = 75

    for i, date in enumerate(dates):
        # Generate realistic wellness scores with some variation
        score_variation = random.uniform(-10, 10)
        daily_score = max(0, min(100, base_score + score_variation))

        wellness_data.append(
            {
                "date": date,
                "wellness_score": daily_score,
                "sleep_quality": random.randint(6, 10),
                "stress_level": random.randint(3, 7),
                "activity_level": random.randint(5, 10),
                "mood_score": random.randint(6, 9),
                "energy_level": random.randint(5, 9),
                "symptom_severity": random.randint(2, 6),
            }
        )

    return wellness_data


def render_today_wellness_input():
    """Render today's wellness input form."""
    st.markdown("### 📝 Today's Wellness Check-in")

    with st.form("wellness_form"):
        col1, col2 = st.columns(2)

        with col1:
            sleep_quality = st.slider(
                "Sleep Quality (1-10)",
                min_value=1,
                max_value=10,
                value=7,
                help="How well did you sleep last night?",
            )

            stress_level = st.slider(
                "Stress Level (1-10)",
                min_value=1,
                max_value=10,
                value=5,
                help="How stressed do you feel today? (1=very low, 10=very high)",
            )

            activity_level = st.slider(
                "Activity Level (1-10)",
                min_value=1,
                max_value=10,
                value=6,
                help="How active were you today?",
            )

        with col2:
            mood_score = st.slider(
                "Mood Score (1-10)",
                min_value=1,
                max_value=10,
                value=7,
                help="How is your mood today?",
            )

            energy_level = st.slider(
                "Energy Level (1-10)",
                min_value=1,
                max_value=10,
                value=6,
                help="How energetic do you feel?",
            )

            symptom_severity = st.slider(
                "Symptom Severity (1-10)",
                min_value=1,
                max_value=10,
                value=4,
                help="How severe are your menopause symptoms today?",
            )

        # Calculate wellness score
        wellness_score = calculate_wellness_score(
            sleep_quality, stress_level, activity_level, mood_score, energy_level, symptom_severity
        )

        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">{wellness_score}</div>
            <div class="metric-label">Today's Wellness Score</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.form_submit_button("💾 Save Today's Wellness Data", use_container_width=True):
            # Save today's data
            today_data = {
                "date": datetime.now().date(),
                "wellness_score": wellness_score,
                "sleep_quality": sleep_quality,
                "stress_level": stress_level,
                "activity_level": activity_level,
                "mood_score": mood_score,
                "energy_level": energy_level,
                "symptom_severity": symptom_severity,
            }

            # Update or add today's data
            today = datetime.now().date()
            st.session_state.wellness_scores = [
                data
                for data in st.session_state.wellness_scores
                if pd.to_datetime(data["date"]).date() != today
            ] + [today_data]

            st.success("✅ Today's wellness data saved!")
            st.rerun()


def calculate_wellness_score(sleep, stress, activity, mood, energy, symptoms):
    """Calculate overall wellness score from individual metrics."""
    # Weighted average with stress and symptoms negatively weighted
    weights = {
        "sleep": 0.2,
        "stress": -0.15,  # Negative weight
        "activity": 0.15,
        "mood": 0.2,
        "energy": 0.15,
        "symptoms": -0.15,  # Negative weight
    }

    base_score = 50  # Base score

    weighted_score = (
        sleep * weights["sleep"]
        + stress * weights["stress"]
        + activity * weights["activity"]
        + mood * weights["mood"]
        + energy * weights["energy"]
        + symptoms * weights["symptoms"]
    )

    final_score = base_score + weighted_score * 5  # Scale to 0-100
    return max(0, min(100, round(final_score)))


def render_wellness_metrics():
    """Render wellness metrics overview."""
    st.markdown("### 📈 Wellness Overview")

    # Get latest data
    latest_data = st.session_state.wellness_scores[-1] if st.session_state.wellness_scores else None

    if latest_data:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Wellness Score",
                f"{latest_data['wellness_score']}/100",
                delta=f"{latest_data['wellness_score'] - 75}"
                if len(st.session_state.wellness_scores) > 1
                else None,
            )

        with col2:
            st.metric(
                "Sleep Quality",
                f"{latest_data['sleep_quality']}/10",
                delta=f"{latest_data['sleep_quality'] - 7}"
                if len(st.session_state.wellness_scores) > 1
                else None,
            )

        with col3:
            st.metric(
                "Stress Level",
                f"{latest_data['stress_level']}/10",
                delta=f"{latest_data['stress_level'] - 5}"
                if len(st.session_state.wellness_scores) > 1
                else None,
            )

        with col4:
            st.metric(
                "Activity Level",
                f"{latest_data['activity_level']}/10",
                delta=f"{latest_data['activity_level'] - 6}"
                if len(st.session_state.wellness_scores) > 1
                else None,
            )


def render_progress_charts():
    """Render progress tracking charts."""
    st.markdown("### 📊 Progress Tracking")

    # Check if we have wellness data
    if not st.session_state.wellness_scores:
        st.info("No wellness data available yet. Please add your daily wellness data above.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.wellness_scores)

    # Check if date column exists and convert it
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    else:
        st.error("Date column missing from wellness data. Please refresh the page.")
        return

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 Wellness Trend", "🔍 Detailed Metrics", "🎯 Goal Progress"])

    with tab1:
        render_wellness_trend_chart(df)

    with tab2:
        render_detailed_metrics_chart(df)

    with tab3:
        render_goal_progress_chart(df)


def render_wellness_trend_chart(df):
    """Render wellness trend chart."""
    fig = go.Figure()

    # Add wellness score line
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["wellness_score"],
            mode="lines+markers",
            name="Wellness Score",
            line=dict(color="#9B59B6", width=3),
            marker=dict(size=8),
        )
    )

    # Add trend line
    z = np.polyfit(range(len(df)), df["wellness_score"], 1)
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
        title="7-Day Wellness Score Trend",
        xaxis_title="Date",
        yaxis_title="Wellness Score",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Trend interpretation
    if len(df) > 1:
        trend = df["wellness_score"].iloc[-1] - df["wellness_score"].iloc[0]
        if trend > 5:
            st.success("📈 Your wellness is improving! Keep up the great work!")
        elif trend < -5:
            st.warning("📉 Your wellness has decreased. Consider reviewing your routine.")
        else:
            st.info("📊 Your wellness is stable. Small adjustments might help improve it further.")


def render_detailed_metrics_chart(df):
    """Render detailed metrics chart."""
    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Sleep Quality", "Stress Level", "Activity Level", "Mood Score"),
        vertical_spacing=0.1,
    )

    metrics = ["sleep_quality", "stress_level", "activity_level", "mood_score"]
    colors = ["#4CAF50", "#F44336", "#2196F3", "#FF9800"]

    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]

    for i, (metric, color, pos) in enumerate(zip(metrics, colors, positions)):
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df[metric],
                mode="lines+markers",
                name=metric.replace("_", " ").title(),
                line=dict(color=color, width=2),
                marker=dict(size=6),
            ),
            row=pos[0],
            col=pos[1],
        )

    fig.update_layout(
        title="Detailed Wellness Metrics Over Time",
        height=500,
        showlegend=False,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_goal_progress_chart(df):
    """Render goal progress chart."""
    # Define wellness goals
    goals = {
        "wellness_score": {
            "target": 80,
            "current": df["wellness_score"].iloc[-1] if len(df) > 0 else 0,
        },
        "sleep_quality": {
            "target": 8,
            "current": df["sleep_quality"].iloc[-1] if len(df) > 0 else 0,
        },
        "stress_level": {"target": 4, "current": df["stress_level"].iloc[-1] if len(df) > 0 else 0},
        "activity_level": {
            "target": 7,
            "current": df["activity_level"].iloc[-1] if len(df) > 0 else 0,
        },
    }

    # Create progress bars
    for goal_name, goal_data in goals.items():
        progress = min(1.0, goal_data["current"] / goal_data["target"])

        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(f"**{goal_name.replace('_', ' ').title()}**")

        with col2:
            st.progress(progress)
            st.markdown(f"{goal_data['current']:.1f} / {goal_data['target']}")

    # Overall goal achievement
    total_progress = sum(
        min(1.0, goals[goal]["current"] / goals[goal]["target"]) for goal in goals
    ) / len(goals)

    st.markdown(
        f"""
    <div class="metric-card">
        <div class="metric-value">{total_progress:.1%}</div>
        <div class="metric-label">Overall Goal Achievement</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_goal_setting():
    """Render goal setting section."""
    st.markdown("---")
    st.markdown("### 🎯 Set Your Wellness Goals")

    with st.form("goals_form"):
        col1, col2 = st.columns(2)

        with col1:
            target_wellness = st.slider(
                "Target Wellness Score",
                min_value=60,
                max_value=100,
                value=80,
                help="What wellness score would you like to achieve?",
            )

            target_sleep = st.slider(
                "Target Sleep Quality",
                min_value=6,
                max_value=10,
                value=8,
                help="What sleep quality score are you aiming for?",
            )

        with col2:
            target_stress = st.slider(
                "Target Stress Level",
                min_value=1,
                max_value=6,
                value=4,
                help="What stress level would you like to maintain?",
            )

            target_activity = st.slider(
                "Target Activity Level",
                min_value=5,
                max_value=10,
                value=7,
                help="What activity level are you aiming for?",
            )

        if st.form_submit_button("🎯 Save Goals", use_container_width=True):
            # Store goals in session state
            st.session_state.wellness_goals = {
                "wellness_score": target_wellness,
                "sleep_quality": target_sleep,
                "stress_level": target_stress,
                "activity_level": target_activity,
            }
            st.success("✅ Your wellness goals have been saved!")

    # Display current goals
    if "wellness_goals" in st.session_state:
        st.markdown("**Your Current Goals:**")
        goals = st.session_state.wellness_goals

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"• Wellness Score: {goals['wellness_score']}")
            st.markdown(f"• Sleep Quality: {goals['sleep_quality']}")

        with col2:
            st.markdown(f"• Stress Level: {goals['stress_level']}")
            st.markdown(f"• Activity Level: {goals['activity_level']}")


def render_wellness_insights():
    """Render wellness insights and recommendations."""
    st.markdown("---")
    st.markdown("### 💡 Wellness Insights")

    if len(st.session_state.wellness_scores) >= 3:
        latest_data = st.session_state.wellness_scores[-1]

        insights = []

        # Sleep insight
        if latest_data["sleep_quality"] < 7:
            insights.append(
                "😴 Your sleep quality could be improved. Consider establishing a bedtime routine."
            )

        # Stress insight
        if latest_data["stress_level"] > 6:
            insights.append(
                "😰 Your stress level is high. Try relaxation techniques or stress management strategies."
            )

        # Activity insight
        if latest_data["activity_level"] < 6:
            insights.append("🏃‍♀️ Increasing your activity level could boost your overall wellness.")

        # Mood insight
        if latest_data["mood_score"] < 6:
            insights.append(
                "😊 Your mood could be improved. Consider activities that bring you joy."
            )

        if insights:
            for insight in insights:
                st.markdown(
                    f"""
                <div class="info-message">
                    <p>{insight}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.success("🌟 Great job! Your wellness metrics are looking good!")

    else:
        st.info("📊 Complete more wellness check-ins to get personalized insights!")
