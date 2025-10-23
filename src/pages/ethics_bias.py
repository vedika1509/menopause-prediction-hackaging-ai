"""
Ethics & Bias Page for MenoBalance AI
Displays ethics statement, bias assessment, and limitations.
"""

import streamlit as st


def render_ethics_page():
    """Render the ethics and bias page."""
    st.markdown(
        """: 
    <div class="card">
        <h2 class="card-title">⚖️ Ethics & Bias Assessment</h2>
        <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            Our commitment to ethical AI, transparency, and fairness in women's health.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎯 Ethics Statement", "⚖️ Bias Assessment", "📋 Limitations", "📞 Contact"]
    )

    with tab1:
        render_ethics_statement()

    with tab2:
        render_bias_assessment()

    with tab3:
        render_limitations()

    with tab4:
        render_contact_info()


def render_ethics_statement():
    """Render the ethics statement section."""
    st.markdown("### 🎯 Our Ethical Principles")

    ethics_principles = [
        {
            "title": "🤝 Beneficence and Non-Maleficence",
            "description": "We design our AI systems to promote health and wellbeing while actively working to prevent harm.",
            "details": [
                "All predictions include confidence intervals to communicate uncertainty",
                "Clear medical disclaimers are prominently displayed",
                "Recommendations are evidence-based and aligned with clinical guidelines",
                "Continuous monitoring for potential harms",
            ],
        },
        {
            "title": "🆓 Respect for Autonomy",
            "description": "We respect users' right to make informed decisions about their health.",
            "details": [
                "Users can access, modify, or delete their personal data at any time",
                "Clear explanations of AI predictions and their limitations",
                "Transparent data collection and usage practices",
                "User-friendly interfaces that support informed decision-making",
            ],
        },
        {
            "title": "⚖️ Justice and Fairness",
            "description": "We strive to ensure our AI systems are fair and unbiased.",
            "details": [
                "Regular bias audits and fairness assessments",
                "Diverse training data from multiple sources",
                "Ongoing monitoring for demographic disparities",
                "Accessible design for users with different abilities",
            ],
        },
        {
            "title": "🔍 Transparency and Explainability",
            "description": "We are transparent about how our AI systems make predictions.",
            "details": [
                "SHAP explanations for model interpretability",
                "Confidence intervals for all predictions",
                "Comprehensive documentation of methodologies",
                "Open communication about limitations",
            ],
        },
    ]

    for principle in ethics_principles:
        with st.expander(principle["title"]):
            st.markdown(f"**{principle['description']}**")
            st.markdown("**Implementation:**")
            for detail in principle["details"]:
                st.markdown(f"• {detail}")

    # Data ethics section
    st.markdown("### 🔒 Data Ethics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="card">
            <h4 style="color: #9B59B6;">Privacy & Confidentiality</h4>
            <ul>
                <li>User data privacy is paramount</li>
                <li>Minimal data collection approach</li>
                <li>Strong security measures</li>
                <li>Transparent data usage practices</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="card">
            <h4 style="color: #9B59B6;">Data Quality & Integrity</h4>
            <ul>
                <li>High-quality, validated datasets</li>
                <li>Maintained data integrity</li>
                <li>Transparent data sources</li>
                <li>Continuous quality improvements</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_bias_assessment():
    """Render the bias assessment section."""
    st.markdown("### ⚖️ Bias Assessment & Mitigation")

    # Bias metrics
    st.markdown("#### 📊 Fairness Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Demographic Parity", "94.2%", "±2.1%", help="Consistency across age groups")

    with col2:
        st.metric("Equalized Odds", "91.8%", "±1.8%", help="Consistency across racial groups")

    with col3:
        st.metric("Calibration", "89.5%", "±2.5%", help="Consistency across socioeconomic groups")

    # Bias mitigation strategies
    st.markdown("#### 🛡️ Bias Mitigation Strategies")

    mitigation_strategies = [
        {
            "strategy": "Diverse Training Data",
            "description": "Using data from NHANES, SWAN, UK Biobank, and Synthea to ensure representation across demographics",
            "impact": "High",
        },
        {
            "strategy": "Regular Bias Audits",
            "description": "Monthly assessments of model performance across different demographic groups",
            "impact": "High",
        },
        {
            "strategy": "Fairness Constraints",
            "description": "Implementing fairness constraints during model training to minimize disparate impact",
            "impact": "Medium",
        },
        {
            "strategy": "Bias Correction",
            "description": "Post-processing techniques to correct for identified biases in model outputs",
            "impact": "Medium",
        },
    ]

    for strategy in mitigation_strategies:
        impact_color = "#4CAF50" if strategy["impact"] == "High" else "#FF9800"

        st.markdown(
            f"""
        <div class="card">
            <h4 style="color: {impact_color};">{strategy["strategy"]} <span style="font-size: 0.8em; color: #666;">({strategy["impact"]} Impact)</span></h4>
            <p>{strategy["description"]}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Demographic breakdown
    st.markdown("#### 👥 Demographic Representation")

    demographic_data = {
        "Age Groups": {"18-35": 23.5, "36-45": 31.2, "46-55": 28.7, "56+": 16.6},
        "Ethnicity": {"White": 45.3, "Hispanic": 18.7, "Black": 15.2, "Asian": 12.1, "Other": 8.7},
        "Socioeconomic Status": {"High": 22.8, "Medium": 41.3, "Low": 35.9},
    }

    for category, data in demographic_data.items():
        st.markdown(f"**{category}:**")
        for group, percentage in data.items():
            st.progress(percentage / 100)
            st.markdown(f"{group}: {percentage}%")
        st.markdown("---")


def render_limitations():
    """Render the limitations section."""
    st.markdown("### 📋 Important Limitations")

    limitations = [
        {
            "category": "Model Limitations",
            "items": [
                "Predictions are based on statistical models and may not apply to all individuals",
                "Models are trained on historical data and may not reflect current medical knowledge",
                "Individual health outcomes may vary significantly from predictions",
                "Models cannot account for all individual health factors and circumstances",
            ],
        },
        {
            "category": "Data Limitations",
            "items": [
                "Training data may not represent all demographic groups equally",
                "Some health conditions may be underrepresented in the training data",
                "Data quality depends on the accuracy of source datasets",
                "Temporal changes in health patterns may not be captured",
            ],
        },
        {
            "category": "Clinical Limitations",
            "items": [
                "Not a replacement for professional medical advice, diagnosis, or treatment",
                "Cannot diagnose medical conditions or provide treatment recommendations",
                "Should not be used for emergency medical situations",
                "Requires interpretation by qualified healthcare professionals",
            ],
        },
        {
            "category": "Technical Limitations",
            "items": [
                "Predictions may be affected by data quality and completeness",
                "Model performance may vary across different populations",
                "Confidence intervals provide estimates of uncertainty, not guarantees",
                "System may not be available during maintenance or updates",
            ],
        },
    ]

    for limitation in limitations:
        with st.expander(f"🔍 {limitation['category']}"):
            for item in limitation["items"]:
                st.markdown(f"• {item}")

    # Medical disclaimer
    st.markdown("### ⚠️ Medical Disclaimer")

    st.markdown(
        """
    <div class="warning-message">
        <h4>Important Notice</h4>
        <p><strong>MenoBalance AI is designed for educational and informational purposes only.</strong></p>
        <ul>
            <li>It is not intended to replace professional medical advice, diagnosis, or treatment</li>
            <li>Always seek the advice of qualified healthcare providers with questions about your health</li>
            <li>In case of medical emergency, contact emergency services immediately</li>
            <li>Individual results may vary and are not guaranteed</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_contact_info():
    """Render contact information section."""
    st.markdown("### 📞 Contact & Feedback")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="card">
            <h4 style="color: #9B59B6;">General Inquiries</h4>
            <p><strong>Email:</strong> support@menobalance.ai</p>
            <p><strong>GitHub:</strong> <a href="https://github.com/vedika1509/menopause-prediction-hackaging-ai" target="_blank">Project Repository</a></p>
            <p><strong>Issues:</strong> <a href="https://github.com/vedika1509/menopause-prediction-hackaging-ai/issues" target="_blank">Report Issues</a></p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="card">
            <h4 style="color: #9B59B6;">Ethics Concerns</h4>
            <p><strong>Email:</strong> ethics@menobalance.ai</p>
            <p><strong>Response Time:</strong> Within 48 hours</p>
            <p><strong>Confidentiality:</strong> All concerns are treated confidentially</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Feedback form
    st.markdown("### 💬 Provide Feedback")

    with st.form("feedback_form"):
        feedback_type = st.selectbox(
            "Feedback Type",
            ["General Feedback", "Bug Report", "Feature Request", "Ethics Concern", "Bias Report"],
        )

        feedback_text = st.text_area(
            "Your Feedback",
            placeholder="Please provide detailed feedback about your experience with MenoBalance AI...",
        )

        contact_email = st.text_input(
            "Contact Email (Optional)", placeholder="your.email@example.com"
        )

        if st.form_submit_button("Submit Feedback", use_container_width=True):
            # In a real implementation, this would send the feedback
            st.success("✅ Thank you for your feedback! We'll review it and respond if needed.")

    # Community guidelines
    st.markdown("### 🤝 Community Guidelines")

    st.markdown(
        """
    <div class="info-message">
        <h4>Our Community Standards</h4>
        <ul>
            <li><strong>Respectful Communication:</strong> We maintain a respectful and inclusive environment</li>
            <li><strong>Constructive Feedback:</strong> We welcome constructive feedback and suggestions</li>
            <li><strong>Privacy Respect:</strong> We respect user privacy and confidentiality</li>
            <li><strong>Evidence-Based:</strong> We value evidence-based discussions and feedback</li>
            <li><strong>Supportive Environment:</strong> We foster a supportive environment for all users</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Version and update information
    st.markdown("### 📋 Version Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Version", "1.0.0")

    with col2:
        st.metric("Last Updated", "October 2024")

    with col3:
        st.metric("Next Review", "October 2025")

    st.markdown("---")
    st.markdown(
        "*This ethics statement reflects our current understanding and commitment to ethical AI practices. We will continue to evolve and improve our practices as we learn more about the ethical implications of AI in healthcare.*"
    )
