"""
Wearable Data Sync Page - Manual entry and tracking of wearable data
"""

from datetime import date, datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_wearables_page():
    """Render the wearable data sync page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Page header
    st.markdown(
        """
    <div class="main-header">
        <h1>⌚ Wearable Data Sync</h1>
        <p style="color: var(--medium-gray);">Track your daily health metrics and wellness score</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize wearable data in session state
    if "wearable_data" not in st.session_state:
        st.session_state.wearable_data = []

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📝 Manual Entry", "📊 Historical View", "🏆 Wellness Score"])

    with tab1:
        render_manual_entry()

    with tab2:
        render_historical_view()

    with tab3:
        render_wellness_score()


def render_manual_entry():
    """Render the manual data entry form."""
    st.markdown("### 📝 Add Today's Data")

    with st.form("wearable_entry_form"):
        col1, col2 = st.columns(2)

        with col1:
            entry_date = st.date_input(
                "Date", value=date.today(), help="Select the date for this data entry"
            )

            daily_steps = st.number_input(
                "Daily Steps",
                min_value=0,
                max_value=50000,
                value=8000,
                help="Total steps taken today",
            )

            sleep_hours = st.slider(
                "Sleep Hours",
                min_value=0.0,
                max_value=24.0,
                value=7.0,
                step=0.5,
                help="Hours of sleep last night",
            )

            sleep_quality = st.slider(
                "Sleep Quality (1-10)",
                min_value=1,
                max_value=10,
                value=7,
                help="Rate your sleep quality",
            )

        with col2:
            resting_hr = st.number_input(
                "Resting Heart Rate (bpm)",
                min_value=40,
                max_value=120,
                value=65,
                help="Resting heart rate in beats per minute",
            )

            hrv = st.number_input(
                "HRV (ms)",
                min_value=0,
                max_value=200,
                value=40,
                help="Heart Rate Variability in milliseconds",
            )

            active_minutes = st.number_input(
                "Active Minutes",
                min_value=0,
                max_value=1440,
                value=30,
                help="Minutes of active exercise today",
            )

            stress_score = st.slider(
                "Stress Score (1-10)",
                min_value=1,
                max_value=10,
                value=5,
                help="Rate your stress level today",
            )

        # Submit button
        submitted = st.form_submit_button("💾 Save Data", use_container_width=True)

        if submitted:
            # Calculate wellness score
            wellness_score = calculate_wellness_score(
                {
                    "daily_steps": daily_steps,
                    "sleep_hours": sleep_hours,
                    "sleep_quality": sleep_quality,
                    "resting_hr": resting_hr,
                    "hrv": hrv,
                    "active_minutes": active_minutes,
                    "stress_score": stress_score,
                }
            )

            # Create data entry
            entry = {
                "date": entry_date,
                "daily_steps": daily_steps,
                "sleep_hours": sleep_hours,
                "sleep_quality": sleep_quality,
                "resting_hr": resting_hr,
                "hrv": hrv,
                "active_minutes": active_minutes,
                "stress_score": stress_score,
                "wellness_score": wellness_score,
                "timestamp": datetime.now().isoformat(),
            }

            # Add to session state
            st.session_state.wearable_data.append(entry)

            # Show success message
            st.success(f"✅ Data saved for {entry_date}! Wellness Score: {wellness_score:.1f}/100")
            st.balloons()


