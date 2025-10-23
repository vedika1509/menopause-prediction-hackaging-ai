"""
Privacy Consent and Contact Information
"""

from datetime import datetime

import streamlit as st


def render_privacy_consent():
    """Render privacy consent and contact information."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Page header
    st.markdown(
        """
    <div class="main-header">
        <h1>🔒 Privacy & Consent</h1>
        <p style="color: var(--medium-gray);">Your privacy and data protection are our top priorities</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Privacy consent form
    render_privacy_consent_form()

    # Contact information
    render_contact_information()

    # Data protection details
    render_data_protection_details()


def render_privacy_consent_form():
    """Render privacy consent form."""
    st.markdown("### 📋 Privacy Consent Form")

    with st.form("privacy_consent_form"):
        st.markdown(
            """
            <div class="info-card">
                <h4>🔐 Data Collection Consent</h4>
                <p>By using MenoBalance AI, you consent to the collection and processing of your health data 
                for the purpose of providing personalized menopause insights and recommendations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Consent checkboxes
        data_collection = st.checkbox(
            "✅ I consent to the collection of my health data for personalized insights",
            help="This includes age, symptoms, hormone levels, and lifestyle factors",
        )

        data_processing = st.checkbox(
            "✅ I consent to the processing of my data using AI models",
            help="Your data will be processed by machine learning models to generate predictions",
        )

        data_storage = st.checkbox(
            "✅ I consent to the secure storage of my data",
            help="Your data will be stored securely and encrypted",
        )

        data_sharing = st.checkbox(
            "✅ I consent to anonymous data sharing for research purposes",
            help="Your data may be used anonymously for medical research (no personal identifiers)",
        )

        marketing_consent = st.checkbox(
            "✅ I consent to receive educational content and updates",
            help="You may receive menopause education tips and app updates",
        )

        # Age verification
        age_verification = st.checkbox(
            "✅ I confirm I am 18 years or older",
            help="This application is intended for adults only",
        )

        # Submit button
        submitted = st.form_submit_button(
            "💾 Save Consent Preferences", use_container_width=True, type="primary"
        )

        if submitted:
            if all([data_collection, data_processing, data_storage, age_verification]):
                # Store consent preferences
                st.session_state.privacy_consent = {
                    "data_collection": data_collection,
                    "data_processing": data_processing,
                    "data_storage": data_storage,
                    "data_sharing": data_sharing,
                    "marketing_consent": marketing_consent,
                    "age_verification": age_verification,
                    "consent_date": datetime.now().isoformat(),
                    "consent_version": "1.0",
                }

                st.success("✅ Privacy consent preferences saved successfully!")
                st.balloons()
            else:
                st.error("❌ Please provide consent for all required data processing activities.")


def render_contact_information():
    """Render contact information."""
    st.markdown("### 📞 Contact Information")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card" style="background: linear-gradient(135deg, #E1BEE7 0%, #F3E5F5 100%);">
                <h3>👨‍💻 Developer & Creator</h3>
                <div style="text-align: center; padding: 1rem;">
                     <h4 style="color: var(--primary); margin: 0;">Vedika Goyal</h4>
                     <p style="color: var(--medium-gray); margin: 0.5rem 0;">AI/ML Engineer & Healthcare Technology Specialist</p>
                     
                     <div style="margin: 1rem 0;">
                         <a href="https://www.linkedin.com/in/vedikagoyal1509/" target="_blank" 
                            style="display: inline-block; margin: 0.5rem; padding: 0.5rem 1rem; 
                                   background: #0077B5; color: white; text-decoration: none; 
                                   border-radius: 8px; font-weight: 500;">
                             💼 LinkedIn Profile
                         </a>
                     </div>
                     
                     <div style="margin: 1rem 0;">
                         <a href="mailto:vedikagoyal1509@gmail.com" 
                            style="display: inline-block; margin: 0.5rem; padding: 0.5rem 1rem; 
                                   background: #9C27B0; color: white; text-decoration: none; 
                                   border-radius: 8px; font-weight: 500;">
                             📧 Email Contact
                         </a>
                     </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card" style="background: linear-gradient(135deg, #B2DFDB 0%, #E8F5E8 100%);">
                <h3>🤝 Support & Feedback</h3>
                <div style="padding: 1rem;">
                    <p><strong>📧 General Inquiries:</strong><br>
                    <a href="mailto:support@menobalance.ai">support@menobalance.ai</a></p>
                    
                    <p><strong>🐛 Bug Reports:</strong><br>
                    <a href="mailto:bugs@menobalance.ai">bugs@menobalance.ai</a></p>
                    
                    <p><strong>💡 Feature Requests:</strong><br>
                    <a href="mailto:features@menobalance.ai">features@menobalance.ai</a></p>
                    
                    <p><strong>🔒 Privacy Concerns:</strong><br>
                    <a href="mailto:privacy@menobalance.ai">privacy@menobalance.ai</a></p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_data_protection_details():
    """Render data protection details."""
    st.markdown("### 🛡️ Data Protection & Privacy")

    # Data collection details
    st.markdown("#### 📊 What Data We Collect")

    data_types = [
        {
            "category": "Personal Information",
            "items": ["Age", "Height", "Weight", "BMI"],
            "purpose": "Basic health profiling and BMI calculation",
            "retention": "Until account deletion",
        },
        {
            "category": "Health Data",
            "items": [
                "Hormone levels (FSH, Estradiol, AMH, Progesterone)",
                "Symptom severity ratings",
                "Sleep quality",
                "Energy levels",
            ],
            "purpose": "Personalized menopause predictions and recommendations",
            "retention": "Until account deletion",
        },
        {
            "category": "Lifestyle Data",
            "items": ["Exercise frequency", "Stress levels", "Diet quality", "Smoking status"],
            "purpose": "Lifestyle factor analysis for recommendations",
            "retention": "Until account deletion",
        },
        {
            "category": "Wearable Data",
            "items": ["Daily steps", "Sleep hours", "Heart rate", "HRV"],
            "purpose": "Wellness tracking and health insights",
            "retention": "Until account deletion",
        },
    ]

    for data_type in data_types:
        with st.expander(f"📋 {data_type['category']}"):
            st.markdown(f"**Items:** {', '.join(data_type['items'])}")
            st.markdown(f"**Purpose:** {data_type['purpose']}")
            st.markdown(f"**Retention:** {data_type['retention']}")

    # Data protection measures
    st.markdown("#### 🔐 Data Protection Measures")

    protection_measures = [
        "🔒 **Encryption**: All data is encrypted in transit and at rest using AES-256 encryption",
        "🛡️ **Access Control**: Strict access controls with role-based permissions",
        "🔐 **Authentication**: Multi-factor authentication for all system access",
        "📊 **Anonymization**: Personal identifiers are removed for research purposes",
        "🔄 **Data Minimization**: We only collect data necessary for our services",
        "⏰ **Retention Limits**: Data is automatically deleted after specified periods",
        "🔍 **Audit Logs**: Comprehensive logging of all data access and modifications",
        "🌍 **GDPR Compliance**: Full compliance with EU General Data Protection Regulation",
    ]

    for measure in protection_measures:
        st.markdown(f"- {measure}")

    # User rights
    st.markdown("#### 👤 Your Rights")

    user_rights = [
        "📋 **Right to Access**: Request a copy of all your personal data",
        "✏️ **Right to Rectification**: Correct inaccurate or incomplete data",
        "🗑️ **Right to Erasure**: Request deletion of your personal data",
        "📤 **Right to Portability**: Export your data in a machine-readable format",
        "⏸️ **Right to Restrict Processing**: Limit how we use your data",
        "🚫 **Right to Object**: Object to certain types of data processing",
        "📞 **Right to Complain**: Contact supervisory authorities if needed",
    ]

    for right in user_rights:
        st.markdown(f"- {right}")

    # Contact for privacy concerns
    st.markdown(
        """
        <div class="warning-card" style="margin-top: 2rem;">
            <h4>🔒 Privacy Concerns?</h4>
            <p>If you have any questions about your data privacy or want to exercise your rights, 
            please contact us at <strong>privacy@menobalance.ai</strong> or use the contact form above.</p>
            <p>We respond to all privacy inquiries within 48 hours.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_privacy_footer():
    """Render privacy footer for all pages."""
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: var(--medium-gray); padding: 1rem; font-size: 0.9rem;">
            <p>🔒 <strong>Privacy Protected</strong> | 
            <a href="mailto:privacy@menobalance.ai" style="color: var(--primary);">Privacy Policy</a> | 
            <a href="mailto:support@menobalance.ai" style="color: var(--primary);">Contact Support</a></p>
            <p>Created with ❤️ by <strong>Vedika Hackagain</strong> | 
            <a href="https://www.linkedin.com/in/vedika-hackagain" target="_blank" style="color: var(--primary);">LinkedIn</a> | 
            <a href="mailto:vedika.hackagain@example.com" style="color: var(--primary);">Email</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def check_privacy_consent():
    """Check if user has provided privacy consent."""
    if "privacy_consent" not in st.session_state:
        return False

    consent = st.session_state.privacy_consent
    required_consents = ["data_collection", "data_processing", "data_storage", "age_verification"]

    return all(consent.get(consent_type, False) for consent_type in required_consents)


def render_privacy_notice():
    """Render privacy notice banner if consent not given."""
    if not check_privacy_consent():
        st.markdown(
            """
            <div class="warning-card" style="background: linear-gradient(135deg, #FFE0B2 0%, #FFF3E0 100%); 
                        border-left: 4px solid #FF7043; margin: 1rem 0;">
                <h4>🔒 Privacy Notice</h4>
                <p>To use MenoBalance AI, please review and accept our privacy policy. 
                <a href="#" onclick="window.parent.postMessage({type: 'navigate', page: 'privacy'}, '*')" 
                   style="color: var(--primary); font-weight: 500;">Click here to review privacy settings</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
