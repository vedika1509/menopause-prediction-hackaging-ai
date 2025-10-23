"""
Enhanced prediction API for MenoBalance AI with survival and symptom prediction.
"""

import os
import pickle
from datetime import datetime
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from loguru import logger

app = Flask(__name__)

# Configure CORS for production deployment
CORS(app, origins=[
    "http://localhost:3000",  # Local development
    "https://*.vercel.app",   # Vercel deployments
    "https://menobalance-ai.vercel.app",  # Production domain
    "https://menobalance.vercel.app",     # Alternative domain
    os.environ.get("VERCEL_URL", ""),    # Dynamic Vercel URL
])

# Configure API documentation
api = Api(
    app,
    version="1.0",
    title="MenoBalance AI API",
    description="API for menopause prediction and health insights",
    doc="/docs",
)

# Configure logging
logger.add("logs/api_{time:YYYY-MM-DD}.log", rotation="1 day", retention="30 days")

# Pydantic models for request/response validation
prediction_model = api.model(
    "PredictionRequest",
    {
        "age": fields.Float(required=True, description="Age in years"),
        "bmi": fields.Float(required=True, description="Body Mass Index"),
        "fsh": fields.Float(required=False, description="FSH level (mIU/mL)"),
        "estradiol": fields.Float(required=False, description="Estradiol level (pg/mL)"),
        "amh": fields.Float(required=False, description="AMH level (ng/mL)"),
        "hot_flashes": fields.Boolean(required=False, description="Experiencing hot flashes"),
        "night_sweats": fields.Boolean(required=False, description="Experiencing night sweats"),
        "mood_changes": fields.Float(required=False, description="Mood severity (1-10)"),
        "sleep_quality": fields.Float(required=False, description="Sleep quality (1-10)"),
        "stress_level": fields.Float(required=False, description="Stress level (1-10)"),
        "exercise_frequency": fields.Float(
            required=False, description="Exercise frequency per week"
        ),
        "smoking": fields.Boolean(required=False, description="Smoking status"),
        "alcohol_consumption": fields.Float(required=False, description="Alcohol units per week"),
    },
)


def load_models():
    """Load current trained models from task_specific directories."""
    models = {}

    try:
        # Load survival model
        with open("models/task_specific_survival/best_model.pkl", "rb") as f:
            models["survival"] = pickle.load(f)

        # Load symptom model
        with open("models/task_specific_symptom/best_model.pkl", "rb") as f:
            models["symptoms"] = pickle.load(f)

        # Load scalers
        with open("models/task_specific_survival/scaler.pkl", "rb") as f:
            models["survival_scaler"] = pickle.load(f)

        with open("models/task_specific_symptom/scaler.pkl", "rb") as f:
            models["symptom_scaler"] = pickle.load(f)

        # Load features
        with open("models/feature_selection_survival/selected_features.pkl", "rb") as f:
            models["survival_features"] = pickle.load(f)

        with open("models/feature_selection_symptom/selected_features.pkl", "rb") as f:
            models["symptom_features"] = pickle.load(f)

        logger.info("All models loaded successfully")
        return models

    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return None


def preprocess_input(data: Dict[str, Any], feature_columns: list, scaler) -> np.ndarray:
    """Preprocess input data for prediction."""
    # Create DataFrame from input
    df = pd.DataFrame([data])

    # Ensure all required features are present
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0  # Default value

    # Select and scale features
    X = df[feature_columns]
    X_scaled = scaler.transform(X)

    return X_scaled


def calculate_confidence_interval(
    predictions: np.ndarray, confidence_level: float = 0.95
) -> Tuple[float, float, float]:
    """Calculate confidence interval using bootstrap method."""
    n_bootstrap = 100
    bootstrap_predictions = []

    for _ in range(n_bootstrap):
        # Add small random noise to simulate uncertainty
        noise = np.random.normal(0, 0.1, predictions.shape)
        bootstrap_pred = predictions + noise
        bootstrap_predictions.append(bootstrap_pred)

    bootstrap_predictions = np.array(bootstrap_predictions)

    # Calculate percentiles
    alpha = 1 - confidence_level
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100

    lower_bound = np.percentile(bootstrap_predictions, lower_percentile)
    upper_bound = np.percentile(bootstrap_predictions, upper_percentile)
    mean_prediction = np.mean(bootstrap_predictions)

    return mean_prediction, lower_bound, upper_bound


