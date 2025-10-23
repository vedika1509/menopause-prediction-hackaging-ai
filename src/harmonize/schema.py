"""
Canonical schema definition for harmonizing all 5 datasets.
"""

# Core demographic fields
CORE_FIELDS = {
    "participant_id": "string",
    "age": "numeric",
    "bmi": "numeric",
    "race_ethnicity": "categorical",
    "smoking_status": "categorical",
    "education": "numeric",
    "physical_activity": "numeric",
    "alcohol_frequency": "numeric",
}

# Hormone fields
HORMONE_FIELDS = {
    "fsh": "numeric",
    "estradiol": "numeric",
    "amh": "numeric",
    "inhibin_b": "numeric",
    "testosterone": "numeric",
    "tsh": "numeric",
    "lh": "numeric",
    "progesterone": "numeric",
}

# Vital signs
VITAL_FIELDS = {
    "height": "numeric",
    "weight": "numeric",
    "systolic_bp": "numeric",
    "diastolic_bp": "numeric",
    "heart_rate": "numeric",
    "waist_circumference": "numeric",
    "hip_circumference": "numeric",
}

# Symptoms and questionnaires
SYMPTOM_FIELDS = {
    "hot_flashes": "boolean",
    "mood_swings": "boolean",
    "sleep_disturbance": "boolean",
    "depression_score": "numeric",
    "anxiety_score": "numeric",
    "stress_score": "numeric",
    "sleep_quality": "numeric",
    "fatigue_score": "numeric",
}

# Wearable device metrics
WEARABLE_FIELDS = {
    "steps_day": "numeric",
    "sedentary_minutes": "numeric",
    "light_minutes": "numeric",
    "moderate_minutes": "numeric",
    "vigorous_minutes": "numeric",
    "avg_heart_rate": "numeric",
    "hrv_proxy": "numeric",
    "activity_window_fraction": "numeric",
    "sleep_duration": "numeric",
    "sleep_efficiency": "numeric",
}

# Target variables - dual prediction targets
TARGET_FIELDS = {"menopause_stage": "categorical", "menopause_stage_encoded": "numeric"}

# Survival analysis fields for Time to Menopause prediction
SURVIVAL_FIELDS = {
    "time_to_menopause_months": "numeric",
    "menopause_event": "numeric",  # 0=censored, 1=event
    "fmp_date": "datetime",  # Final menstrual period date
    "last_followup_date": "datetime",
    "age_at_menopause": "numeric",
    "menopause_age_group": "categorical",  # <40, 40-45, 45-50, 50-55, >55
}

# Symptom severity fields for regression prediction
SYMPTOM_SEVERITY_FIELDS = {
    "hot_flash_severity": "numeric",  # 0-10 scale
    "mood_severity": "numeric",  # 0-10 scale
    "sleep_severity": "numeric",  # 0-10 scale
    "total_symptom_burden": "numeric",  # Combined score
    "symptom_frequency": "numeric",  # Days per month
    "symptom_duration": "numeric",  # Months experiencing symptoms
}

# Longitudinal tracking fields
LONGITUDINAL_FIELDS = {
    "visit_number": "numeric",
    "months_from_baseline": "numeric",
    "amh_decline_rate": "numeric",
    "fsh_trajectory": "numeric",
    "hormone_change_velocity": "numeric",
    "symptom_progression": "numeric",
}

# Comorbidity risk fields
COMORBIDITY_FIELDS = {
    "cvd_risk": "numeric",
    "bone_density_risk": "numeric",
    "cognitive_risk": "numeric",
    "diabetes_risk": "numeric",
    "osteoporosis_risk": "numeric",
}

# Data source tracking
METADATA_FIELDS = {
    "data_source": "categorical",
    "visit_number": "numeric",
    "sample_date": "datetime",
    "collection_method": "categorical",
    "study_phase": "categorical",
    "data_quality_score": "numeric",
}

# Complete canonical schema
CANONICAL_SCHEMA = {
    **CORE_FIELDS,
    **HORMONE_FIELDS,
    **VITAL_FIELDS,
    **SYMPTOM_FIELDS,
    **WEARABLE_FIELDS,
    **TARGET_FIELDS,
    **SURVIVAL_FIELDS,
    **SYMPTOM_SEVERITY_FIELDS,
    **LONGITUDINAL_FIELDS,
    **COMORBIDITY_FIELDS,
    **METADATA_FIELDS,
}

# Field categories for easier access
FIELD_CATEGORIES = {
    "core": CORE_FIELDS,
    "hormones": HORMONE_FIELDS,
    "vitals": VITAL_FIELDS,
    "symptoms": SYMPTOM_FIELDS,
    "wearables": WEARABLE_FIELDS,
    "target": TARGET_FIELDS,
    "survival": SURVIVAL_FIELDS,
    "symptom_severity": SYMPTOM_SEVERITY_FIELDS,
    "longitudinal": LONGITUDINAL_FIELDS,
    "comorbidity": COMORBIDITY_FIELDS,
    "metadata": METADATA_FIELDS,
}

# Data type mappings
DATA_TYPE_MAPPINGS = {
    "string": "object",
    "numeric": "float64",
    "categorical": "category",
    "boolean": "bool",
    "datetime": "datetime64[ns]",
}


def get_canonical_schema():
    """
    Return the complete canonical schema.

    Returns:
        dict: Canonical schema with field names and types
    """
    return CANONICAL_SCHEMA


def get_field_categories():
    """
    Return field categories for easier access.

    Returns:
        dict: Field categories
    """
    return FIELD_CATEGORIES


def get_data_type_mappings():
    """
    Return data type mappings for pandas.

    Returns:
        dict: Data type mappings
    """
    return DATA_TYPE_MAPPINGS


def validate_schema(df, schema=None):
    """
    Validate a DataFrame against the canonical schema.

    Args:
        df (pd.DataFrame): DataFrame to validate
        schema (dict): Schema to validate against (default: canonical)

    Returns:
        dict: Validation results
    """
    if schema is None:
        schema = CANONICAL_SCHEMA

    results = {
        "valid": True,
        "missing_fields": [],
        "extra_fields": [],
        "type_mismatches": [],
        "coverage": 0,
    }

    # Check for missing fields
    for field in schema.keys():
        if field not in df.columns:
            results["missing_fields"].append(field)

    # Check for extra fields
    for field in df.columns:
        if field not in schema.keys():
            results["extra_fields"].append(field)

    # Check type mismatches
    for field, expected_type in schema.items():
        if field in df.columns:
            actual_type = str(df[field].dtype)
            expected_pandas_type = DATA_TYPE_MAPPINGS.get(expected_type, expected_type)

            if expected_pandas_type != actual_type:
                results["type_mismatches"].append(
                    {"field": field, "expected": expected_pandas_type, "actual": actual_type}
                )

    # Calculate coverage
    total_fields = len(schema)
    present_fields = total_fields - len(results["missing_fields"])
    results["coverage"] = present_fields / total_fields if total_fields > 0 else 0

    # Overall validation
    results["valid"] = len(results["missing_fields"]) == 0 and len(results["type_mismatches"]) == 0

    return results


if __name__ == "__main__":
    # Print schema information
    print("Canonical Schema:")
    for category, fields in FIELD_CATEGORIES.items():
        print(f"\n{category.upper()}:")
        for field, dtype in fields.items():
            print(f"  {field}: {dtype}")

    print(f"\nTotal fields: {len(CANONICAL_SCHEMA)}")
    print(f"Data type mappings: {DATA_TYPE_MAPPINGS}")
