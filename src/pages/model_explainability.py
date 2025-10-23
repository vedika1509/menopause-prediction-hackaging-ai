"""
Model Explainability Page for MenoBalance AI
Provides SHAP visualizations and feature importance analysis
"""

import os

# Add project root to path
import sys

import plotly.graph_objects as go
import streamlit as st
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def load_shap_visualizations():
    """Load SHAP visualization images if available."""
    shap_images = {}
    shap_dir = "reports/shap"

    if os.path.exists(shap_dir):
        # Load available SHAP plots
        plots = {
            "classification": [
                "classification_feature_importance.png",
                "classification_summary_plot.png",
            ],
            "survival": ["survival_feature_importance.png", "survival_summary_plot.png"],
            "symptom": ["symptom_feature_importance.png", "symptom_summary_plot.png"],
            "interaction": ["feature_interaction_analysis.png"],
        }

        for model_type, plot_files in plots.items():
            for plot_file in plot_files:
                plot_path = os.path.join(shap_dir, plot_file)
                if os.path.exists(plot_path):
                    if model_type not in shap_images:
                        shap_images[model_type] = []
                    shap_images[model_type].append(
                        {
                            "name": plot_file.replace(".png", "").replace("_", " ").title(),
                            "path": plot_path,
                        }
                    )

    return shap_images


def create_feature_importance_chart():
    """Create an interactive feature importance chart."""
    # Sample feature importance data (in real implementation, this would come from the model)
    features = [
        "Age",
        "AMH Level",
        "FSH Level",
        "BMI",
        "Estradiol",
        "Smoking History",
        "Family History",
        "Exercise Frequency",
        "Stress Level",
        "Sleep Quality",
    ]

    importance_scores = [0.25, 0.22, 0.18, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01]

    # Create horizontal bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=features,
            x=importance_scores,
            orientation="h",
            marker=dict(
                color=importance_scores,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Importance Score"),
            ),
            text=[f"{score:.3f}" for score in importance_scores],
            textposition="auto",
        )
    )

    fig.update_layout(
        title="Feature Importance Analysis",
        xaxis_title="Importance Score",
        yaxis_title="Features",
        height=500,
        showlegend=False,
    )

    return fig


def create_model_performance_dashboard():
    """Create a comprehensive model performance dashboard."""
    # Sample performance data
    models = ["Survival Analysis", "Symptom Prediction", "Classification"]
    metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]

    # Create performance matrix
    performance_data = {
        "Survival Analysis": [0.95, 0.92, 0.94, 0.93],
        "Symptom Prediction": [0.88, 0.85, 0.87, 0.86],
        "Classification": [0.92, 0.90, 0.91, 0.90],
    }

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=[performance_data[model] for model in models],
            x=metrics,
            y=models,
            colorscale="RdYlGn",
            showscale=True,
            colorbar=dict(title="Score"),
        )
    )

    fig.update_layout(
        title="Model Performance Comparison",
        xaxis_title="Metrics",
        yaxis_title="Models",
        height=400,
    )

    return fig


def create_confidence_interval_visualization():
    """Create visualization showing confidence intervals for predictions."""
    # Sample prediction data with confidence intervals
    predictions = ["Time to Menopause", "Symptom Severity", "Stage Classification"]
    point_estimates = [3.2, 6.5, 0.68]
    lower_bounds = [2.0, 5.0, 0.55]
    upper_bounds = [4.5, 8.0, 0.81]

    fig = go.Figure()

    for i, (pred, point, lower, upper) in enumerate(
        zip(predictions, point_estimates, lower_bounds, upper_bounds)
    ):
        fig.add_trace(
            go.Scatter(
                x=[point],
                y=[pred],
                mode="markers",
                marker=dict(
                    size=10, color=f"rgba({50 + i * 50}, {100 + i * 30}, {150 + i * 20}, 0.8)"
                ),
                name=f"{pred} (Point Estimate)",
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[lower, upper],
                y=[pred, pred],
                mode="lines",
                line=dict(
                    color=f"rgba({50 + i * 50}, {100 + i * 30}, {150 + i * 20}, 0.6)", width=3
                ),
                name=f"{pred} (95% CI)",
                showlegend=True,
            )
        )

    fig.update_layout(
        title="Prediction Confidence Intervals",
        xaxis_title="Predicted Value",
        yaxis_title="Prediction Type",
        height=400,
    )

    return fig


