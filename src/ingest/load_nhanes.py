import os
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")


def load_nhanes_demographics(data_path="data/raw/NHANES/"):
    """
    Load NHANES Demographics data from P_DEMO.xpt.

    Args:
        data_path (str): Path to NHANES data directory

    Returns:
        pd.DataFrame: Demographics data
    """
    try:
        # Look for demographics XPT file in Demographics subdirectory
        demo_files = list(Path(data_path).glob("Demographics/*DEMO*.xpt"))
        if not demo_files:
            print("No demographics XPT file found")
            return None

        print(f"Attempting to load: {demo_files[0]}")
        df = pd.read_sas(demo_files[0])
        print(f"NHANES Demographics loaded: {df.shape}")

        # Save intermediate CSV for easier processing
        output_path = "data/processed/NHANES/demographics.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Saved demographics to {output_path}")

        return df

    except Exception as e:
        print(
            f"Error loading NHANES demographics from {demo_files[0] if 'demo_files' in locals() else 'unknown file'}: {e}"
        )
        print("This may be due to unsupported SAS XPT format or file corruption")
        return None


def load_nhanes_lab(data_path="data/raw/NHANES/"):
    """
    Load NHANES Laboratory data (hormones) from multiple lab files.

    Args:
        data_path (str): Path to NHANES data directory

    Returns:
        pd.DataFrame: Combined laboratory data
    """
    try:
        # Look for specific hormone-related lab files in Laboratory subdirectory
        lab_files = []
        lab_files.extend(
            list(Path(data_path).glob("Laboratory/*BIOPRO*.xpt"))
        )  # Biochemistry profile
        lab_files.extend(
            list(Path(data_path).glob("Laboratory/*FERTIN*.xpt"))
        )  # Fertility hormones
        lab_files.extend(list(Path(data_path).glob("Laboratory/*TST*.xpt")))  # Testosterone
        lab_files.extend(
            list(Path(data_path).glob("Laboratory/*ALB_CR*.xpt"))
        )  # Albumin/Creatinine
        lab_files.extend(list(Path(data_path).glob("Laboratory/*BPXO*.xpt")))  # Blood pressure
        lab_files.extend(list(Path(data_path).glob("Laboratory/*BMX*.xpt")))  # Body measures

        if not lab_files:
            print("No laboratory XPT files found")
            return None

        # Load and combine all lab files
        lab_dfs = []
        skipped_files = []
        for lab_file in lab_files:
            try:
                print(f"Attempting to load: {lab_file.name}")
                df = pd.read_sas(lab_file)
                lab_dfs.append(df)
                print(f"✓ Loaded {lab_file.name}: {df.shape}")
            except Exception as e:
                print(f"✗ Error loading {lab_file.name}: {e}")
                print("  This may be due to unsupported SAS XPT format or file corruption")
                skipped_files.append(lab_file.name)
                continue

        if skipped_files:
            print(f"Skipped {len(skipped_files)} files due to loading errors: {skipped_files}")

        if not lab_dfs:
            print("No laboratory files could be loaded")
            return None

        # Combine all lab data
        combined_df = lab_dfs[0]
        for df in lab_dfs[1:]:
            # Explicitly use SEQN as merge key
            if "SEQN" in combined_df.columns and "SEQN" in df.columns:
                combined_df = combined_df.merge(df, on="SEQN", how="outer")
                print(f"After merging {df.shape}: {combined_df.shape}")
            else:
                print("Warning: SEQN not found in both datasets, skipping merge")
                print(f"Combined columns: {list(combined_df.columns)}")
                print(f"New dataset columns: {list(df.columns)}")

        # Save intermediate CSV
        output_path = "data/processed/NHANES/laboratory.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        combined_df.to_csv(output_path, index=False)
        print(f"Saved laboratory data to {output_path}")

        return combined_df

    except Exception as e:
        print(f"Error loading NHANES lab data: {e}")
        return None


