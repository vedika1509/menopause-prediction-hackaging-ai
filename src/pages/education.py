"""
Education Page - Health tips, resources, and educational content
"""

import streamlit as st


def render_education_page():
    """Render the education page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Page header
    st.markdown(
        """
    <div class="main-header">
        <h1>📚 Health Education</h1>
        <p style="color: var(--medium-gray);">Learn about menopause and women's health</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Tabs for different content types
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📖 Understanding Menopause",
            "🩺 Managing Symptoms",
            "🏃‍♀️ Lifestyle & Nutrition",
            "🧠 Mental Health",
        ]
    )

    with tab1:
        render_menopause_education()

    with tab2:
        render_symptom_management()

    with tab3:
        render_lifestyle_nutrition()

    with tab4:
        render_mental_health()


def render_menopause_education():
    """Render menopause education content."""
    st.markdown("### 🌸 Understanding Menopause")

    # Educational sections
    sections = [
        {
            "title": "What is Menopause?",
            "content": """
            Menopause is a natural biological process that marks the end of a woman's reproductive years. 
            It occurs when the ovaries stop producing eggs and hormone levels (especially estrogen and progesterone) decline.
            
            **Key Points:**
            - Natural process, not a disease
            - Usually occurs between ages 45-55
            - Marked by 12 consecutive months without menstruation
            - Affects every woman differently
            """,
            "icon": "🌸",
        },
        {
            "title": "The Three Stages",
            "content": """
            **1. Perimenopause (2-8 years before menopause)**
            - Irregular periods
            - Hormone fluctuations
            - Early symptoms may appear
            
            **2. Menopause (12 months without periods)**
            - Official transition point
            - Hormone levels stabilize at low levels
            - Symptoms may peak
            
            **3. Postmenopause (after menopause)**
            - Long-term health considerations
            - Focus on bone and heart health
            - New normal established
            """,
            "icon": "📅",
        },
        {
            "title": "Common Symptoms",
            "content": """
            **Physical Symptoms:**
            - Hot flashes and night sweats
            - Sleep disturbances
            - Vaginal dryness
            - Weight gain
            - Hair and skin changes
            
            **Emotional Symptoms:**
            - Mood swings
            - Anxiety and depression
            - Irritability
            - Memory and concentration issues
            
            **Remember:** Not all women experience all symptoms, and severity varies greatly.
            """,
            "icon": "🩺",
        },
    ]

    for section in sections:
        with st.expander(f"{section['icon']} {section['title']}"):
            st.markdown(section["content"])

    # Interactive quiz
    st.markdown("### 🧠 Test Your Knowledge")

    with st.expander("Take the Menopause Quiz"):
        st.markdown("**Question 1: What defines menopause?**")
        answer1 = st.radio(
            "What defines menopause?",
            ["12 months without periods", "Hot flashes", "Age 50", "Weight gain"],
            key="q1",
        )

        st.markdown("**Question 2: When does perimenopause typically begin?**")
        answer2 = st.radio(
            "When does perimenopause typically begin?",
            ["Age 30", "Age 40-45", "Age 60", "After menopause"],
            key="q2",
        )

        if st.button("Check Answers"):
            score = 0
            if answer1 == "12 months without periods":
                score += 1
                st.success(
                    "✅ Correct! Menopause is defined as 12 consecutive months without menstruation."
                )
            else:
                st.error(
                    "❌ Incorrect. Menopause is defined as 12 consecutive months without menstruation."
                )

            if answer2 == "Age 40-45":
                score += 1
                st.success("✅ Correct! Perimenopause typically begins in the 40s.")
            else:
                st.error("❌ Incorrect. Perimenopause typically begins in the 40s.")

            st.markdown(f"**Score: {score}/2**")
            if score == 2:
                st.balloons()
                st.success("🎉 Perfect! You have a good understanding of menopause basics.")


