import pandas as pd


def load_synthea_data(data_path="data/raw/SYNTHEA/synthea_menopause_baseline.csv"):
    """
    Load SYNTHEA synthetic patient data with fallback paths.

    Args:
        data_path (str): Path to SYNTHEA CSV file

    Returns:
        pd.DataFrame: Loaded SYNTHEA data
    """
    print("Loading SYNTHEA data...")

    # Try multiple possible paths
    possible_paths = [
        data_path,
        "data/raw/SYNTHEA/synthea_menopause_baseline.csv",
        "data/raw/SYNTHEA/synthea_baseline.csv",
        "data/raw/SYNTHEA/baseline.csv",
        "data/raw/SYNTHEA/synthea.csv",
    ]

    df = None
    for path in possible_paths:
        try:
            print(f"Attempting to load: {path}")
            df = pd.read_csv(path)
            print(f"[OK] SYNTHEA data loaded from {path}: {df.shape}")
            break
        except FileNotFoundError:
            print(f"[SKIP] File not found: {path}")
            continue
        except Exception as e:
            print(f"[ERROR] Error loading {path}: {e}")
            continue

    if df is None:
        print("ERROR: No SYNTHEA files found in any expected location")
        print("Expected locations:")
        for path in possible_paths:
            print(f"  - {path}")
        return None

    print(f"Columns: {list(df.columns)}")

    # Add data source identifier
    df["data_source"] = "SYNTHEA"

    # Convert boolean columns explicitly
    print("Converting boolean columns...")
    bool_cols = ["hot_flashes", "mood_swings", "sleep_disturbance"]
    for col in bool_cols:
        if col in df.columns:
            # Handle different boolean representations
            if df[col].dtype == "object":
                # Convert string representations
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.lower()
                    .map(
                        {
                            "true": True,
                            "false": False,
                            "yes": True,
                            "no": False,
                            "1": True,
                            "0": False,
                            "y": True,
                            "n": False,
                        }
                    )
                )
            elif df[col].dtype in ["int64", "int32"]:
                # Convert integer representations
                df[col] = df[col].astype(bool)

            print(f"  Converted {col} to boolean")
        else:
            print(f"  Column {col} not found")

    # Validate against expected schema
    print("\nValidating against SYNTHEA schema...")
    schema = get_synthea_schema()
    expected_fields = schema["key_fields"]

    missing_fields = []
    present_fields = []

    for field in expected_fields:
        if field in df.columns:
            present_fields.append(field)
        else:
            missing_fields.append(field)

    print("Schema validation:")
    print(f"  Expected fields: {len(expected_fields)}")
    print(f"  Present fields: {len(present_fields)}")
    print(f"  Missing fields: {len(missing_fields)}")
    print(f"  Coverage: {len(present_fields) / len(expected_fields) * 100:.1f}%")

    if missing_fields:
        print(f"  Missing fields: {missing_fields}")
        print("  Note: Some fields may not exist in this SYNTHEA dataset version")

    # Basic data quality check with improved output
    print("\nMissing values per column:")
    missing_summary = df.isnull().sum().sort_values(ascending=False)
    if len(missing_summary) > 20:
        print("Top 20 columns with missing values:")
        print(missing_summary.head(20))
        print(f"... and {len(missing_summary) - 20} more columns")
    else:
        print(missing_summary)

    return df


def get_synthea_schema():
    """
    Return SYNTHEA data schema information.

    Returns:
        dict: Schema information for SYNTHEA data
    """
    return {
        "source": "SYNTHEA",
        "description": "Synthetic patient data for menopause baseline",
        "key_fields": [
            "participant_id",
            "age",
            "bmi",
            "fsh",
            "estradiol",
            "amh",
            "menopause_transition_stage",
            "smoking_status",
            "race_ethnicity",
            "hot_flashes",
            "mood_swings",
            "sleep_disturbance",
        ],
        "target_variable": "menopause_transition_stage",
        "data_types": {
            "participant_id": "string",
            "age": "numeric",
            "bmi": "numeric",
            "fsh": "numeric",
            "estradiol": "numeric",
            "amh": "numeric",
            "menopause_transition_stage": "categorical",
            "smoking_status": "categorical",
            "race_ethnicity": "categorical",
            "hot_flashes": "boolean",
            "mood_swings": "boolean",
            "sleep_disturbance": "boolean",
        },
    }


if __name__ == "__main__":
    # Test loading
    df = load_synthea_data()
    if df is not None:
        print("\nSYNTHEA Schema:")
        schema = get_synthea_schema()
        for key, value in schema.items():
            print(f"{key}: {value}")
