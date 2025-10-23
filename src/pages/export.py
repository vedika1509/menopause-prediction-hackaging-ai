import streamlit as st
import pandas as pd
from datetime import datetime
import json

def render_export_page():
    """Render the export page for downloading health summaries."""
    st.markdown("### 📄 Export Health Summary")
    
    st.markdown("""
    Export your health data and predictions in various formats for your records or to share with healthcare providers.
    """)
    
    # Check if user has any data to export
    if not st.session_state.get('health_data') and not st.session_state.get('predictions'):
        st.warning("No health data available to export. Please input your health information first.")
        return
    
    # Create export options
    export_format = st.selectbox(
        "Select Export Format:",
        ["PDF Health Summary", "CSV Data", "JSON Data", "Comprehensive Report"]
    )
    
    if export_format == "PDF Health Summary":
        render_pdf_export()
    elif export_format == "CSV Data":
        render_csv_export()
    elif export_format == "JSON Data":
        render_json_export()
    elif export_format == "Comprehensive Report":
        render_comprehensive_export()

def render_pdf_export():
    """Render PDF export functionality."""
    st.markdown("#### 📄 PDF Health Summary")
    
    # Generate PDF content
    pdf_content = generate_pdf_content()
    
    # Create download button
    if st.button("📥 Download PDF Summary", type="primary"):
        st.success("PDF generation feature will be implemented with reportlab library")
        st.info("For now, you can copy the summary below and save it manually")
        
        # Display the content that would be in the PDF
        st.markdown("---")
        st.markdown("### Health Summary Preview")
        st.markdown(pdf_content)

def render_csv_export():
    """Render CSV export functionality."""
    st.markdown("#### 📊 CSV Data Export")
    
    # Prepare data for CSV export
    export_data = prepare_csv_data()
    
    if export_data:
        csv = export_data.to_csv(index=False)
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"menopause_health_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data available for CSV export")

def render_json_export():
    """Render JSON export functionality."""
    st.markdown("#### 📋 JSON Data Export")
    
    # Prepare data for JSON export
    export_data = prepare_json_data()
    
    if export_data:
        json_str = json.dumps(export_data, indent=2, default=str)
        
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"menopause_health_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    else:
        st.warning("No data available for JSON export")

def render_comprehensive_export():
    """Render comprehensive report export."""
    st.markdown("#### 📑 Comprehensive Report")
    
    st.markdown("""
    A comprehensive report includes:
    - Health data summary
    - Prediction results with confidence intervals
    - Wellness trends
    - Recommendations
    - Model insights
    """)
    
    if st.button("📥 Generate Comprehensive Report", type="primary"):
        st.success("Comprehensive report generation feature will be implemented")
        st.info("This will create a detailed multi-page report with all your health insights")

def generate_pdf_content():
    """Generate content for PDF export."""
    content = f"""
# MenoBalance AI Health Summary
Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

## Health Information
"""
    
    # Add health data if available
    if st.session_state.get('health_data'):
        health_data = st.session_state.health_data
        content += f"""
- Age: {health_data.get('age', 'Not provided')}
- BMI: {health_data.get('bmi', 'Not calculated')}
- Menopause Status: {health_data.get('menopause_status', 'Not specified')}
"""
    
    # Add predictions if available
    if st.session_state.get('predictions'):
        predictions = st.session_state.predictions
        content += """
## AI Predictions
"""
        for task, prediction in predictions.items():
            content += f"- {task.title()}: {prediction}\n"
    
    content += """
## Important Notes
- This summary is for educational purposes only
- Consult with healthcare providers for medical decisions
- Data privacy is maintained throughout the process
"""
    
    return content

def prepare_csv_data():
    """Prepare data for CSV export."""
    data_dict = {}
    
    # Add health data
    if st.session_state.get('health_data'):
        data_dict.update(st.session_state.health_data)
    
    # Add predictions
    if st.session_state.get('predictions'):
        for task, prediction in st.session_state.predictions.items():
            data_dict[f"prediction_{task}"] = prediction
    
    # Add timestamp
    data_dict['export_date'] = datetime.now().isoformat()
    
    if data_dict:
        return pd.DataFrame([data_dict])
    return None

def prepare_json_data():
    """Prepare data for JSON export."""
    export_data = {
        'export_info': {
            'timestamp': datetime.now().isoformat(),
            'source': 'MenoBalance AI',
            'version': '1.0'
        },
        'health_data': st.session_state.get('health_data', {}),
        'predictions': st.session_state.get('predictions', {}),
        'wellness_scores': st.session_state.get('wellness_scores', [])
    }
    
    return export_data
