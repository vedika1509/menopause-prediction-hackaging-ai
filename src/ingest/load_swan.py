import os
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")


def load_swan_baseline(data_path="data/raw/SWAN/"):
    """
    Load SWAN baseline data from Stata/CSV files.

    Args:
        data_path (str): Path to SWAN data directory

    Returns:
        pd.DataFrame: SWAN baseline data
    """
    try:
        # Look for baseline files with more specific patterns
        baseline_files = []

        # Primary: Look in specific SWAN directories
        baseline_files.extend(list(Path(data_path).glob("extracted/*/DS0001/*.dta")))
        baseline_files.extend(list(Path(data_path).glob("extracted/*/DS0001/*.csv")))

        # Secondary: Look for baseline-specific files (more restrictive)
        baseline_files.extend(list(Path(data_path).glob("*baseline*.dta")))
        baseline_files.extend(list(Path(data_path).glob("*baseline*.csv")))
        baseline_files.extend(list(Path(data_path).glob("*BL*.dta")))
        baseline_files.extend(list(Path(data_path).glob("*BL*.csv")))

        # Tertiary: Look for visit 1 files
        baseline_files.extend(list(Path(data_path).glob("*visit1*.dta")))
        baseline_files.extend(list(Path(data_path).glob("*visit1*.csv")))

        # Remove duplicates and filter by file extension
        baseline_files = list(set(baseline_files))
        baseline_files = [f for f in baseline_files if f.suffix.lower() in [".dta", ".csv"]]

        print(f"Found {len(baseline_files)} potential baseline files")

        if not baseline_files:
            print("No SWAN baseline files found")
            return None

        # Try to load the first available file
        for file_path in baseline_files:
            try:
                if file_path.suffix.lower() == ".dta":
                    df = pd.read_stata(file_path)
                elif file_path.suffix.lower() == ".csv":
                    df = pd.read_csv(file_path)
                else:
                    continue

                print(f"SWAN baseline data loaded from {file_path.name}: {df.shape}")

                # Save intermediate CSV
                output_path = "data/processed/SWAN/baseline.csv"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                df.to_csv(output_path, index=False)
                print(f"Saved baseline data to {output_path}")

                return df

            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
                continue

        print("No SWAN baseline files could be loaded")
        return None

    except Exception as e:
        print(f"Error loading SWAN baseline data: {e}")
        return None


def load_swan_visits(data_path="data/raw/SWAN/"):
    """
    Load SWAN visit data from all longitudinal visits.

    Args:
        data_path (str): Path to SWAN data directory

    Returns:
        pd.DataFrame: Combined SWAN visit data
    """
    try:
        # Look for visit files in extracted folders
        visit_files = []
        visit_files.extend(list(Path(data_path).glob("extracted/*/DS0001/*.dta")))
        visit_files.extend(list(Path(data_path).glob("extracted/*/DS0001/*.csv")))
        visit_files.extend(list(Path(data_path).glob("*visit*")))
        visit_files.extend(list(Path(data_path).glob("*V*")))

        if not visit_files:
            print("No SWAN visit files found")
            return None

        # Load and combine all visit files
        visit_dfs = []
        for file_path in visit_files:
            try:
                if file_path.suffix.lower() == ".dta":
                    df = pd.read_stata(file_path)
                elif file_path.suffix.lower() == ".csv":
                    df = pd.read_csv(file_path)
                else:
                    continue

                # Add visit number if not present
                if "visit_number" not in df.columns:
                    # Try to extract visit number from filename
                    if "visit" in file_path.name.lower():
                        visit_num = file_path.name.lower().split("visit")[1].split("_")[0]
                        try:
                            df["visit_number"] = int(visit_num)
                        except:
                            df["visit_number"] = 1
                    else:
                        df["visit_number"] = 1

                visit_dfs.append(df)
                print(f"SWAN visit data loaded from {file_path.name}: {df.shape}")

            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
                continue

        if not visit_dfs:
            print("No SWAN visit files could be loaded")
            return None

        # Combine all visit data
        combined_df = pd.concat(visit_dfs, ignore_index=True)

        # Save intermediate CSV
        output_path = "data/processed/SWAN/visits_combined.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        combined_df.to_csv(output_path, index=False)
        print(f"Saved combined visit data to {output_path}")

        return combined_df

    except Exception as e:
        print(f"Error loading SWAN visit data: {e}")
        return None


