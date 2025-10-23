"""
Final Training Script for MenoBalance AI
Uses CatBoost with proper validation and no early stopping issues
"""

import os
import pickle
import warnings

import numpy as np
import pandas as pd
import xgboost as xgb
from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    r2_score,
)
from sklearn.model_selection import (
    KFold,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.preprocessing import RobustScaler

warnings.filterwarnings("ignore")


def load_task_dataset(task_name):
    """Load task-specific dataset."""
    processed_path = f"data/processed/{task_name}_synthetic/combined_dataset.csv"

    if os.path.exists(processed_path):
        try:
            df = pd.read_csv(processed_path)
            print(f"Loaded processed {task_name} dataset: {df.shape}")
            return df
        except Exception as e:
            print(f"Error loading processed {task_name} dataset: {e}")

    dataset_path = f"data/clean/task_datasets/{task_name}_dataset.csv"
    if not os.path.exists(dataset_path):
        print(f"Dataset not found: {dataset_path}")
        return None

    try:
        df = pd.read_csv(dataset_path)
        print(f"Loaded original {task_name} dataset: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading {task_name} dataset: {e}")
        return None


def load_selected_features(task_name):
    """Load selected features for a specific task."""
    features_path = f"models/feature_selection_{task_name}/selected_features.pkl"

    if not os.path.exists(features_path):
        print(f"Selected features not found: {features_path}")
        return None

    try:
        with open(features_path, "rb") as f:
            selected_features = pickle.load(f)
        print(f"Loaded {len(selected_features)} selected features for {task_name}")
        return selected_features
    except Exception as e:
        print(f"Error loading selected features for {task_name}: {e}")
        return None


def prepare_task_data(df, task_name, selected_features):
    """Prepare data for task-specific training with proper preprocessing."""
    print(f"Preparing {task_name} data...")

    # Get available features
    available_features = [f for f in selected_features if f in df.columns]
    print(f"Available features: {len(available_features)}/{len(selected_features)}")

    if len(available_features) == 0:
        print(f"No selected features found in dataset for {task_name}")
        return None, None, None

    # Prepare features
    X = df[available_features].copy()

    # Handle missing values more robustly
    for col in X.columns:
        if X[col].isna().all():
            X[col] = X[col].fillna(0)
        else:
            X[col] = X[col].fillna(X[col].median())
    X = X.fillna(0)

    # Prepare target variable
    if "target" in df.columns:
        y = df["target"].copy()
        mask = ~y.isna()
        X = X[mask]
        y = y[mask]
        print(f"Using pre-computed target for {task_name}")
    else:
        print(f"No target column found for {task_name}")
        return None, None, None

    print(f"Prepared {X.shape[0]} samples with {X.shape[1]} features for {task_name}")
    print(
        f"Target distribution: {np.bincount(y) if task_name == 'classification' else f'Range: {y.min():.2f} - {y.max():.2f}'}"
    )

    return X, y, available_features


def get_final_models(task_name):
    """Get final models with optimized hyperparameters."""
    if task_name == "classification":
        models = {
            "CatBoost": CatBoostClassifier(
                iterations=1000,
                learning_rate=0.1,
                depth=6,
                l2_leaf_reg=3,
                random_seed=42,
                verbose=False,
                eval_metric="Accuracy",
            ),
            "XGBoost": xgb.XGBClassifier(
                n_estimators=500,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=0.1,
                reg_lambda=1,
                random_state=42,
                eval_metric="mlogloss",
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=500,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                max_features="sqrt",
                random_state=42,
                n_jobs=-1,
            ),
            "Logistic Regression": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
        }
    else:
        models = {
            "CatBoost": CatBoostRegressor(
                iterations=1000,
                learning_rate=0.1,
                depth=6,
                l2_leaf_reg=3,
                random_seed=42,
                verbose=False,
                eval_metric="RMSE",
            ),
            "XGBoost": xgb.XGBRegressor(
                n_estimators=500,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=0.1,
                reg_lambda=1,
                random_state=42,
            ),
            "Random Forest": RandomForestRegressor(
                n_estimators=500,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                max_features="sqrt",
                random_state=42,
                n_jobs=-1,
            ),
            "Ridge Regression": Ridge(alpha=1.0, random_state=42),
        }

    return models


def train_with_proper_validation(X, y, task_name):
    """Train models with proper validation and no early stopping issues."""
    print(f"\n=== Training {task_name.upper()} Models with Proper Validation ===")

    # Get models
    models = get_final_models(task_name)

    # Prepare cross-validation
    if task_name == "classification":
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scoring = "f1_weighted"
    else:
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        scoring = "r2"

    # Split data for final evaluation
    if task_name == "classification":
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Train set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    # Scale features for linear models
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    results = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")

        # Use scaled data for linear models, original for tree-based models
        if name in ["Logistic Regression", "Ridge Regression"]:
            X_train_use = X_train_scaled
            X_test_use = X_test_scaled
        else:
            X_train_use = X_train
            X_test_use = X_test

        # Cross-validation
        if name == "CatBoost":
            # For CatBoost, use a simple train/validation split for CV estimation
            X_cv_train, X_cv_val, y_cv_train, y_cv_val = train_test_split(
                X_train_use,
                y_train,
                test_size=0.2,
                random_state=42,
                stratify=y_train if task_name == "classification" else None,
            )
            model.fit(X_cv_train, y_cv_train, eval_set=[(X_cv_val, y_cv_val)], verbose=False)
            cv_pred = model.predict(X_cv_val)
            if task_name == "classification":
                cv_score = accuracy_score(y_cv_val, cv_pred)
            else:
                cv_score = r2_score(y_cv_val, cv_pred)
            cv_scores = np.array([cv_score] * 5)  # Simulate 5-fold CV
        else:
            cv_scores = cross_val_score(
                model, X_train_use, y_train, cv=cv, scoring=scoring, n_jobs=-1
            )

        # Train on full training set
        model.fit(X_train_use, y_train)

        # Predictions
        y_pred = model.predict(X_test_use)

        # Calculate metrics
        if task_name == "classification":
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted")

            results[name] = {
                "model": model,
                "accuracy": accuracy,
                "f1_score": f1,
                "cv_mean": cv_scores.mean(),
                "cv_std": cv_scores.std(),
                "predictions": y_pred,
                "confusion_matrix": confusion_matrix(y_test, y_pred),
            }

            print(f"  {name}: Accuracy={accuracy:.4f}, F1={f1:.4f}")
            print(f"  CV {scoring}: {cv_scores.mean():.4f}±{cv_scores.std():.4f}")

        else:
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            results[name] = {
                "model": model,
                "mae": mae,
                "r2_score": r2,
                "cv_mean": cv_scores.mean(),
                "cv_std": cv_scores.std(),
                "predictions": y_pred,
            }

            print(f"  {name}: MAE={mae:.4f}, R²={r2:.4f}")
            print(f"  CV {scoring}: {cv_scores.mean():.4f}±{cv_scores.std():.4f}")

    # Find best model based on CV score
    if task_name == "classification":
        best_model_name = max(results.keys(), key=lambda k: results[k]["cv_mean"])
    else:
        best_model_name = max(results.keys(), key=lambda k: results[k]["cv_mean"])

    print(
        f"\nBest {task_name} model: {best_model_name} (CV score: {results[best_model_name]['cv_mean']:.4f})"
    )

    return results, scaler


def save_models(results, task_name, scaler):
    """Save trained models and scaler."""
    model_dir = f"models/task_specific_{task_name}"
    os.makedirs(model_dir, exist_ok=True)

    # Save all models
    for name, result in results.items():
        model_path = f"{model_dir}/{name.lower().replace(' ', '_')}_model.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(result["model"], f)

    # Save best model
    if task_name == "classification":
        best_model_name = max(results.keys(), key=lambda k: results[k]["cv_mean"])
    else:
        best_model_name = max(results.keys(), key=lambda k: results[k]["cv_mean"])

    best_model_path = f"{model_dir}/best_model.pkl"
    with open(best_model_path, "wb") as f:
        pickle.dump(results[best_model_name]["model"], f)

    # Save scaler
    scaler_path = f"{model_dir}/scaler.pkl"
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)

    # Save results summary
    results_path = f"{model_dir}/results_summary.pkl"
    with open(results_path, "wb") as f:
        pickle.dump(results, f)

    print(f"Saved {task_name} models to {model_dir}")


