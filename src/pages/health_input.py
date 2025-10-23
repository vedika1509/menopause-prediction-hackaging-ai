"""
Enhanced Health Input Page for MenoBalance AI
Allows users to input health data and get predictions with comprehensive validation and visualizations
"""

import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def validate_health_data(data):
    """Validate health input data with comprehensive checks."""
    errors = []
    warnings = []

    # Age validation
    if data["age"] < 18:
        errors.append("Age must be at least 18 years")
    elif data["age"] > 65:
        warnings.append("Age is above typical menopause range (45-55)")

    # BMI validation
    if data["bmi"] < 15 or data["bmi"] > 50:
        errors.append("BMI should be between 15 and 50")
    elif data["bmi"] < 18.5:
        warnings.append("BMI suggests underweight - consult healthcare provider")
    elif data["bmi"] > 30:
        warnings.append("BMI suggests overweight - may affect hormone levels")

    # Hormone level validations
    if data["fsh"] < 1 or data["fsh"] > 100:
        errors.append("FSH level should be between 1-100 mIU/mL")
    elif data["fsh"] > 25:
        warnings.append("High FSH levels may indicate perimenopause")

    if data["amh"] < 0.1 or data["amh"] > 10:
        errors.append("AMH level should be between 0.1-10 ng/mL")
    elif data["amh"] < 1.0:
        warnings.append("Low AMH levels may indicate reduced ovarian reserve")

    if data["estradiol"] < 10 or data["estradiol"] > 500:
        errors.append("Estradiol level should be between 10-500 pg/mL")

    # Last period validation
    if data["last_period_months"] > 12:
        warnings.append("No period for over 12 months - may indicate menopause")

    # Symptom severity validation
    symptom_scores = [
        data["hot_flashes"],
        data["mood_changes"],
        data["sleep_quality"],
        data["stress_level"],
    ]
    if any(score < 0 or score > 10 for score in symptom_scores):
        errors.append("Symptom scores must be between 0-10")

    return errors, warnings


