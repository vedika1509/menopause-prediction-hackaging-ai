#!/usr/bin/env python3
"""
Comprehensive Performance Report Generator for MenoBalance AI
Generates detailed performance reports with visualizations and medical metrics.
"""

import json
import os
import pickle
from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better plots
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


def load_training_results():
    """Load training results from our current model structure."""
    results = {}
    tasks = ["classification", "survival", "symptom"]

    for task in tasks:
        try:
            # Load results summary from our current structure
            results_path = f"models/task_specific_{task}/results_summary.pkl"
            if os.path.exists(results_path):
                with open(results_path, "rb") as f:
                    task_results = pickle.load(f)
                    results[task] = task_results
                    print(f"Loaded {task} results: {len(task_results)} models")
            else:
                print(f"No results found for {task}")
        except Exception as e:
            print(f"Error loading {task} results: {e}")

    if not results:
        print("No training results found. Please run training first.")
        return None

    return results


def generate_performance_summary(results):
    """Generate comprehensive performance summary."""
    print("=== MenoBalance AI Performance Report ===")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Classification Performance
    if "classification" in results:
        print("CLASSIFICATION (Menopause Stage Prediction)")
        print("=" * 50)
        class_results = results["classification"]
        best_class = max(class_results.items(), key=lambda x: x[1]["cv_mean"])
        print(f"Best Model: {best_class[0]}")
        print(f"Accuracy: {best_class[1]['accuracy']:.4f}")
        print(f"F1 Score: {best_class[1]['f1_score']:.4f}")
        print(f"CV F1: {best_class[1]['cv_mean']:.4f}")
        print(
            f"Performance: {'Excellent' if best_class[1]['accuracy'] > 0.95 else 'Good' if best_class[1]['accuracy'] > 0.8 else 'Needs Improvement'}"
        )
        print()

    # Survival Analysis Performance
    if "survival" in results:
        print("SURVIVAL ANALYSIS (Age/Risk Prediction)")
        print("=" * 50)
        survival_results = results["survival"]
        best_survival = max(survival_results.items(), key=lambda x: x[1]["cv_mean"])
        print(f"Best Model: {best_survival[0]}")
        print(f"R² Score: {best_survival[1]['r2_score']:.4f}")
        print(f"MAE: {best_survival[1]['mae']:.4f}")
        print(f"CV R²: {best_survival[1]['cv_mean']:.4f}")
        print(
            f"Performance: {'Excellent' if best_survival[1]['r2_score'] > 0.95 else 'Good' if best_survival[1]['r2_score'] > 0.8 else 'Needs Improvement'}"
        )
        print()

    # Symptom Severity Performance
    if "symptom" in results:
        print("SYMPTOM SEVERITY PREDICTION")
        print("=" * 50)
        symptom_results = results["symptom"]
        best_symptom = max(symptom_results.items(), key=lambda x: x[1]["cv_mean"])
        print(f"Best Model: {best_symptom[0]}")
        print(f"R² Score: {best_symptom[1]['r2_score']:.4f}")
        print(f"MAE: {best_symptom[1]['mae']:.4f}")
        print(f"CV R²: {best_symptom[1]['cv_mean']:.4f}")
        print(
            f"Performance: {'Excellent' if best_symptom[1]['r2_score'] > 0.8 else 'Good' if best_symptom[1]['r2_score'] > 0.6 else 'Needs Improvement'}"
        )
        print()


