import pandas as pd


def load_ukbb_data(data_path="data/raw/UKBB/ukb_synthetic_baseline.csv"):
    """
    Load UK Biobank synthetic data with fallback paths and data type conversion.

    Args:
        data_path (str): Path to UKBB CSV file

    Returns:
        pd.DataFrame: Loaded UKBB data
    """
    print("Loading UKBB data...")

    # Try multiple possible paths
    possible_paths = [
        data_path,
        "data/raw/UKBB/ukb_synthetic_baseline.csv",
        "data/raw/UKBB/ukb_baseline.csv",
        "data/raw/UKBB/baseline.csv",
        "data/raw/UKBB/ukb.csv",
    ]

    df = None
    for path in possible_paths:
        try:
            print(f"Attempting to load: {path}")
            df = pd.read_csv(path)
            print(f"[OK] UKBB data loaded from {path}: {df.shape}")
            break
        except FileNotFoundError:
            print(f"[SKIP] File not found: {path}")
            continue
        except Exception as e:
            print(f"[ERROR] Error loading {path}: {e}")
            continue

    if df is None:
        print("ERROR: No UKBB files found in any expected location")
        print("Expected locations:")
        for path in possible_paths:
            print(f"  - {path}")
        return None

    print(f"Columns: {list(df.columns)}")

    # Add data source identifier
    df["data_source"] = "UKBB"

    # Convert data types according to schema
    print("\nConverting data types...")
    schema = get_ukbb_schema()
    data_types = schema["data_types"]

    # Convert numeric columns
    numeric_cols = [col for col, dtype in data_types.items() if dtype == "numeric"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            print(f"  Converted {col} to numeric")
        else:
            print(f"  Column {col} not found")

    # Convert categorical columns
    categorical_cols = [col for col, dtype in data_types.items() if dtype == "categorical"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")
            print(f"  Converted {col} to categorical")
        else:
            print(f"  Column {col} not found")

    # Convert string columns
    string_cols = [col for col, dtype in data_types.items() if dtype == "string"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype("string")
            print(f"  Converted {col} to string")
        else:
            print(f"  Column {col} not found")

    # Validate against expected schema
    print("\nValidating against UKBB schema...")
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
        print("  Note: Some fields may not exist in this UKBB dataset version")

    # Basic data quality check with improved output
    print("\nMissing values per column:")
    missing_summary = df.isnull().sum().sort_values(ascending=False)
    if len(missing_summary) > 20:
        print("Top 20 columns with missing values:")
        print(missing_summary.head(20))
        print(f"... and {len(missing_summary) - 20} more columns")
    else:
        print(missing_summary)

    # Memory management for large datasets
    if len(df) > 10000:
        print(
            f"\nLarge dataset detected ({len(df)} rows). Consider sampling for memory efficiency."
        )
        print("Note: Full dataset will be returned, but sampling may be needed downstream.")

    return df


def sample_ukbb_data(df, target_size=None, random_state=42):
    """
    Sample UKBB data for memory efficiency while preserving data distribution.

    Args:
        df (pd.DataFrame): Full UKBB dataset
        target_size (int): Target number of rows to sample
        random_state (int): Random seed for reproducibility

    Returns:
        pd.DataFrame: Sampled dataset
    """
    if target_size is None or len(df) <= target_size:
        print(f"Using all {len(df)} UKBB rows (no sampling limit)")
        return df

    print(f"Sampling {len(df)} rows to {target_size} for memory efficiency...")

    # Stratified sampling by menopause_status if available
    if "menopause_status" in df.columns:
        try:
            # Use stratified sampling to preserve class distribution
            from sklearn.model_selection import train_test_split

            df_sampled, _ = train_test_split(
                df,
                train_size=target_size,
                stratify=df["menopause_status"],
                random_state=random_state,
            )
            print(f"Stratified sampling completed: {len(df_sampled)} rows")
        except Exception as e:
            print(f"Stratified sampling failed ({e}), using random sampling")
            df_sampled = df.sample(n=target_size, random_state=random_state)
    else:
        # Random sampling if no stratification column
        df_sampled = df.sample(n=target_size, random_state=random_state)
        print(f"Random sampling completed: {len(df_sampled)} rows")

    return df_sampled


def get_ukbb_schema():
    """
    Return UKBB data schema information.

    Returns:
        dict: Schema information for UKBB data
    """
    return {
        "source": "UKBB",
        "description": "Synthetic UK Biobank data for menopause baseline",
        "key_fields": [
            "participant_id",
            "age",
            "bmi",
            "fsh",
            "estradiol",
            "testosterone",
            "menopause_status",
            "smoking",
            "ethnicity",
            "height",
            "weight",
            "systolic_bp",
            "diastolic_bp",
            "alcohol_frequency",
            "physical_activity",
            "education",
        ],
        "target_variable": "menopause_status",
        "data_types": {
            "participant_id": "string",
            "age": "numeric",
            "bmi": "numeric",
            "fsh": "numeric",
            "estradiol": "numeric",
            "testosterone": "numeric",
            "menopause_status": "categorical",
            "smoking": "categorical",
            "ethnicity": "categorical",
            "height": "numeric",
            "weight": "numeric",
            "systolic_bp": "numeric",
            "diastolic_bp": "numeric",
            "alcohol_frequency": "numeric",
            "physical_activity": "numeric",
            "education": "numeric",
        },
    }


if __name__ == "__main__":
    # Test loading
    df = load_ukbb_data()
    if df is not None:
        print("\nUKBB Schema:")
        schema = get_ukbb_schema()
        for key, value in schema.items():
            print(f"{key}: {value}")

        # Test sampling if dataset is large
        if len(df) > 1000:
            print(f"\nTesting sampling from {len(df)} rows...")
            df_sampled = sample_ukbb_data(df, target_size=None)  # No sampling limit
            print(f"Sampled dataset shape: {df_sampled.shape}")
