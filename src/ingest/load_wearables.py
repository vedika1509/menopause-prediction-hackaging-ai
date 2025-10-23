import os
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")


def load_paxday_data(data_path="data/raw/Physical_Activity_Wearables/"):
    """
    Load PAXDAY (daily activity) data from XPT files.

    Args:
        data_path (str): Path to wearables data directory

    Returns:
        pd.DataFrame: Daily activity data
    """
    try:
        # Look for PAXDAY XPT files
        paxday_files = list(Path(data_path).glob("*PAXDAY*.xpt"))
        if not paxday_files:
            print("No PAXDAY XPT files found")
            return None

        print(f"Found {len(paxday_files)} PAXDAY files")

        # Load and concatenate all PAXDAY files
        dfs = []
        for i, file_path in enumerate(paxday_files):
            try:
                print(f"Loading PAXDAY file {i + 1}/{len(paxday_files)}: {file_path.name}")
                df = pd.read_sas(file_path)
                dfs.append(df)
                print(f"  Loaded {df.shape[0]} rows, {df.shape[1]} columns")
            except Exception as e:
                print(f"  Error loading {file_path.name}: {e}")
                continue

        if not dfs:
            print("No PAXDAY files could be loaded successfully")
            return None

        # Concatenate all dataframes
        df = pd.concat(dfs, ignore_index=True)
        print(f"PAXDAY data loaded: {df.shape} (combined from {len(dfs)} files)")
        return df

    except Exception as e:
        print(f"Error loading PAXDAY data: {e}")
        return None


def load_paxhd_data(data_path="data/raw/Physical_Activity_Wearables/"):
    """
    Load PAXHD (high-resolution activity) data from XPT files.

    Args:
        data_path (str): Path to wearables data directory

    Returns:
        pd.DataFrame: High-resolution activity data
    """
    try:
        # Look for PAXHD XPT files
        paxhd_files = list(Path(data_path).glob("*PAXHD*.xpt"))
        if not paxhd_files:
            print("No PAXHD XPT files found")
            return None

        print(f"Found {len(paxhd_files)} PAXHD files")

        # Load and concatenate all PAXHD files
        dfs = []
        for i, file_path in enumerate(paxhd_files):
            try:
                print(f"Loading PAXHD file {i + 1}/{len(paxhd_files)}: {file_path.name}")
                df = pd.read_sas(file_path)
                dfs.append(df)
                print(f"  Loaded {df.shape[0]} rows, {df.shape[1]} columns")
            except Exception as e:
                print(f"  Error loading {file_path.name}: {e}")
                continue

        if not dfs:
            print("No PAXHD files could be loaded successfully")
            return None

        # Concatenate all dataframes
        df = pd.concat(dfs, ignore_index=True)
        print(f"PAXHD data loaded: {df.shape} (combined from {len(dfs)} files)")
        return df

    except Exception as e:
        print(f"Error loading PAXHD data: {e}")
        return None


def load_paxhr_data(data_path="data/raw/Physical_Activity_Wearables/"):
    """
    Load PAXHR (heart rate) data from XPT files.

    Args:
        data_path (str): Path to wearables data directory

    Returns:
        pd.DataFrame: Heart rate data
    """
    try:
        # Look for PAXHR XPT files
        paxhr_files = list(Path(data_path).glob("*PAXHR*.xpt"))
        if not paxhr_files:
            print("No PAXHR XPT files found")
            return None

        print(f"Found {len(paxhr_files)} PAXHR files")

        # Load and concatenate all PAXHR files
        dfs = []
        for i, file_path in enumerate(paxhr_files):
            try:
                print(f"Loading PAXHR file {i + 1}/{len(paxhr_files)}: {file_path.name}")
                df = pd.read_sas(file_path)
                dfs.append(df)
                print(f"  Loaded {df.shape[0]} rows, {df.shape[1]} columns")
            except Exception as e:
                print(f"  Error loading {file_path.name}: {e}")
                continue

        if not dfs:
            print("No PAXHR files could be loaded successfully")
            return None

        # Concatenate all dataframes
        df = pd.concat(dfs, ignore_index=True)
        print(f"PAXHR data loaded: {df.shape} (combined from {len(dfs)} files)")
        return df

    except Exception as e:
        print(f"Error loading PAXHR data: {e}")
        return None


