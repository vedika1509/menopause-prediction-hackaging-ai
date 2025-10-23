"""
Predictions Page - Beautiful visualization of health predictions
"""

import streamlit as st

# Try to import plotly with fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available. Some visualizations may be limited.")


def render_predictions_page():
    """Render the predictions results page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Check if predictions exist
    if "predictions" not in st.session_state or not st.session_state.predictions:
        st.markdown(
            """
        <div class="warning-card">
            <h3>📊 No Predictions Available</h3>
            <p>Please complete your health assessment first to see your personalized predictions.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("📝 Complete Health Assessment", use_container_width=True):
            st.session_state.current_page = "health_input"
            st.rerun()
        return

    predictions = st.session_state.predictions

    # Page header
    st.markdown(
        """
    <div class="main-header">
        <h1>📊 Your Health Insights</h1>
        <p style="color: var(--medium-gray);">Personalized predictions based on your health profile</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Main prediction cards
    col1, col2 = st.columns(2)

    with col1:
        render_survival_card(predictions.get("survival", {}))

    with col2:
        render_symptom_card(predictions.get("symptoms", {}))

    # Recommendations section
    if "recommendations" in predictions and predictions["recommendations"]:
        render_recommendations_section(predictions["recommendations"])

    # SHAP explainability section
    render_explainability_section(predictions)

    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💬 Chat with AI Assistant", use_container_width=True):
            st.session_state.current_page = "chatbot"
            st.rerun()

    with col2:
        if st.button("📈 View Health Timeline", use_container_width=True):
            st.session_state.current_page = "timeline"
            st.rerun()

    with col3:
        if st.button("📄 Export Report", use_container_width=True):
            st.session_state.current_page = "export"
            st.rerun()


def render_survival_card(survival_data):
    """Render the survival prediction card."""
    if not survival_data:
        return

    years = survival_data.get("time_to_menopause_years", 0)
    risk_level = survival_data.get("risk_level", "unknown")
    confidence_interval = survival_data.get("confidence_interval", [0, 0])
    explanation = survival_data.get("explanation", "")

    # Determine card color based on risk level
    if risk_level == "high":
        card_class = "warning-card"
        color = "#FF7043"
    elif risk_level == "moderate":
        card_class = "info-card"
        color = "#9C27B0"
    else:
        card_class = "success-card"
        color = "#26A69A"

    st.markdown(
        f"""
    <div class="prediction-card {card_class}">
        <h3>⏰ Menopause Timeline</h3>
        <div class="gauge-container">
            <div class="gauge-value" style="color: {color};">{years:.1f} years</div>
            <div class="gauge-label">Predicted time to menopause</div>
        </div>
        <p><strong>Confidence Range:</strong> {confidence_interval[0]:.1f} - {confidence_interval[1]:.1f} years</p>
        <p><strong>Risk Level:</strong> {risk_level.title()}</p>
        <p style="font-size: 0.9rem; color: var(--medium-gray);">{explanation}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Create gauge chart
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=years,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Years to Menopause"},
            gauge={
                "axis": {"range": [None, 10]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 2], "color": "#FFE0E0"},
                    {"range": [2, 5], "color": "#FFF0E0"},
                    {"range": [5, 10], "color": "#E0FFE0"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 5},
            },
        )
    )

    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def render_symptom_card(symptom_data):
    """Render the symptom prediction card."""
    if not symptom_data:
        return

    severity_score = symptom_data.get("severity_score", 0)
    severity_level = symptom_data.get("severity_level", "unknown")
    confidence_interval = symptom_data.get("confidence_interval", [0, 0])
    top_symptoms = symptom_data.get("top_symptoms", [])
    symptom_breakdown = symptom_data.get("symptom_breakdown", {})
    explanation = symptom_data.get("explanation", "")

    # Determine card color based on severity
    if severity_level == "high":
        card_class = "warning-card"
        color = "#FF7043"
    elif severity_level == "moderate":
        card_class = "info-card"
        color = "#9C27B0"
    else:
        card_class = "success-card"
        color = "#26A69A"

    st.markdown(
        f"""
    <div class="prediction-card {card_class}">
        <h3>🩺 Symptom Severity</h3>
        <div class="gauge-container">
            <div class="gauge-value" style="color: {color};">{severity_score:.1f}/10</div>
            <div class="gauge-label">Overall symptom severity</div>
        </div>
        <p><strong>Confidence Range:</strong> {confidence_interval[0]:.1f} - {confidence_interval[1]:.1f}</p>
        <p><strong>Severity Level:</strong> {severity_level.title()}</p>
        <p style="font-size: 0.9rem; color: var(--medium-gray);">{explanation}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Create symptom breakdown chart
    if symptom_breakdown:
        symptoms = list(symptom_breakdown.keys())
        scores = list(symptom_breakdown.values())

        fig = px.bar(
            x=symptoms,
            y=scores,
            title="Symptom Breakdown",
            color=scores,
            color_continuous_scale="RdYlBu_r",
        )
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)


def render_recommendations_section(recommendations):
    """Render the recommendations section."""
    st.markdown("### 🎯 Personalized Recommendations")

    for i, rec in enumerate(recommendations):
        priority = rec.get("priority", "medium")
        category = rec.get("category", "general")
        title = rec.get("title", "Recommendation")
        description = rec.get("description", "")
        actions = rec.get("actions", [])
        resources = rec.get("resources", [])

        # Determine card style based on priority
        if priority == "high":
            card_class = "warning-card"
            icon = "🔴"
        elif priority == "medium":
            card_class = "info-card"
            icon = "🟡"
        else:
            card_class = "success-card"
            icon = "🟢"

        with st.expander(f"{icon} {title} ({priority.title()} Priority)"):
            st.markdown(f"**{description}**")

            if actions:
                st.markdown("**Actions you can take:**")
                for action in actions:
                    st.markdown(f"• {action}")

            if resources:
                st.markdown("**Helpful resources:**")
                for resource in resources:
                    st.markdown(f"• {resource}")


def render_explainability_section(predictions):
    """Render the SHAP explainability section."""
    st.markdown("### 🔍 Understanding Your Results")

    with st.expander("Why did the AI make these predictions?", expanded=False):
        st.markdown("""
        **How the AI works:**
        
        Your predictions are based on advanced machine learning models that analyze patterns in your health data:
        
        - **Menopause Timeline Model**: Considers your age, hormone levels, and health factors to estimate when menopause might occur
        - **Symptom Severity Model**: Analyzes your current symptoms and lifestyle factors to predict severity
        
        **Key factors that influenced your predictions:**
        """)

        # Show which factors were most important (simplified)
        if "user_data" in st.session_state:
            user_data = st.session_state.user_data

            # Create a simple feature importance display
            factors = []
            if user_data.get("age", 0) > 45:
                factors.append("Age (45+) - Higher likelihood of menopause transition")
            if user_data.get("fsh", 0) > 25:
                factors.append("FSH Level - Elevated levels indicate hormonal changes")
            if user_data.get("stress_level", 0) > 7:
                factors.append("Stress Level - High stress can affect hormonal balance")
            if user_data.get("exercise_frequency", 0) < 3:
                factors.append("Exercise Frequency - Regular exercise helps manage symptoms")

            for factor in factors:
                st.markdown(f"• {factor}")

        st.markdown("""
        **Important Notes:**
        - These are educational predictions, not medical diagnoses
        - Individual experiences vary greatly
        - Always consult your healthcare provider for medical decisions
        - Models are continuously improved with new data
        """)


# This file is imported by the main app
