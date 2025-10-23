"""
MenoBalance AI - Unified Cohort Builder with Task-Specific Datasets
"""

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Add parent directory to path for imports
try:
    parent_dir = Path(__file__).parent.parent
    sys.path.append(str(parent_dir))
except NameError:
    parent_dir = Path.cwd()
    sys.path.append(str(parent_dir))

# Import required modules
try:
    from harmonize.map_sources import (
        apply_field_mapping,
        apply_unit_conversions,
        apply_value_mapping,
    )
    from harmonize.schema import CANONICAL_SCHEMA, validate_schema
    from ingest.load_nhanes import load_nhanes_data
    from ingest.load_swan import load_swan_data
    from ingest.load_synthea import load_synthea_data
    from ingest.load_ukbb import load_ukbb_data
    from ingest.load_wearables import load_wearables_data

    print("[OK] All required modules imported successfully")
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    sys.exit(1)


def load_all_sources():
    sources = {}
    for name, loader in [
        ("SYNTHEA", load_synthea_data),
        ("UKBB", load_ukbb_data),
        ("NHANES", load_nhanes_data),
        ("Wearables", load_wearables_data),
        ("SWAN", load_swan_data),
    ]:
        df = loader()
        if df is not None:
            sources[name] = df
            print(f"{name} loaded: {df.shape}")
    return sources


def harmonize_source(df, source_name):
    harmonization_failures = []
    try:
        try:
            df = apply_field_mapping(df, source_name)
        except Exception as e:
            harmonization_failures.append(f"Field mapping failed: {e}")
        try:
            df = apply_value_mapping(df, source_name)
        except Exception as e:
            harmonization_failures.append(f"Value mapping failed: {e}")
        try:
            df = apply_unit_conversions(df, source_name)
        except Exception as e:
            harmonization_failures.append(f"Unit conversions failed: {e}")
        if "data_source" not in df.columns:
            df["data_source"] = source_name
        if harmonization_failures:
            print(f"[WARNING] {len(harmonization_failures)} issues in {source_name}")
        return df
    except Exception as e:
        print(f"[CRITICAL] Harmonization failed for {source_name}: {e}")
        df_copy = df.copy()
        df_copy["data_source"] = source_name
        return df_copy


def align_datatypes(df, schema=None):
    if schema is None:
        schema = CANONICAL_SCHEMA
    aligned_df = df.copy()
    for field, expected_type in schema.items():
        if field in aligned_df.columns:
            if expected_type == "numeric":
                aligned_df[field] = pd.to_numeric(aligned_df[field], errors="coerce")
            elif expected_type == "categorical":
                aligned_df[field] = aligned_df[field].astype("category")
            elif expected_type == "boolean":
                aligned_df[field] = aligned_df[field].astype("boolean", errors="ignore")
            elif expected_type == "string":
                aligned_df[field] = aligned_df[field].astype("string")
    return aligned_df


def unify_missing_values(df, source_name=None):
    unified_df = df.copy()
    string_missing = [
        "Unknown",
        "Not reported",
        "Refused",
        "Don't know",
        "Missing",
        "N/A",
        "Not applicable",
    ]
    numeric_missing = [999, 888, 777, 666, 555, 444, 333, 222, 111, -1]
    for col in unified_df.columns:
        if unified_df[col].dtype == "object":
            unified_df[col] = unified_df[col].replace(string_missing, np.nan)
        else:
            unified_df[col] = unified_df[col].replace(numeric_missing, np.nan)
            if "age" in col.lower() or "bmi" in col.lower():
                unified_df[col] = unified_df[col].replace(0, np.nan)
    return unified_df


def aggregate_wearables_to_person_level(df):
    if "data_source" in df.columns and df["data_source"].iloc[0] == "Wearables":
        if "participant_id" not in df.columns and "SEQN" in df.columns:
            df["participant_id"] = df["SEQN"].astype(str)
        if "participant_id" in df.columns:
            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
            numeric_cols = [c for c in numeric_cols if c not in ["participant_id"]]
            agg_dict = {c: ["mean", "std", "min", "max"] for c in numeric_cols}
            aggregated_df = df.groupby("participant_id").agg(agg_dict).reset_index()
            # flatten columns
            aggregated_df.columns = [
                "_".join(filter(None, col)).strip() if isinstance(col, tuple) else col
                for col in aggregated_df.columns
            ]
            aggregated_df["data_source"] = "Wearables"
            return aggregated_df
    return df


