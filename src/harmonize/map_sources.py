"""
Source-specific field mappings to canonical schema.
"""

# SYNTHEA field mappings
SYNTHEA_MAPPINGS = {
    "participant_id": "participant_id",
    "age": "age",
    "bmi": "bmi",
    "fsh": "fsh",
    "estradiol": "estradiol",
    "amh": "amh",
    "menopause_transition_stage": "menopause_stage",
    "smoking_status": "smoking_status",
    "race_ethnicity": "race_ethnicity",
    "hot_flashes": "hot_flashes",
    "mood_swings": "mood_swings",
    "sleep_disturbance": "sleep_disturbance",
    "amh_decline_rate": "amh_decline_rate",
    "afc": "afc",
    "inhibin_b": "inhibin_b",
    "menstrual_cycle_status": "menstrual_cycle_status",
    "mothers_anm": "mothers_anm",
    "sample_storage_time": "sample_storage_time",
    "venipuncture_time": "venipuncture_time",
}

# UKBB field mappings
UKBB_MAPPINGS = {
    "participant_id": "participant_id",
    "age": "age",
    "bmi": "bmi",
    "fsh": "fsh",
    "estradiol": "estradiol",
    "testosterone": "testosterone",
    "menopause_status": "menopause_stage",
    "smoking": "smoking_status",
    "ethnicity": "race_ethnicity",
    "height": "height",
    "weight": "weight",
    "systolic_bp": "systolic_bp",
    "diastolic_bp": "diastolic_bp",
    "alcohol_frequency": "alcohol_frequency",
    "physical_activity": "physical_activity",
    "education": "education",
}

# NHANES field mappings
NHANES_MAPPINGS = {
    "SEQN": "participant_id",
    "RIDAGEYR": "age",
    "BMXBMI": "bmi",
    "LBXFSH": "fsh",
    "LBXEST": "estradiol",
    "LBXAMH": "amh",
    "LBXTSH": "tsh",
    "LBXTT3": "testosterone",
    "RIDRETH1": "race_ethnicity",
    "SMQ020": "smoking_status",
    "BMXHT": "height",
    "BMXWT": "weight",
    "BPXSY1": "systolic_bp",
    "BPXDI1": "diastolic_bp",
    "ALQ110": "alcohol_frequency",
    "PAQ605": "physical_activity",
    "DMDEDUC2": "education",
    "DPQ010": "depression_score",
    "DPQ020": "anxiety_score",
    "SLD010H": "sleep_quality",
    "SLD012": "sleep_disturbance",
}

# SWAN field mappings
SWAN_MAPPINGS = {
    "IDNUM": "participant_id",
    "AGE": "age",
    "BMI": "bmi",
    "FSH": "fsh",
    "ESTRADIOL": "estradiol",
    "AMH": "amh",
    "INHIBIN_B": "inhibin_b",
    "TESTOSTERONE": "testosterone",
    "MENOPAUSE_STATUS": "menopause_stage",
    "SMOKING": "smoking_status",
    "RACE": "race_ethnicity",
    "EDUCATION": "education",
    "HOT_FLASHES": "hot_flashes",
    "MOOD_SWINGS": "mood_swings",
    "SLEEP_DISTURBANCE": "sleep_disturbance",
    "DEPRESSION_SCORE": "depression_score",
    "ANXIETY_SCORE": "anxiety_score",
    "STRESS_SCORE": "stress_score",
    "PHYSICAL_ACTIVITY": "physical_activity",
    "ALCOHOL_FREQUENCY": "alcohol_frequency",
    "DIET_QUALITY": "diet_quality",
}

# Wearables field mappings
WEARABLES_MAPPINGS = {
    "SEQN": "participant_id",
    "PAXSTEP": "steps_day",
    "PAXSED": "sedentary_minutes",
    "PAXLIG": "light_minutes",
    "PAXMOD": "moderate_minutes",
    "PAXVIG": "vigorous_minutes",
    "PAXHR": "avg_heart_rate",
    "PAXHRVM": "hrv_proxy",
    "WEARABLE_STEPS_MEAN": "steps_day",
    "WEARABLE_SEDENTARY_MEAN": "sedentary_minutes",
    "WEARABLE_LIGHT_MEAN": "light_minutes",
    "WEARABLE_MODERATE_MEAN": "moderate_minutes",
    "WEARABLE_VIGOROUS_MEAN": "vigorous_minutes",
}

# Value mappings for categorical variables
VALUE_MAPPINGS = {
    "smoking_status": {
        "SYNTHEA": {"Never": "Never", "Former": "Former", "Current": "Current"},
        "UKBB": {0: "Never", 1: "Former", 2: "Current"},
        "NHANES": {1: "Never", 2: "Former", 3: "Current"},
        "SWAN": {"Never": "Never", "Former": "Former", "Current": "Current"},
    },
    "race_ethnicity": {
        "SYNTHEA": {
            "White": "White",
            "Black": "Black",
            "Asian": "Asian",
            "Hispanic": "Hispanic",
            "Other": "Other",
        },
        "UKBB": {1: "White", 2: "Black", 3: "Asian", 4: "Hispanic", 5: "Other"},
        "NHANES": {1: "White", 2: "Black", 3: "Asian", 4: "Hispanic", 5: "Other"},
        "SWAN": {
            "White": "White",
            "Black": "Black",
            "Asian": "Asian",
            "Hispanic": "Hispanic",
            "Other": "Other",
        },
    },
    "menopause_stage": {
        "SYNTHEA": {"Early": "Early", "Late": "Late", "Post": "Post"},
        "UKBB": {0: "Early", 1: "Late", 2: "Post"},
        "NHANES": {1: "Early", 2: "Late", 3: "Post"},
        "SWAN": {"Early": "Early", "Late": "Late", "Post": "Post"},
    },
}

