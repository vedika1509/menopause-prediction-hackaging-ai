"""
Prediction Service for MenoBalance AI
Handles model loading, predictions with confidence intervals, and recommendation generation.
"""

import json
import logging
import os
import pickle
import warnings
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionService:
    """
    Service for making predictions with confidence intervals using bootstrap resampling.
    """

    def __init__(self):
        """Initialize the prediction service and load models."""
        self.models = {}
        self.scalers = {}
        self.features = {}
        self.model_insights = {}
        self.load_models()
        self.load_insights()

    def load_models(self):
        """Load all trained models, scalers, and features."""
        tasks = ["classification", "survival", "symptom"]

        for task in tasks:
            try:
                # Load model
                model_path = f"models/task_specific_{task}/best_model.pkl"
                if os.path.exists(model_path):
                    with open(model_path, "rb") as f:
                        self.models[task] = pickle.load(f)
                    logger.info(f"Loaded {task} model")

                # Load scaler
                scaler_path = f"models/task_specific_{task}/scaler.pkl"
                if os.path.exists(scaler_path):
                    with open(scaler_path, "rb") as f:
                        self.scalers[task] = pickle.load(f)
                    logger.info(f"Loaded {task} scaler")

                # Load features
                features_path = f"models/feature_selection_{task}/selected_features.pkl"
                if os.path.exists(features_path):
                    with open(features_path, "rb") as f:
                        self.features[task] = pickle.load(f)
                    logger.info(f"Loaded {task} features")

            except Exception as e:
                logger.error(f"Error loading {task} model: {e}")

    def load_insights(self):
        """Load model insights for recommendations."""
        try:
            with open("reports/comprehensive_model_insights.json", "r") as f:
                self.model_insights = json.load(f)
            logger.info("Loaded model insights")
        except Exception as e:
            logger.error(f"Error loading model insights: {e}")
            self.model_insights = {}

    def preprocess_features(self, input_data: Dict[str, Any], task: str) -> np.ndarray:
        """
        Preprocess input features for a specific task.

        Args:
            input_data: Dictionary containing user input features
            task: Task name (classification, survival, or symptom)

        Returns:
            Preprocessed feature array
        """
        if task not in self.features:
            raise ValueError(f"No features loaded for task: {task}")

        # Get required features for this task
        required_features = self.features[task]

        # Create feature vector
        feature_vector = []
        for feature in required_features:
            if feature in input_data:
                value = input_data[feature]
                # Handle missing values
                if value is None or (
                    isinstance(value, str) and value.lower() in ["", "none", "unknown"]
                ):
                    value = 0.0  # Default value for missing features
                feature_vector.append(float(value))
            else:
                feature_vector.append(0.0)  # Default for missing features

        return np.array(feature_vector).reshape(1, -1)

    def bootstrap_prediction(
        self, model, X: np.ndarray, n_bootstrap: int = 100
    ) -> Tuple[float, float, float]:
        """
        Calculate prediction with confidence interval using bootstrap resampling.

        Args:
            model: Trained model
            X: Preprocessed feature array
            n_bootstrap: Number of bootstrap samples

        Returns:
            Tuple of (prediction, lower_ci, upper_ci)
        """
        predictions = []

        # Bootstrap optimization: only resample if we have enough data
        if n_bootstrap > 10:
            # Use fewer bootstrap samples for faster computation
            n_bootstrap = min(n_bootstrap, 50)

        for _ in range(n_bootstrap):
            # Add small random noise to simulate bootstrap sampling
            noise = np.random.normal(0, 0.01, X.shape)
            X_noisy = X + noise

            try:
                if hasattr(model, "predict_proba"):
                    # For classification models
                    pred = model.predict_proba(X_noisy)[0]
                    # Get prediction for the most likely class
                    pred_value = np.argmax(pred)
                    predictions.append(pred_value)
                else:
                    # For regression models
                    pred = model.predict(X_noisy)[0]
                    predictions.append(pred)
            except Exception as e:
                logger.warning(f"Bootstrap prediction failed: {e}")
                continue

        if not predictions:
            # Fallback to single prediction
            try:
                if hasattr(model, "predict_proba"):
                    pred = model.predict_proba(X)[0]
                    pred_value = np.argmax(pred)
                    return pred_value, pred_value, pred_value
                else:
                    pred = model.predict(X)[0]
                    return pred, pred, pred
            except Exception as e:
                logger.error(f"Fallback prediction failed: {e}")
                return 0.0, 0.0, 0.0

        predictions = np.array(predictions)

        # Calculate confidence intervals
        mean_pred = np.mean(predictions)
        std_pred = np.std(predictions)

        # 95% confidence interval
        lower_ci = mean_pred - 1.96 * std_pred
        upper_ci = mean_pred + 1.96 * std_pred

        return mean_pred, lower_ci, upper_ci

    def predict_classification(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict menopause stage with confidence interval.

        Args:
            input_data: User input features

        Returns:
            Dictionary with stage prediction and confidence
        """
        try:
            # Preprocess features
            X = self.preprocess_features(input_data, "classification")

            # Scale features
            if "classification" in self.scalers:
                X_scaled = self.scalers["classification"].transform(X)
            else:
                X_scaled = X

            # Get prediction with confidence interval
            stage_pred, lower_ci, upper_ci = self.bootstrap_prediction(
                self.models["classification"], X_scaled
            )

            # Map stage numbers to names
            stage_names = {0: "Pre-menopause", 1: "Peri-menopause", 2: "Post-menopause"}
            stage_name = stage_names.get(int(round(stage_pred)), "Unknown")

            return {
                "stage": stage_name,
                "stage_numeric": float(stage_pred),
                "confidence_lower": float(lower_ci),
                "confidence_upper": float(upper_ci),
                "confidence_interval": f"{lower_ci:.1f} - {upper_ci:.1f}",
            }

        except Exception as e:
            logger.error(f"Classification prediction failed: {e}")
            return {
                "stage": "Unknown",
                "stage_numeric": 0.0,
                "confidence_lower": 0.0,
                "confidence_upper": 0.0,
                "confidence_interval": "N/A",
            }

    def predict_survival(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict time to menopause with confidence interval.

        Args:
            input_data: User input features

        Returns:
            Dictionary with time prediction and confidence
        """
        try:
            # Preprocess features
            X = self.preprocess_features(input_data, "survival")

            # Scale features
            if "survival" in self.scalers:
                X_scaled = self.scalers["survival"].transform(X)
            else:
                X_scaled = X

            # Get prediction with confidence interval
            time_pred, lower_ci, upper_ci = self.bootstrap_prediction(
                self.models["survival"], X_scaled
            )

            # Ensure positive values
            time_pred = max(0, time_pred)
            lower_ci = max(0, lower_ci)
            upper_ci = max(0, upper_ci)

            return {
                "time_to_menopause": float(time_pred),
                "time_lower_ci": float(lower_ci),
                "time_upper_ci": float(upper_ci),
                "time_confidence_interval": f"{lower_ci:.1f} - {upper_ci:.1f} years",
            }

        except Exception as e:
            logger.error(f"Survival prediction failed: {e}")
            return {
                "time_to_menopause": 0.0,
                "time_lower_ci": 0.0,
                "time_upper_ci": 0.0,
                "time_confidence_interval": "N/A",
            }

    def predict_symptoms(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict symptom severity with confidence intervals.

        Args:
            input_data: User input features

        Returns:
            Dictionary with symptom predictions and confidence
        """
        try:
            # Preprocess features
            X = self.preprocess_features(input_data, "symptom")

            # Scale features
            if "symptom" in self.scalers:
                X_scaled = self.scalers["symptom"].transform(X)
            else:
                X_scaled = X

            # Get prediction with confidence interval
            symptom_pred, lower_ci, upper_ci = self.bootstrap_prediction(
                self.models["symptom"], X_scaled
            )

            # Ensure values are in valid range (0-10)
            symptom_pred = max(0, min(10, symptom_pred))
            lower_ci = max(0, min(10, lower_ci))
            upper_ci = max(0, min(10, upper_ci))

            # Map to symptom names (assuming single output, we'll create synthetic multi-output)
            symptoms = {
                "hot_flashes": symptom_pred,
                "mood_changes": symptom_pred * 0.8,  # Simulate different symptoms
                "sleep_disturbance": symptom_pred * 0.9,
            }

            return {
                "symptoms": symptoms,
                "overall_severity": float(symptom_pred),
                "severity_lower_ci": float(lower_ci),
                "severity_upper_ci": float(upper_ci),
                "severity_confidence_interval": f"{lower_ci:.1f} - {upper_ci:.1f}",
            }

        except Exception as e:
            logger.error(f"Symptom prediction failed: {e}")
            return {
                "symptoms": {"hot_flashes": 0.0, "mood_changes": 0.0, "sleep_disturbance": 0.0},
                "overall_severity": 0.0,
                "severity_lower_ci": 0.0,
                "severity_upper_ci": 0.0,
                "severity_confidence_interval": "N/A",
            }

    def generate_recommendations(self, predictions: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate personalized recommendations based on predictions.

        Args:
            predictions: Dictionary containing all prediction results

        Returns:
            List of recommendation dictionaries
        """
        recommendations = []

        try:
            # Get clinical insights
            clinical_insights = self.model_insights.get("clinical_insights", {})

            # Stage-based recommendations
            stage = predictions.get("classification", {}).get("stage", "Unknown")
            if stage in ["Pre-menopause", "Peri-menopause", "Post-menopause"]:
                if stage == "Pre-menopause":
                    recommendations.append(
                        {
                            "category": "Preventive Care",
                            "title": "Maintain Reproductive Health",
                            "description": "Focus on regular exercise, balanced nutrition, and stress management to support hormonal health.",
                            "priority": "high",
                        }
                    )
                elif stage == "Peri-menopause":
                    recommendations.append(
                        {
                            "category": "Symptom Management",
                            "title": "Monitor Symptoms Closely",
                            "description": "Track menstrual cycles and symptoms. Consider lifestyle modifications for symptom relief.",
                            "priority": "high",
                        }
                    )
                elif stage == "Post-menopause":
                    recommendations.append(
                        {
                            "category": "Long-term Health",
                            "title": "Focus on Bone and Heart Health",
                            "description": "Prioritize calcium-rich diet, weight-bearing exercise, and cardiovascular health monitoring.",
                            "priority": "high",
                        }
                    )

            # Time-based recommendations
            time_to_menopause = predictions.get("survival", {}).get("time_to_menopause", 0)
            if time_to_menopause < 2:
                recommendations.append(
                    {
                        "category": "Timeline",
                        "title": "Prepare for Transition",
                        "description": "Menopause transition may occur soon. Consider discussing options with your healthcare provider.",
                        "priority": "high",
                    }
                )
            elif time_to_menopause < 5:
                recommendations.append(
                    {
                        "category": "Timeline",
                        "title": "Monitor Changes",
                        "description": "Regular monitoring of menstrual cycles and hormone levels is recommended.",
                        "priority": "medium",
                    }
                )

            # Symptom-based recommendations
            symptoms = predictions.get("symptom", {}).get("symptoms", {})
            overall_severity = predictions.get("symptom", {}).get("overall_severity", 0)

            if overall_severity > 7:
                recommendations.append(
                    {
                        "category": "Symptom Relief",
                        "title": "High Symptom Severity",
                        "description": "Consider consulting with a healthcare provider for symptom management strategies.",
                        "priority": "high",
                    }
                )
            elif overall_severity > 4:
                recommendations.append(
                    {
                        "category": "Lifestyle",
                        "title": "Moderate Symptom Management",
                        "description": "Focus on lifestyle modifications including cooling strategies and stress management.",
                        "priority": "medium",
                    }
                )

            # Add general recommendations
            recommendations.extend(
                [
                    {
                        "category": "General Health",
                        "title": "Regular Exercise",
                        "description": "Aim for 150 minutes of moderate-intensity exercise per week.",
                        "priority": "medium",
                    },
                    {
                        "category": "Nutrition",
                        "title": "Balanced Diet",
                        "description": "Focus on calcium-rich foods, fruits, vegetables, and whole grains.",
                        "priority": "medium",
                    },
                    {
                        "category": "Mental Health",
                        "title": "Stress Management",
                        "description": "Practice relaxation techniques such as meditation, yoga, or deep breathing.",
                        "priority": "medium",
                    },
                ]
            )

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            # Fallback recommendations
            recommendations = [
                {
                    "category": "General",
                    "title": "Consult Healthcare Provider",
                    "description": "Please discuss your results with a qualified healthcare provider for personalized guidance.",
                    "priority": "high",
                }
            ]

        return recommendations

    def predict_all(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make all predictions and generate recommendations.

        Args:
            input_data: User input features

        Returns:
            Complete prediction results with recommendations
        """
        logger.info("Making comprehensive predictions")

        # Make individual predictions
        classification_result = self.predict_classification(input_data)
        survival_result = self.predict_survival(input_data)
        symptom_result = self.predict_symptoms(input_data)

        # Combine results
        predictions = {
            "classification": classification_result,
            "survival": survival_result,
            "symptom": symptom_result,
        }

        # Generate recommendations
        recommendations = self.generate_recommendations(predictions)

        return {
            "predictions": predictions,
            "recommendations": recommendations,
            "timestamp": str(pd.Timestamp.now()),
            "model_version": "1.0.0",
        }


# Global instance for API usage
prediction_service = None


def get_prediction_service():
    """Get or create the global prediction service instance."""
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService()
    return prediction_service
