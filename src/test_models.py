"""
Proper Test Script for MenoBalance AI Models
Creates proper train/test splits and tests model generalization
"""

import os
import warnings

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    mean_absolute_error,
    r2_score,
)
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")


def load_and_prepare_data(task_name):
    """Load and prepare data for a specific task"""
    print(f"Loading and preparing {task_name} data...")

    # Load processed dataset
    processed_path = f"data/processed/{task_name}_synthetic/combined_dataset.csv"

    if not os.path.exists(processed_path):
        print(f"Processed dataset not found: {processed_path}")
        return None, None, None

    try:
        df = pd.read_csv(processed_path)
        print(f"Loaded {task_name} dataset: {df.shape}")
    except Exception as e:
        print(f"Error loading {task_name} dataset: {e}")
        return None, None, None

    # Separate features and target
    if "target" not in df.columns:
        print(f"No target column found in {task_name} dataset")
        return None, None, None

    # Get feature columns (exclude target)
    feature_cols = [col for col in df.columns if col != "target"]
    X = df[feature_cols].copy()
    y = df["target"].copy()

    # Handle missing values
    for col in X.columns:
        if X[col].isna().all():
            X[col] = X[col].fillna(0)
        else:
            X[col] = X[col].fillna(X[col].median())
    X = X.fillna(0)

    # Remove rows with missing targets
    mask = ~y.isna()
    X = X[mask]
    y = y[mask]

    print(f"Prepared {X.shape[0]} samples with {X.shape[1]} features")
    print(
        f"Target distribution: {np.bincount(y) if task_name == 'classification' else f'Range: {y.min():.2f} - {y.max():.2f}'}"
    )

    return X, y, task_name


def train_and_test_classification(X, y):
    """Train and test classification models"""
    print("\n=== CLASSIFICATION TRAINING AND TESTING ===")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Train set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    # Train models
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": xgb.XGBClassifier(random_state=42, eval_metric="logloss"),
    }

    results = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted")

            print(f"  {name}: Accuracy={accuracy:.4f}, F1={f1:.4f}")

            results[name] = {
                "model": model,
                "accuracy": accuracy,
                "f1_score": f1,
                "predictions": y_pred,
            }

        except Exception as e:
            print(f"  {name}: Error - {e}")
            results[name] = None

    # Test best model
    best_model_name = max(
        [k for k, v in results.items() if v is not None], key=lambda k: results[k]["f1_score"]
    )
    best_model = results[best_model_name]["model"]

    print(f"\nBest model: {best_model_name}")
    print("Final test results:")
    print(f"  Accuracy: {results[best_model_name]['accuracy']:.4f}")
    print(f"  F1 Score: {results[best_model_name]['f1_score']:.4f}")

    # Classification report
    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            results[best_model_name]["predictions"],
            target_names=["Pre-menopause", "Peri-menopause", "Post-menopause"],
        )
    )

    return results[best_model_name]


def train_and_test_regression(X, y, task_name):
    """Train and test regression models"""
    print(f"\n=== {task_name.upper()} REGRESSION TRAINING AND TESTING ===")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Train set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    # Train models
    models = {
        "Ridge Regression": Ridge(random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost": xgb.XGBRegressor(random_state=42),
    }

    results = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            print(f"  {name}: MAE={mae:.4f}, R²={r2:.4f}")

            results[name] = {"model": model, "mae": mae, "r2_score": r2, "predictions": y_pred}

        except Exception as e:
            print(f"  {name}: Error - {e}")
            results[name] = None

    # Test best model
    best_model_name = max(
        [k for k, v in results.items() if v is not None], key=lambda k: results[k]["r2_score"]
    )
    best_model = results[best_model_name]["model"]

    print(f"\nBest model: {best_model_name}")
    print("Final test results:")
    print(f"  MAE: {results[best_model_name]['mae']:.4f}")
    print(f"  R²: {results[best_model_name]['r2_score']:.4f}")

    # Sample predictions
    print("\nSample Predictions (first 10):")
    for i in range(min(10, len(y_test))):
        print(
            f"  True: {y_test.iloc[i]:.2f}, Predicted: {results[best_model_name]['predictions'][i]:.2f}"
        )

    return results[best_model_name]


def test_task(task_name):
    """Test a specific task with proper train/test split"""
    print(f"\n{'=' * 60}")
    print(f"TESTING {task_name.upper()} TASK WITH PROPER SPLIT")
    print(f"{'=' * 60}")

    # Load and prepare data
    X, y, task_type = load_and_prepare_data(task_name)
    if X is None:
        return None

    # Train and test models
    if task_name == "classification":
        results = train_and_test_classification(X, y)
    else:
        results = train_and_test_regression(X, y, task_name)

    print(f"\n[SUCCESS] {task_name.upper()} testing completed!")
    return results


def main():
    """Main function to test all tasks with proper splits"""
    print("=== MenoBalance AI Proper Model Testing ===")
    print("Testing models with proper train/test splits...")

    tasks = ["classification", "survival", "symptom"]
    all_results = {}

    for task in tasks:
        results = test_task(task)
        if results:
            all_results[task] = results
        else:
            print(f"[ERROR] {task.upper()} testing failed!")

    # Summary
    print(f"\n{'=' * 60}")
    print("PROPER TESTING SUMMARY")
    print(f"{'=' * 60}")

    for task, results in all_results.items():
        if task == "classification":
            print(
                f"{task.upper()}: Accuracy={results['accuracy']:.4f}, F1={results['f1_score']:.4f}"
            )
        else:
            print(f"{task.upper()}: MAE={results['mae']:.4f}, R²={results['r2_score']:.4f}")

    print("\n[SUCCESS] All proper model testing completed!")
    return all_results


if __name__ == "__main__":
    main()