def create_performance_visualizations(results):
    """Create comprehensive performance visualizations."""
    print("Generating Performance Visualizations...")

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("MenoBalance AI Model Performance Dashboard", fontsize=16, fontweight="bold")

    # 1. Classification Performance
    if "classification" in results:
        ax1 = axes[0, 0]
        class_results = results["classification"]
        models = list(class_results.keys())
        accuracies = [class_results[m]["accuracy"] for m in models]
        f1_scores = [class_results[m]["f1_score"] for m in models]

        x = range(len(models))
        width = 0.35

        ax1.bar([i - width / 2 for i in x], accuracies, width, label="Accuracy", alpha=0.8)
        ax1.bar([i + width / 2 for i in x], f1_scores, width, label="F1 Score", alpha=0.8)

        ax1.set_title("Classification Performance")
        ax1.set_ylabel("Score")
        ax1.set_xticks(x)
        ax1.set_xticklabels(models, rotation=45)
        ax1.legend()
        ax1.set_ylim(0, 1)

    # 2. Survival Performance
    if "survival" in results:
        ax2 = axes[0, 1]
        survival_results = results["survival"]
        models = list(survival_results.keys())
        r2_scores = [survival_results[m]["r2_score"] for m in models]

        ax2.bar(models, r2_scores, color="skyblue", alpha=0.7)
        ax2.set_title("Survival Analysis - R² Scores")
        ax2.set_ylabel("R² Score")
        ax2.tick_params(axis="x", rotation=45)
        ax2.set_ylim(0, 1)

    # 3. Symptom Performance
    if "symptom" in results:
        ax3 = axes[1, 0]
        symptom_results = results["symptom"]
        models = list(symptom_results.keys())
        r2_scores = [symptom_results[m]["r2_score"] for m in models]

        ax3.bar(models, r2_scores, color="lightcoral", alpha=0.7)
        ax3.set_title("Symptom Severity - R² Scores")
        ax3.set_ylabel("R² Score")
        ax3.tick_params(axis="x", rotation=45)
        ax3.set_ylim(0, 1)

    # 4. Cross-Validation Comparison
    ax4 = axes[1, 1]
    all_cv_scores = []
    all_models = []
    all_tasks = []

    for task, task_results in results.items():
        for model_name, metrics in task_results.items():
            all_cv_scores.append(metrics["cv_mean"])
            all_models.append(f"{model_name}")
            all_tasks.append(task)

    if all_cv_scores:
        scatter = ax4.scatter(
            all_models,
            all_cv_scores,
            c=[hash(task) for task in all_tasks],
            cmap="viridis",
            alpha=0.7,
            s=100,
        )
        ax4.set_title("Cross-Validation Scores Comparison")
        ax4.set_ylabel("CV Score")
        ax4.tick_params(axis="x", rotation=45)
        ax4.set_ylim(0, 1)

    plt.tight_layout()

    # Save the plot
    os.makedirs("reports", exist_ok=True)
    plt.savefig("reports/performance_dashboard.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("Performance visualizations saved to reports/performance_dashboard.png")


def generate_medical_insights(results):
    """Generate medical insights and recommendations."""
    print("\nMEDICAL INSIGHTS & RECOMMENDATIONS")
    print("=" * 50)

    insights = []

    # Classification insights
    if "classification" in results:
        class_results = results["classification"]
        best_class = max(class_results.items(), key=lambda x: x[1]["cv_mean"])
        accuracy = best_class[1]["accuracy"]

        if accuracy > 0.9:
            insights.append(
                "Menopause stage prediction is highly accurate - suitable for clinical decision support"
            )
        elif accuracy > 0.8:
            insights.append(
                "Menopause stage prediction is good but could benefit from more training data"
            )
        else:
            insights.append(
                "Menopause stage prediction needs improvement - consider feature engineering"
            )

    # Survival insights
    if "survival" in results:
        survival_results = results["survival"]
        best_survival = max(survival_results.items(), key=lambda x: x[1]["cv_mean"])
        r2 = best_survival[1]["r2_score"]

        if r2 > 0.8:
            insights.append(
                "Age/risk prediction is highly reliable - good for personalized care planning"
            )
        elif r2 > 0.6:
            insights.append("Age/risk prediction is moderate - consider additional risk factors")
        else:
            insights.append("Age/risk prediction needs improvement - review feature selection")

    # Symptom insights
    if "symptom" in results:
        symptom_results = results["symptom"]
        best_symptom = max(symptom_results.items(), key=lambda x: x[1]["cv_mean"])
        r2 = best_symptom[1]["r2_score"]

        if r2 > 0.7:
            insights.append(
                "Symptom severity prediction is accurate - useful for treatment planning"
            )
        elif r2 > 0.5:
            insights.append(
                "Symptom severity prediction is moderate - consider patient-reported outcomes"
            )
        else:
            insights.append(
                "Symptom severity prediction needs improvement - focus on symptom-specific features"
            )

    for insight in insights:
        print(insight)

    print("\nRECOMMENDATIONS:")
    print("• Use balanced datasets for better generalization")
    print("• Consider ensemble methods for improved robustness")
    print("• Validate models on diverse patient populations")
    print("• Monitor model performance over time")
    print("• Implement explainable AI for clinical transparency")


def save_detailed_report(results):
    """Save detailed report to JSON file."""
    report_data = {"timestamp": datetime.now().isoformat(), "summary": {}, "detailed_results": {}}

    # Add summary statistics and clean results for JSON serialization
    for task, task_results in results.items():
        if task_results:
            best_model = max(task_results.items(), key=lambda x: x[1]["cv_mean"])
            report_data["summary"][task] = {
                "best_model": best_model[0],
                "best_cv_score": best_model[1]["cv_mean"],
                "total_models": len(task_results),
            }

            # Clean results for JSON serialization (remove model objects)
            clean_results = {}
            for model_name, metrics in task_results.items():
                clean_results[model_name] = {
                    k: v
                    for k, v in metrics.items()
                    if k not in ["model", "predictions", "confusion_matrix"]
                }
            report_data["detailed_results"][task] = clean_results

    # Save to file
    os.makedirs("reports", exist_ok=True)
    with open("reports/performance_report.json", "w") as f:
        json.dump(report_data, f, indent=2)

    print("Detailed report saved to reports/performance_report.json")


def main():
    """Main function to generate comprehensive performance report."""
    print("Generating Comprehensive Performance Report...")

    # Load results
    results = load_training_results()
    if results is None:
        return

    # Generate summary
    generate_performance_summary(results)

    # Create visualizations
    create_performance_visualizations(results)

    # Generate medical insights
    generate_medical_insights(results)

    # Save detailed report
    save_detailed_report(results)

    print("\nPerformance report generation completed!")
    print("Files generated:")
    print("  - reports/performance_dashboard.png")
    print("  - reports/performance_report.json")


if __name__ == "__main__":
    main()
