"""
Ethics and Bias Documentation Page for MenoBalance AI
Comprehensive documentation of ethical considerations and bias mitigation
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def load_model_insights():
    """Load model insights JSON if available."""
    try:
        insights_path = "reports/model_insights.json"
        if os.path.exists(insights_path):
            with open(insights_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading model insights: {e}")
    return None

def render_ethics_bias():
    """Render the ethics and bias documentation page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--foreground); margin-bottom: 0.5rem;">⚖️ Ethics & Bias Documentation</h1>
            <p style="color: var(--text-muted);">Comprehensive documentation of ethical considerations, bias assessment, and responsible AI practices</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Load model insights
    model_insights = load_model_insights()
    
    # Ethics Statement
    st.markdown("### 🎯 Our Ethical Commitment")
    
    st.markdown(
        """
        <div class="pastel-card">
            <h4>Core Ethical Principles</h4>
            <p>MenoBalance AI is committed to responsible AI development and deployment. We prioritize:</p>
            <ul>
                <li><strong>Transparency:</strong> Clear communication about model capabilities and limitations</li>
                <li><strong>Fairness:</strong> Equitable treatment across all demographic groups</li>
                <li><strong>Privacy:</strong> Protection of user health data and personal information</li>
                <li><strong>Safety:</strong> Ensuring predictions do not cause harm</li>
                <li><strong>Accountability:</strong> Taking responsibility for AI decisions and outcomes</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Bias Assessment
    st.markdown("### 🔍 Bias Assessment & Mitigation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="coral-card" style="padding: 1.5rem;">
                <h4>🚨 Identified Biases</h4>
                <ul>
                    <li><strong>Data Bias:</strong> Training on synthetic data may not represent real-world diversity</li>
                    <li><strong>Age Bias:</strong> Limited representation of extreme age groups (<25, >65)</li>
                    <li><strong>Geographic Bias:</strong> Primarily trained on certain regional datasets</li>
                    <li><strong>Socioeconomic Bias:</strong> May not capture full socioeconomic diversity</li>
                    <li><strong>Cultural Bias:</strong> Limited cultural and ethnic representation</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div class="mint-card" style="padding: 1.5rem;">
                <h4>✅ Mitigation Strategies</h4>
                <ul>
                    <li><strong>Diverse Training Data:</strong> Actively seeking diverse datasets</li>
                    <li><strong>Bias Monitoring:</strong> Regular assessment across demographic groups</li>
                    <li><strong>Clinical Validation:</strong> Partnering with diverse healthcare providers</li>
                    <li><strong>User Feedback:</strong> Continuous improvement based on user input</li>
                    <li><strong>Transparent Reporting:</strong> Open about limitations and uncertainties</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Model Performance by Demographics
    st.markdown("### 📊 Model Performance Analysis")
    
    if model_insights and 'bias_assessment' in model_insights:
        bias_data = model_insights['bias_assessment']
        
        st.markdown("#### Data Limitations")
        for limitation, description in bias_data.get('data_limitations', {}).items():
            st.markdown(f"**{limitation.replace('_', ' ').title()}:** {description}")
        
        st.markdown("#### Monitoring Metrics")
        for metric, description in bias_data.get('monitoring_metrics', {}).items():
            st.markdown(f"**{metric.replace('_', ' ').title()}:** {description}")
    
    # Clinical Guidelines
    st.markdown("### 🩺 Clinical Guidelines & Limitations")
    
    st.markdown(
        """
        <div class="lavender-card" style="padding: 1.5rem;">
            <h4>Important Clinical Disclaimers</h4>
            <ul>
                <li><strong>NOT a Diagnostic Tool:</strong> Cannot replace professional medical diagnosis</li>
                <li><strong>Educational Purpose:</strong> Designed for health awareness and education only</li>
                <li><strong>Clinical Validation Required:</strong> Needs validation with real patient data</li>
                <li><strong>Individual Variation:</strong> Cannot account for all personal health factors</li>
                <li><strong>Professional Consultation:</strong> Always recommend consulting healthcare providers</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Privacy and Data Protection
    st.markdown("### 🔒 Privacy & Data Protection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Data Handling")
        st.markdown(
            """
            - **Local Processing:** Data processed locally when possible
            - **Minimal Collection:** Only collect necessary health information
            - **No Third-Party Sharing:** Personal data not shared with third parties
            - **User Control:** Users can delete their data at any time
            - **Encryption:** All data transmission encrypted
            """
        )
    
    with col2:
        st.markdown("#### Compliance")
        st.markdown(
            """
            - **GDPR Compliant:** European data protection standards
            - **HIPAA Considerations:** Healthcare data protection principles
            - **Transparent Policies:** Clear privacy policy and terms
            - **Regular Audits:** Periodic security and privacy assessments
            - **User Rights:** Full control over personal data
            """
        )
    
    # Safety Measures
    st.markdown("### 🛡️ Safety Measures")
    
    st.markdown(
        """
        <div class="pastel-card">
            <h4>Safety Protocols</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <h5>🚨 Crisis Detection</h5>
                    <ul>
                        <li>Emergency keyword detection</li>
                        <li>Crisis resource provision</li>
                        <li>Professional referral system</li>
                        <li>Safety disclaimers</li>
                    </ul>
                </div>
                <div>
                    <h5>📋 Content Safety</h5>
                    <ul>
                        <li>Evidence-based information only</li>
                        <li>Medical professional review</li>
                        <li>Age-appropriate content</li>
                        <li>Regular content updates</li>
                    </ul>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Accessibility and Inclusion
    st.markdown("### ♿ Accessibility & Inclusion")
    
    st.markdown(
        """
        <div class="mint-card" style="padding: 1.5rem;">
            <h4>Inclusive Design Principles</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <h5>🎯 Accessibility Features</h5>
                    <ul>
                        <li>Screen reader compatible</li>
                        <li>Keyboard navigation support</li>
                        <li>High contrast options</li>
                        <li>Clear, simple language</li>
                    </ul>
                </div>
                <div>
                    <h5>🌍 Inclusion Efforts</h5>
                    <ul>
                        <li>Diverse representation in training</li>
                        <li>Cultural sensitivity</li>
                        <li>Multi-language support planned</li>
                        <li>Economic accessibility</li>
                    </ul>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Model Performance Metrics
    if model_insights and 'models' in model_insights:
        st.markdown("### 📈 Model Performance Metrics")
        
        for model_type, model_data in model_insights['models'].items():
            if 'performance' in model_data:
                perf = model_data['performance']
                st.markdown(f"#### {model_type.title()} Model")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Best Model", perf.get('best_model', 'N/A'))
                    st.metric("R² Score", f"{perf.get('r2_score', 0):.3f}")
                
                with col2:
                    st.metric("MAE", f"{perf.get('mae', 0):.3f}")
                    st.metric("CV Score", f"{perf.get('cv_mean', 0):.3f}")
                
                with col3:
                    st.metric("Total Models", perf.get('total_models', 0))
                    st.metric("Clinical Relevance", perf.get('clinical_relevance', 'N/A'))
    
    # Recommendations for Improvement
    st.markdown("### 🚀 Recommendations for Improvement")
    
    if model_insights and 'recommendations' in model_insights:
        recs = model_insights['recommendations']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Immediate Actions")
            for action in recs.get('immediate_actions', []):
                st.markdown(f"• {action}")
        
        with col2:
            st.markdown("#### Medium Term")
            for action in recs.get('medium_term', []):
                st.markdown(f"• {action}")
        
        with col3:
            st.markdown("#### Long Term")
            for action in recs.get('long_term', []):
                st.markdown(f"• {action}")
    
    # Contact and Reporting
    st.markdown("### 📞 Contact & Reporting")
    
    st.markdown(
        """
        <div class="pastel-card">
            <h4>Questions, Concerns, or Feedback</h4>
            <p>We are committed to continuous improvement and transparency. If you have questions about our ethical practices, concerns about bias, or suggestions for improvement, please reach out:</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div>
                    <h5>📧 Contact Information</h5>
                    <ul>
                        <li><strong>Email:</strong> ethics@menobalance.ai</li>
                        <li><strong>Feedback:</strong> Built-in feedback mechanisms</li>
                        <li><strong>Updates:</strong> Regular communication about improvements</li>
                    </ul>
                </div>
                <div>
                    <h5>📋 Report Issues</h5>
                    <ul>
                        <li><strong>Bias Concerns:</strong> Report potential bias or unfairness</li>
                        <li><strong>Technical Issues:</strong> Report bugs or technical problems</li>
                        <li><strong>Content Accuracy:</strong> Report inaccurate information</li>
                        <li><strong>Privacy Concerns:</strong> Report privacy or security issues</li>
                    </ul>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Last Updated
    st.markdown("### 📅 Documentation Status")
    
    st.markdown(
        f"""
        <div class="metric-card" style="text-align: center;">
            <h4>Last Updated</h4>
            <p style="font-size: 1.2rem; color: var(--primary);">{datetime.now().strftime('%B %d, %Y')}</p>
            <p style="color: var(--text-muted);">This documentation is reviewed and updated regularly</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_ethics_bias()