def create_risk_gauge(value, title, color_scheme="RdYlGn"):
    """Create a gauge chart for risk assessment."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title},
            delta={"reference": 5},
            gauge={
                "axis": {"range": [None, 10]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 3], "color": "lightgray"},
                    {"range": [3, 7], "color": "yellow"},
                    {"range": [7, 10], "color": "red"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 8},
            },
        )
    )

    fig.update_layout(
        height=300,
        font={"color": "darkblue", "family": "Arial"},
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


def create_symptom_bar_chart(symptoms):
    """Create a bar chart for symptom severity."""
    symptom_names = ["Hot Flashes", "Mood Changes", "Sleep Quality", "Stress Level"]
    symptom_values = [
        symptoms.get("hot_flashes", 0),
        symptoms.get("mood_changes", 0),
        symptoms.get("sleep_quality", 0),
        symptoms.get("stress_level", 0),
    ]

    # For sleep quality, invert the scale (10 = excellent, 0 = poor)
    symptom_values[2] = 10 - symptom_values[2]

    fig = px.bar(
        x=symptom_names,
        y=symptom_values,
        title="Current Symptom Severity",
        color=symptom_values,
        color_continuous_scale="RdYlGn_r",
        labels={"x": "Symptoms", "y": "Severity (0-10)"},
    )

    fig.update_layout(
        height=400, showlegend=False, xaxis_title="Symptoms", yaxis_title="Severity Score"
    )

    return fig


def create_confidence_interval_chart(predictions):
    """Create confidence interval visualization."""
    if not predictions:
        return None

    survival = predictions.get("survival", {})
    symptoms = predictions.get("symptoms", {})

    # Prepare data for confidence intervals
    data = []

    if "confidence_interval" in survival:
        ci = survival["confidence_interval"]
        data.append(
            {
                "Metric": "Time to Menopause (years)",
                "Value": survival.get("time_to_menopause_years", 0),
                "Lower": ci[0],
                "Upper": ci[1],
                "Confidence": survival.get("confidence_level", 0.95),
            }
        )

    if "confidence_interval" in symptoms:
        ci = symptoms["confidence_interval"]
        data.append(
            {
                "Metric": "Symptom Severity",
                "Value": symptoms.get("severity_score", 0),
                "Lower": ci[0],
                "Upper": ci[1],
                "Confidence": symptoms.get("confidence_level", 0.95),
            }
        )

    if not data:
        return None

    df = pd.DataFrame(data)

    fig = go.Figure()

    for _, row in df.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["Metric"]],
                y=[row["Value"]],
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=[row["Upper"] - row["Value"]],
                    arrayminus=[row["Value"] - row["Lower"]],
                    visible=True,
                ),
                mode="markers",
                name=row["Metric"],
                marker=dict(size=10, color="blue"),
            )
        )

    fig.update_layout(
        title="Prediction Confidence Intervals",
        xaxis_title="Metrics",
        yaxis_title="Values",
        height=400,
    )

    return fig


def render_health_input():
    """Render the enhanced health input page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Empathetic header with supportive messaging
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h1 style="color: white; margin-bottom: 1rem;">💜 Your Health Journey</h1>
            <p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">We understand that sharing your health information is personal and important. Your data helps us provide better, more personalized insights for your menopause journey.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Supportive message
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #6B46C1;">
            <h4 style="color: #6B46C1; margin-top: 0;">🤗 Your Privacy Matters</h4>
            <p style="color: #6B46C1; margin: 0; line-height: 1.6;">All your health information is processed securely and privately. We use this data only to provide you with personalized insights and never share it with third parties. You're in control of your health journey.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Health Input Form
    with st.form("health_assessment", clear_on_submit=False):
        st.markdown("### 📋 Basic Information")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=45,
                help="Your current age - this helps us understand where you are in your menopause journey",
            )

            bmi = st.number_input(
                "BMI (Body Mass Index)",
                min_value=15.0,
                max_value=50.0,
                value=25.0,
                step=0.1,
                help="Your BMI (weight in kg / height in m²)",
            )

            last_period = st.number_input(
                "Months since last period",
                min_value=0,
                max_value=120,
                value=6,
                help="Number of months since your last menstrual period",
            )

        with col2:
            fsh = st.number_input(
                "FSH Level (mIU/mL)",
                min_value=1.0,
                max_value=100.0,
                value=15.0,
                step=0.1,
                help="Follicle Stimulating Hormone level",
            )

            amh = st.number_input(
                "AMH Level (ng/mL)",
                min_value=0.1,
                max_value=10.0,
                value=1.5,
                step=0.1,
                help="Anti-Müllerian Hormone level",
            )

            estradiol = st.number_input(
                "Estradiol Level (pg/mL)",
                min_value=10.0,
                max_value=500.0,
                value=50.0,
                step=1.0,
                help="Estradiol hormone level",
            )

        st.markdown("### 🩺 Current Symptoms")

        col1, col2 = st.columns(2)

        with col1:
            hot_flashes = st.slider(
                "Hot Flashes Severity (0-10)",
                min_value=0,
                max_value=10,
                value=3,
                help="Rate the severity of hot flashes",
            )

            mood_changes = st.slider(
                "Mood Changes (0-10)",
                min_value=0,
                max_value=10,
                value=4,
                help="Rate mood fluctuations and irritability",
            )

        with col2:
            sleep_quality = st.slider(
                "Sleep Quality (0-10)",
                min_value=0,
                max_value=10,
                value=6,
                help="Rate your sleep quality (0=poor, 10=excellent)",
            )

            stress_level = st.slider(
                "Stress Level (0-10)",
                min_value=0,
                max_value=10,
                value=5,
                help="Rate your current stress level",
            )

        st.markdown("### 🏃‍♀️ Lifestyle Factors")

        col1, col2, col3 = st.columns(3)

        with col1:
            smoking = st.checkbox(
                "Smoking History", help="Do you currently smoke or have a history of smoking?"
            )
            exercise = st.selectbox(
                "Exercise Frequency",
                ["None", "Light", "Moderate", "Intense"],
                index=2,
                help="How often do you exercise?",
            )

        with col2:
            family_history = st.checkbox(
                "Family History of Early Menopause",
                help="Do you have family history of early menopause?",
            )
            diabetes = st.checkbox("Diabetes", help="Do you have diabetes?")

        with col3:
            hypertension = st.checkbox("Hypertension", help="Do you have high blood pressure?")
            thyroid = st.checkbox("Thyroid Issues", help="Do you have thyroid problems?")

        # Submit button
        submitted = st.form_submit_button("🔮 Get My Predictions", width="stretch")

        if submitted:
            # Prepare health data
            health_data = {
                "age": age,
                "bmi": bmi,
                "fsh": fsh,
                "amh": amh,
                "estradiol": estradiol,
                "last_period_months": last_period,
                "hot_flashes": hot_flashes,
                "mood_changes": mood_changes,
                "sleep_quality": sleep_quality,
                "stress_level": stress_level,
                "smoking": smoking,
                "exercise": exercise,
                "family_history": family_history,
                "diabetes": diabetes,
                "hypertension": hypertension,
                "thyroid": thyroid,
            }

            # Validate data
            errors, warnings = validate_health_data(health_data)

            # Show validation results
            if errors:
                st.error("❌ Please fix the following errors:")
                for error in errors:
                    st.error(f"• {error}")
                return

            if warnings:
                st.warning("⚠️ Please review the following warnings:")
                for warning in warnings:
                    st.warning(f"• {warning}")

            # Store in session state
            st.session_state.user_data = health_data

            # Get predictions
            with st.spinner("🔮 Analyzing your health data..."):
                try:
                    from app_streamlit_main import get_predictions

                    predictions = get_predictions(health_data)
                    st.session_state.predictions = predictions

                    # Show success message
                    st.success("✅ Predictions generated successfully!")
                    st.balloons()

                    # Redirect to predictions page
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error generating predictions: {str(e)}")
                    st.error("Please try again or contact support if the issue persists.")

    # Show current predictions if available
    if "predictions" in st.session_state and st.session_state.predictions:
        st.markdown("### 📊 Your Current Predictions")

        predictions = st.session_state.predictions

        # Display predictions in cards
        col1, col2, col3 = st.columns(3)

        with col1:
            survival = predictions.get("survival", {})
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3 style="color: var(--primary); margin-bottom: 0.5rem;">Time to Menopause</h3>
                    <div style="font-size: 2rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                        {survival.get("time_to_menopause_years", "N/A"):.1f} years
                    </div>
                    <p style="margin: 0; color: var(--text-muted);">
                        {survival.get("risk_level", "Unknown").title()} Risk
                    </p>
                    <p style="margin: 0; color: var(--text-muted); font-size: 0.8rem;">
                        Confidence: {survival.get("model_confidence", 0):.1%}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            symptoms = predictions.get("symptoms", {})
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3 style="color: var(--coral); margin-bottom: 0.5rem;">Symptom Severity</h3>
                    <div style="font-size: 2rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                        {symptoms.get("severity_score", "N/A"):.1f}/10
                    </div>
                    <p style="margin: 0; color: var(--text-muted);">
                        {symptoms.get("severity_level", "Unknown").title()} Level
                    </p>
                    <p style="margin: 0; color: var(--text-muted); font-size: 0.8rem;">
                        Confidence: {symptoms.get("model_confidence", 0):.1%}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            classification = predictions.get("classification", {})
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3 style="color: var(--mint); margin-bottom: 0.5rem;">Menopause Stage</h3>
                    <div style="font-size: 1.5rem; font-weight: 700; color: var(--foreground); margin: 1rem 0;">
                        {classification.get("predicted_class", "Unknown")}
                    </div>
                    <p style="margin: 0; color: var(--text-muted);">
                        Confidence: {classification.get("confidence", 0):.1%}
                    </p>
                    <p style="margin: 0; color: var(--text-muted); font-size: 0.8rem;">
                        Method: {predictions.get("method", "Unknown")}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Enhanced visualizations section
        st.markdown("### 📈 Detailed Analysis")

        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🎯 Risk Assessment",
                "📊 Symptom Analysis",
                "📈 Confidence Intervals",
                "💡 Recommendations",
            ]
        )

        with tab1:
            # Risk assessment gauges
            col1, col2 = st.columns(2)

            with col1:
                # Time to menopause risk gauge
                time_to_menopause = survival.get("time_to_menopause_years", 3.0)
                risk_value = max(0, min(10, 10 - time_to_menopause))  # Convert to 0-10 scale
                fig1 = create_risk_gauge(risk_value, "Menopause Risk Level")
                st.plotly_chart(fig1, width="stretch")

            with col2:
                # Symptom severity gauge
                severity_score = symptoms.get("severity_score", 5.0)
                fig2 = create_risk_gauge(severity_score, "Symptom Severity")
                st.plotly_chart(fig2, width="stretch")

        with tab2:
            # Symptom bar chart
            if "user_data" in st.session_state:
                user_symptoms = {
                    "hot_flashes": st.session_state.user_data.get("hot_flashes", 0),
                    "mood_changes": st.session_state.user_data.get("mood_changes", 0),
                    "sleep_quality": st.session_state.user_data.get("sleep_quality", 0),
                    "stress_level": st.session_state.user_data.get("stress_level", 0),
                }
                fig = create_symptom_bar_chart(user_symptoms)
                st.plotly_chart(fig, width="stretch")
            else:
                st.info("No symptom data available for visualization")

        with tab3:
            # Confidence intervals chart
            fig = create_confidence_interval_chart(predictions)
            if fig:
                st.plotly_chart(fig, width="stretch")
            else:
                st.info("No confidence interval data available")

            # Also show text-based confidence intervals
            col1, col2 = st.columns(2)
            with col1:
                if "confidence_interval" in survival:
                    ci = survival["confidence_interval"]
                    st.markdown(f"**Time to Menopause:** {ci[0]:.1f} - {ci[1]:.1f} years")
            with col2:
                if "confidence_interval" in symptoms:
                    ci = symptoms["confidence_interval"]
                    st.markdown(f"**Symptom Severity:** {ci[0]:.1f} - {ci[1]:.1f}")

        with tab4:
            # Show recommendations
            if "recommendations" in predictions:
                st.markdown("### 💡 Personalized Recommendations")
                for i, rec in enumerate(predictions["recommendations"], 1):
                    priority_emoji = (
                        "🔴"
                        if rec.get("priority") == "high"
                        else "🟡"
                        if rec.get("priority") == "medium"
                        else "🟢"
                    )
                    st.markdown(
                        f"{priority_emoji} **{rec.get('title', 'Recommendation')}**: {rec.get('description', '')}"
                    )
            else:
                st.info("No recommendations available")

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render_health_input()