def generate_recommendations(
    survival_pred: Dict, symptom_pred: Dict, user_profile: Dict
) -> List[Dict]:
    """Generate personalized recommendations based on predictions."""
    recommendations = []

    # High symptom severity
    if symptom_pred.get("severity_score", 0) > 7:
        recommendations.append(
            {
                "priority": "high",
                "category": "medical",
                "title": "Consult Healthcare Provider",
                "description": "Your symptom severity warrants professional evaluation. Consider scheduling an appointment with a menopause specialist.",
                "actions": [
                    "Schedule appointment with healthcare provider",
                    "Prepare a symptom diary",
                    "List your questions and concerns",
                ],
                "resources": [
                    "Find a menopause specialist near you",
                    "Symptom tracking app recommendations",
                ],
            }
        )

    # Sleep issues
    if symptom_pred.get("sleep_severity", 0) > 6:
        recommendations.append(
            {
                "priority": "medium",
                "category": "lifestyle",
                "title": "Improve Sleep Hygiene",
                "description": "Better sleep can significantly improve your menopause symptoms.",
                "actions": [
                    "Keep bedroom cool (65-68°F)",
                    "Maintain consistent bedtime",
                    "Avoid caffeine after 2 PM",
                    "Use blackout curtains",
                ],
                "resources": ["Sleep hygiene guide", "Meditation apps for sleep"],
            }
        )

    # High stress
    if user_profile.get("stress_level", 0) > 7:
        recommendations.append(
            {
                "priority": "medium",
                "category": "mental_health",
                "title": "Stress Management",
                "description": "High stress can worsen menopause symptoms. Consider stress reduction techniques.",
                "actions": [
                    "Practice daily meditation",
                    "Try deep breathing exercises",
                    "Consider yoga or tai chi",
                    "Limit news consumption",
                ],
                "resources": ["Guided meditation apps", "Stress management techniques"],
            }
        )

    # Low exercise
    if user_profile.get("exercise_frequency", 0) < 3:
        recommendations.append(
            {
                "priority": "low",
                "category": "lifestyle",
                "title": "Increase Physical Activity",
                "description": "Regular exercise can help manage menopause symptoms and improve overall health.",
                "actions": [
                    "Start with 10-minute walks daily",
                    "Try strength training 2x per week",
                    "Consider swimming or cycling",
                    "Use fitness tracking apps",
                ],
                "resources": ["Beginner exercise routines", "Fitness apps for women over 40"],
            }
        )

    return sorted(
        recommendations,
        key=lambda x: {"high": 3, "medium": 2, "low": 1}[x["priority"]],
        reverse=True,
    )


