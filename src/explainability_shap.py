"""
SHAP analysis for MenoBalance AI models.
Generates explainability visualizations and feature importance analysis.
"""

import os
import pickle
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

warnings.filterwarnings("ignore")


def load_models():
    """
    Load all trained models from the new structure.
    """
    print("Loading trained models...")

    models = {}

    try:
        # Load models from task-specific directories
        tasks = ["classification", "survival", "symptom"]

        for task in tasks:
            model_dir = f"models/task_specific_{task}"

            # Load best model
            with open(f"{model_dir}/best_model.pkl", "rb") as f:
                models[task] = {"model": pickle.load(f)}

            # Load scaler
            with open(f"{model_dir}/scaler.pkl", "rb") as f:
                models[task]["scaler"] = pickle.load(f)

            # Load selected features
            with open(f"models/feature_selection_{task}/selected_features.pkl", "rb") as f:
                models[task]["features"] = pickle.load(f)

            print(f"Loaded {task} model with {len(models[task]['features'])} features")

        print("All models loaded successfully!")
        return models

    except Exception as e:
        print(f"Error loading models: {e}")
        return None


def load_data():
    """
    Load the processed datasets for SHAP analysis.
    """
    print("Loading processed datasets...")

    datasets = {}
    tasks = ["classification", "survival", "symptom"]

    for task in tasks:
        try:
            df = pd.read_csv(f"data/processed/{task}_synthetic/combined_dataset.csv")
            datasets[task] = df
            print(f"Loaded {task} dataset: {df.shape}")
        except Exception as e:
            print(f"Error loading {task} dataset: {e}")
            return None

    return datasets


def prepare_data_for_shap(df, model_info, task_name):
    """
    Prepare data for SHAP analysis using our current approach.
    """
    print(f"Preparing {task_name} data for SHAP...")

    # Select features
    features = model_info["features"]
    available_features = [f for f in features if f in df.columns]
    X = df[available_features].copy()

    # Handle missing values (same as in training)
    for col in X.columns:
        if X[col].isna().all():
            X[col] = X[col].fillna(0)
        else:
            X[col] = X[col].fillna(X[col].median())
    X = X.fillna(0)

    # Scale features for linear models, keep original for tree-based models
    if task_name in ["classification", "survival"]:
        # For tree-based models (CatBoost, XGBoost, Random Forest), use original data
        X_processed = X.copy()
    else:
        # For linear models, use scaled data
        X_processed = model_info["scaler"].transform(X)
        X_processed = pd.DataFrame(X_processed, columns=available_features)

    print(f"{task_name} data prepared: {X_processed.shape}")
    return X_processed