def load_nhanes_questionnaire(data_path="data/raw/NHANES/"):
    """
    Load NHANES Questionnaire data (DPQ, sleep, lifestyle, reproductive health).

    Args:
        data_path (str): Path to NHANES data directory

    Returns:
        pd.DataFrame: Combined questionnaire data
    """
    try:
        # Look for all relevant questionnaire files in Questionnaire subdirectory
        q_files = []
        q_files.extend(
            list(Path(data_path).glob("Questionnaire/*DPQ*.xpt"))
        )  # Depression questionnaire
        q_files.extend(list(Path(data_path).glob("Questionnaire/*SLQ*.xpt")))  # Sleep questionnaire
        q_files.extend(
            list(Path(data_path).glob("Questionnaire/*SMQ*.xpt"))
        )  # Smoking questionnaire
        q_files.extend(
            list(Path(data_path).glob("Questionnaire/*ALQ*.xpt"))
        )  # Alcohol questionnaire
        q_files.extend(
            list(Path(data_path).glob("Questionnaire/*PAQ*.xpt"))
        )  # Physical activity questionnaire
        q_files.extend(
            list(Path(data_path).glob("Questionnaire/*RHQ*.xpt"))
        )  # Reproductive health questionnaire
        q_files.extend(
            list(Path(data_path).glob("Questionnaire/*WHQ*.xpt"))
        )  # Women's health questionnaire
        q_files.extend(
            list(Path(data_path).glob("Questionnaire/*OSQ*.xpt"))
        )  # Osteoporosis questionnaire
        q_files.extend(
            list(Path(data_path).glob("Questionnaire/*MCQ*.xpt"))
        )  # Medical conditions questionnaire

        if not q_files:
            print("No questionnaire XPT files found")
            return None

        # Load and combine all questionnaire files
        quest_dfs = []
        for q_file in q_files:
            try:
                df = pd.read_sas(q_file)
                quest_dfs.append(df)
                print(f"Loaded {q_file.name}: {df.shape}")
            except Exception as e:
                print(f"Error loading {q_file.name}: {e}")
                continue

        if not quest_dfs:
            print("No questionnaire files could be loaded")
            return None

        # Combine all questionnaire data
        combined_df = quest_dfs[0]
        for df in quest_dfs[1:]:
            # Explicitly use SEQN as merge key
            if "SEQN" in combined_df.columns and "SEQN" in df.columns:
                combined_df = combined_df.merge(df, on="SEQN", how="outer")
                print(f"After merging {df.shape}: {combined_df.shape}")
            else:
                print("Warning: SEQN not found in both datasets, skipping merge")
                print(f"Combined columns: {list(combined_df.columns)}")
                print(f"New dataset columns: {list(df.columns)}")

        # Save intermediate CSV
        output_path = "data/processed/NHANES/questionnaires.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        combined_df.to_csv(output_path, index=False)
        print(f"Saved questionnaire data to {output_path}")

        return combined_df

    except Exception as e:
        print(f"Error loading NHANES questionnaire data: {e}")
        return None


def load_nhanes_dietary(data_path="data/raw/NHANES/"):
    """
    Load NHANES Dietary data from dietary recall files.

    Args:
        data_path (str): Path to NHANES data directory

    Returns:
        pd.DataFrame: Dietary data
    """
    try:
        # Look for dietary XPT files in Dietary subdirectory
        diet_files = list(Path(data_path).glob("Dietary/*DR*.xpt"))  # Dietary recall
        if not diet_files:
            print("No dietary XPT files found")
            return None

        # Load and combine dietary files
        diet_dfs = []
        for diet_file in diet_files:
            try:
                df = pd.read_sas(diet_file)
                diet_dfs.append(df)
                print(f"Loaded {diet_file.name}: {df.shape}")
            except Exception as e:
                print(f"Error loading {diet_file.name}: {e}")
                continue

        if not diet_dfs:
            print("No dietary files could be loaded")
            return None

        # Combine dietary data
        combined_df = diet_dfs[0]
        for df in diet_dfs[1:]:
            # Explicitly use SEQN as merge key
            if "SEQN" in combined_df.columns and "SEQN" in df.columns:
                combined_df = combined_df.merge(df, on="SEQN", how="outer")
                print(f"After merging {df.shape}: {combined_df.shape}")
            else:
                print("Warning: SEQN not found in both datasets, skipping merge")
                print(f"Combined columns: {list(combined_df.columns)}")
                print(f"New dataset columns: {list(df.columns)}")

        # Save intermediate CSV
        output_path = "data/processed/NHANES/dietary.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        combined_df.to_csv(output_path, index=False)
        print(f"Saved dietary data to {output_path}")

        return combined_df

    except Exception as e:
        print(f"Error loading NHANES dietary data: {e}")
        return None