def create_time_series_features(daily_df):
    """
    Create time-series features from daily wearable data with robust column checks.

    Args:
        daily_df (pd.DataFrame): Daily wearable data

    Returns:
        pd.DataFrame: Data with time-series features
    """
    print("Creating time-series features...")

    df_features = daily_df.copy()

    # Check for required columns
    required_cols = ["SEQN", "PAXDAY"]
    missing_cols = [col for col in required_cols if col not in df_features.columns]
    if missing_cols:
        print(f"  Warning: Missing required columns {missing_cols}, skipping time-series features")
        return df_features

    # Sort by participant and date
    df_features = df_features.sort_values(["SEQN", "PAXDAY"])

    # Calculate sleep efficiency from sedentary patterns (with wear time validation)
    if "PAXSED" in df_features.columns:
        # Sleep efficiency = 1 - (sedentary_time / total_wear_time)
        # Use actual wear time if available, otherwise assume 24h
        if "PAXWEAR" in df_features.columns:
            # Use actual wear time
            df_features["sleep_efficiency"] = 1 - (
                df_features["PAXSED"] / (df_features["PAXWEAR"] * 60)
            )
        else:
            # Assume 24h wear but validate values
            df_features["sleep_efficiency"] = 1 - (df_features["PAXSED"] / (24 * 60))
            # Clamp to reasonable range [0, 1]
            df_features["sleep_efficiency"] = df_features["sleep_efficiency"].clip(0, 1)
        print("  Created sleep_efficiency")

    # Calculate circadian rhythm disruption
    if "PAXSTEP" in df_features.columns:
        # Activity variability (standard deviation of daily steps)
        df_features["activity_variability"] = df_features.groupby("SEQN")["PAXSTEP"].transform(
            "std"
        )
        print("  Created activity_variability")

    # Calculate stress proxy from heart rate variability
    if "PAXHR" in df_features.columns:
        # HRV proxy = standard deviation of heart rate
        df_features["hrv_proxy"] = df_features.groupby("SEQN")["PAXHR"].transform("std")
        print("  Created hrv_proxy")

    # Calculate activity window fraction (time with activity > threshold)
    if "PAXINTEN" in df_features.columns:
        # Fraction of day with moderate+ activity (improved thresholding)
        median_intensity = df_features["PAXINTEN"].median()
        # Use 75th percentile as threshold for moderate activity
        threshold = df_features["PAXINTEN"].quantile(0.75)
        df_features["activity_window_fraction"] = (df_features["PAXINTEN"] > threshold).astype(int)
        print(f"  Created activity_window_fraction (threshold: {threshold:.2f})")

    # Calculate sleep duration estimate (improved)
    if "PAXSED" in df_features.columns:
        # Estimate sleep as longest continuous sedentary period
        # Convert to hours and validate range
        df_features["sleep_duration_estimate"] = (df_features["PAXSED"] / 60).clip(
            0, 12
        )  # Max 12 hours
        print("  Created sleep_duration_estimate")

    return df_features


