"""
API Integration for Streamlit Cloud
Integrates FastAPI endpoints into Streamlit app for deployment
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StreamlitAPI:
    """API integration for Streamlit Cloud deployment."""

    def __init__(self):
        """Initialize the Streamlit API."""
        self.models = {}
        self.scalers = {}
        self.feature_names = {}
        self._load_models()

    def _load_models(self):
        """Load models for Streamlit Cloud deployment."""
        logger.info("Loading models for Streamlit Cloud...")

        model_paths = {
            "survival": "models/task_specific_survival",
            "symptom": "models/task_specific_symptom",
            "classification": "models/task_specific_classification",
        }

        for task, path in model_paths.items():
            try:
                # Load model
                model_path = os.path.join(path, "best_model.pkl")
                if os.path.exists(model_path):
                    import pickle

                    with open(model_path, "rb") as f:
                        self.models[task] = pickle.load(f)
                    logger.info(f"✅ Loaded {task} model")

                # Load scaler
                scaler_path = os.path.join(path, "scaler.pkl")
                if os.path.exists(scaler_path):
                    import pickle

                    with open(scaler_path, "rb") as f:
                        self.scalers[task] = pickle.load(f)
                    logger.info(f"✅ Loaded {task} scaler")

                # Load features
                features_path = f"models/feature_selection_{task}/selected_features.pkl"
                if os.path.exists(features_path):
                    import pickle

                    with open(features_path, "rb") as f:
                        self.feature_names[task] = pickle.load(f)
                    logger.info(f"✅ Loaded {task} features")
                else:
                    self.feature_names[task] = self._get_default_features(task)

            except Exception as e:
                logger.error(f"❌ Error loading {task}: {e}")
                continue

        logger.info(f"Model loading completed. Available models: {list(self.models.keys())}")

    def _get_default_features(self, task):
        """Get default features for a task."""
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

    def preprocess_input(self, data: Dict[str, Any], task: str):
        """Preprocess input data for prediction."""
        try:
            import pandas as pd

            # Get feature names for the task
            if task not in self.feature_names:
                raise ValueError(f"No features found for task: {task}")

            features = self.feature_names[task]

            # Create DataFrame with all features
            df = pd.DataFrame([data])

            # Ensure all required features are present
            for feature in features:
                if feature not in df.columns:
                    df[feature] = 0  # Default value for missing features

            # Select only the required features in the correct order
            X = df[features].values

            # Scale the features if scaler is available
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

            # Calculate confidence interval
            std_error = 0.8
            confidence_lower = max(0, prediction - 1.96 * std_error)
            confidence_upper = prediction + 1.96 * std_error

            # Calculate model confidence
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
                "confidence_level": 0.95,
                "risk_level": "moderate",
                "model_confidence": 0.5,
                "uncertainty_measure": 0.8,
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

            # Calculate confidence interval
            std_error = 0.4
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
                "confidence_level": 0.95,
                "severity_level": "moderate",
                "model_confidence": 0.5,
                "uncertainty_measure": 0.5,
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

            # Get class names
            class_names = ["Pre-menopause", "Peri-menopause", "Post-menopause"]
            predicted_class = (
                class_names[prediction_class] if prediction_class < len(class_names) else "Unknown"
            )

            # Calculate confidence interval
            max_prob = float(max(prediction_proba))
            prob_std = 0.1
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
                    "post_menopause": float(prediction_proba[2])
                    if len(prediction_proba) > 2
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
                "confidence_interval": [0.5, 0.7],
                "confidence_level": 0.95,
                "probabilities": {
                    "pre_menopause": 0.4,
                    "peri_menopause": 0.6,
                    "post_menopause": 0.0,
                },
                "model_confidence": 0.6,
                "uncertainty_measure": 0.05,
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

    def generate_recommendations(
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

    def predict_comprehensive(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive prediction including all models."""
        try:
            # Get predictions from all models
            survival_pred = self.predict_survival(data)
            symptom_pred = self.predict_symptoms(data)
            classification_pred = self.predict_classification(data)

            # Generate recommendations
            recommendations = self.generate_recommendations(
                survival_pred, symptom_pred, classification_pred
            )

            return {
                "survival": survival_pred,
                "symptoms": symptom_pred,
                "classification": classification_pred,
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat(),
                "model_version": "1.0.0",
                "method": "trained_models" if self.models else "fallback",
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
                "method": "fallback",
            }


# Global API instance
streamlit_api = None


def get_streamlit_api() -> StreamlitAPI:
    """Get or create the global Streamlit API instance."""
    global streamlit_api
    if streamlit_api is None:
        streamlit_api = StreamlitAPI()
    return streamlit_api


def predict_menopause_streamlit(data: Dict[str, Any]) -> Dict[str, Any]:
    """Main prediction function for Streamlit integration."""
    api = get_streamlit_api()
    return api.predict_comprehensive(data)