def load_nhanes_data(data_path="data/raw/NHANES/"):
    """
    Load all available NHANES data and combine.

    Args:
        data_path (str): Path to NHANES data directory

    Returns:
        pd.DataFrame: Combined NHANES data
    """
    print("Loading NHANES data...")

    # Load different components
    demo_df = load_nhanes_demographics(data_path)
    lab_df = load_nhanes_lab(data_path)
    quest_df = load_nhanes_questionnaire(data_path)
    diet_df = load_nhanes_dietary(data_path)

    # Start with demographics as base
    if demo_df is not None:
        combined_df = demo_df.copy()
        print(f"Starting with demographics: {combined_df.shape}")

        # Merge other components if available - use SEQN explicitly
        if lab_df is not None:
            if "SEQN" in combined_df.columns and "SEQN" in lab_df.columns:
                combined_df = combined_df.merge(lab_df, on="SEQN", how="left")
                print(f"After merging lab data: {combined_df.shape}")
            else:
                print("Warning: SEQN not found in demographics or lab data, skipping lab merge")

        if quest_df is not None:
            if "SEQN" in combined_df.columns and "SEQN" in quest_df.columns:
                combined_df = combined_df.merge(quest_df, on="SEQN", how="left")
                print(f"After merging questionnaire data: {combined_df.shape}")
            else:
                print(
                    "Warning: SEQN not found in demographics or questionnaire data, skipping questionnaire merge"
                )

        if diet_df is not None:
            if "SEQN" in combined_df.columns and "SEQN" in diet_df.columns:
                combined_df = combined_df.merge(diet_df, on="SEQN", how="left")
                print(f"After merging dietary data: {combined_df.shape}")
            else:
                print(
                    "Warning: SEQN not found in demographics or dietary data, skipping dietary merge"
                )

        # Check for and handle duplicates in SEQN
        if "SEQN" in combined_df.columns:
            duplicate_count = combined_df["SEQN"].duplicated().sum()
            if duplicate_count > 0:
                print(f"Warning: Found {duplicate_count} duplicate SEQN values")
                print("Removing duplicates (keeping first occurrence)")
                combined_df = combined_df.drop_duplicates(subset=["SEQN"], keep="first")
                print(f"After removing duplicates: {combined_df.shape}")

        # Add data source identifier
        combined_df["data_source"] = "NHANES"

        # Save final combined dataset
        output_path = "data/processed/NHANES/nhanes_combined.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        combined_df.to_csv(output_path, index=False)
        print(f"Saved combined NHANES data to {output_path}")

        print(f"Final NHANES data shape: {combined_df.shape}")
        print("Missing values per column:")
        missing_summary = combined_df.isnull().sum().sort_values(ascending=False)
        print(missing_summary)

        # Add basic missing value imputation for critical columns
        print("\nApplying basic missing value imputation...")

        # Impute numeric columns with median
        numeric_cols = combined_df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            if combined_df[col].isnull().sum() > 0:
                median_val = combined_df[col].median()
                combined_df[col] = combined_df[col].fillna(median_val)
                print(f"  Imputed {col} with median: {median_val:.2f}")

        # Impute categorical columns with mode
        categorical_cols = combined_df.select_dtypes(include=["object", "category"]).columns
        for col in categorical_cols:
            if combined_df[col].isnull().sum() > 0:
                mode_val = (
                    combined_df[col].mode().iloc[0]
                    if not combined_df[col].mode().empty
                    else "Unknown"
                )
                combined_df[col] = combined_df[col].fillna(mode_val)
                print(f"  Imputed {col} with mode: {mode_val}")

        print(f"After imputation - Missing values: {combined_df.isnull().sum().sum()}")

        # Validate columns against expected schema
        print("\n" + "=" * 50)
        validate_nhanes_columns(combined_df)
        print("=" * 50)

        return combined_df
    else:
        print("No NHANES data could be loaded")
        return None


