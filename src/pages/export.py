"""
Export Page - Generate and download comprehensive health reports
"""

import json
import os
import sys
from datetime import datetime

import streamlit as st

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def render_export_page():
    """Render the export page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Page header
    st.markdown(
        """
    <div class="main-header">
        <h1>📄 Export Health Report</h1>
        <p style="color: var(--medium-gray);">Generate comprehensive health reports for your records</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Check if user has predictions
    if "predictions" not in st.session_state or not st.session_state.predictions:
        st.markdown(
            """
        <div class="warning-card">
            <h3>📊 No Data Available</h3>
            <p>Complete your health assessment first to generate a report.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("📝 Complete Health Assessment", use_container_width=True):
            st.session_state.current_page = "health_input"
            st.rerun()
        return

    # Report options
    st.markdown("### 📋 Report Options")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="card">
            <h3>📊 Full Comprehensive Report</h3>
            <p>Complete health assessment with all predictions, recommendations, and insights.</p>
            <ul>
                <li>Executive summary</li>
                <li>Detailed predictions</li>
                <li>Personalized recommendations</li>
                <li>Health timeline (if available)</li>
                <li>Educational resources</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="card">
            <h3>📄 Summary Report</h3>
            <p>Concise 2-page summary of key findings and recommendations.</p>
            <ul>
                <li>Key predictions</li>
                <li>Top recommendations</li>
                <li>Next steps</li>
                <li>Contact information</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Report generation
    st.markdown("### 🚀 Generate Report")

    # Report type selection
    report_type = st.selectbox(
        "Select Report Type",
        ["Full Comprehensive Report", "Summary Report", "Predictions Only", "Timeline Data Only"],
        help="Choose the type of report you'd like to generate",
    )

    # Date range for timeline data
    if report_type in ["Full Comprehensive Report", "Timeline Data Only"]:
        st.markdown("#### 📅 Timeline Data Range")

        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.now().date().replace(day=1),  # First day of current month
                help="Start date for timeline data",
            )

        with col2:
            end_date = st.date_input(
                "End Date", value=datetime.now().date(), help="End date for timeline data"
            )

    # Additional options
    st.markdown("#### ⚙️ Report Options")

    col1, col2 = st.columns(2)

    with col1:
        include_timeline = st.checkbox(
            "Include Health Timeline", value=True, help="Include timeline charts and trends"
        )
        include_education = st.checkbox(
            "Include Educational Content",
            value=True,
            help="Include relevant health education materials",
        )

    with col2:
        include_recommendations = st.checkbox(
            "Include Recommendations",
            value=True,
            help="Include personalized health recommendations",
        )
        include_disclaimers = st.checkbox(
            "Include Medical Disclaimers", value=True, help="Include important medical disclaimers"
        )

    # Generate report button
    if st.button("📄 Generate Report", use_container_width=True):
        with st.spinner("🔄 Generating your health report..."):
            try:
                # Generate report data
                report_data = generate_report_data(
                    report_type,
                    start_date if "start_date" in locals() else None,
                    end_date if "end_date" in locals() else None,
                    {
                        "include_timeline": include_timeline,
                        "include_education": include_education,
                        "include_recommendations": include_recommendations,
                        "include_disclaimers": include_disclaimers,
                    },
                )

                # Store report data in session state
                st.session_state.generated_report = report_data
                st.session_state.report_type = report_type

                st.success("✅ Report generated successfully!")
                st.balloons()

            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")

    # Display generated report
    if "generated_report" in st.session_state:
        st.markdown("### 📋 Generated Report")

        report_data = st.session_state.generated_report

        # Show report preview
        with st.expander("👁️ Preview Report", expanded=True):
            render_report_preview(report_data)

        # Download options
        st.markdown("### 📥 Download Options")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📄 Download PDF", use_container_width=True):
                # Generate PDF (placeholder)
                st.info("PDF generation coming soon! For now, you can copy the report content.")

        with col2:
            if st.button("📊 Download JSON", use_container_width=True):
                # Download as JSON
                json_data = json.dumps(report_data, indent=2, default=str)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"menobalance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                )

        with col3:
            if st.button("📧 Email Report", use_container_width=True):
                st.info("Email functionality coming soon!")


def generate_report_data(report_type, start_date, end_date, options):
    """Generate report data based on user selections."""
    # Get user data and predictions
    user_data = st.session_state.get("user_data", {})
    predictions = st.session_state.get("predictions", {})
    timeline_data = st.session_state.get("timeline_data", [])
    wearable_data = st.session_state.get("wearable_data", [])

    # Base report structure
    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "report_type": report_type,
            "user_age": user_data.get("age", "Not provided"),
            "report_id": f"MBR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        },
        "executive_summary": generate_executive_summary(predictions),
        "predictions": predictions if predictions else {},
        "recommendations": predictions.get("recommendations", [])
        if options["include_recommendations"]
        else [],
        "timeline_data": timeline_data if options["include_timeline"] else [],
        "wellness_data": wearable_data if options["include_timeline"] else [],
        "educational_content": get_educational_content() if options["include_education"] else {},
        "disclaimers": get_medical_disclaimers() if options["include_disclaimers"] else {},
    }

    return report


def generate_executive_summary(predictions):
    """Generate executive summary of predictions."""
    if not predictions:
        return "No predictions available. Please complete your health assessment."

    survival = predictions.get("survival", {})
    symptoms = predictions.get("symptoms", {})

    summary = f"""
    **Health Assessment Summary**
    
    Based on your health profile, here are your key insights:
    
    **Menopause Timeline:** {survival.get("time_to_menopause_years", "Not available")} years
    **Risk Level:** {survival.get("risk_level", "Not available").title()}
    **Symptom Severity:** {symptoms.get("severity_score", "Not available")}/10 ({symptoms.get("severity_level", "Not available").title()})
    
    **Key Recommendations:**
    """

    recommendations = predictions.get("recommendations", [])
    if recommendations:
        for i, rec in enumerate(recommendations[:3], 1):  # Top 3 recommendations
            summary += f"\n{i}. {rec.get('title', 'Recommendation')}"
    else:
        summary += "\n- Consult with your healthcare provider for personalized guidance"

    return summary


def get_educational_content():
    """Get relevant educational content."""
    return {
        "menopause_basics": "Menopause is a natural biological process that marks the end of reproductive years...",
        "symptom_management": "Common symptoms include hot flashes, sleep disturbances, and mood changes...",
        "lifestyle_tips": "Regular exercise, balanced nutrition, and stress management can help...",
        "when_to_see_doctor": "Consult your healthcare provider if symptoms are severe or concerning...",
    }


def get_medical_disclaimers():
    """Get medical disclaimers."""
    return {
        "educational_only": "This report is for educational purposes only and is not a substitute for professional medical advice.",
        "not_diagnostic": "This tool does not provide medical diagnoses or replace consultation with healthcare providers.",
        "individual_variation": "Individual experiences with menopause vary greatly, and these predictions may not apply to everyone.",
        "seek_professional_help": "Always consult your healthcare provider for medical decisions and treatment options.",
    }


def render_report_preview(report_data):
    """Render a preview of the generated report."""
    st.markdown("#### 📋 Report Preview")

    # Executive summary
    st.markdown("**Executive Summary:**")
    st.markdown(report_data.get("executive_summary", "No summary available"))

    # Predictions
    if report_data.get("predictions"):
        st.markdown("**Predictions:**")
        predictions = report_data["predictions"]

        if "survival" in predictions:
            survival = predictions["survival"]
            st.markdown(
                f"- Menopause Timeline: {survival.get('time_to_menopause_years', 'N/A')} years"
            )
            st.markdown(f"- Risk Level: {survival.get('risk_level', 'N/A').title()}")

        if "symptoms" in predictions:
            symptoms = predictions["symptoms"]
            st.markdown(f"- Symptom Severity: {symptoms.get('severity_score', 'N/A')}/10")
            st.markdown(f"- Severity Level: {symptoms.get('severity_level', 'N/A').title()}")

    # Recommendations
    if report_data.get("recommendations"):
        st.markdown("**Top Recommendations:**")
        for i, rec in enumerate(report_data["recommendations"][:3], 1):
            st.markdown(f"{i}. {rec.get('title', 'Recommendation')}")

    # Data summary
    st.markdown("**Data Included:**")
    if report_data.get("timeline_data"):
        st.markdown(f"- Timeline data: {len(report_data['timeline_data'])} entries")
    if report_data.get("wellness_data"):
        st.markdown(f"- Wellness data: {len(report_data['wellness_data'])} entries")

    # Disclaimers
    if report_data.get("disclaimers"):
        st.markdown("**Important Disclaimers:**")
        for key, disclaimer in report_data["disclaimers"].items():
            st.markdown(f"- {disclaimer}")


# This file is imported by the main app