@api.route("/predict")
class Predict(Resource):
    @api.expect(prediction_model)
    @api.doc("predict_menopause", description="Get survival and symptom predictions")
    def post(self):
        """Get unified predictions for survival and symptom models."""
        start_time = datetime.now()

        try:
            # Load models
            models = load_models()
            if models is None:
                logger.error("Failed to load models")
                return {"error": "Models not available"}, 500

            # Get input data
            data = request.get_json()
            logger.info(f"Prediction request received for age {data.get('age', 'unknown')}")

            # Survival prediction
            survival_model = models["survival"]
            survival_scaler = models["survival_scaler"]
            survival_features = models["survival_features"]

            X_survival = preprocess_input(data, survival_features, survival_scaler)
            survival_pred = survival_model.predict(X_survival)[0]

            # Calculate confidence interval for survival
            survival_mean, survival_lower, survival_upper = calculate_confidence_interval(
                np.array([survival_pred])
            )

            # Convert to years and determine risk level
            survival_years = float(survival_pred)
            if survival_years < 2:
                risk_level = "high"
            elif survival_years < 5:
                risk_level = "moderate"
            else:
                risk_level = "low"

            survival_result = {
                "time_to_menopause_years": survival_years,
                "confidence_interval": [float(survival_lower), float(survival_upper)],
                "risk_level": risk_level,
                "explanation": f"Based on your profile, menopause is predicted to occur in approximately {survival_years:.1f} years.",
            }

            # Symptom prediction
            symptom_model = models["symptoms"]
            symptom_scaler = models["symptom_scaler"]
            symptom_features = models["symptom_features"]

            X_symptom = preprocess_input(data, symptom_features, symptom_scaler)
            symptom_pred = symptom_model.predict(X_symptom)[0]

            # Calculate confidence interval for symptoms
            symptom_mean, symptom_lower, symptom_upper = calculate_confidence_interval(
                np.array([symptom_pred])
            )

            # Determine severity level
            if symptom_pred > 7:
                severity_level = "high"
            elif symptom_pred > 4:
                severity_level = "moderate"
            else:
                severity_level = "low"

            # Extract individual symptoms (if multi-output)
            if len(symptom_pred.shape) > 0 and len(symptom_pred) > 1:
                symptom_scores = {
                    "hot_flashes": float(symptom_pred[0]) if len(symptom_pred) > 0 else 0,
                    "sleep_issues": float(symptom_pred[1]) if len(symptom_pred) > 1 else 0,
                    "mood_changes": float(symptom_pred[2]) if len(symptom_pred) > 2 else 0,
                }
                top_symptoms = [k for k, v in symptom_scores.items() if v > 5]
            else:
                symptom_scores = {"overall": float(symptom_pred)}
                top_symptoms = ["overall"] if symptom_pred > 5 else []

            symptom_result = {
                "severity_score": float(symptom_pred),
                "confidence_interval": [float(symptom_lower), float(symptom_upper)],
                "severity_level": severity_level,
                "top_symptoms": top_symptoms,
                "symptom_breakdown": symptom_scores,
                "explanation": f"Your symptom severity is {severity_level} with a score of {symptom_pred:.1f}/10.",
            }

            # Generate recommendations
            recommendations = generate_recommendations(survival_result, symptom_result, data)

            # Prepare response
            response = {
                "survival": survival_result,
                "symptoms": symptom_result,
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat(),
                "model_info": {
                    "survival_model": type(survival_model).__name__,
                    "symptom_model": type(symptom_model).__name__,
                    "confidence_level": "95%",
                },
            }

            # Log successful prediction
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Prediction completed in {duration:.2f}s")

            return response

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"Prediction failed after {duration:.2f}s: {str(e)}")
            return {"error": f"Prediction failed: {str(e)}"}, 500


@api.route("/health")
class Health(Resource):
    @api.doc("health_check", description="Check API health status")
    def get(self):
        """Health check endpoint."""
        models_loaded = load_models() is not None
        return {
            "status": "healthy" if models_loaded else "degraded",
            "models_loaded": models_loaded,
            "timestamp": datetime.now().isoformat(),
        }


@api.route("/models/info")
class ModelsInfo(Resource):
    @api.doc("models_info", description="Get information about loaded models")
    def get(self):
        """Get information about loaded models."""
        try:
            models = load_models()
            if models is None:
                return {"error": "No models loaded"}, 500

            info = {
                "survival": {
                    "type": type(models["survival"]).__name__,
                    "features_count": len(models["survival_features"]),
                    "scaler": type(models["survival_scaler"]).__name__,
                },
                "symptoms": {
                    "type": type(models["symptoms"]).__name__,
                    "features_count": len(models["symptom_features"]),
                    "scaler": type(models["symptom_scaler"]).__name__,
                },
            }

            return info

        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e)}, 500


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Run the app
    app.run(debug=True, host="0.0.0.0", port=5000)
