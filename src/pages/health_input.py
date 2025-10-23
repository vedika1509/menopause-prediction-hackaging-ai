"""
Health Input Page for MenoBalance AI
Comprehensive health data collection form with validation and progress tracking.
"""

import streamlit as st


def validate_age(age):
    """Validate age input."""
    try:
        age = float(age)
        if 18 <= age <= 100:
            return True, ""
        else:
            return False, "Age must be between 18 and 100 years"
    except:
        return False, "Please enter a valid age"


def validate_bmi(bmi):
    """Validate BMI input."""
    try:
        bmi = float(bmi)
        if 10 <= bmi <= 80:
            return True, ""
        else:
            return False, "BMI must be between 10 and 80"
    except:
        return False, "Please enter a valid BMI"


def validate_hormone_value(value, hormone_name, min_val=0, max_val=1000):
    """Validate hormone values."""
    if value is None or value == "":
        return True, ""  # Optional field

    try:
        value = float(value)
        if min_val <= value <= max_val:
            return True, ""
        else:
            return False, f"{hormone_name} must be between {min_val} and {max_val}"
    except:
        return False, f"Please enter a valid {hormone_name} value"


def calculate_bmi(weight, height):
    """Calculate BMI from weight and height."""
    if weight and height and height > 0:
        height_m = height / 100  # Convert cm to meters
        return round(weight / (height_m**2), 1)
    return None