def load_swan_hormones(data_path="data/raw/SWAN/"):
    """
    Load SWAN hormone data from Stata/CSV files.

    Args:
        data_path (str): Path to SWAN data directory

    Returns:
        pd.DataFrame: SWAN hormone data
    """
    try:
        # Look for hormone files
        hormone_files = list(Path(data_path).glob("*hormone*"))
        hormone_files.extend(list(Path(data_path).glob("*lab*")))
        hormone_files.extend(list(Path(data_path).glob("*blood*")))

        if not hormone_files:
            print("No SWAN hormone files found")
            return None

        # Try to load the first available file
        for file_path in hormone_files:
            try:
                if file_path.suffix.lower() == ".dta":
                    df = pd.read_stata(file_path)
                elif file_path.suffix.lower() == ".csv":
                    df = pd.read_csv(file_path)
                else:
                    continue

                print(f"SWAN hormone data loaded from {file_path.name}: {df.shape}")
                return df

            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
                continue

        print("No SWAN hormone files could be loaded")
        return None

    except Exception as e:
        print(f"Error loading SWAN hormone data: {e}")
        return None


def load_swan_questionnaires(data_path="data/raw/SWAN/"):
    """
    Load SWAN questionnaire data from Stata/CSV files.

    Args:
        data_path (str): Path to SWAN data directory

    Returns:
        pd.DataFrame: SWAN questionnaire data
    """
    try:
        # Look for questionnaire files
        quest_files = list(Path(data_path).glob("*quest*"))
        quest_files.extend(list(Path(data_path).glob("*symptom*")))
        quest_files.extend(list(Path(data_path).glob("*depression*")))
        quest_files.extend(list(Path(data_path).glob("*anxiety*")))

        if not quest_files:
            print("No SWAN questionnaire files found")
            return None

        # Try to load the first available file
        for file_path in quest_files:
            try:
                if file_path.suffix.lower() == ".dta":
                    df = pd.read_stata(file_path)
                elif file_path.suffix.lower() == ".csv":
                    df = pd.read_csv(file_path)
                else:
                    continue

                print(f"SWAN questionnaire data loaded from {file_path.name}: {df.shape}")
                return df

            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
                continue

        print("No SWAN questionnaire files could be loaded")
        return None

    except Exception as e:
        print(f"Error loading SWAN questionnaire data: {e}")
        return None


def create_longitudinal_features(df):
    """
    Create longitudinal features from SWAN data.

    Args:
        df (pd.DataFrame): SWAN data with visit information

    Returns:
        pd.DataFrame: Data with longitudinal features
    """
    print("Creating longitudinal features...")

    df_features = df.copy()

    # Detect participant ID column automatically
    id_col = None
    for col in ["IDNUM", "ID", "SUBJID", "participant_id"]:
        if col in df_features.columns:
            id_col = col
            break

    if id_col is None:
        print("Warning: No participant ID column found, using first column")
        id_col = df_features.columns[0]

    print(f"Using participant ID column: {id_col}")

    # Sort by participant ID and visit number
    if "visit_number" in df_features.columns:
        df_features = df_features.sort_values([id_col, "visit_number"])

        # Calculate AMH decline rate for each participant
        if "AMH" in df_features.columns:
            df_features["amh_decline_rate"] = (
                df_features.groupby(id_col)["AMH"].diff()
                / df_features.groupby(id_col)["visit_number"].diff()
            )
            print("  Created amh_decline_rate")

        # Calculate FSH trajectory
        if "FSH" in df_features.columns:
            df_features["fsh_trajectory"] = df_features.groupby(id_col)["FSH"].diff()
            print("  Created fsh_trajectory")

        # Calculate months from baseline
        df_features["months_from_baseline"] = df_features["visit_number"] * 12  # Approximate
        print("  Created months_from_baseline")

    return df_features


def calculate_survival_targets(df):
    """
    Calculate survival analysis targets from SWAN data.

    Args:
        df (pd.DataFrame): SWAN data

    Returns:
        pd.DataFrame: Data with survival targets
    """
    print("Calculating survival targets...")

    df_survival = df.copy()

    # Validate essential columns
    if "AGE" not in df_survival.columns:
        print("ERROR: AGE column missing, cannot calculate survival targets")
        print("Available columns:", list(df_survival.columns))
        return df_survival

    # Calculate time to menopause (in months)
    if "AGE" in df_survival.columns:
        # Estimate menopause age (typically 51 years)
        menopause_age = 51
        df_survival["time_to_menopause_months"] = (menopause_age - df_survival["AGE"]) * 12

        # Create menopause event indicator
        df_survival["menopause_event"] = (df_survival["AGE"] >= menopause_age).astype(int)

        # Age at menopause
        df_survival["age_at_menopause"] = df_survival["AGE"]

        # Menopause age groups
        df_survival["menopause_age_group"] = pd.cut(
            df_survival["AGE"],
            bins=[0, 40, 45, 50, 55, 100],
            labels=["<40", "40-45", "45-50", "50-55", ">55"],
        )

        print("  Created survival targets")

    return df_survival