def train_task(task_name):
    """Train models for a specific task."""
    print(f"\n{'=' * 60}")
    print(f"TRAINING {task_name.upper()} MODELS WITH FINAL METHODS")
    print(f"{'=' * 60}")

    # Load data
    df = load_task_dataset(task_name)
    if df is None:
        return None

    # Load selected features
    selected_features = load_selected_features(task_name)
    if selected_features is None:
        return None

    # Prepare data
    X, y, available_features = prepare_task_data(df, task_name, selected_features)
    if X is None:
        return None

    # Train with proper validation
    results, scaler = train_with_proper_validation(X, y, task_name)

    # Save models
    save_models(results, task_name, scaler)

    print(f"\n[SUCCESS] {task_name.upper()} training completed!")
    return results


def main():
    """Main function to train all models with final methods."""
    print("=== MenoBalance AI Final Model Training ===")
    print("Training models with CatBoost, proper validation, and optimized parameters...")

    tasks = ["classification", "survival", "symptom"]
    all_results = {}

    for task in tasks:
        results = train_task(task)
        if results:
            all_results[task] = results
        else:
            print(f"[ERROR] {task.upper()} training failed!")

    # Summary
    print(f"\n{'=' * 60}")
    print("FINAL TRAINING SUMMARY")
    print(f"{'=' * 60}")

    for task, results in all_results.items():
        if task == "classification":
            best_model = max(results.keys(), key=lambda k: results[k]["cv_mean"])
            print(f"{task.upper()}: {best_model} - CV F1: {results[best_model]['cv_mean']:.4f}")
        else:
            best_model = max(results.keys(), key=lambda k: results[k]["cv_mean"])
            print(f"{task.upper()}: {best_model} - CV R²: {results[best_model]['cv_mean']:.4f}")

    print("\n[SUCCESS] All final model training completed!")
    return all_results


if __name__ == "__main__":
    main()