def aggregate_wearables_to_daily(paxday_df, paxhd_df=None, paxhr_df=None):
    """
    Aggregate wearable data to daily summaries.

    Args:
        paxday_df (pd.DataFrame): Daily activity data
        paxhd_df (pd.DataFrame): High-resolution activity data
        paxhr_df (pd.DataFrame): Heart rate data

    Returns:
        pd.DataFrame: Aggregated daily wearable metrics
    """
    print("Aggregating wearable data to daily summaries...")

    if paxday_df is None:
        print("No PAXDAY data available for aggregation")
        return None

    # Start with PAXDAY as base
    daily_df = paxday_df.copy()

    # Add PAXHD aggregations if available
    if paxhd_df is not None:
        # Group by participant and date, calculate daily summaries
        if "SEQN" in paxhd_df.columns and "PAXDAY" in paxhd_df.columns:
            hd_daily = (
                paxhd_df.groupby(["SEQN", "PAXDAY"])
                .agg(
                    {
                        "PAXINTEN": ["mean", "std", "min", "max"],
                        "PAXSTEP": ["sum", "mean"],
                        "PAXVM": ["mean", "std"],
                    }
                )
                .reset_index()
            )

            # Flatten column names safely
            hd_daily.columns = ["SEQN", "PAXDAY"] + [
                f"HD_{'_'.join(filter(None, col))}" for col in hd_daily.columns[2:]
            ]

            # Merge with daily data
            daily_df = daily_df.merge(hd_daily, on=["SEQN", "PAXDAY"], how="left")
            print(f"After merging PAXHD data: {daily_df.shape}")

    # Add PAXHR aggregations if available
    if paxhr_df is not None:
        # Group by participant and date, calculate daily heart rate summaries
        if "SEQN" in paxhr_df.columns and "PAXDAY" in paxhr_df.columns:
            hr_daily = (
                paxhr_df.groupby(["SEQN", "PAXDAY"])
                .agg({"PAXHR": ["mean", "std", "min", "max"], "PAXHRVM": ["mean", "std"]})
                .reset_index()
            )

            # Flatten column names safely
            hr_daily.columns = ["SEQN", "PAXDAY"] + [
                f"HR_{'_'.join(filter(None, col))}" for col in hr_daily.columns[2:]
            ]

            # Merge with daily data
            daily_df = daily_df.merge(hr_daily, on=["SEQN", "PAXDAY"], how="left")
            print(f"After merging PAXHR data: {daily_df.shape}")

    # Create time-series features
    daily_df = create_time_series_features(daily_df)

    # Save daily patterns for time-series analysis
    output_path = "data/processed/Wearables/daily_patterns.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    daily_df.to_csv(output_path, index=False)
    print(f"Saved daily patterns to {output_path}")

    return daily_df


def aggregate_to_person_level(daily_df):
    """
    Aggregate daily wearable data to person-level summaries.

    Args:
        daily_df (pd.DataFrame): Daily wearable data

    Returns:
        pd.DataFrame: Person-level wearable summaries
    """
    print("Aggregating to person-level summaries...")

    if daily_df is None:
        print("No daily data available for person-level aggregation")
        return None

    # Group by participant and calculate person-level metrics
    person_df = (
        daily_df.groupby("SEQN")
        .agg(
            {
                # Activity metrics
                "PAXSTEP": ["mean", "std", "sum"],
                "PAXINTEN": ["mean", "std"],
                "PAXVM": ["mean", "std"],
                # Sedentary time
                "PAXSED": ["mean", "std"],
                # Light activity
                "PAXLIG": ["mean", "std"],
                # Moderate activity
                "PAXMOD": ["mean", "std"],
                # Vigorous activity
                "PAXVIG": ["mean", "std"],
                # Heart rate metrics (if available)
                **{col: ["mean", "std"] for col in daily_df.columns if col.startswith("HR_")},
            }
        )
        .reset_index()
    )

    # Flatten column names
    person_df.columns = ["SEQN"] + [f"WEARABLE_{col[0]}_{col[1]}" for col in person_df.columns[1:]]

    print(f"Person-level wearable data shape: {person_df.shape}")
    return person_df


