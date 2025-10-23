"""
Simple Data Preparation and Synthetic Target Creation for MenoBalance AI
Creates synthetic target variables for Classification, Survival, and Symptom datasets
"""

import logging
import os

import numpy as np
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_task_dataset(task_name):
    """Load dataset for a specific task"""
    dataset_path = os.path.join("data", "clean", "task_datasets", f"{task_name}_dataset.csv")
    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found: {dataset_path}")
        return None
    try:
        df = pd.read_csv(dataset_path)
        logger.info(f"Loaded {task_name} dataset: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading {task_name} dataset: {e}")
        return None


def create_synthetic_targets(df, task_name):
    """Create synthetic target variables for each task"""
    logger.info(f"Creating synthetic targets for {task_name} task...")

    # Exclude ID/source columns
    exclude_cols = ["participant_id", "seqn", "idnum", "data_source"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [col for col in numeric_cols if col.lower() not in exclude_cols]

    logger.info(f"Found {len(feature_cols)} numeric features")

    if task_name == "classification":
        # Create balanced synthetic menopause stage based on multiple factors
        if "age" in df.columns:
            age = df["age"].copy()
            y = pd.Series(index=age.index, dtype=int)

            # More complex logic incorporating hormone levels and symptoms
            for idx in age.index:
                if pd.isna(age[idx]):
                    continue

                age_val = age[idx]

                # Get hormone levels if available
                fsh_val = (
                    df.loc[idx, "fsh"]
                    if "fsh" in df.columns and not pd.isna(df.loc[idx, "fsh"])
                    else 10
                )
                estradiol_val = (
                    df.loc[idx, "estradiol"]
                    if "estradiol" in df.columns and not pd.isna(df.loc[idx, "estradiol"])
                    else 50
                )

                # Get symptom indicators
                hot_flashes = df.loc[idx, "hot_flashes"] if "hot_flashes" in df.columns else False
                if isinstance(hot_flashes, str):
                    hot_flashes = hot_flashes.lower() == "true"

                # Complex classification logic with balanced approach
                if age_val < 40:
                    # Pre-menopause: young age, normal hormones
                    if fsh_val < 15 and estradiol_val > 30:
                        y[idx] = 0  # Pre-menopause
                    else:
                        y[idx] = 1  # Early peri-menopause
                elif age_val < 50:
                    # Peri-menopause: transition period
                    if fsh_val > 25 or estradiol_val < 20 or hot_flashes:
                        y[idx] = 1  # Peri-menopause
                    elif fsh_val < 15 and estradiol_val > 30:
                        y[idx] = 0  # Still pre-menopause
                    else:
                        y[idx] = 1  # Peri-menopause
                elif age_val < 60:
                    # Post-menopause: older age, high FSH, low estradiol
                    if fsh_val > 30 and estradiol_val < 20:
                        y[idx] = 2  # Post-menopause
                    elif fsh_val > 20 or estradiol_val < 30:
                        y[idx] = 1  # Still peri-menopause
                    else:
                        y[idx] = 1  # Peri-menopause
                else:
                    # Definitely post-menopause
                    y[idx] = 2  # Post-menopause

            mask = ~y.isna()
            y = y[mask]

            # Get features for balancing
            X = df[feature_cols].copy()

            # Balance the classes by stratified sampling

            # Get class counts
            class_counts = np.bincount(y)
            min_class_count = min(class_counts)
            logger.info(f"Original class distribution: {class_counts}")
            logger.info(f"Minimum class count: {min_class_count}")

            # Create balanced dataset
            balanced_indices = []
            for class_label in range(3):
                class_indices = np.where(y == class_label)[0]
                if len(class_indices) > min_class_count:
                    # Randomly sample to match minimum class count
                    np.random.seed(42)
                    selected_indices = np.random.choice(
                        class_indices, min_class_count, replace=False
                    )
                    balanced_indices.extend(selected_indices)
                else:
                    balanced_indices.extend(class_indices)

            # Apply balanced sampling
            balanced_indices = np.array(balanced_indices)
            y = y.iloc[balanced_indices]
            X = X.iloc[balanced_indices]

            logger.info(f"Created balanced synthetic menopause stage: {len(np.unique(y))} classes")
            logger.info(f"Balanced class distribution: {np.bincount(y)}")
            logger.info(f"Total samples after balancing: {len(y)}")
        else:
            logger.error("Age column not found for synthetic target creation")
            return None

    elif task_name == "survival":
        # Create complex survival target based on multiple risk factors
        if "age" in df.columns:
            age = df["age"].copy()
            y = pd.Series(index=age.index, dtype=float)

            for idx in age.index:
                if pd.isna(age[idx]):
                    continue

                age_val = age[idx]
                base_survival = age_val

                # Adjust based on health factors
                if "bmi" in df.columns and not pd.isna(df.loc[idx, "bmi"]):
                    bmi = df.loc[idx, "bmi"]
                    if bmi > 30:  # Obesity reduces survival
                        base_survival -= 5
                    elif bmi < 18.5:  # Underweight reduces survival
                        base_survival -= 3

                # Adjust based on cardiovascular risk
                if "systolic_bp" in df.columns and not pd.isna(df.loc[idx, "systolic_bp"]):
                    sbp = df.loc[idx, "systolic_bp"]
                    if sbp > 140:  # Hypertension reduces survival
                        base_survival -= 8
                    elif sbp > 120:  # Pre-hypertension
                        base_survival -= 2

                # Adjust based on hormone levels
                if "fsh" in df.columns and not pd.isna(df.loc[idx, "fsh"]):
                    fsh = df.loc[idx, "fsh"]
                    if fsh > 40:  # High FSH (post-menopause) may affect survival
                        base_survival -= 2

                # Add some random variation
                import random

                random.seed(idx)  # For reproducibility
                variation = random.uniform(-3, 3)
                base_survival += variation

                # Ensure reasonable bounds
                y[idx] = max(0, min(100, base_survival))

            mask = ~y.isna()
            y = y[mask]

            # Get features for survival
            X = df[feature_cols].copy()
            X = X.loc[mask]

            # Balance survival data to match classification size
            if len(y) > 10000:  # If we have too many samples, sample down
                np.random.seed(42)
                sample_indices = np.random.choice(len(y), 10000, replace=False)
                y = y.iloc[sample_indices]
                X = X.iloc[sample_indices]
                logger.info(f"Sampled survival data to {len(y)} samples for consistency")

            logger.info(f"Created complex survival target: Range {y.min():.1f} - {y.max():.1f}")
        else:
            logger.error("Age column not found for survival target")
            return None

    elif task_name == "symptom":
        # Create complex synthetic symptom severity score
        y = pd.Series(index=df.index, dtype=float)

        for idx in df.index:
            if pd.isna(df.loc[idx, "age"]):
                continue

            age_val = df.loc[idx, "age"]
            base_score = 0.0

            # Age-based symptom severity (peaks around 45-55)
            if 40 <= age_val <= 55:
                age_factor = 1.0
            elif 35 <= age_val < 40 or 55 < age_val <= 60:
                age_factor = 0.7
            else:
                age_factor = 0.3

            # Hormone-based symptoms
            if "fsh" in df.columns and not pd.isna(df.loc[idx, "fsh"]):
                fsh = df.loc[idx, "fsh"]
                if fsh > 30:  # High FSH increases symptoms
                    base_score += 1.5 * age_factor
                elif fsh > 20:
                    base_score += 1.0 * age_factor
                elif fsh > 10:
                    base_score += 0.5 * age_factor

            if "estradiol" in df.columns and not pd.isna(df.loc[idx, "estradiol"]):
                estradiol = df.loc[idx, "estradiol"]
                if estradiol < 20:  # Low estradiol increases symptoms
                    base_score += 1.2 * age_factor
                elif estradiol < 40:
                    base_score += 0.8 * age_factor

            # BMI and stress factors
            if "bmi" in df.columns and not pd.isna(df.loc[idx, "bmi"]):
                bmi = df.loc[idx, "bmi"]
                if bmi > 30:  # Obesity increases symptoms
                    base_score += 0.8
                elif bmi > 25:
                    base_score += 0.4

            # Stress and mental health factors
            if "stress_score" in df.columns and not pd.isna(df.loc[idx, "stress_score"]):
                stress = df.loc[idx, "stress_score"]
                base_score += stress * 0.3

            if "depression_score" in df.columns and not pd.isna(df.loc[idx, "depression_score"]):
                depression = df.loc[idx, "depression_score"]
                base_score += depression * 0.2

            # Sleep quality impact
            if "sleep_quality" in df.columns and not pd.isna(df.loc[idx, "sleep_quality"]):
                sleep = df.loc[idx, "sleep_quality"]
                if sleep < 3:  # Poor sleep increases symptoms
                    base_score += 0.6

            # Physical activity (inverse relationship)
            if "physical_activity" in df.columns and not pd.isna(df.loc[idx, "physical_activity"]):
                activity = df.loc[idx, "physical_activity"]
                if activity < 2:  # Low activity increases symptoms
                    base_score += 0.5
                elif activity > 4:  # High activity reduces symptoms
                    base_score -= 0.3

            # Add some random variation
            import random

            random.seed(idx)
            variation = random.uniform(-0.5, 0.5)
            base_score += variation

            # Ensure reasonable bounds (0-5 scale)
            y[idx] = max(0, min(5, base_score))

        mask = ~y.isna()
        y = y[mask]

        # Get features for symptom
        X = df[feature_cols].copy()
        X = X.loc[mask]

        # Balance symptom data to match classification size
        if len(y) > 10000:  # If we have too many samples, sample down
            np.random.seed(42)
            sample_indices = np.random.choice(len(y), 10000, replace=False)
            y = y.iloc[sample_indices]
            X = X.iloc[sample_indices]
            logger.info(f"Sampled symptom data to {len(y)} samples for consistency")

        logger.info(f"Created complex symptom severity score: Range {y.min():.1f} - {y.max():.1f}")
        logger.info(f"Symptom distribution: Mean={y.mean():.2f}, Std={y.std():.2f}")

    # Prepare features (X is already set in the task-specific sections)
    X = X.fillna(X.median())  # Fill missing values with median

    logger.info(f"Final dataset: {X.shape[0]} samples, {X.shape[1]} features")
    logger.info(f"Target range: {y.min():.2f} - {y.max():.2f}")

    return X, y


def save_processed_data(X, y, task_name):
    """Save processed data with synthetic targets"""
    output_dir = f"data/processed/{task_name}_synthetic"
    os.makedirs(output_dir, exist_ok=True)

    # Save features
    X.to_csv(f"{output_dir}/features.csv", index=False)

    # Save targets
    y.to_csv(f"{output_dir}/targets.csv", index=False)

    # Save combined dataset
    combined = X.copy()
    combined["target"] = y
    combined.to_csv(f"{output_dir}/combined_dataset.csv", index=False)

    logger.info(f"Saved processed {task_name} data to {output_dir}")


def save_feature_selection_files(X, task_name):
    """Save feature selection files for training script"""
    import pickle

    # Create feature selection directory
    feature_dir = f"models/feature_selection_{task_name}"
    os.makedirs(feature_dir, exist_ok=True)

    # Save selected features (all available features)
    selected_features = list(X.columns)
    with open(f"{feature_dir}/selected_features.pkl", "wb") as f:
        pickle.dump(selected_features, f)

    logger.info(f"Saved feature selection files for {task_name} to {feature_dir}")


def process_task(task_name):
    """Process a single task"""
    logger.info(f"\n{'=' * 50}")
    logger.info(f"Processing {task_name.upper()} task")
    logger.info(f"{'=' * 50}")

    # Load data
    df = load_task_dataset(task_name)
    if df is None:
        return False

    # Create synthetic targets
    result = create_synthetic_targets(df, task_name)
    if result is None:
        return False

    X, y = result

    # Save processed data
    save_processed_data(X, y, task_name)

    # Save feature selection files for training script
    save_feature_selection_files(X, task_name)

    logger.info(f"{task_name.upper()} processing completed successfully!")
    return True


def main():
    """Main function to process all tasks"""
    tasks = ["classification", "survival", "symptom"]

    for task in tasks:
        success = process_task(task)
        if not success:
            logger.error(f"Failed to process {task} task")

    logger.info(f"\n{'=' * 50}")
    logger.info("ALL TASKS COMPLETED")
    logger.info(f"{'=' * 50}")


if __name__ == "__main__":
    main()