def build_unified_cohort(sources):
    harmonized_sources = []
    for source_name, df in sources.items():
        df = harmonize_source(df, source_name)
        df = align_datatypes(df)
        df = unify_missing_values(df, source_name)
        if source_name == "Wearables":
            df = aggregate_wearables_to_person_level(df)
        harmonized_sources.append(df)
    # align to canonical columns
    canonical_cols = list(CANONICAL_SCHEMA.keys())
    aligned_sources = []
    for df in harmonized_sources:
        aligned_df = pd.DataFrame()
        for col in canonical_cols:
            aligned_df[col] = df[col] if col in df.columns else np.nan
        aligned_df["data_source"] = df["data_source"]
        aligned_sources.append(aligned_df)
    unified_df = pd.concat(aligned_sources, ignore_index=True)
    return unified_df


def filter_complete_rows(df, required_features, min_completeness=0.6):
    """
    Filter rows to ensure at least 60% data completeness for required features.
    
    Args:
        df (pd.DataFrame): Input dataset
        required_features (list): List of required feature columns
        min_completeness (float): Minimum completeness threshold (0.6 = 60%)
    
    Returns:
        pd.DataFrame: Filtered dataset with sufficient data completeness
    """
    print(f"Filtering for {min_completeness*100:.0f}% data completeness...")
    
    # Calculate completeness for each row
    completeness_scores = df[required_features].notna().mean(axis=1)
    
    # Filter rows that meet the completeness threshold
    mask = completeness_scores >= min_completeness
    filtered_df = df[mask].copy()
    
    print(f"Original dataset: {len(df)} rows")
    print(f"Filtered dataset: {len(filtered_df)} rows with >= {min_completeness*100:.0f}% completeness")
    print(f"Completeness range: {completeness_scores[mask].min():.2f} - {completeness_scores[mask].max():.2f}")
    
    return filtered_df


def create_task_datasets(unified_df):
    """
    Create task-specific datasets with no capacity limits and 60% data completeness.
    """
    print(f"\n=== Creating Task-Specific Datasets ===")
    print(f"Total unified dataset: {len(unified_df)} rows")
    
    # Use features that actually exist in the canonical schema
    survival_features = ["age", "menopause_stage", "fsh", "estradiol", "bmi"]
    symptom_features = ["hot_flashes", "mood_swings", "sleep_disturbance", "age", "bmi"]
    classification_features = [
        "menopause_stage",
        "age",
        "bmi",
        "smoking_status",
        "physical_activity",
    ]

    # Check which features actually exist in the dataset
    available_survival = [f for f in survival_features if f in unified_df.columns]
    available_symptom = [f for f in symptom_features if f in unified_df.columns]
    available_classification = [f for f in classification_features if f in unified_df.columns]

    print(f"Available survival features: {available_survival}")
    print(f"Available symptom features: {available_symptom}")
    print(f"Available classification features: {available_classification}")

    # Create datasets with 60% completeness requirement (no capacity limits)
    print(f"\n--- Survival Analysis Dataset ---")
    if len(available_survival) >= 3:
        survival_df = filter_complete_rows(unified_df, available_survival, min_completeness=0.6)
    else:
        print("Insufficient survival features, using full dataset")
        survival_df = unified_df.copy()

    print(f"\n--- Symptom Severity Dataset ---")
    if len(available_symptom) >= 3:
        symptom_df = filter_complete_rows(unified_df, available_symptom, min_completeness=0.6)
    else:
        print("Insufficient symptom features, using full dataset")
        symptom_df = unified_df.copy()

    print(f"\n--- Classification Dataset ---")
    if len(available_classification) >= 3:
        classification_df = filter_complete_rows(unified_df, available_classification, min_completeness=0.6)
    else:
        print("Insufficient classification features, using full dataset")
        classification_df = unified_df.copy()

    # Print final dataset statistics
    print(f"\n=== Final Dataset Statistics ===")
    print(f"Survival dataset: {len(survival_df)} rows")
    print(f"Symptom dataset: {len(symptom_df)} rows")
    print(f"Classification dataset: {len(classification_df)} rows")
    
    # Check data source distribution for each dataset
    for dataset_name, dataset in [("Survival", survival_df), ("Symptom", symptom_df), ("Classification", classification_df)]:
        if "data_source" in dataset.columns:
            source_dist = dataset["data_source"].value_counts()
            print(f"\n{dataset_name} data source distribution:")
            for source, count in source_dist.items():
                print(f"  {source}: {count} rows ({count/len(dataset)*100:.1f}%)")

    # Save datasets
    os.makedirs("data/clean/task_datasets", exist_ok=True)
    survival_df.to_csv("data/clean/task_datasets/survival_dataset.csv", index=False)
    symptom_df.to_csv("data/clean/task_datasets/symptom_dataset.csv", index=False)
    classification_df.to_csv("data/clean/task_datasets/classification_dataset.csv", index=False)
    
    print(f"\n=== Task Datasets Saved ===")
    print(f"Saved to: data/clean/task_datasets/")

    return {
        "survival": survival_df,
        "symptom": symptom_df,
        "classification": classification_df,
    }