def create_shap_analysis(model_info, X, task_name):
    """
    Create SHAP analysis for any model using our current approach.
    """
    print(f"Creating {task_name} model SHAP analysis...")

    model = model_info["model"]

    # Create output directory
    os.makedirs("reports/shap", exist_ok=True)

    try:
        # Use TreeExplainer for tree-based models (CatBoost, XGBoost, Random Forest)
        if hasattr(model, "predict_proba") or hasattr(model, "feature_importances_"):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X.iloc[:100])
        else:
            # Use Explainer for other models
            explainer = shap.Explainer(model, X.iloc[:50])
            shap_values = explainer(X.iloc[:50])

        # Summary plot
        plt.figure(figsize=(10, 8))
        if task_name == "classification":
            # For classification, use the first class SHAP values
            if len(shap_values) > 1:
                shap.summary_plot(shap_values[0], X.iloc[:100], show=False)
            else:
                shap.summary_plot(shap_values, X.iloc[:100], show=False)
        else:
            shap.summary_plot(shap_values, X.iloc[:100], show=False)

        plt.title(f"{task_name.title()} Model SHAP Summary Plot")
        plt.tight_layout()
        plt.savefig(f"reports/shap/{task_name}_summary_plot.png", dpi=300, bbox_inches="tight")
        plt.close()

        # Feature importance bar plot
        plt.figure(figsize=(10, 6))
        if task_name == "classification" and len(shap_values) > 1:
            shap.summary_plot(shap_values[0], X.iloc[:100], plot_type="bar", show=False)
        else:
            shap.summary_plot(shap_values, X.iloc[:100], plot_type="bar", show=False)

        plt.title(f"{task_name.title()} Model Feature Importance")
        plt.tight_layout()
        plt.savefig(
            f"reports/shap/{task_name}_feature_importance.png", dpi=300, bbox_inches="tight"
        )
        plt.close()

        # Waterfall plot for first prediction (regression models)
        if task_name != "classification":
            plt.figure(figsize=(12, 8))
            if hasattr(shap_values, "__len__") and len(shap_values) > 0:
                shap.waterfall_plot(shap_values[0], show=False)
                plt.title(f"{task_name.title()} Model Waterfall Plot (First Prediction)")
                plt.tight_layout()
                plt.savefig(
                    f"reports/shap/{task_name}_waterfall_plot.png", dpi=300, bbox_inches="tight"
                )
                plt.close()

        print(f"{task_name.title()} SHAP analysis completed!")
        return shap_values

    except Exception as e:
        print(f"SHAP analysis failed for {task_name}: {e}")
        print("Creating simple feature importance plot instead...")

        # Create simple feature importance plot
        if hasattr(model, "feature_importances_"):
            importance = model.feature_importances_
            feature_names = X.columns

            plt.figure(figsize=(10, 6))
            # Get top 20 features
            top_indices = np.argsort(importance)[-20:]
            plt.barh(range(len(top_indices)), importance[top_indices])
            plt.yticks(range(len(top_indices)), [feature_names[i] for i in top_indices])
            plt.title(f"{task_name.title()} Model Feature Importance")
            plt.xlabel("Importance")
            plt.tight_layout()
            plt.savefig(
                f"reports/shap/{task_name}_feature_importance.png", dpi=300, bbox_inches="tight"
            )
            plt.close()

            print(f"Simple feature importance plot created for {task_name}!")
            return None
        else:
            print(f"No feature importance available for {task_name}")
            return None