def render_symptom_management():
    """Render symptom management content."""
    st.markdown("### 🩺 Managing Symptoms")

    # Symptom management tips
    symptoms = {
        "Hot Flashes": {
            "description": "Sudden feelings of warmth, often with sweating and flushing",
            "tips": [
                "Dress in layers for easy temperature regulation",
                "Keep bedroom cool (65-68°F)",
                "Avoid triggers like spicy foods, caffeine, and alcohol",
                "Practice deep breathing exercises",
                "Consider cooling products like fans or cooling towels",
            ],
            "when_to_see_doctor": "If hot flashes are severe, frequent, or significantly impact daily life",
        },
        "Sleep Issues": {
            "description": "Difficulty falling asleep, staying asleep, or poor sleep quality",
            "tips": [
                "Maintain consistent sleep schedule",
                "Create cool, dark bedroom environment",
                "Avoid caffeine after 2 PM",
                "Practice relaxation techniques before bed",
                "Limit screen time before sleep",
            ],
            "when_to_see_doctor": "If sleep problems persist for more than a few weeks",
        },
        "Mood Changes": {
            "description": "Irritability, anxiety, depression, or mood swings",
            "tips": [
                "Practice stress management techniques",
                "Maintain regular exercise routine",
                "Connect with friends and family",
                "Consider therapy or counseling",
                "Practice mindfulness and meditation",
            ],
            "when_to_see_doctor": "If mood changes are severe, persistent, or include thoughts of self-harm",
        },
        "Vaginal Dryness": {
            "description": "Dryness, itching, or discomfort in the vaginal area",
            "tips": [
                "Use water-based lubricants",
                "Stay hydrated",
                "Avoid harsh soaps and douches",
                "Consider vaginal moisturizers",
                "Maintain regular sexual activity if desired",
            ],
            "when_to_see_doctor": "If symptoms are severe or don't improve with self-care",
        },
    }

    # Display symptom management content
    for symptom, info in symptoms.items():
        with st.expander(f"🔥 {symptom}"):
            st.markdown(f"**What it is:** {info['description']}")

            st.markdown("**Management Tips:**")
            for tip in info["tips"]:
                st.markdown(f"• {tip}")

            st.markdown(f"**When to see a doctor:** {info['when_to_see_doctor']}")

    # Personalized recommendations
    if "predictions" in st.session_state and st.session_state.predictions:
        st.markdown("### 🎯 Personalized Tips for You")

        predictions = st.session_state.predictions
        symptoms_data = predictions.get("symptoms", {})
        top_symptoms = symptoms_data.get("top_symptoms", [])

        if top_symptoms:
            st.markdown(
                "Based on your health profile, here are specific tips for your main concerns:"
            )

            for symptom in top_symptoms:
                if symptom in symptoms:
                    st.markdown(f"**{symptom.replace('_', ' ').title()}:**")
                    for tip in symptoms[symptom]["tips"][:3]:  # Show top 3 tips
                        st.markdown(f"• {tip}")


def render_lifestyle_nutrition():
    """Render lifestyle and nutrition content."""
    st.markdown("### 🏃‍♀️ Lifestyle & Nutrition")

    # Nutrition section
    st.markdown("#### 🥗 Nutrition for Menopause")

    nutrition_tips = [
        {
            "category": "Bone Health",
            "foods": [
                "Calcium-rich foods (dairy, leafy greens)",
                "Vitamin D (fatty fish, fortified foods)",
                "Magnesium (nuts, seeds, whole grains)",
            ],
            "why": "Estrogen decline increases bone loss risk",
        },
        {
            "category": "Heart Health",
            "foods": [
                "Omega-3 fatty acids (fish, flaxseeds)",
                "Fiber (whole grains, fruits, vegetables)",
                "Antioxidants (berries, dark leafy greens)",
            ],
            "why": "Heart disease risk increases after menopause",
        },
        {
            "category": "Hormone Balance",
            "foods": [
                "Phytoestrogens (soy, flaxseeds)",
                "Cruciferous vegetables (broccoli, kale)",
                "Healthy fats (avocado, olive oil)",
            ],
            "why": "Natural compounds that may help with hormone balance",
        },
    ]

    for tip in nutrition_tips:
        with st.expander(f"🥗 {tip['category']}"):
            st.markdown(f"**Why it matters:** {tip['why']}")
            st.markdown("**Foods to include:**")
            for food in tip["foods"]:
                st.markdown(f"• {food}")

    # Exercise section
    st.markdown("#### 🏃‍♀️ Exercise for Menopause")

    exercise_types = {
        "Cardiovascular": {
            "benefits": "Improves heart health, helps with weight management, reduces hot flashes",
            "examples": ["Walking", "Swimming", "Cycling", "Dancing", "Aerobic classes"],
            "frequency": "150 minutes per week of moderate intensity",
        },
        "Strength Training": {
            "benefits": "Builds bone density, maintains muscle mass, improves metabolism",
            "examples": ["Weight lifting", "Resistance bands", "Bodyweight exercises", "Pilates"],
            "frequency": "2-3 times per week",
        },
        "Flexibility & Balance": {
            "benefits": "Improves mobility, reduces fall risk, helps with stress",
            "examples": ["Yoga", "Tai chi", "Stretching", "Balance exercises"],
            "frequency": "Daily stretching, 2-3 times per week for yoga/tai chi",
        },
    }

    for exercise_type, info in exercise_types.items():
        with st.expander(f"💪 {exercise_type}"):
            st.markdown(f"**Benefits:** {info['benefits']}")
            st.markdown("**Examples:**")
            for example in info["examples"]:
                st.markdown(f"• {example}")
            st.markdown(f"**Frequency:** {info['frequency']}")

    # Lifestyle tips
    st.markdown("#### 🌟 General Lifestyle Tips")

    lifestyle_tips = [
        "Stay hydrated - aim for 8 glasses of water daily",
        "Limit alcohol and caffeine, especially before bed",
        "Quit smoking - it can worsen menopause symptoms",
        "Maintain a healthy weight through balanced diet and exercise",
        "Get regular health checkups and screenings",
        "Practice stress management techniques",
        "Maintain social connections and relationships",
        "Prioritize sleep and create a relaxing bedtime routine",
    ]

    for tip in lifestyle_tips:
        st.markdown(f"• {tip}")


