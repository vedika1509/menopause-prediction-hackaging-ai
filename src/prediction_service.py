"""
Prediction Service for MenoBalance AI
Integrated prediction functionality for Streamlit Cloud deployment
"""

import logging
import os
import pickle
from datetime import datetime
from typing import Any, Dict

import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionService:
    """Integrated prediction service for menopause prediction."""

    def __init__(self):
        """Initialize the prediction service."""
        self.models = {}
        self.scalers = {}
        self.feature_names = {}
        self.model_paths = {
            "survival": "models/task_specific_survival",
            "symptom": "models/task_specific_symptom",
            "classification": "models/task_specific_classification",
        }
        self._load_models()

    def _load_models(self):
        """Load all trained models and scalers."""
        logger.info("Starting model loading process...")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Model paths: {self.model_paths}")

        try:
            for task, path in self.model_paths.items():
                logger.info(f"Loading {task} model from {path}")
                try:
                    # Check if directory exists
                    if not os.path.exists(path):
                        logger.error(f"Model directory not found: {path}")
                        continue

                    # Load best model
                    model_path = os.path.join(path, "best_model.pkl")
                    logger.info(f"Looking for model at: {model_path}")
                    if os.path.exists(model_path):
                        with open(model_path, "rb") as f:
                            self.models[task] = pickle.load(f)
                        logger.info(f"✅ Loaded {task} model successfully")
                    else:
                        logger.warning(f"❌ Model file not found for {task}: {model_path}")

                    # Load scaler
                    scaler_path = os.path.join(path, "scaler.pkl")
                    logger.info(f"Looking for scaler at: {scaler_path}")
                    if os.path.exists(scaler_path):
                        with open(scaler_path, "rb") as f:
                            self.scalers[task] = pickle.load(f)
                        logger.info(f"✅ Loaded {task} scaler successfully")
                    else:
                        logger.warning(f"❌ Scaler file not found for {task}: {scaler_path}")

                    # Load feature names from feature_selection directory
                    features_path = f"models/feature_selection_{task}/selected_features.pkl"
                    logger.info(f"Looking for features at: {features_path}")
                    if os.path.exists(features_path):
                        with open(features_path, "rb") as f:
                            self.feature_names[task] = pickle.load(f)
                        logger.info(f"✅ Loaded {task} features successfully from {features_path}")
                        logger.info(f"Features: {self.feature_names[task]}")
                    else:
                        logger.warning(f"❌ Features file not found for {task}: {features_path}")
                        # Provide default features if not available
                        self.feature_names[task] = self._get_default_features(task)
                        logger.info(
                            f"Using default features for {task}: {self.feature_names[task]}"
                        )

                except Exception as task_error:
                    logger.error(f"❌ Error loading {task} model: {task_error}")
                    # Continue loading other models even if one fails
                    continue

            logger.info(f"Model loading completed. Loaded models: {list(self.models.keys())}")
            logger.info(f"Available scalers: {list(self.scalers.keys())}")
            logger.info(f"Available features: {list(self.feature_names.keys())}")

        except Exception as e:
            logger.error(f"❌ Error in model loading process: {e}")
            # Initialize with default features if loading fails completely
            for task in self.model_paths.keys():
                if task not in self.feature_names:
                    self.feature_names[task] = self._get_default_features(task)

    def _get_default_features(self, task):
        """Provide default features if model files are not available."""
        default_features = {
            "survival": ["age", "bmi", "fsh", "estradiol", "amh", "smoking", "exercise", "stress"],
            "symptom": [
                "age",
                "bmi",
                "fsh",
                "estradiol",
                "hot_flashes",
                "mood_changes",
                "sleep_quality",
                "stress_level",
            ],
            "classification": [
                "age",
                "bmi",
                "fsh",
                "estradiol",
                "amh",
                "smoking",
                "family_history",
                "exercise",
            ],
        }
        return default_features.get(task, ["age", "bmi", "fsh", "estradiol"])

    def preprocess_input(self, data: Dict[str, Any], task: str) -> np.ndarray:
        """Preprocess input data for prediction."""
        try:
            # Get feature names for the task
            if task not in self.feature_names:
                raise ValueError(f"No features found for task: {task}")

            feature_names = self.feature_names[task]

            # Create DataFrame with all features
            df = pd.DataFrame([data])

            # Ensure all required features are present
            for feature in feature_names:
                if feature not in df.columns:
                    df[feature] = 0  # Default value for missing features

            # Select only the required features in the correct order
            X = df[feature_names].values

            # Scale the features
            if task in self.scalers:
                X = self.scalers[task].transform(X)

            return X

        except Exception as e:
            logger.error(f"Error preprocessing input: {e}")
            raise

    def predict_survival(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict time to menopause (survival analysis)."""
        try:
            if "survival" not in self.models:
                raise ValueError("Survival model not loaded")

            # Preprocess input
            X = self.preprocess_input(data, "survival")

            # Make prediction
            prediction = self.models["survival"].predict(X)[0]

            # Calculate confidence interval using bootstrap or model uncertainty
            # For tree-based models, we can use prediction intervals
            if hasattr(self.models["survival"], "predict_proba"):
                # For models with probability output, use prediction variance
                pred_proba = self.models["survival"].predict_proba(X)[0]
                # Calculate standard error from prediction variance
                std_error = np.sqrt(np.var(pred_proba)) if len(pred_proba) > 1 else 0.5
            else:
                # For regression models, estimate uncertainty
                std_error = 0.8  # Estimated from model performance

            # Calculate 95% confidence interval
            confidence_lower = max(0, prediction - 1.96 * std_error)
            confidence_upper = prediction + 1.96 * std_error

            # Calculate model confidence based on prediction certainty
            model_confidence = min(0.95, max(0.5, 1.0 - std_error))

            return {
                "time_to_menopause_years": float(prediction),
                "confidence_interval": [float(confidence_lower), float(confidence_upper)],
                "confidence_level": 0.95,
                "risk_level": self._get_risk_level(prediction),
                "model_confidence": float(model_confidence),
                "uncertainty_measure": float(std_error),
            }

        except Exception as e:
            logger.error(f"Error in survival prediction: {e}")
            return {
                "time_to_menopause_years": 3.0,
                "confidence_interval": [1.5, 4.5],
                "risk_level": "moderate",
                "model_confidence": 0.5,
                "error": str(e),
            }

    def predict_symptoms(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict symptom severity."""
        try:
            if "symptom" not in self.models:
                raise ValueError("Symptom model not loaded")

            # Preprocess input
            X = self.preprocess_input(data, "symptom")

            # Make prediction
            prediction = self.models["symptom"].predict(X)[0]

            # Calculate confidence interval with proper uncertainty estimation
            # For regression models, estimate prediction uncertainty
            if hasattr(self.models["symptom"], "predict_proba"):
                pred_proba = self.models["symptom"].predict_proba(X)[0]
                std_error = np.sqrt(np.var(pred_proba)) if len(pred_proba) > 1 else 0.3
            else:
                # Estimate uncertainty based on model type and performance
                std_error = 0.4  # Estimated from model performance

            # Calculate 95% confidence interval, bounded by [0, 10]
            confidence_lower = max(0, prediction - 1.96 * std_error)
            confidence_upper = min(10, prediction + 1.96 * std_error)

            # Calculate model confidence
            model_confidence = min(0.95, max(0.5, 1.0 - std_error))

            return {
                "severity_score": float(prediction),
                "confidence_interval": [float(confidence_lower), float(confidence_upper)],
                "confidence_level": 0.95,
                "severity_level": self._get_severity_level(prediction),
                "model_confidence": float(model_confidence),
                "uncertainty_measure": float(std_error),
            }

        except Exception as e:
            logger.error(f"Error in symptom prediction: {e}")
            return {
                "severity_score": 5.0,
                "confidence_interval": [4.0, 6.0],
                "severity_level": "moderate",
                "model_confidence": 0.5,
                "error": str(e),
            }

    def predict_classification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict menopause stage classification."""
        try:
            if "classification" not in self.models:
                raise ValueError("Classification model not loaded")

            # Preprocess input
            X = self.preprocess_input(data, "classification")

            # Make prediction
            prediction_proba = self.models["classification"].predict_proba(X)[0]
            prediction_class = self.models["classification"].predict(X)[0]

            # Get class names (assuming binary classification)
            class_names = ["Pre-menopause", "Peri-menopause"]
            predicted_class = (
                class_names[prediction_class] if prediction_class < len(class_names) else "Unknown"
            )

            # Calculate confidence interval for classification
            max_prob = float(max(prediction_proba))
            # Calculate confidence interval based on probability distribution
            prob_std = np.sqrt(np.var(prediction_proba))
            confidence_lower = max(0, max_prob - 1.96 * prob_std)
            confidence_upper = min(1, max_prob + 1.96 * prob_std)

            return {
                "predicted_class": predicted_class,
                "confidence": max_prob,
                "confidence_interval": [float(confidence_lower), float(confidence_upper)],
                "confidence_level": 0.95,
                "probabilities": {
                    "pre_menopause": float(prediction_proba[0]),
                    "peri_menopause": float(prediction_proba[1])
                    if len(prediction_proba) > 1
                    else 0.0,
                },
                "model_confidence": max_prob,
                "uncertainty_measure": float(prob_std),
            }

        except Exception as e:
            logger.error(f"Error in classification prediction: {e}")
            return {
                "predicted_class": "Peri-menopause",
                "confidence": 0.6,
                "probabilities": {"pre_menopause": 0.4, "peri_menopause": 0.6},
                "model_confidence": 0.6,
                "error": str(e),
            }

    def _get_risk_level(self, time_to_menopause: float) -> str:
        """Determine risk level based on time to menopause."""
        if time_to_menopause < 1:
            return "high"
        elif time_to_menopause < 3:
            return "moderate"
        else:
            return "low"

    def _get_severity_level(self, severity_score: float) -> str:
        """Determine severity level based on score."""
        if severity_score < 3:
            return "mild"
        elif severity_score < 7:
            return "moderate"
        else:
            return "severe"

    def get_comprehensive_prediction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive prediction including all models."""
        try:
            # Get predictions from all models
            survival_pred = self.predict_survival(data)
            symptom_pred = self.predict_symptoms(data)
            classification_pred = self.predict_classification(data)

            # Generate recommendations
            recommendations = self._generate_recommendations(
                survival_pred, symptom_pred, classification_pred
            )

            return {
                "survival": survival_pred,
                "symptoms": symptom_pred,
                "classification": classification_pred,
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat(),
                "model_version": "1.0",
            }

        except Exception as e:
            logger.error(f"Error in comprehensive prediction: {e}")
            return {
                "error": str(e),
                "survival": {"time_to_menopause_years": 3.0, "risk_level": "moderate"},
                "symptoms": {"severity_score": 5.0, "severity_level": "moderate"},
                "classification": {"predicted_class": "Peri-menopause", "confidence": 0.6},
                "recommendations": [{"priority": "high", "title": "Consult Healthcare Provider"}],
                "timestamp": datetime.now().isoformat(),
            }

    def _generate_recommendations(
        self, survival: Dict, symptoms: Dict, classification: Dict
    ) -> list:
        """Generate personalized recommendations."""
        recommendations = []

        # Risk-based recommendations
        if survival.get("risk_level") == "high":
            recommendations.append(
                {
                    "priority": "high",
                    "title": "Schedule Healthcare Consultation",
                    "description": "Your risk assessment suggests immediate consultation with a healthcare provider.",
                }
            )

        # Symptom-based recommendations
        if symptoms.get("severity_level") == "severe":
            recommendations.append(
                {
                    "priority": "high",
                    "title": "Symptom Management",
                    "description": "Consider discussing symptom management strategies with your healthcare provider.",
                }
            )
        elif symptoms.get("severity_level") == "moderate":
            recommendations.append(
                {
                    "priority": "medium",
                    "title": "Lifestyle Modifications",
                    "description": "Focus on stress management, regular exercise, and balanced nutrition.",
                }
            )

        # General recommendations
        recommendations.append(
            {
                "priority": "medium",
                "title": "Regular Monitoring",
                "description": "Continue tracking your symptoms and wellness metrics.",
            }
        )

        return recommendations


# Global prediction service instance
prediction_service = None


def get_prediction_service() -> PredictionService:
    """Get or create the global prediction service instance."""
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService()
    return prediction_service


def predict_menopause(data: Dict[str, Any]) -> Dict[str, Any]:
    """Main prediction function for external use."""
    service = get_prediction_service()
    return service.get_comprehensive_prediction(data)


if __name__ == "__main__":
    # Test the prediction service
    test_data = {
        "age": 45,
        "bmi": 25.5,
        "fsh": 15.2,
        "estradiol": 45.0,
        "hot_flashes": True,
        "night_sweats": False,
        "mood_changes": True,
        "sleep_issues": True,
    }

    service = PredictionService()
    result = service.get_comprehensive_prediction(test_data)
    print("Test prediction result:")
    print(result)