def create_schema_catalog(unified_df):
    catalog = {
        "total_records": len(unified_df),
        "total_fields": len(unified_df.columns),
        "data_sources": unified_df["data_source"].value_counts().to_dict(),
        "field_info": {},
    }
    for col in unified_df.columns:
        field_info = {
            "dtype": str(unified_df[col].dtype),
            "missing_count": unified_df[col].isnull().sum(),
            "missing_percentage": (unified_df[col].isnull().sum() / len(unified_df)) * 100,
            "unique_values": unified_df[col].nunique(),
            "sample_values": unified_df[col].dropna().head(5).tolist(),
        }
        if unified_df[col].dtype in ["int64", "float64"]:
            field_info.update(
                {
                    "min": unified_df[col].min(),
                    "max": unified_df[col].max(),
                    "mean": unified_df[col].mean(),
                    "std": unified_df[col].std(),
                }
            )
        catalog["field_info"][col] = field_info
    return catalog


def save_schema_catalog(catalog, output_path="reports/schema_catalog.md"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("# Unified Dataset Schema Catalog\n\n")
        f.write(f"**Total Records:** {catalog['total_records']:,}\n")
        f.write(f"**Total Fields:** {catalog['total_fields']}\n\n")
        f.write("## Data Sources Distribution\n\n")
        for source, count in catalog["data_sources"].items():
            f.write(f"- **{source}:** {count:,} records\n")
        f.write("\n## Field Information\n\n")
        for field, info in catalog["field_info"].items():
            f.write(f"### {field}\n")
            f.write(f"- **Type:** {info['dtype']}\n")
            f.write(
                f"- **Missing:** {info['missing_count']:,} ({info['missing_percentage']:.1f}%)\n"
            )
            f.write(f"- **Unique Values:** {info['unique_values']:,}\n")
            if "min" in info:
                f.write(f"- **Range:** {info['min']:.2f} to {info['max']:.2f}\n")
                f.write(f"- **Mean:** {info['mean']:.2f} (SD: {info['std']:.2f})\n")
            f.write(f"- **Sample Values:** {info['sample_values']}\n\n")


def main():
    print("=== MenoBalance AI - Unified Cohort with Task Datasets ===")
    sources = load_all_sources()
    if not sources:
        print("[ERROR] No data sources loaded")
        return None

    unified_df = build_unified_cohort(sources)

    # Save full unified dataset
    os.makedirs("data/clean", exist_ok=True)
    unified_df.to_csv("data/clean/combined_raw_unified.csv", index=False)
    print(f"Unified dataset saved: {len(unified_df)} rows")

    # Create task-specific datasets
    task_datasets = create_task_datasets(unified_df)

    # Create and save schema catalog
    catalog = create_schema_catalog(unified_df)
    save_schema_catalog(catalog)

    print("=== Completed ===")
    return task_datasets


if __name__ == "__main__":
    task_datasets = main()
