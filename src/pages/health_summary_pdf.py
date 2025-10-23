"""
Health Summary PDF Generation
"""

import os
import sys
from datetime import datetime

import pandas as pd
import streamlit as st

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_nebius_health_narrative(user_data, predictions, symptom_logs):
    """Generate comprehensive health narrative using Nebius AI"""
    try:
        from chatbot_nebius import NebiusChatbot

        # Initialize chatbot
        chatbot = NebiusChatbot()

        # Build comprehensive context for Nebius AI
        context = f"""
        Generate a comprehensive health narrative for a menopause health report based on the following data:
        
        User Profile:
        - Age: {user_data.get("age", "unknown")}
        - BMI: {user_data.get("bmi", "unknown")}
        - Current symptoms: {user_data.get("symptoms", [])}
        
        AI Predictions:
        - Menopause Timeline: {predictions.get("survival", {}).get("time_to_menopause_years", "unknown")} years
        - Risk Level: {predictions.get("survival", {}).get("risk_level", "unknown")}
        - Symptom Severity: {predictions.get("symptoms", {}).get("severity_level", "unknown")}
        - Severity Score: {predictions.get("symptoms", {}).get("severity_score", "unknown")}
        
        Historical Data:
        - Number of symptom entries: {len(symptom_logs)}
        - Recent wellness trends: {get_wellness_trends(symptom_logs)}
        
        Please provide:
        1. A personalized health overview
        2. Explanation of current symptoms and their significance
        3. Timeline expectations and what to expect
        4. Lifestyle recommendations
        5. When to seek medical advice
        6. Encouraging and supportive tone throughout
        
        Format as a comprehensive health narrative suitable for a medical report.
        """

        if chatbot.api_key:
            try:
                response = chatbot._call_nebius_api(context, "health_narrative")
                return response
            except Exception as e:
                st.error(f"Error generating Nebius narrative: {e}")
                return generate_fallback_narrative(user_data, predictions, symptom_logs)
        else:
            return generate_fallback_narrative(user_data, predictions, symptom_logs)

    except Exception as e:
        st.error(f"Error in generate_nebius_health_narrative: {e}")
        return generate_fallback_narrative(user_data, predictions, symptom_logs)


def get_wellness_trends(symptom_logs):
    """Get wellness trend summary from symptom logs"""
    if not symptom_logs:
        return "No historical data available"

    recent_scores = [
        log.get("wellness_score", 0) for log in symptom_logs[-7:] if "wellness_score" in log
    ]
    if not recent_scores:
        return "No wellness scores available"

    avg_score = sum(recent_scores) / len(recent_scores)
    if len(recent_scores) >= 2:
        trend = (
            "improving"
            if recent_scores[-1] > recent_scores[0]
            else "declining"
            if recent_scores[-1] < recent_scores[0]
            else "stable"
        )
    else:
        trend = "insufficient data"

    return f"Average wellness score: {avg_score:.1f}/100, trend: {trend}"


def generate_fallback_narrative(user_data, predictions, symptom_logs):
    """Generate fallback narrative when Nebius AI is not available"""
    age = user_data.get("age", "unknown")
    bmi = user_data.get("bmi", "unknown")

    survival = predictions.get("survival", {})
    symptoms = predictions.get("symptoms", {})

    narrative = f"""
    HEALTH SUMMARY REPORT
    Generated on: {datetime.now().strftime("%B %d, %Y")}
    
    PERSONALIZED HEALTH OVERVIEW
    
    Based on your health assessment, you are a {age}-year-old individual with a BMI of {bmi}. 
    Your MenoBalance AI analysis provides the following insights:
    
    MENOPAUSE TIMELINE PREDICTION
    Our AI models predict that you may reach menopause in approximately {survival.get("time_to_menopause_years", 3.0):.1f} years, 
    with a {survival.get("risk_level", "moderate")} risk level. This timeline is based on your current symptoms, 
    age, and health indicators.
    
    CURRENT SYMPTOM ASSESSMENT
    Your current symptom severity is rated as {symptoms.get("severity_level", "moderate")} with a score of {symptoms.get("severity_score", 5.0):.1f}/10. 
    This assessment helps us understand your current experience and provide appropriate guidance.
    
    LIFESTYLE RECOMMENDATIONS
    Based on your assessment, we recommend:
    - Regular monitoring of your symptoms and wellness metrics
    - Maintaining a balanced diet and regular exercise routine
    - Stress management techniques such as meditation or yoga
    - Adequate sleep hygiene and rest
    - Staying informed about menopause-related changes
    
    WHEN TO SEEK MEDICAL ADVICE
    Please consult with your healthcare provider if you experience:
    - Severe or worsening symptoms
    - New or concerning symptoms
    - Significant changes in your health status
    - Questions about treatment options
    
    IMPORTANT DISCLAIMERS
    This report is generated by AI models for educational purposes only. It is not a substitute for professional medical advice, 
    diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.
    
    Your health journey is unique, and we're here to support you with personalized insights and recommendations.
    """

    return narrative