def create_simple_longitudinal_features(df):
    """
    Create simplified longitudinal features (SIMULATED for testing).

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: DataFrame with simple longitudinal features
    """
    print("Creating SIMULATED longitudinal features (for testing only)...")

    df_features = df.copy()

    # Add simple derived features without complex grouping
    if "AMH" in df_features.columns:
        # Simple AMH decline rate (SIMULATED)
        df_features["amh_decline_rate"] = -0.1  # Fixed rate for simplicity
        print("  Created amh_decline_rate (SIMULATED)")

    if "FSH" in df_features.columns:
        # Simple FSH trajectory (SIMULATED)
        df_features["fsh_trajectory"] = 0.5  # Fixed trajectory
        print("  Created fsh_trajectory (SIMULATED)")

    # Add months from baseline (simplified)
    df_features["months_from_baseline"] = 0  # Baseline visit
    print("  Created months_from_baseline (SIMULATED)")

    print("  WARNING: These are SIMULATED features for testing - not real longitudinal data")

    return df_features


def load_swan_data(data_path="data/raw/SWAN/"):
    """
    Load SWAN baseline data only for memory efficiency.

    Args:
        data_path (str): Path to SWAN data directory

    Returns:
        pd.DataFrame: SWAN baseline data
    """
    print("Loading SWAN baseline data only for memory efficiency...")

    # Load only baseline data to avoid memory issues
    baseline_df = load_swan_baseline(data_path)

    if baseline_df is not None:
        # Apply participant-level sampling to preserve longitudinal continuity
        if len(baseline_df) > 2000:
            # Detect participant ID column
            id_col = None
            for col in ["IDNUM", "ID", "SUBJID", "participant_id"]:
                if col in baseline_df.columns:
                    id_col = col
                    break

            if id_col is None:
                print("Warning: No participant ID found, using row sampling")
                # No sampling limit - use all available data
                print(f"Using all {len(baseline_df)} SWAN participants (no sampling limit)")
            else:
                # Sample participants, not rows
                participant_ids = baseline_df[id_col].unique()
                # No sampling limit - use all available participants
                print(f"Using all {len(participant_ids)} SWAN participants (no sampling limit)")

            print(f"Final dataset: {len(baseline_df)} rows for memory efficiency")

        # Create basic longitudinal features (simplified)
        baseline_df = create_simple_longitudinal_features(baseline_df)

        # Calculate survival targets
        baseline_df = calculate_survival_targets(baseline_df)

        # Add data source identifier
        baseline_df["data_source"] = "SWAN"

        # Save final dataset
        output_path = "data/processed/SWAN/swan_baseline_sampled.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        baseline_df.to_csv(output_path, index=False)
        print(f"Saved sampled SWAN data to {output_path}")

        print(f"Final SWAN data shape: {baseline_df.shape}")
        print("Missing values per column:")
        print(baseline_df.isnull().sum().sort_values(ascending=False))

        return baseline_df
    else:
        print("No SWAN data could be loaded")
        return None


def get_swan_schema():
    """
    Return SWAN data schema information.

    Returns:
        dict: Schema information for SWAN data
    """
    return {
        "source": "SWAN",
        "description": "Study of Women's Health Across the Nation (SWAN) data",
        "key_fields": [
            "IDNUM",
            "AGE",
            "BMI",
            "FSH",
            "ESTRADIOL",
            "AMH",
            "INHIBIN_B",
            "MENOPAUSE_STATUS",
            "SMOKING",
            "RACE",
            "EDUCATION",
            "HOT_FLASHES",
            "MOOD_SWINGS",
            "SLEEP_DISTURBANCE",
            "DEPRESSION_SCORE",
            "ANXIETY_SCORE",
            "STRESS_SCORE",
            "PHYSICAL_ACTIVITY",
            "ALCOHOL_FREQUENCY",
            "DIET_QUALITY",
        ],
        "target_variable": "MENOPAUSE_STATUS",
        "data_types": {
            "IDNUM": "string",
            "AGE": "numeric",
            "BMI": "numeric",
            "FSH": "numeric",
            "ESTRADIOL": "numeric",
            "AMH": "numeric",
            "INHIBIN_B": "numeric",
            "MENOPAUSE_STATUS": "categorical",
            "SMOKING": "categorical",
            "RACE": "categorical",
            "EDUCATION": "categorical",
            "HOT_FLASHES": "boolean",
            "MOOD_SWINGS": "boolean",
            "SLEEP_DISTURBANCE": "boolean",
            "DEPRESSION_SCORE": "numeric",
            "ANXIETY_SCORE": "numeric",
            "STRESS_SCORE": "numeric",
            "PHYSICAL_ACTIVITY": "numeric",
            "ALCOHOL_FREQUENCY": "numeric",
            "DIET_QUALITY": "numeric",
        },
    }


if __name__ == "__main__":
    # Test loading
    df = load_swan_data()
    if df is not None:
        print("\nSWAN Schema:")
        schema = get_swan_schema()
        for key, value in schema.items():
            print(f"{key}: {value}")