def render_model_explainability():
    """Render the model explainability page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--foreground); margin-bottom: 0.5rem;">🔍 Model Explainability</h1>
            <p style="color: var(--text-muted);">Understand how our AI models make predictions and what factors influence your results</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load SHAP visualizations
    shap_images = load_shap_visualizations()

    # Model Performance Overview
    st.markdown("### 📊 Model Performance Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Performance Metrics")
        perf_fig = create_model_performance_dashboard()
        st.plotly_chart(perf_fig, use_container_width=True)

    with col2:
        st.markdown("#### Confidence Intervals")
        conf_fig = create_confidence_interval_visualization()
        st.plotly_chart(conf_fig, use_container_width=True)

    # Feature Importance Analysis
    st.markdown("### 🎯 Feature Importance Analysis")

    st.markdown(
        """
        <div class="pastel-card">
            <h4>Understanding Feature Importance</h4>
            <p>Feature importance shows which factors have the most influence on our predictions. 
            Higher scores indicate stronger predictive power for that feature.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Interactive feature importance chart
    importance_fig = create_feature_importance_chart()
    st.plotly_chart(importance_fig, use_container_width=True)

    # SHAP Visualizations
    if shap_images:
        st.markdown("### 🔬 SHAP Analysis")

        st.markdown(
            """
            <div class="pastel-card">
                <h4>What is SHAP?</h4>
                <p>SHAP (SHapley Additive exPlanations) provides a unified framework for explaining 
                model predictions. It shows how each feature contributes to the final prediction.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Display available SHAP plots
        for model_type, plots in shap_images.items():
            if plots:
                st.markdown(f"#### {model_type.title()} Model Analysis")

                cols = st.columns(min(len(plots), 2))
                for i, plot in enumerate(plots):
                    with cols[i % 2]:
                        try:
                            image = Image.open(plot["path"])
                            st.image(image, caption=plot["name"], use_column_width=True)
                        except Exception as e:
                            st.error(f"Error loading {plot['name']}: {str(e)}")
    else:
        st.markdown(
            """
            <div class="pastel-card" style="text-align: center; padding: 2rem;">
                <h3 style="color: var(--text-muted); margin-bottom: 1rem;">SHAP Analysis Not Available</h3>
                <p style="color: var(--text-muted);">Run the SHAP analysis script to generate explainability visualizations</p>
                <p style="color: var(--text-muted);">Command: <code>python src/explainability_shap.py</code></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Model Interpretability Guidelines
    st.markdown("### 📖 How to Interpret the Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="mint-card" style="padding: 1.5rem;">
                <h4>🎯 Feature Importance</h4>
                <ul>
                    <li><strong>High Importance:</strong> Features that strongly influence predictions</li>
                    <li><strong>Medium Importance:</strong> Features with moderate influence</li>
                    <li><strong>Low Importance:</strong> Features with minimal influence</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="lavender-card" style="padding: 1.5rem;">
                <h4>📊 Confidence Intervals</h4>
                <ul>
                    <li><strong>Narrow CI:</strong> High confidence in prediction</li>
                    <li><strong>Wide CI:</strong> Lower confidence, more uncertainty</li>
                    <li><strong>95% CI:</strong> Range where true value likely falls</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Model Limitations and Biases
    st.markdown("### ⚠️ Model Limitations and Considerations")

    st.markdown(
        """
        <div class="coral-card" style="padding: 1.5rem;">
            <h4>Important Limitations</h4>
            <ul>
                <li><strong>Training Data:</strong> Models trained on synthetic data, not real clinical outcomes</li>
                <li><strong>Population Bias:</strong> May not represent all demographic groups equally</li>
                <li><strong>Individual Variation:</strong> Cannot account for all personal health factors</li>
                <li><strong>Clinical Validation:</strong> Requires validation with real patient data</li>
            </ul>
            <p><strong>Remember:</strong> These predictions are for educational purposes only and should not replace professional medical advice.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Technical Details
    with st.expander("🔧 Technical Implementation Details"):
        st.markdown(
            """
            **Model Architecture:**
            - **Survival Analysis:** CatBoost with Cox Proportional Hazards
            - **Symptom Prediction:** XGBoost Multi-output Regression
            - **Classification:** XGBoost with Logistic Regression
            
            **Feature Engineering:**
            - StandardScaler for normalization
            - Median imputation for missing values
            - Feature selection using mutual information
            
            **Validation:**
            - GroupKFold cross-validation
            - Stratified train-test split
            - Data source grouping for robustness
            """
        )

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render_model_explainability()