def render_historical_view():
    """Render the historical data view."""
    if not st.session_state.wearable_data:
        st.markdown(
            """
        <div class="info-card">
            <h3>📊 No Data Yet</h3>
            <p>Start tracking your daily metrics to see your health trends over time.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.wearable_data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    st.markdown("### 📈 Your Health Trends")

    # Date range selector
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=df["date"].min().date(),
            min_value=df["date"].min().date(),
            max_value=df["date"].max().date(),
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=df["date"].max().date(),
            min_value=df["date"].min().date(),
            max_value=df["date"].max().date(),
        )

    # Filter data
    filtered_df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

    if len(filtered_df) == 0:
        st.warning("No data available for the selected date range.")
        return

    # Create charts
    col1, col2 = st.columns(2)

    with col1:
        # Steps chart
        fig_steps = px.line(
            filtered_df,
            x="date",
            y="daily_steps",
            title="Daily Steps",
            labels={"daily_steps": "Steps", "date": "Date"},
        )
        fig_steps.update_layout(height=300)
        st.plotly_chart(fig_steps, use_container_width=True)

        # Sleep chart
        fig_sleep = px.line(
            filtered_df,
            x="date",
            y="sleep_hours",
            title="Sleep Hours",
            labels={"sleep_hours": "Hours", "date": "Date"},
        )
        fig_sleep.update_layout(height=300)
        st.plotly_chart(fig_sleep, use_container_width=True)

    with col2:
        # Wellness score chart
        fig_wellness = px.line(
            filtered_df,
            x="date",
            y="wellness_score",
            title="Wellness Score",
            labels={"wellness_score": "Score", "date": "Date"},
        )
        fig_wellness.update_layout(height=300)
        st.plotly_chart(fig_wellness, use_container_width=True)

        # Stress vs HRV
        fig_stress = px.scatter(
            filtered_df,
            x="stress_score",
            y="hrv",
            title="Stress vs HRV",
            labels={"stress_score": "Stress Score", "hrv": "HRV (ms)"},
        )
        fig_stress.update_layout(height=300)
        st.plotly_chart(fig_stress, use_container_width=True)

    # Summary statistics
    st.markdown("### 📊 Summary Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_steps = filtered_df["daily_steps"].mean()
        st.metric("Avg Daily Steps", f"{avg_steps:.0f}")

    with col2:
        avg_sleep = filtered_df["sleep_hours"].mean()
        st.metric("Avg Sleep Hours", f"{avg_sleep:.1f}")

    with col3:
        avg_wellness = filtered_df["wellness_score"].mean()
        st.metric("Avg Wellness Score", f"{avg_wellness:.1f}")

    with col4:
        avg_stress = filtered_df["stress_score"].mean()
        st.metric("Avg Stress Score", f"{avg_stress:.1f}")

    # Export data
    if st.button("📥 Export Data as CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"wearable_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )


def render_wellness_score():
    """Render the wellness score dashboard."""
    if not st.session_state.wearable_data:
        st.markdown(
            """
        <div class="info-card">
            <h3>🏆 No Wellness Data Yet</h3>
            <p>Start tracking your daily metrics to see your wellness score.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    # Get latest data
    latest_data = st.session_state.wearable_data[-1]
    wellness_score = latest_data["wellness_score"]

    # Determine wellness level and color
    if wellness_score >= 75:
        level = "Excellent"
        color = "#26A69A"
        card_class = "success-card"
    elif wellness_score >= 50:
        level = "Good"
        color = "#9C27B0"
        card_class = "info-card"
    else:
        level = "Needs Improvement"
        color = "#FF7043"
        card_class = "warning-card"

    # Main wellness score display
    st.markdown(
        f"""
    <div class="prediction-card {card_class}">
        <h3>🏆 Your Wellness Score</h3>
        <div class="gauge-container">
            <div class="gauge-value" style="color: {color}; font-size: 3rem;">{wellness_score:.1f}/100</div>
            <div class="gauge-label" style="font-size: 1.2rem;">{level}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Create wellness gauge
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=wellness_score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Wellness Score"},
            gauge={
                "axis": {"range": [None, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 50], "color": "#FFE0E0"},
                    {"range": [50, 75], "color": "#FFF0E0"},
                    {"range": [75, 100], "color": "#E0FFE0"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 75},
            },
        )
    )

    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # Wellness breakdown
    st.markdown("### 📊 Wellness Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Today's Metrics:**")
        st.write(f"• Steps: {latest_data['daily_steps']:,}")
        st.write(f"• Sleep: {latest_data['sleep_hours']:.1f} hours")
        st.write(f"• Sleep Quality: {latest_data['sleep_quality']}/10")
        st.write(f"• Active Minutes: {latest_data['active_minutes']}")

    with col2:
        st.markdown("**Health Indicators:**")
        st.write(f"• Resting HR: {latest_data['resting_hr']} bpm")
        st.write(f"• HRV: {latest_data['hrv']} ms")
        st.write(f"• Stress Score: {latest_data['stress_score']}/10")
        st.write(f"• Wellness Score: {wellness_score:.1f}/100")

    # Wellness tips
    st.markdown("### 💡 Wellness Tips")

    tips = []
    if latest_data["daily_steps"] < 10000:
        tips.append("Try to reach 10,000 steps daily for better cardiovascular health")
    if latest_data["sleep_hours"] < 7:
        tips.append("Aim for 7-9 hours of sleep for optimal recovery")
    if latest_data["stress_score"] > 7:
        tips.append("Consider stress management techniques like meditation or deep breathing")
    if latest_data["hrv"] < 30:
        tips.append("Low HRV may indicate stress - try relaxation techniques")

    if tips:
        for tip in tips:
            st.markdown(f"• {tip}")
    else:
        st.markdown(
            "🎉 Great job! Your wellness metrics are looking good. Keep up the healthy habits!"
        )


def calculate_wellness_score(data):
    """Calculate wellness score from wearable data."""
    # Normalize each metric to 0-100 scale
    steps_score = min(100, (data["daily_steps"] / 10000) * 100)
    sleep_score = min(100, (data["sleep_hours"] / 8) * 100)
    sleep_quality_score = (data["sleep_quality"] / 10) * 100
    activity_score = min(100, (data["active_minutes"] / 60) * 100)
    stress_score = max(0, 100 - (data["stress_score"] / 10) * 100)
    hrv_score = min(100, (data["hrv"] / 50) * 100)

    # Weighted average
    wellness_score = (
        steps_score * 0.2
        + sleep_score * 0.2
        + sleep_quality_score * 0.2
        + activity_score * 0.15
        + stress_score * 0.15
        + hrv_score * 0.1
    )

    return min(100, max(0, wellness_score))


# This file is imported by the main app