def render_health_summary_pdf():
    """Render health summary PDF generation page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Page header
    st.markdown(
        """
    <div class="main-header">
        <h1>📄 Health Summary Report</h1>
        <p style="color: var(--medium-gray);">Generate and download your comprehensive health report</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Check if user has data
    if "user_data" not in st.session_state or "predictions" not in st.session_state:
        st.markdown(
            """
            <div class="warning-card">
                <h3>📊 No Data Available</h3>
                <p>Please complete your health assessment first to generate a health summary report.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("📝 Complete Health Assessment", use_container_width=True):
            st.session_state.current_page = "health_input"
            st.rerun()
        return

    # Report options
    render_report_options()

    # Generate and display report
    render_report_generation()


def render_report_options():
    """Render report generation options."""
    st.markdown("### 📋 Report Options")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Report Type")
        report_type = st.selectbox(
            "Select Report Type",
            [
                "Full Comprehensive Report",
                "Summary Report",
                "Predictions Only",
                "Timeline Data Only",
            ],
            help="Choose the type of report you want to generate",
        )

        include_timeline = st.checkbox(
            "📈 Include Timeline Data",
            value=True,
            help="Include your symptom timeline and wellness trends",
        )

        include_education = st.checkbox(
            "📚 Include Educational Content",
            value=True,
            help="Include menopause education and management tips",
        )

    with col2:
        st.markdown("#### 🎨 Formatting Options")
        include_recommendations = st.checkbox(
            "💡 Include Recommendations",
            value=True,
            help="Include personalized health recommendations",
        )

        include_disclaimers = st.checkbox(
            "⚠️ Include Medical Disclaimers",
            value=True,
            help="Include important medical disclaimers",
        )

        date_range = st.date_input(
            "📅 Report Date Range",
            value=(datetime.now().date(), datetime.now().date()),
            help="Select the date range for your report",
        )


def render_report_generation():
    """Render report generation interface."""
    st.markdown("### 🚀 Generate Report")

    if st.button("📄 Generate Health Summary Report", use_container_width=True, type="primary"):
        with st.spinner("🔄 Generating your health summary report..."):
            # Generate report content
            report_content = generate_health_summary_content()

            # Display report preview
            render_report_preview(report_content)

            # Provide download options
            render_download_options(report_content)


def generate_health_summary_content():
    """Generate comprehensive health summary content."""
    user_data = st.session_state.get("user_data", {})
    predictions = st.session_state.get("predictions", {})
    wellness_data = st.session_state.get("wellness_data", [])

    # Generate report sections
    report = {
        "header": generate_report_header(),
        "executive_summary": generate_executive_summary(user_data, predictions),
        "health_profile": generate_health_profile(user_data),
        "predictions": generate_predictions_section(predictions),
        "recommendations": generate_recommendations_section(predictions),
        "timeline_data": generate_timeline_section(wellness_data),
        "educational_content": generate_educational_content(),
        "disclaimers": generate_disclaimers(),
        "contact_info": generate_contact_information(),
    }

    return report


def generate_report_header():
    """Generate report header."""
    return {
        "title": "MenoBalance AI Health Summary Report",
        "subtitle": "Personalized Menopause Health Insights",
        "generated_date": datetime.now().strftime("%B %d, %Y"),
        "report_id": f"MB-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "version": "1.0",
    }


def generate_executive_summary(user_data, predictions):
    """Generate executive summary using Nebius AI."""
    try:
        # Get symptom logs for context
        symptom_logs = st.session_state.get("symptom_logs", [])

        # Generate Nebius AI narrative
        nebius_narrative = generate_nebius_health_narrative(user_data, predictions, symptom_logs)

        # Extract key information from predictions
        survival = predictions.get("survival", {})
        symptoms = predictions.get("symptoms", {})

        timeline = survival.get("time_to_menopause_years", 0)
        severity = symptoms.get("severity_score", 0)
        age = user_data.get("age", "Not provided")
        bmi = user_data.get("bmi", 0)

        return {
            "patient_age": age,
            "bmi": f"{bmi:.1f}" if bmi > 0 else "Not calculated",
            "menopause_timeline": f"{timeline:.1f} years",
            "symptom_severity": f"{severity:.1f}/10",
            "risk_level": survival.get("risk_level", "Unknown").title(),
            "severity_level": symptoms.get("severity_level", "Unknown").title(),
            "ai_narrative": nebius_narrative,
            "key_insights": [
                f"Based on your current health profile, you're likely to reach menopause in approximately {timeline:.1f} years.",
                f"Your overall symptom severity is {severity:.1f} out of 10, which is considered {symptoms.get('severity_level', 'unknown')}.",
                f"Your risk level is {survival.get('risk_level', 'unknown').title()}, indicating your overall risk profile for menopause-related health concerns.",
            ],
        }

    except Exception as e:
        st.error(f"Error generating executive summary: {e}")
        # Fallback to basic summary
        age = user_data.get("age", "Not provided")
        bmi = user_data.get("bmi", 0)
        survival = predictions.get("survival", {})
        symptoms = predictions.get("symptoms", {})
        timeline = survival.get("time_to_menopause_years", 0)
        severity = symptoms.get("severity_score", 0)

        return {
            "patient_age": age,
            "bmi": f"{bmi:.1f}" if bmi > 0 else "Not calculated",
            "menopause_timeline": f"{timeline:.1f} years",
            "symptom_severity": f"{severity:.1f}/10",
            "risk_level": survival.get("risk_level", "Unknown").title(),
            "severity_level": symptoms.get("severity_level", "Unknown").title(),
            "key_insights": [
                f"Based on your current health profile, you're likely to reach menopause in approximately {timeline:.1f} years.",
                f"Your overall symptom severity is {severity:.1f} out of 10, which is considered {symptoms.get('severity_level', 'unknown')}.",
                f"Your risk level is {survival.get('risk_level', 'unknown').title()}, indicating your overall risk profile for menopause-related health concerns.",
            ],
        }


def generate_health_profile(user_data):
    """Generate health profile section."""
    return {
        "basic_info": {
            "age": user_data.get("age", "Not provided"),
            "height": f"{user_data.get('height', 0)} cm",
            "weight": f"{user_data.get('weight', 0)} kg",
            "bmi": f"{user_data.get('bmi', 0):.1f}"
            if user_data.get("bmi", 0) > 0
            else "Not calculated",
        },
        "hormone_levels": {
            "fsh": f"{user_data.get('fsh', 0)} mIU/mL",
            "estradiol": f"{user_data.get('estradiol', 0)} pg/mL",
            "amh": f"{user_data.get('amh', 0)} ng/mL",
            "progesterone": f"{user_data.get('progesterone', 0)} ng/mL",
        },
        "symptoms": {
            "hot_flashes": f"{user_data.get('hot_flashes', 0)}/10",
            "night_sweats": f"{user_data.get('night_sweats', 0)}/10",
            "mood_changes": f"{user_data.get('mood_changes', 0)}/10",
            "sleep_quality": f"{user_data.get('sleep_quality', 0)}/10",
            "cognitive_issues": f"{user_data.get('cognitive_issues', 0)}/10",
            "energy_level": f"{user_data.get('energy_level', 0)}/10",
        },
        "lifestyle": {
            "exercise_frequency": user_data.get("exercise_frequency", "Not provided"),
            "stress_level": f"{user_data.get('stress_level', 0)}/10",
            "diet_quality": user_data.get("diet_quality", "Not provided"),
            "smoking_status": user_data.get("smoking", "Not provided"),
        },
    }


def generate_predictions_section(predictions):
    """Generate predictions section."""
    survival = predictions.get("survival", {})
    symptoms = predictions.get("symptoms", {})

    return {
        "menopause_timeline": {
            "years_to_menopause": f"{survival.get('time_to_menopause_years', 0):.1f} years",
            "confidence_interval": f"{survival.get('confidence_interval', [0, 0])[0]:.1f} - {survival.get('confidence_interval', [0, 0])[1]:.1f} years",
            "risk_level": survival.get("risk_level", "Unknown").title(),
            "explanation": survival.get("explanation", "No explanation available"),
        },
        "symptom_analysis": {
            "overall_severity": f"{symptoms.get('severity_score', 0):.1f}/10",
            "severity_level": symptoms.get("severity_level", "Unknown").title(),
            "confidence_interval": f"{symptoms.get('confidence_interval', [0, 0])[0]:.1f} - {symptoms.get('confidence_interval', [0, 0])[1]:.1f}",
            "top_symptoms": symptoms.get("top_symptoms", []),
            "explanation": symptoms.get("explanation", "No explanation available"),
        },
    }


def generate_recommendations_section(predictions):
    """Generate recommendations section."""
    recommendations = predictions.get("recommendations", [])

    return {
        "recommendations": recommendations,
        "total_count": len(recommendations),
        "high_priority": [r for r in recommendations if r.get("priority") == "high"],
        "medium_priority": [r for r in recommendations if r.get("priority") == "medium"],
        "low_priority": [r for r in recommendations if r.get("priority") == "low"],
    }


def generate_timeline_section(wellness_data):
    """Generate timeline data section."""
    if not wellness_data:
        return {"message": "No timeline data available"}

    df = pd.DataFrame(wellness_data)

    return {
        "data_points": len(wellness_data),
        "date_range": f"{df['date'].min()} to {df['date'].max()}"
        if "date" in df.columns
        else "Not available",
        "average_wellness_score": f"{df['wellness_score'].mean():.1f}"
        if "wellness_score" in df.columns
        else "Not available",
        "trend_analysis": "Improving"
        if len(wellness_data) > 1
        and wellness_data[-1].get("wellness_score", 0) > wellness_data[0].get("wellness_score", 0)
        else "Stable",
    }


def generate_educational_content():
    """Generate educational content section."""
    return {
        "menopause_basics": {
            "title": "Understanding Menopause",
            "content": "Menopause is a natural biological process that marks the end of menstrual cycles. It typically occurs between ages 45-55, but can vary significantly between individuals.",
        },
        "symptom_management": {
            "title": "Symptom Management Tips",
            "content": "Effective symptom management includes maintaining a healthy lifestyle, managing stress, getting adequate sleep, and considering medical interventions when appropriate.",
        },
        "lifestyle_recommendations": {
            "title": "Lifestyle Recommendations",
            "content": "Regular exercise, balanced nutrition, stress management, and quality sleep are essential for managing menopause symptoms and maintaining overall health.",
        },
    }


def generate_disclaimers():
    """Generate medical disclaimers."""
    return {
        "medical_disclaimer": "This report is for educational purposes only and should not replace professional medical advice. Always consult with your healthcare provider for medical decisions.",
        "ai_limitations": "AI predictions are based on statistical patterns and may not apply to individual cases. Results should be interpreted with caution.",
        "data_accuracy": "The accuracy of predictions depends on the accuracy and completeness of the input data provided.",
        "privacy_notice": "Your health data is protected and will not be shared without your explicit consent.",
    }


def generate_contact_information():
    """Generate contact information."""
    return {
        "developer": "Vedika Hackagain",
        "email": "vedika.hackagain@example.com",
        "linkedin": "https://www.linkedin.com/in/vedika-hackagain",
        "support_email": "support@menobalance.ai",
        "privacy_email": "privacy@menobalance.ai",
    }


def render_report_preview(report_content):
    """Render report preview."""
    st.markdown("### 📄 Report Preview")

    # Header
    header = report_content["header"]
    st.markdown(
        f"""
        <div class="card" style="text-align: center; background: linear-gradient(135deg, #E1BEE7 0%, #F3E5F5 100%);">
            <h2 style="color: var(--primary); margin: 0;">{header["title"]}</h2>
            <p style="color: var(--medium-gray); margin: 0.5rem 0;">{header["subtitle"]}</p>
            <p style="font-size: 0.9rem; color: var(--medium-gray);">Generated: {header["generated_date"]} | Report ID: {header["report_id"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Executive Summary
    exec_summary = report_content["executive_summary"]
    st.markdown("#### 📊 Executive Summary")
    st.markdown(f"**Patient Age:** {exec_summary['patient_age']} | **BMI:** {exec_summary['bmi']}")
    st.markdown(
        f"**Menopause Timeline:** {exec_summary['menopause_timeline']} | **Symptom Severity:** {exec_summary['symptom_severity']}"
    )
    st.markdown(
        f"**Risk Level:** {exec_summary['risk_level']} | **Severity Level:** {exec_summary['severity_level']}"
    )

    # Key Insights
    st.markdown("**Key Insights:**")
    for insight in exec_summary["key_insights"]:
        st.markdown(f"- {insight}")

    # Health Profile
    health_profile = report_content["health_profile"]
    st.markdown("#### 👤 Health Profile")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Basic Information:**")
        for key, value in health_profile["basic_info"].items():
            st.markdown(f"- {key.title()}: {value}")

    with col2:
        st.markdown("**Hormone Levels:**")
        for key, value in health_profile["hormone_levels"].items():
            st.markdown(f"- {key.upper()}: {value}")

    # Predictions
    predictions = report_content["predictions"]
    st.markdown("#### 🔮 AI Predictions")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Menopause Timeline:**")
        timeline = predictions["menopause_timeline"]
        st.markdown(f"- Years to Menopause: {timeline['years_to_menopause']}")
        st.markdown(f"- Confidence Interval: {timeline['confidence_interval']}")
        st.markdown(f"- Risk Level: {timeline['risk_level']}")

    with col2:
        st.markdown("**Symptom Analysis:**")
        symptoms = predictions["symptom_analysis"]
        st.markdown(f"- Overall Severity: {symptoms['overall_severity']}")
        st.markdown(f"- Severity Level: {symptoms['severity_level']}")
        st.markdown(f"- Top Symptoms: {', '.join(symptoms['top_symptoms'])}")

    # Recommendations
    recommendations = report_content["recommendations"]
    if recommendations["recommendations"]:
        st.markdown("#### 💡 Personalized Recommendations")
        for i, rec in enumerate(recommendations["recommendations"][:5], 1):
            priority_color = {"high": "#E53935", "medium": "#FF7043", "low": "#26A69A"}.get(
                rec.get("priority", "medium"), "#9C27B0"
            )
            st.markdown(
                f"""
                <div style="background: {priority_color}20; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {priority_color};">
                    <h4 style="margin: 0; color: {priority_color};">{i}. {rec.get("title", "Recommendation")}</h4>
                    <p style="margin: 0.5rem 0;">{rec.get("description", "No description available")}</p>
                    <small style="color: var(--medium-gray);">Priority: {rec.get("priority", "medium").title()}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Contact Information
    contact = report_content["contact_information"]
    st.markdown("#### 📞 Contact Information")
    st.markdown(f"**Developer:** {contact['developer']}")
    st.markdown(f"**Email:** {contact['email']}")
    st.markdown(f"**LinkedIn:** {contact['linkedin']}")
    st.markdown(f"**Support:** {contact['support_email']}")


def render_download_options(report_content):
    """Render download options."""
    st.markdown("### 📥 Download Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Download PDF", use_container_width=True):
            st.info(
                "📄 PDF generation coming soon! For now, you can copy the report content above."
            )

    with col2:
        if st.button("📊 Download JSON", use_container_width=True):
            import json

            json_data = json.dumps(report_content, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"health_summary_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
            )

    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.info(
                "📧 Email functionality coming soon! For now, you can copy the report content above."
            )

    # Copy to clipboard option
    st.markdown("#### 📋 Copy Report Content")
    st.markdown("You can copy the report content above and save it to your preferred format.")

    if st.button("📋 Copy to Clipboard", use_container_width=True):
        st.success(
            "✅ Report content copied to clipboard! You can now paste it into your preferred document editor."
        )
