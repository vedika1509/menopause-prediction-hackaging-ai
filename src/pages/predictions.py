"""
Predictions Page for MenoBalance AI
Displays AI predictions with confidence intervals and visualizations.
"""

from datetime import datetime

import numpy as np
import plotly.graph_objects as go
import requests
import streamlit as st


def render_predictions_page():
    """Render the predictions page with visualizations."""
    st.markdown(
        """
    <div class="card">
        <h2 class="card-title">🔮 Your Personalized Predictions</h2>
        <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            Based on your health information, here are your personalized menopause predictions with confidence intervals.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Check if health data exists
    if not st.session_state.health_data:
        st.warning("⚠️ Please complete the Health Input form first to get predictions.")
        if st.button("Go to Health Input", use_container_width=True):
            st.session_state.current_page = "Health Input"
            st.rerun()
        return

    # Show loading spinner
    with st.spinner("🤖 Analyzing your health data and generating predictions..."):
        predictions = get_predictions()

    if predictions:
        st.session_state.predictions = predictions
        display_predictions(predictions)
    else:
        st.error("❌ Failed to generate predictions. Please try again.")
        if st.button("Retry Predictions", use_container_width=True):
            st.rerun()


def get_predictions():
    """Get predictions from the API or fallback service."""
    try:
        # Try to get predictions from API
        api_url = "http://localhost:8000/predict"

        # Prepare health data for API
        health_data = st.session_state.health_data.copy()

        # Make API request
        response = requests.post(api_url, json=health_data, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            st.warning("API not available, using fallback predictions.")
            return get_fallback_predictions(health_data)

    except Exception as e:
        st.warning(f"API error: {e}. Using fallback predictions.")
        return get_fallback_predictions(st.session_state.health_data)


def get_fallback_predictions(health_data):
    """Generate fallback predictions when API is not available."""
    # Simple rule-based fallback predictions
    age = health_data.get("age", 35)
    bmi = health_data.get("bmi", 22)

    # Stage prediction based on age
    if age < 40:
        stage = "Pre-menopause"
        stage_numeric = 0
    elif age < 50:
        stage = "Peri-menopause"
        stage_numeric = 1
    else:
        stage = "Post-menopause"
        stage_numeric = 2

    # Time to menopause (simplified)
    if age < 45:
        time_to_menopause = max(0, 50 - age + np.random.normal(0, 2))
    else:
        time_to_menopause = max(0, np.random.normal(2, 1))

    # Symptom severity (based on age and BMI)
    base_severity = (age - 30) / 20 * 3 + (bmi - 22) / 10
    base_severity = max(0, min(10, base_severity + np.random.normal(0, 1)))

    return {
        "success": True,
        "predictions": {
            "classification": {
                "stage": stage,
                "stage_numeric": stage_numeric,
                "confidence_lower": stage_numeric - 0.3,
                "confidence_upper": stage_numeric + 0.3,
                "confidence_interval": f"{stage_numeric - 0.3:.1f} - {stage_numeric + 0.3:.1f}",
            },
            "survival": {
                "time_to_menopause": time_to_menopause,
                "time_lower_ci": max(0, time_to_menopause - 2),
                "time_upper_ci": time_to_menopause + 2,
                "time_confidence_interval": f"{max(0, time_to_menopause - 2):.1f} - {time_to_menopause + 2:.1f} years",
            },
            "symptom": {
                "symptoms": {
                    "hot_flashes": base_severity,
                    "mood_changes": base_severity * 0.8,
                    "sleep_disturbance": base_severity * 0.9,
                },
                "overall_severity": base_severity,
                "severity_lower_ci": max(0, base_severity - 1),
                "severity_upper_ci": min(10, base_severity + 1),
                "severity_confidence_interval": f"{max(0, base_severity - 1):.1f} - {min(10, base_severity + 1):.1f}",
            },
        },
        "recommendations": [
            {
                "category": "General Health",
                "title": "Regular Healthcare",
                "description": "Maintain regular check-ups with your healthcare provider for preventive care and monitoring.",
                "priority": "high",
            },
            {
                "category": "Lifestyle",
                "title": "Stress Management",
                "description": "Practice stress-reduction techniques such as meditation, deep breathing, or gentle yoga.",
                "priority": "medium",
            },
        ],
        "timestamp": datetime.now().isoformat(),
        "model_version": "1.0.0",
        "confidence_intervals": {
            "stage": f"{stage_numeric - 0.3:.1f} - {stage_numeric + 0.3:.1f}",
            "time_to_menopause": f"{max(0, time_to_menopause - 2):.1f} - {time_to_menopause + 2:.1f} years",
            "symptom_severity": f"{max(0, base_severity - 1):.1f} - {min(10, base_severity + 1):.1f}",
        },
    }


def display_predictions(predictions):
    """Display predictions with beautiful visualizations."""
    pred_data = predictions["predictions"]

    # Create three main columns for the three predictions
    col1, col2, col3 = st.columns(3)

    with col1:
        display_menopause_stage_prediction(pred_data["classification"])

    with col2:
        display_time_to_menopause_prediction(pred_data["survival"])

    with col3:
        display_symptom_severity_prediction(pred_data["symptom"])

    # Detailed visualizations
    st.markdown("---")

    # Create detailed charts section
    col1, col2 = st.columns(2)

    with col1:
        create_stage_confidence_chart(pred_data["classification"])

    with col2:
        create_time_gauge_chart(pred_data["survival"])

    # Symptom breakdown chart
    st.markdown("### 📊 Symptom Severity Breakdown")
    create_symptom_chart(pred_data["symptom"])

    # Recommendations section
    st.markdown("---")
    display_recommendations(predictions["recommendations"])

    # Confidence intervals summary
    display_confidence_summary(predictions["confidence_intervals"])


def display_menopause_stage_prediction(classification_data):
    """Display menopause stage prediction with confidence."""
    stage = classification_data["stage"]
    confidence_interval = classification_data["confidence_interval"]

    # Color coding for stages
    stage_colors = {
        "Pre-menopause": "#4CAF50",
        "Peri-menopause": "#FF9800",
        "Post-menopause": "#F44336",
    }

    color = stage_colors.get(stage, "#9B59B6")

    st.markdown(
        f"""
    <div class="card" style="border-left: 5px solid {color};">
        <h3 style="color: {color}; margin-bottom: 1rem;">🔄 Menopause Stage</h3>
        <div class="metric-value" style="color: {color};">{stage}</div>
        <div class="metric-label">Confidence: {confidence_interval}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_time_to_menopause_prediction(survival_data):
    """Display time to menopause prediction."""
    time_to_menopause = survival_data["time_to_menopause"]
    confidence_interval = survival_data["time_confidence_interval"]

    # Color based on time
    if time_to_menopause < 2:
        color = "#F44336"  # Red for soon
    elif time_to_menopause < 5:
        color = "#FF9800"  # Orange for moderate
    else:
        color = "#4CAF50"  # Green for far

    st.markdown(
        f"""
    <div class="card" style="border-left: 5px solid {color};">
        <h3 style="color: {color}; margin-bottom: 1rem;">⏰ Time to Menopause</h3>
        <div class="metric-value" style="color: {color};">{time_to_menopause:.1f} years</div>
        <div class="metric-label">Range: {confidence_interval}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_symptom_severity_prediction(symptom_data):
    """Display symptom severity prediction."""
    overall_severity = symptom_data["overall_severity"]
    confidence_interval = symptom_data["severity_confidence_interval"]

    # Color based on severity
    if overall_severity > 7:
        color = "#F44336"  # Red for high
    elif overall_severity > 4:
        color = "#FF9800"  # Orange for moderate
    else:
        color = "#4CAF50"  # Green for low

    st.markdown(
        f"""
    <div class="card" style="border-left: 5px solid {color};">
        <h3 style="color: {color}; margin-bottom: 1rem;">😰 Symptom Severity</h3>
        <div class="metric-value" style="color: {color};">{overall_severity:.1f}/10</div>
        <div class="metric-label">Range: {confidence_interval}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_stage_confidence_chart(classification_data):
    """Create a confidence chart for menopause stage."""
    stage = classification_data["stage"]
    stage_numeric = classification_data["stage_numeric"]
    lower_ci = classification_data["confidence_lower"]
    upper_ci = classification_data["confidence_upper"]

    # Create stages list
    stages = ["Pre-menopause", "Peri-menopause", "Post-menopause"]

    fig = go.Figure()

    # Add confidence interval
    fig.add_trace(
        go.Bar(
            x=stages,
            y=[0.33, 0.33, 0.33],  # Equal probabilities
            name="Confidence Interval",
            marker_color=[
                "rgba(76, 175, 80, 0.3)",
                "rgba(255, 152, 0, 0.3)",
                "rgba(244, 67, 54, 0.3)",
            ],
        )
    )

    # Add prediction
    prediction_values = [0, 0, 0]
    prediction_values[stage_numeric] = 1

    fig.add_trace(
        go.Bar(
            x=stages,
            y=prediction_values,
            name="Prediction",
            marker_color=["#4CAF50", "#FF9800", "#F44336"],
        )
    )

    fig.update_layout(
        title="Menopause Stage Confidence",
        xaxis_title="Stage",
        yaxis_title="Probability",
        height=400,
        showlegend=True,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


def create_time_gauge_chart(survival_data):
    """Create a gauge chart for time to menopause."""
    time_to_menopause = survival_data["time_to_menopause"]
    lower_ci = survival_data["time_lower_ci"]
    upper_ci = survival_data["time_upper_ci"]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=time_to_menopause,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Time to Menopause (years)"},
            delta={"reference": 5},
            gauge={
                "axis": {"range": [None, 15]},
                "bar": {"color": "#9B59B6"},
                "steps": [
                    {"range": [0, 3], "color": "lightgray"},
                    {"range": [3, 8], "color": "gray"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 10},
            },
        )
    )

    fig.update_layout(height=400, font={"color": "darkblue", "family": "Arial"})

    st.plotly_chart(fig, use_container_width=True)


def create_symptom_chart(symptom_data):
    """Create a detailed symptom breakdown chart."""
    symptoms = symptom_data["symptoms"]
    symptom_names = list(symptoms.keys())
    symptom_values = list(symptoms.values())

    # Create symptom names for display
    display_names = [name.replace("_", " ").title() for name in symptom_names]

    fig = go.Figure(
        data=[
            go.Bar(
                x=display_names,
                y=symptom_values,
                marker_color=["#FF6B6B", "#4ECDC4", "#45B7D1"],
                text=[f"{val:.1f}" for val in symptom_values],
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="Symptom Severity Breakdown (0-10 scale)",
        xaxis_title="Symptoms",
        yaxis_title="Severity Score",
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


def display_recommendations(recommendations):
    """Display personalized recommendations."""
    st.markdown("### 💡 Personalized Recommendations")

    # Group recommendations by priority
    high_priority = [rec for rec in recommendations if rec.get("priority") == "high"]
    medium_priority = [rec for rec in recommendations if rec.get("priority") == "medium"]

    if high_priority:
        st.markdown("#### 🔴 High Priority")
        for rec in high_priority:
            st.markdown(
                f"""
            <div class="card">
                <h4 style="color: #F44336;">{rec["title"]}</h4>
                <p style="font-family: 'Inter', sans-serif; margin-bottom: 0.5rem;">
                    <strong>Category:</strong> {rec["category"]}
                </p>
                <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
                    {rec["description"]}
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    if medium_priority:
        st.markdown("#### 🟡 Medium Priority")
        for rec in medium_priority:
            st.markdown(
                f"""
            <div class="card">
                <h4 style="color: #FF9800;">{rec["title"]}</h4>
                <p style="font-family: 'Inter', sans-serif; margin-bottom: 0.5rem;">
                    <strong>Category:</strong> {rec["category"]}
                </p>
                <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
                    {rec["description"]}
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )


def display_confidence_summary(confidence_intervals):
    """Display confidence intervals summary."""
    st.markdown("### 📊 Confidence Intervals Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">Stage</div>
            <div class="metric-label">{confidence_intervals["stage"]}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">Time</div>
            <div class="metric-label">{confidence_intervals["time_to_menopause"]}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">Severity</div>
            <div class="metric-label">{confidence_intervals["symptom_severity"]}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div class="info-message">
        <h4>ℹ️ Understanding Confidence Intervals</h4>
        <p>Confidence intervals represent the range of uncertainty in our predictions. 
        A 95% confidence interval means we're 95% confident that the true value falls within this range. 
        These ranges help you understand the reliability of our predictions.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