def load_wearables_data(data_path="data/raw/Physical_Activity_Wearables/"):
    """
    Load all available wearable data and aggregate with real calculations.

    Args:
        data_path (str): Path to wearables data directory

    Returns:
        pd.DataFrame: Aggregated wearable data
    """
    print("Loading wearable data...")

    # Load different components
    paxday_df = load_paxday_data(data_path)
    paxhd_df = load_paxhd_data(data_path)
    paxhr_df = load_paxhr_data(data_path)

    # Create comprehensive summary with real calculations
    if paxday_df is not None:
        print("Creating comprehensive wearable summaries...")

        # Get unique participants
        unique_participants = paxday_df["SEQN"].unique()
        print(f"Found {len(unique_participants)} unique participants")

        # Create comprehensive summary DataFrame
        summary_data = []

        for seqn in unique_participants:
            participant_data = paxday_df[paxday_df["SEQN"] == seqn]

            # Calculate real wearable metrics
            wearable_days = len(participant_data)

            # Calculate activity level based on actual step data
            if "PAXSTEP" in participant_data.columns:
                avg_steps = participant_data["PAXSTEP"].mean()
                if avg_steps < 5000:
                    activity_level = "low"
                elif avg_steps < 10000:
                    activity_level = "moderate"
                else:
                    activity_level = "high"
            else:
                activity_level = "unknown"

            # Calculate additional metrics if available
            avg_sedentary = (
                participant_data["PAXSED"].mean() if "PAXSED" in participant_data.columns else None
            )
            avg_light = (
                participant_data["PAXLIG"].mean() if "PAXLIG" in participant_data.columns else None
            )
            avg_moderate = (
                participant_data["PAXMOD"].mean() if "PAXMOD" in participant_data.columns else None
            )
            avg_vigorous = (
                participant_data["PAXVIG"].mean() if "PAXVIG" in participant_data.columns else None
            )

            summary_data.append(
                {
                    "participant_id": str(seqn),
                    "data_source": "Wearables",
                    "wearable_days": wearable_days,
                    "activity_level": activity_level,
                    "avg_steps": participant_data["PAXSTEP"].mean()
                    if "PAXSTEP" in participant_data.columns
                    else None,
                    "avg_sedentary_minutes": avg_sedentary,
                    "avg_light_minutes": avg_light,
                    "avg_moderate_minutes": avg_moderate,
                    "avg_vigorous_minutes": avg_vigorous,
                }
            )

        summary_df = pd.DataFrame(summary_data)
        print(f"Created comprehensive summaries for {len(summary_df)} participants")

        # Apply sampling to target size
        if len(summary_df) > 1000:
            # No sampling limit - use all available data
            print(f"Using all {len(summary_df)} participants (no sampling limit)")
            print(f"Sampled wearables data to {len(summary_df)} rows")

        # Save final dataset
        output_path = "data/processed/Wearables/wearables_processed.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        summary_df.to_csv(output_path, index=False)
        print(f"Saved processed wearables data to {output_path}")

        print(f"Final wearables data shape: {summary_df.shape}")
        return summary_df

    print("No wearable data could be loaded")
    return None


def get_wearables_schema():
    """
    Return wearables data schema information.

    Returns:
        dict: Schema information for wearables data
    """
    return {
        "source": "Wearables",
        "description": "ActiGraph wearable device data (PAXDAY, PAXHD, PAXHR)",
        "key_fields": [
            "SEQN",
            "PAXSTEP",
            "PAXINTEN",
            "PAXVM",
            "PAXSED",
            "PAXLIG",
            "PAXMOD",
            "PAXVIG",
            "PAXHR",
            "PAXHRVM",
            "WEARABLE_STEPS_MEAN",
            "WEARABLE_STEPS_STD",
            "WEARABLE_SEDENTARY_MEAN",
            "WEARABLE_LIGHT_MEAN",
            "WEARABLE_MODERATE_MEAN",
            "WEARABLE_VIGOROUS_MEAN",
        ],
        "target_variable": None,  # Wearables data alone doesn't contain menopause status
        "data_types": {
            "SEQN": "string",
            "PAXSTEP": "numeric",
            "PAXINTEN": "numeric",
            "PAXVM": "numeric",
            "PAXSED": "numeric",
            "PAXLIG": "numeric",
            "PAXMOD": "numeric",
            "PAXVIG": "numeric",
            "PAXHR": "numeric",
            "PAXHRVM": "numeric",
            "WEARABLE_STEPS_MEAN": "numeric",
            "WEARABLE_STEPS_STD": "numeric",
            "WEARABLE_SEDENTARY_MEAN": "numeric",
            "WEARABLE_LIGHT_MEAN": "numeric",
            "WEARABLE_MODERATE_MEAN": "numeric",
            "WEARABLE_VIGOROUS_MEAN": "numeric",
        },
    }


if __name__ == "__main__":
    # Test loading
    df = load_wearables_data()
    if df is not None:
        print("\nWearables Schema:")
        schema = get_wearables_schema()
        for key, value in schema.items():
            print(f"{key}: {value}")