def render_mental_health():
    """Render mental health content."""
    st.markdown("### 🧠 Mental Health & Wellbeing")

    # Mental health challenges
    st.markdown("#### 🧠 Common Mental Health Challenges")

    challenges = {
        "Mood Swings": {
            "description": "Rapid changes in mood, irritability, or emotional sensitivity",
            "causes": "Hormonal fluctuations, stress, sleep disturbances",
            "coping": [
                "Practice mindfulness and deep breathing",
                "Maintain regular sleep schedule",
                "Engage in regular physical activity",
                "Consider therapy or counseling",
                "Connect with supportive friends and family",
            ],
        },
        "Anxiety": {
            "description": "Feelings of worry, nervousness, or unease",
            "causes": "Hormonal changes, life transitions, health concerns",
            "coping": [
                "Practice relaxation techniques",
                "Limit caffeine and alcohol",
                "Engage in regular exercise",
                "Consider meditation or yoga",
                "Seek professional help if needed",
            ],
        },
        "Depression": {
            "description": "Persistent feelings of sadness, hopelessness, or loss of interest",
            "causes": "Hormonal changes, life stress, health concerns",
            "coping": [
                "Maintain social connections",
                "Engage in activities you enjoy",
                "Practice self-care and self-compassion",
                "Consider therapy or medication",
                "Seek immediate help if you have thoughts of self-harm",
            ],
        },
    }

    for challenge, info in challenges.items():
        with st.expander(f"🧠 {challenge}"):
            st.markdown(f"**What it is:** {info['description']}")
            st.markdown(f"**Common causes:** {info['causes']}")
            st.markdown("**Coping strategies:**")
            for strategy in info["coping"]:
                st.markdown(f"• {strategy}")

    # Stress management techniques
    st.markdown("#### 🧘‍♀️ Stress Management Techniques")

    techniques = [
        {
            "name": "Deep Breathing",
            "description": "Simple breathing exercises to calm the nervous system",
            "how_to": "Inhale for 4 counts, hold for 4, exhale for 6. Repeat 5-10 times.",
        },
        {
            "name": "Progressive Muscle Relaxation",
            "description": "Systematically tense and relax different muscle groups",
            "how_to": "Start with your toes, work up to your head, tensing each muscle group for 5 seconds then relaxing.",
        },
        {
            "name": "Mindfulness Meditation",
            "description": "Focus on the present moment without judgment",
            "how_to": "Sit comfortably, focus on your breath, gently return attention when mind wanders.",
        },
        {
            "name": "Journaling",
            "description": "Write about your thoughts, feelings, and experiences",
            "how_to": "Set aside 10-15 minutes daily to write freely about whatever comes to mind.",
        },
    ]

    for technique in techniques:
        with st.expander(f"🧘‍♀️ {technique['name']}"):
            st.markdown(f"**What it is:** {technique['description']}")
            st.markdown(f"**How to do it:** {technique['how_to']}")

    # Crisis resources
    st.markdown("#### 🆘 Crisis Resources")

    st.markdown("""
    **If you're having thoughts of self-harm or suicide, please seek help immediately:**
    
    - **National Suicide Prevention Lifeline:** 988
    - **Crisis Text Line:** Text HOME to 741741
    - **Emergency Services:** 911
    
    **Remember:** You are not alone, and help is available. Your mental health matters.
    """)

    # Self-care checklist
    st.markdown("#### ✅ Daily Self-Care Checklist")

    self_care_items = [
        "Get 7-9 hours of sleep",
        "Eat nutritious meals",
        "Drink enough water",
        "Move your body for at least 30 minutes",
        "Spend time outdoors or in nature",
        "Connect with someone you care about",
        "Do something you enjoy",
        "Practice gratitude",
        "Take breaks when needed",
        "Be kind to yourself",
    ]

    st.markdown("**Check off what you've done today:**")
    for item in self_care_items:
        st.checkbox(item, key=f"selfcare_{item}")


# This file is imported by the main app
