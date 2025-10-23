"""
Education Page for MenoBalance AI
Educational resources and content about menopause.
"""

import os

# Import Nebius AI service for dynamic content generation
import sys
from datetime import datetime

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatbot_nebius import get_nebius_service


def render_education_page():
    """Render the education page."""
    st.markdown(
        """
    <div class="card">
        <h2 class="card-title">📚 Educational Resources</h2>
        <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            Learn about menopause, symptoms, and management strategies through our comprehensive educational content.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Get Nebius AI service
    nebius_service = get_nebius_service()

    # Create tabs for different educational topics
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🔬 Understanding Menopause",
            "🎯 Management Strategies",
            "🥗 Lifestyle & Nutrition",
            "💡 Ask AI",
        ]
    )

    with tab1:
        render_menopause_basics(nebius_service)

    with tab2:
        render_management_strategies(nebius_service)

    with tab3:
        render_lifestyle_nutrition(nebius_service)

    with tab4:
        render_ai_education(nebius_service)


def render_menopause_basics(nebius_service):
    """Render menopause basics educational content."""
    st.markdown("### 🔬 Understanding Menopause")

    # Static content
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #9B59B6;">What is Menopause?</h4>
            <p>Menopause is a natural biological process that marks the end of a woman's reproductive years. 
            It typically occurs between the ages of 45 and 55, with the average age being 51.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Three stages of menopause
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h4 style="color: #4CAF50;">Pre-menopause</h4>
                <p>Regular menstrual cycles and normal hormone levels. This is the time before any 
                menopausal symptoms begin.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h4 style="color: #FF9800;">Peri-menopause</h4>
                <p>The transition period when menstrual cycles become irregular and symptoms begin to appear. 
                This can last 4-8 years.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <h4 style="color: #F44336;">Post-menopause</h4>
                <p>Begins 12 months after the last menstrual period. Hormone levels stabilize at lower levels.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Common symptoms
    st.markdown("#### 🌡️ Common Symptoms")

    symptoms = [
        ("🔥 Hot Flashes", "Sudden feelings of heat, often with sweating and flushing"),
        ("😴 Sleep Disturbances", "Difficulty falling asleep or staying asleep"),
        ("😰 Mood Changes", "Irritability, anxiety, or depression"),
        ("💤 Fatigue", "Persistent tiredness and lack of energy"),
        ("🤕 Headaches", "Increased frequency or intensity of headaches"),
        ("💪 Joint Pain", "Aches and stiffness in joints"),
        ("🧠 Memory Issues", "Difficulty concentrating or remembering things"),
        ("💔 Heart Palpitations", "Irregular or rapid heartbeat"),
    ]

    for symptom, description in symptoms:
        with st.expander(symptom):
            st.markdown(description)

    # Generate dynamic content using Nebius AI
    if st.button("🤖 Get Personalized Information", use_container_width=True):
        with st.spinner("Generating personalized content..."):
            content = nebius_service.generate_educational_content("menopause stages and symptoms")
            st.markdown(f"**{content['title']}**")
            st.markdown(content["content"])


def render_management_strategies(nebius_service):
    """Render management strategies educational content."""
    st.markdown("### 🎯 Management Strategies")

    # Treatment options
    st.markdown("#### 💊 Treatment Options")

    treatments = [
        {
            "title": "Hormone Therapy",
            "description": "Estrogen and progesterone replacement to manage symptoms",
            "pros": ["Effective for hot flashes", "Prevents bone loss", "Improves sleep"],
            "cons": ["Risk of blood clots", "Breast cancer risk", "Not for everyone"],
            "color": "#4CAF50",
        },
        {
            "title": "Non-Hormonal Medications",
            "description": "Alternative medications for symptom management",
            "pros": ["Lower risk profile", "Good for specific symptoms", "Fewer side effects"],
            "cons": ["May be less effective", "Multiple medications needed", "Cost considerations"],
            "color": "#2196F3",
        },
        {
            "title": "Lifestyle Modifications",
            "description": "Natural approaches to symptom management",
            "pros": ["No side effects", "Improves overall health", "Cost-effective"],
            "cons": ["May take longer to work", "Requires commitment", "Results vary"],
            "color": "#FF9800",
        },
    ]

    for treatment in treatments:
        with st.expander(f"{treatment['title']}"):
            st.markdown(f"**{treatment['description']}**")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Pros:**")
                for pro in treatment["pros"]:
                    st.markdown(f"✅ {pro}")

            with col2:
                st.markdown("**Cons:**")
                for con in treatment["cons"]:
                    st.markdown(f"❌ {con}")

    # Natural remedies
    st.markdown("#### 🌿 Natural Remedies")

    remedies = [
        ("🌿 Black Cohosh", "May help with hot flashes and night sweats"),
        ("🧘‍♀️ Meditation", "Reduces stress and improves sleep quality"),
        ("🏃‍♀️ Regular Exercise", "Improves mood and overall health"),
        ("🥗 Phytoestrogens", "Plant compounds that may help with symptoms"),
        ("🧊 Cooling Techniques", "Immediate relief for hot flashes"),
        ("💤 Sleep Hygiene", "Better sleep habits for improved rest"),
    ]

    for remedy, description in remedies:
        st.markdown(f"**{remedy}** - {description}")

    # Generate personalized recommendations
    if st.button("🎯 Get Personalized Management Tips", use_container_width=True):
        with st.spinner("Generating personalized recommendations..."):
            content = nebius_service.generate_educational_content("menopause management strategies")
            st.markdown(f"**{content['title']}**")
            st.markdown(content["content"])


def render_lifestyle_nutrition(nebius_service):
    """Render lifestyle and nutrition educational content."""
    st.markdown("### 🥗 Lifestyle & Nutrition")

    # Nutrition guidelines
    st.markdown("#### 🍎 Nutrition Guidelines")

    nutrition_tips = [
        {
            "category": "Calcium-Rich Foods",
            "foods": ["Dairy products", "Leafy greens", "Fortified foods", "Sardines"],
            "benefit": "Supports bone health during menopause",
        },
        {
            "category": "Phytoestrogens",
            "foods": ["Soy products", "Flaxseeds", "Chickpeas", "Lentils"],
            "benefit": "May help balance hormones naturally",
        },
        {
            "category": "Omega-3 Fatty Acids",
            "foods": ["Fatty fish", "Walnuts", "Chia seeds", "Flaxseeds"],
            "benefit": "Reduces inflammation and supports heart health",
        },
        {
            "category": "Antioxidant-Rich Foods",
            "foods": ["Berries", "Dark leafy greens", "Nuts", "Colorful vegetables"],
            "benefit": "Protects against oxidative stress and aging",
        },
    ]

    for tip in nutrition_tips:
        with st.expander(tip["category"]):
            st.markdown(f"**Benefit:** {tip['benefit']}")
            st.markdown("**Foods to include:**")
            for food in tip["foods"]:
                st.markdown(f"• {food}")

    # Exercise recommendations
    st.markdown("#### 🏃‍♀️ Exercise Recommendations")

    exercise_types = [
        ("💪 Strength Training", "Builds muscle mass and bone density", "2-3 times per week"),
        ("🏃‍♀️ Cardiovascular Exercise", "Improves heart health and mood", "150 minutes per week"),
        ("🧘‍♀️ Yoga & Stretching", "Reduces stress and improves flexibility", "Daily"),
        ("🚶‍♀️ Walking", "Low-impact exercise for overall health", "30 minutes daily"),
        ("🏊‍♀️ Swimming", "Full-body workout that's easy on joints", "2-3 times per week"),
    ]

    for exercise, benefit, frequency in exercise_types:
        st.markdown(f"**{exercise}**")
        st.markdown(f"*{benefit}*")
        st.markdown(f"**Recommended frequency:** {frequency}")
        st.markdown("---")

    # Stress management
    st.markdown("#### 🧘‍♀️ Stress Management")

    stress_techniques = [
        ("🧘‍♀️ Meditation", "Practice mindfulness meditation for 10-15 minutes daily"),
        ("🫁 Deep Breathing", "Use 4-7-8 breathing technique during stressful moments"),
        ("📝 Journaling", "Write about your thoughts and feelings regularly"),
        ("🎵 Music Therapy", "Listen to calming music to reduce stress"),
        ("🌿 Nature Time", "Spend time outdoors to reduce cortisol levels"),
        ("👥 Social Support", "Connect with friends and family for emotional support"),
    ]

    for technique, description in stress_techniques:
        st.markdown(f"**{technique}** - {description}")

    # Generate personalized nutrition plan
    if st.button("🍎 Get Personalized Nutrition Plan", use_container_width=True):
        with st.spinner("Generating personalized nutrition recommendations..."):
            content = nebius_service.generate_educational_content(
                "menopause nutrition and lifestyle"
            )
            st.markdown(f"**{content['title']}**")
            st.markdown(content["content"])


def render_ai_education(nebius_service):
    """Render AI-powered educational content."""
    st.markdown("### 💡 Ask AI About Menopause")

    st.markdown(
        "Ask our AI assistant any questions about menopause, symptoms, or management strategies."
    )

    # Chat interface for educational questions
    if "education_chat_history" not in st.session_state:
        st.session_state.education_chat_history = []

    # Display chat history
    for message in st.session_state.education_chat_history:
        if message["role"] == "user":
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(90deg, #E8DAEF, #F8F4FF);
                    padding: 1rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                    margin-left: 2rem;
                    border-left: 4px solid #9B59B6;
                ">
                    <strong>You:</strong> {message["content"]}
                    <br>
                    <small style="color: #666;">{message["timestamp"]}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(90deg, #F0F8FF, #E3F2FD);
                    padding: 1rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                    margin-right: 2rem;
                    border-left: 4px solid #5DADE2;
                ">
                    <strong>🌸 AI Assistant:</strong> {message["content"]}
                    <br>
                    <small style="color: #666;">{message["timestamp"]}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Chat input
    user_question = st.text_area(
        "Ask a question about menopause...",
        height=100,
        placeholder="e.g., What are the best natural remedies for hot flashes?",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Ask AI", use_container_width=True, type="primary"):
            if user_question.strip():
                # Add user message to history
                user_msg = {
                    "role": "user",
                    "content": user_question,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
                st.session_state.education_chat_history.append(user_msg)

                # Get AI response
                try:
                    with st.spinner("AI is thinking..."):
                        ai_response = nebius_service.chat(user_question, {"context": "education"})

                    # Add AI response to history
                    ai_msg = {
                        "role": "assistant",
                        "content": ai_response,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                    }
                    st.session_state.education_chat_history.append(ai_msg)

                    st.rerun()

                except Exception:
                    st.error("Sorry, I'm having trouble responding right now. Please try again.")

    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.education_chat_history = []
            st.rerun()

    # Quick question suggestions
    st.markdown("#### 💡 Quick Question Suggestions")

    quick_questions = [
        "What are the stages of menopause?",
        "How can I manage hot flashes naturally?",
        "What foods should I avoid during menopause?",
        "Is hormone therapy safe for me?",
        "How does exercise help with menopause symptoms?",
        "What are the long-term health risks of menopause?",
    ]

    for question in quick_questions:
        if st.button(question, use_container_width=True):
            # Add user message to history
            user_msg = {
                "role": "user",
                "content": question,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            }
            st.session_state.education_chat_history.append(user_msg)

            # Get AI response
            try:
                with st.spinner("AI is thinking..."):
                    ai_response = nebius_service.chat(question, {"context": "education"})

                # Add AI response to history
                ai_msg = {
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
                st.session_state.education_chat_history.append(ai_msg)

                st.rerun()

            except Exception:
                st.error("Sorry, I'm having trouble responding right now. Please try again.")

    # Educational disclaimer
    st.markdown(
        """
        <div class="warning-message">
            <h4>⚠️ Educational Disclaimer</h4>
            <p>This educational content is for informational purposes only and should not replace 
            professional medical advice. Always consult with your healthcare provider for 
            personalized medical guidance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