def validate_nhanes_columns(df):
    """
    Validate that expected NHANES columns exist in the dataset.

    Args:
        df (pd.DataFrame): NHANES dataset to validate

    Returns:
        dict: Validation results
    """
    schema = get_nhanes_schema()
    expected_fields = schema["key_fields"]

    missing_fields = []
    present_fields = []

    for field in expected_fields:
        if field in df.columns:
            present_fields.append(field)
        else:
            missing_fields.append(field)

    validation_result = {
        "total_expected": len(expected_fields),
        "present": len(present_fields),
        "missing": len(missing_fields),
        "missing_fields": missing_fields,
        "present_fields": present_fields,
        "coverage": len(present_fields) / len(expected_fields) * 100,
    }

    print("NHANES Column Validation:")
    print(f"  Expected fields: {validation_result['total_expected']}")
    print(f"  Present fields: {validation_result['present']}")
    print(f"  Missing fields: {validation_result['missing']}")
    print(f"  Coverage: {validation_result['coverage']:.1f}%")

    if missing_fields:
        print(f"  Missing fields: {missing_fields}")
        print("  Note: Some fields may not exist in all NHANES cycles")

    return validation_result


def get_nhanes_schema():
    """
    Return NHANES data schema information.

    Returns:
        dict: Schema information for NHANES data
    """
    return {
        "source": "NHANES",
        "description": "National Health and Nutrition Examination Survey data",
        "key_fields": [
            "SEQN",
            "RIDAGEYR",
            "BMXBMI",
            "LBXFSH",
            "LBXEST",
            "LBXAMH",
            "LBXTSH",
            "LBXTT3",  # Testosterone (may not exist in all cycles)
            "DPQ010",
            "DPQ020",
            "DPQ030",
            "DPQ040",
            "DPQ050",  # Depression questions
            "SLD010H",
            "SLD012",  # Sleep questions
            "ALQ101",
            "ALQ110",
            "ALQ120U",  # Alcohol questions
            "PAQ605",
            "PAQ620",
            "PAQ635",
            "PAQ650",  # Physical activity
            "DMDEDUC2",
            "DMDMARTL",
            "DMDHHSIZ",  # Demographics
            "RIDRETH1",  # Race/ethnicity
            "SMQ020",  # Smoking
            "BMXHT",  # Height
            "BMXWT",  # Weight
            "BPXSY1",  # Systolic BP
            "BPXDI1",  # Diastolic BP
            "RHQ010",  # Reproductive health
            "RHQ020",  # Menstrual status
            "RHQ030",  # Last period
        ],
        "target_variable": "menopause_status",  # Will need to be derived
        "survival_targets": [
            "time_to_menopause_months",
            "menopause_event",
            "fmp_date",
            "last_followup_date",
        ],
        "symptom_targets": ["hot_flash_severity", "mood_severity", "sleep_severity"],
        "data_types": {
            "SEQN": "string",
            "RIDAGEYR": "numeric",
            "BMXBMI": "numeric",
            "LBXFSH": "numeric",
            "LBXEST": "numeric",
            "LBXAMH": "numeric",
            "LBXTSH": "numeric",
            "LBXTT3": "numeric",
            "DPQ010": "categorical",
            "DPQ020": "categorical",
            "DPQ030": "categorical",
            "DPQ040": "categorical",
            "DPQ050": "categorical",
            "SLD010H": "numeric",
            "SLD012": "categorical",
            "ALQ101": "categorical",
            "ALQ110": "numeric",
            "ALQ120U": "categorical",
            "PAQ605": "categorical",
            "PAQ620": "categorical",
            "PAQ635": "categorical",
            "PAQ650": "categorical",
            "DMDEDUC2": "categorical",
            "DMDMARTL": "categorical",
            "DMDHHSIZ": "numeric",
            "RIDRETH1": "categorical",
            "SMQ020": "categorical",
            "BMXHT": "numeric",
            "BMXWT": "numeric",
            "BPXSY1": "numeric",
            "BPXDI1": "numeric",
            "RHQ010": "categorical",
            "RHQ020": "categorical",
            "RHQ030": "categorical",
        },
    }


if __name__ == "__main__":
    # Test loading
    df = load_nhanes_data()
    if df is not None:
        print("\nNHANES Schema:")
        schema = get_nhanes_schema()
        for key, value in schema.items():
            print(f"{key}: {value}")