# Unit conversions
UNIT_CONVERSIONS = {
    "height": {"cm_to_m": lambda x: x / 100, "inches_to_m": lambda x: x * 0.0254},
    "weight": {"kg_to_lbs": lambda x: x * 2.20462, "lbs_to_kg": lambda x: x / 2.20462},
    "fsh": {"mIU_L_to_mIU_mL": lambda x: x / 1000, "mIU_mL_to_mIU_L": lambda x: x * 1000},
    "estradiol": {"pg_mL_to_pmol_L": lambda x: x * 3.671, "pmol_L_to_pg_mL": lambda x: x / 3.671},
}


def get_source_mappings(source):
    """
    Get field mappings for a specific data source.

    Args:
        source (str): Data source name

    Returns:
        dict: Field mappings for the source
    """
    # Normalize source name to uppercase for consistent lookup
    source = source.strip().upper()

    mapping_dict = {
        "SYNTHEA": SYNTHEA_MAPPINGS,
        "UKBB": UKBB_MAPPINGS,
        "NHANES": NHANES_MAPPINGS,
        "SWAN": SWAN_MAPPINGS,
        "WEARABLES": WEARABLES_MAPPINGS,  # Also handle "Wearables" -> "WEARABLES"
    }

    return mapping_dict.get(source, {})


def get_value_mappings(field, source):
    """
    Get value mappings for a specific field and source.

    Args:
        field (str): Field name
        source (str): Data source name

    Returns:
        dict: Value mappings for the field and source
    """
    # Normalize source name to uppercase for consistent lookup
    source = source.strip().upper()

    if field in VALUE_MAPPINGS and source in VALUE_MAPPINGS[field]:
        return VALUE_MAPPINGS[field][source]
    return {}


def get_unit_conversions(field, from_unit, to_unit):
    """
    Get unit conversion function for a field.

    Args:
        field (str): Field name
        from_unit (str): Source unit
        to_unit (str): Target unit

    Returns:
        function: Conversion function
    """
    if field in UNIT_CONVERSIONS:
        conversion_key = f"{from_unit}_to_{to_unit}"
        if conversion_key in UNIT_CONVERSIONS[field]:
            return UNIT_CONVERSIONS[field][conversion_key]
        else:
            print(f"⚠️ No conversion defined for {field} from {from_unit} to {to_unit}")
    return None


def apply_field_mapping(df, source):
    """
    Apply field mappings to a DataFrame.

    Args:
        df (pd.DataFrame): Source DataFrame
        source (str): Data source name

    Returns:
        pd.DataFrame: Mapped DataFrame
    """
    mappings = get_source_mappings(source)
    mapped_df = df.copy()

    # Check for duplicate canonical names
    canonical_names = list(mappings.values())
    if len(canonical_names) != len(set(canonical_names)):
        print(f"⚠️ Warning: Duplicate canonical names in {source} mappings")

    # Rename columns
    for source_field, canonical_field in mappings.items():
        if source_field in mapped_df.columns:
            mapped_df = mapped_df.rename(columns={source_field: canonical_field})

    return mapped_df


def apply_value_mapping(df, source):
    """
    Apply value mappings to a DataFrame.

    Note: Must be applied after apply_field_mapping() to ensure canonical field names exist.

    Args:
        df (pd.DataFrame): Source DataFrame
        source (str): Data source name

    Returns:
        pd.DataFrame: Mapped DataFrame
    """
    # Normalize source name to uppercase for consistent lookup
    source = source.strip().upper()
    mapped_df = df.copy()

    for field, source_mappings in VALUE_MAPPINGS.items():
        if field in mapped_df.columns and source in source_mappings:
            field_mappings = source_mappings[source]
            # Safe fallback: keep original values for unmapped categories
            mapped_df[field] = mapped_df[field].map(field_mappings).fillna(mapped_df[field])

    return mapped_df


def apply_unit_conversions(df, source):
    """
    Apply unit conversions to a DataFrame.

    Note: Currently applies only NHANES height conversion (cm to meters).
    Other conversion functions are defined in UNIT_CONVERSIONS but not yet implemented.

    Args:
        df (pd.DataFrame): Source DataFrame
        source (str): Data source name

    Returns:
        pd.DataFrame: Converted DataFrame
    """
    # Normalize source name to uppercase for consistent lookup
    source = source.strip().upper()
    converted_df = df.copy()

    # Apply known conversions based on source
    if source == "NHANES":
        # NHANES height is in cm, convert to meters
        if "height" in converted_df.columns:
            converted_df["height"] = converted_df["height"] / 100

    # Add more source-specific conversions as needed

    return converted_df


if __name__ == "__main__":
    # Print mapping information
    print("Source Mappings:")
    for source in ["SYNTHEA", "UKBB", "NHANES", "SWAN", "Wearables"]:
        mappings = get_source_mappings(source)
        print(f"\n{source}:")
        for source_field, canonical_field in mappings.items():
            print(f"  {source_field} -> {canonical_field}")

    print("\nValue Mappings:")
    for field, sources in VALUE_MAPPINGS.items():
        print(f"\n{field}:")
        for source, mappings in sources.items():
            print(f"  {source}: {mappings}")

    print("\nUnit Conversions:")
    for field, conversions in UNIT_CONVERSIONS.items():
        print(f"\n{field}:")
        for conversion, func in conversions.items():
            print(f"  {conversion}: {func.__name__}")

    print()  # Add final newline