def create_feature_interaction_analysis(models, datasets):
    """
    Create feature interaction analysis for our current models.
    """
    print("Creating feature interaction analysis...")

    # Create interaction plots for each model
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    tasks = ["classification", "survival", "symptom"]

    for i, task in enumerate(tasks):
        if task in models and task in datasets:
            try:
                model = models[task]["model"]
                df = datasets[task]
                X = prepare_data_for_shap(df, models[task], task)

                # Create SHAP explainer
                if hasattr(model, "predict_proba") or hasattr(model, "feature_importances_"):
                    explainer = shap.TreeExplainer(model)
                    shap_values = explainer.shap_values(X.iloc[:50])
                else:
                    explainer = shap.Explainer(model, X.iloc[:25])
                    shap_values = explainer(X.iloc[:25])

                # Plot feature interactions
                if i == 0:  # Classification
                    if "age" in X.columns and "fsh" in X.columns:
                        age_idx = X.columns.get_loc("age")
                        fsh_idx = X.columns.get_loc("fsh")

                        scatter = axes[0, 0].scatter(
                            X.iloc[:50, age_idx],
                            X.iloc[:50, fsh_idx],
                            c=shap_values[:, age_idx]
                            if len(shap_values.shape) == 2
                            else shap_values[0][:, age_idx],
                            cmap="viridis",
                        )
                        axes[0, 0].set_xlabel("Age")
                        axes[0, 0].set_ylabel("FSH")
                        axes[0, 0].set_title("Classification: Age vs FSH")
                        plt.colorbar(scatter, ax=axes[0, 0])

                elif i == 1:  # Survival
                    if "age" in X.columns and "bmi" in X.columns:
                        age_idx = X.columns.get_loc("age")
                        bmi_idx = X.columns.get_loc("bmi")

                        scatter = axes[0, 1].scatter(
                            X.iloc[:50, age_idx],
                            X.iloc[:50, bmi_idx],
                            c=shap_values[:, age_idx]
                            if len(shap_values.shape) == 2
                            else shap_values[0][:, age_idx],
                            cmap="viridis",
                        )
                        axes[0, 1].set_xlabel("Age")
                        axes[0, 1].set_ylabel("BMI")
                        axes[0, 1].set_title("Survival: Age vs BMI")
                        plt.colorbar(scatter, ax=axes[0, 1])

                elif i == 2:  # Symptom
                    if "age" in X.columns and "bmi" in X.columns:
                        age_idx = X.columns.get_loc("age")
                        bmi_idx = X.columns.get_loc("bmi")

                        scatter = axes[1, 0].scatter(
                            X.iloc[:50, age_idx],
                            X.iloc[:50, bmi_idx],
                            c=shap_values[:, age_idx]
                            if len(shap_values.shape) == 2
                            else shap_values[0][:, age_idx],
                            cmap="viridis",
                        )
                        axes[1, 0].set_xlabel("Age")
                        axes[1, 0].set_ylabel("BMI")
                        axes[1, 0].set_title("Symptom: Age vs BMI")
                        plt.colorbar(scatter, ax=axes[1, 0])

            except Exception as e:
                print(f"Error creating interaction plot for {task}: {e}")

    # Feature importance comparison
    try:
        feature_importance = {}
        for task in tasks:
            if task in models:
                model = models[task]["model"]
                if hasattr(model, "feature_importances_"):
                    importance = model.feature_importances_
                    features = models[task]["features"]
                    feature_importance[task] = dict(zip(features, importance))

        if feature_importance:
            # Get top 10 features across all models
            all_features = set()
            for imp_dict in feature_importance.values():
                all_features.update(imp_dict.keys())

            # Create comparison plot
            comparison_data = []
            for feature in list(all_features)[:10]:  # Top 10 features
                for model_name, imp_dict in feature_importance.items():
                    comparison_data.append(
                        {
                            "Feature": feature,
                            "Model": model_name,
                            "Importance": imp_dict.get(feature, 0),
                        }
                    )

            comparison_df = pd.DataFrame(comparison_data)
            pivot_df = comparison_df.pivot(index="Feature", columns="Model", values="Importance")
            pivot_df.plot(kind="bar", ax=axes[1, 1])
            axes[1, 1].set_title("Feature Importance Comparison")
            axes[1, 1].set_xlabel("Features")
            axes[1, 1].set_ylabel("Importance")
            axes[1, 1].tick_params(axis="x", rotation=45)

    except Exception as e:
        print(f"Error creating feature importance comparison: {e}")

    plt.tight_layout()
    plt.savefig("reports/shap/feature_interaction_analysis.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("Feature interaction analysis completed!")


def main():
    """
    Main SHAP analysis pipeline for our current approach.
    """
    print("=== MenoBalance AI SHAP Analysis Pipeline ===")

    # Load models and data
    models = load_models()
    if models is None:
        print("Failed to load models. Please run training first.")
        return

    datasets = load_data()
    if datasets is None:
        print("Failed to load datasets. Please run feature selection first.")
        return

    # Create SHAP analyses for each task
    shap_results = {}
    tasks = ["classification", "survival", "symptom"]

    for task in tasks:
        if task in models and task in datasets:
            print(f"\n=== Processing {task.upper()} ===")
            try:
                # Prepare data
                X = prepare_data_for_shap(datasets[task], models[task], task)

                # Create SHAP analysis
                shap_values = create_shap_analysis(models[task], X, task)
                shap_results[task] = shap_values

            except Exception as e:
                print(f"Error processing {task}: {e}")
                shap_results[task] = None

    # Create feature interaction analysis
    try:
        create_feature_interaction_analysis(models, datasets)
    except Exception as e:
        print(f"Error creating feature interaction analysis: {e}")

    print("\n=== SHAP Analysis Pipeline Completed ===")
    print("All SHAP visualizations saved to reports/shap/ directory")
    print("Generated plots:")
    for task in tasks:
        print(f"  - {task.title()} model: summary, feature importance")
    print("  - Feature interaction analysis")

    return shap_results


if __name__ == "__main__":
    results = main()