def render_health_input_page():
    """Render the health input form page."""
    st.markdown(
        """
    <div class="card">
        <h2 class="card-title">📝 Health Information Form</h2>
        <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            Please provide your health information to receive personalized predictions. 
            All fields marked with * are required. Your data is kept private and secure.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize form data if not exists
    if "health_data" not in st.session_state:
        st.session_state.health_data = {}

    # Progress tracking
    total_sections = 4
    completed_sections = 0

    # Check completed sections
    if st.session_state.health_data.get("demographics_completed", False):
        completed_sections += 1
    if st.session_state.health_data.get("hormones_completed", False):
        completed_sections += 1
    if st.session_state.health_data.get("lifestyle_completed", False):
        completed_sections += 1
    if st.session_state.health_data.get("medical_history_completed", False):
        completed_sections += 1

    # Progress bar
    progress = completed_sections / total_sections
    st.progress(progress)
    st.markdown(f"**Progress:** {completed_sections}/{total_sections} sections completed")

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(
        ["👤 Demographics", "🧪 Hormones", "🏃‍♀️ Lifestyle", "🏥 Medical History"]
    )

    with tab1:
        render_demographics_section()

    with tab2:
        render_hormones_section()

    with tab3:
        render_lifestyle_section()

    with tab4:
        render_medical_history_section()

    # Form validation and submission
    if st.button("📊 Get My Predictions", use_container_width=True, type="primary"):
        if validate_form():
            st.success("✅ Form completed successfully! Redirecting to predictions...")
            st.session_state.current_page = "Predictions"
            st.rerun()
        else:
            st.error("⚠️ Please complete all required fields before proceeding.")


def render_demographics_section():
    """Render the demographics section."""
    st.markdown("### 👤 Demographics")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age *",
            min_value=18,
            max_value=100,
            value=st.session_state.health_data.get("age", 35),
            help="Your current age in years",
        )

        height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=st.session_state.health_data.get("height", 165),
            help="Your height in centimeters",
        )

    with col2:
        weight = st.number_input(
            "Weight (kg)",
            min_value=30,
            max_value=300,
            value=st.session_state.health_data.get("weight", 65),
            help="Your current weight in kilograms",
        )

        # Auto-calculate BMI
        bmi = calculate_bmi(weight, height)
        if bmi:
            st.metric("Calculated BMI", f"{bmi:.1f}")
            st.session_state.health_data["bmi"] = bmi

    # Store data
    st.session_state.health_data.update(
        {"age": age, "height": height, "weight": weight, "demographics_completed": True}
    )

    # Validation feedback
    age_valid, age_msg = validate_age(age)
    if not age_valid:
        st.error(age_msg)

    if bmi:
        bmi_valid, bmi_msg = validate_bmi(bmi)
        if not bmi_valid:
            st.error(bmi_msg)


def render_hormones_section():
    """Render the hormones section."""
    st.markdown("### 🧪 Hormone Levels")
    st.markdown("*These are optional but will improve prediction accuracy if available.*")

    col1, col2 = st.columns(2)

    with col1:
        fsh = st.number_input(
            "FSH (mIU/mL)",
            min_value=0.0,
            max_value=200.0,
            value=st.session_state.health_data.get("fsh"),
            help="Follicle Stimulating Hormone level",
        )

        amh = st.number_input(
            "AMH (ng/mL)",
            min_value=0.0,
            max_value=20.0,
            value=st.session_state.health_data.get("amh"),
            help="Anti-Mullerian Hormone level",
        )

    with col2:
        estradiol = st.number_input(
            "Estradiol (pg/mL)",
            min_value=0.0,
            max_value=1000.0,
            value=st.session_state.health_data.get("estradiol"),
            help="Estradiol level",
        )

        # Cycle regularity
        regular_cycles = st.selectbox(
            "Menstrual Cycle Regularity",
            ["Regular", "Irregular", "Not applicable"],
            index=0 if st.session_state.health_data.get("regular_cycles") else 2,
        )

    # Store data
    st.session_state.health_data.update(
        {
            "fsh": fsh if fsh > 0 else None,
            "amh": amh if amh > 0 else None,
            "estradiol": estradiol if estradiol > 0 else None,
            "regular_cycles": regular_cycles == "Regular",
            "hormones_completed": True,
        }
    )

    # Validation feedback
    fsh_valid, fsh_msg = validate_hormone_value(fsh, "FSH", 0, 200)
    if not fsh_valid:
        st.error(fsh_msg)

    amh_valid, amh_msg = validate_hormone_value(amh, "AMH", 0, 20)
    if not amh_valid:
        st.error(amh_msg)

    estradiol_valid, estradiol_msg = validate_hormone_value(estradiol, "Estradiol", 0, 1000)
    if not estradiol_valid:
        st.error(estradiol_msg)


def render_lifestyle_section():
    """Render the lifestyle section."""
    st.markdown("### 🏃‍♀️ Lifestyle Factors")

    col1, col2 = st.columns(2)

    with col1:
        exercise_frequency = st.selectbox(
            "Exercise Frequency per Week", ["0", "1-2", "3-4", "5-6", "Daily"], index=2
        )

        sleep_hours = st.slider(
            "Average Sleep Hours per Night",
            min_value=3.0,
            max_value=12.0,
            value=st.session_state.health_data.get("sleep_hours", 7.5),
            step=0.5,
            help="How many hours do you typically sleep per night?",
        )

    with col2:
        stress_level = st.slider(
            "Current Stress Level",
            min_value=1,
            max_value=10,
            value=st.session_state.health_data.get("stress_level", 5),
            help="Rate your current stress level (1 = very low, 10 = very high)",
        )

        diet_quality = st.selectbox("Diet Quality", ["Poor", "Fair", "Good", "Excellent"], index=2)

    # Store data
    exercise_map = {"0": 0, "1-2": 1.5, "3-4": 3.5, "5-6": 5.5, "Daily": 7}

    st.session_state.health_data.update(
        {
            "exercise_frequency": exercise_map[exercise_frequency],
            "sleep_hours": sleep_hours,
            "stress_level": stress_level,
            "diet_quality": diet_quality,
            "lifestyle_completed": True,
        }
    )


def render_medical_history_section():
    """Render the medical history section."""
    st.markdown("### 🏥 Medical History")

    col1, col2 = st.columns(2)

    with col1:
        smoking_status = st.selectbox("Smoking Status", ["Never", "Former", "Current"], index=0)

        family_history = st.selectbox(
            "Family History of Early Menopause", ["No", "Yes", "Unknown"], index=0
        )

    with col2:
        medications = st.text_area(
            "Current Medications",
            value=st.session_state.health_data.get("medications", ""),
            help="List any medications you're currently taking (optional)",
        )

        chronic_conditions = st.text_area(
            "Chronic Conditions",
            value=st.session_state.health_data.get("chronic_conditions", ""),
            help="List any chronic health conditions (optional)",
        )

    # Store data
    st.session_state.health_data.update(
        {
            "smoking_status": smoking_status == "Current",
            "family_history_menopause": family_history == "Yes",
            "medications": medications,
            "chronic_conditions": chronic_conditions,
            "medical_history_completed": True,
        }
    )


def validate_form():
    """Validate the entire form."""
    required_fields = ["age", "demographics_completed"]
    optional_sections = ["hormones_completed", "lifestyle_completed", "medical_history_completed"]

    # Check required fields
    for field in required_fields:
        if field not in st.session_state.health_data:
            return False

    # Check if at least one optional section is completed
    completed_optional = any(
        st.session_state.health_data.get(section, False) for section in optional_sections
    )

    return completed_optional


def render_form_summary():
    """Render a summary of the form data."""
    if st.session_state.health_data:
        st.markdown("### 📋 Form Summary")

        # Demographics
        if st.session_state.health_data.get("demographics_completed"):
            st.markdown("**Demographics:** ✅ Completed")
            st.markdown(f"- Age: {st.session_state.health_data.get('age', 'N/A')}")
            st.markdown(f"- BMI: {st.session_state.health_data.get('bmi', 'N/A')}")

        # Hormones
        if st.session_state.health_data.get("hormones_completed"):
            st.markdown("**Hormones:** ✅ Completed")
            hormones = []
            if st.session_state.health_data.get("fsh"):
                hormones.append(f"FSH: {st.session_state.health_data['fsh']}")
            if st.session_state.health_data.get("amh"):
                hormones.append(f"AMH: {st.session_state.health_data['amh']}")
            if st.session_state.health_data.get("estradiol"):
                hormones.append(f"Estradiol: {st.session_state.health_data['estradiol']}")

            if hormones:
                st.markdown("- " + ", ".join(hormones))
            else:
                st.markdown("- No hormone data provided")

        # Lifestyle
        if st.session_state.health_data.get("lifestyle_completed"):
            st.markdown("**Lifestyle:** ✅ Completed")
            st.markdown(
                f"- Exercise: {st.session_state.health_data.get('exercise_frequency', 'N/A')} times/week"
            )
            st.markdown(
                f"- Sleep: {st.session_state.health_data.get('sleep_hours', 'N/A')} hours/night"
            )
            st.markdown(f"- Stress: {st.session_state.health_data.get('stress_level', 'N/A')}/10")

        # Medical History
        if st.session_state.health_data.get("medical_history_completed"):
            st.markdown("**Medical History:** ✅ Completed")
            st.markdown(
                f"- Smoking: {'Yes' if st.session_state.health_data.get('smoking_status') else 'No'}"
            )
            st.markdown(
                f"- Family History: {'Yes' if st.session_state.health_data.get('family_history_menopause') else 'No'}"
            )
