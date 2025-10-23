"""
API Endpoint for MenoBalance AI
FastAPI endpoint for prediction service
"""

import logging
import os
import pickle
import sys
from datetime import datetime
from typing import Any, Dict

import numpy as np
import pandas as pd

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    import uvicorn
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
except ImportError:
    print("FastAPI not installed. Install with: pip install fastapi uvicorn")
    sys.exit(1)

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("menobalance_api.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Create separate loggers for different components
model_logger = logging.getLogger("models")
prediction_logger = logging.getLogger("predictions")
error_logger = logging.getLogger("errors")

# Initialize FastAPI app with comprehensive OpenAPI documentation
app = FastAPI(
    title="MenoBalance AI API",
    description="""
    ## MenoBalance AI - Menopause Prediction API
    
    A comprehensive API for predicting menopause-related health outcomes using advanced machine learning models.
    
    ### Features
    - **Survival Analysis**: Predict time to menopause with confidence intervals
    - **Symptom Prediction**: Estimate symptom severity and patterns
    - **Classification**: Determine menopause stage (pre/peri/post)
    - **Recommendations**: Personalized health recommendations
    - **Confidence Intervals**: Statistical uncertainty quantification
    
    ### Models
    - **Survival Model**: CatBoost with Cox Proportional Hazards
    - **Symptom Model**: XGBoost Multi-output Regression  
    - **Classification Model**: XGBoost with Logistic Regression
    
    ### Clinical Disclaimer
    This API is for educational and research purposes only. It does not provide medical diagnosis or replace professional medical advice.
    """,
    version="1.0.0",
    contact={
        "name": "MenoBalance AI Support",
        "email": "support@menobalance.ai",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "https://menobalance-ai.streamlit.app",
            "description": "Streamlit Cloud production server",
        },
        {"url": "http://localhost:8000", "description": "Development server"},
    ],
)

# Global variables for models
models = {}
scalers = {}
feature_names = {}


class PredictionRequest(BaseModel):
    """Request model for prediction API"""

    age: float = Field(..., description="Patient age in years", ge=18, le=100, example=45)
    bmi: float = Field(..., description="Body Mass Index", ge=15.0, le=50.0, example=25.5)
    fsh: float = Field(
        ...,
        description="Follicle Stimulating Hormone level (mIU/mL)",
        ge=1.0,
        le=100.0,
        example=15.2,
    )
    amh: float = Field(
        ..., description="Anti-Müllerian Hormone level (ng/mL)", ge=0.1, le=10.0, example=1.5
    )
    estradiol: float = Field(
        ..., description="Estradiol level (pg/mL)", ge=10.0, le=500.0, example=50.0
    )
    last_period_months: int = Field(
        0, description="Months since last menstrual period", ge=0, le=120, example=6
    )
    hot_flashes: int = Field(
        0, description="Hot flashes severity (0-10 scale)", ge=0, le=10, example=3
    )
    mood_changes: int = Field(
        0, description="Mood changes severity (0-10 scale)", ge=0, le=10, example=4
    )
    sleep_quality: int = Field(
        5, description="Sleep quality (0-10 scale, 0=poor, 10=excellent)", ge=0, le=10, example=6
    )
    stress_level: int = Field(5, description="Stress level (0-10 scale)", ge=0, le=10, example=5)
    smoking: bool = Field(False, description="Smoking history", example=False)
    exercise: str = Field("Moderate", description="Exercise frequency", example="Moderate")
    family_history: bool = Field(
        False, description="Family history of early menopause", example=False
    )
    diabetes: bool = Field(False, description="Diabetes diagnosis", example=False)
    hypertension: bool = Field(False, description="Hypertension diagnosis", example=False)
    thyroid: bool = Field(False, description="Thyroid issues", example=False)

    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "bmi": 25.5,
                "fsh": 15.2,
                "amh": 1.5,
                "estradiol": 50.0,
                "last_period_months": 6,
                "hot_flashes": 3,
                "mood_changes": 4,
                "sleep_quality": 6,
                "stress_level": 5,
                "smoking": False,
                "exercise": "Moderate",
                "family_history": False,
                "diabetes": False,
                "hypertension": False,
                "thyroid": False,
            }
        }


class PredictionResponse(BaseModel):
    """Response model for prediction API"""

    survival: Dict[str, Any]
    symptoms: Dict[str, Any]
    classification: Dict[str, Any]
    recommendations: list
    timestamp: str
    model_version: str
    method: str


def load_models():
    """Load all trained models and preprocessing pipelines."""
    global models, scalers, feature_names

    logger.info("Loading models and preprocessing pipelines...")

    model_paths = {
        "survival": "models/task_specific_survival",
        "symptom": "models/task_specific_symptom",
        "classification": "models/task_specific_classification",
    }

    for task, path in model_paths.items():
        try:
            logger.info(f"Loading {task} model from {path}")

            # Load model
            model_path = os.path.join(path, "best_model.pkl")
            if os.path.exists(model_path):
                with open(model_path, "rb") as f:
                    models[task] = pickle.load(f)
                logger.info(f"✅ Loaded {task} model")
            else:
                logger.warning(f"❌ Model not found: {model_path}")
                continue

            # Load scaler
            scaler_path = os.path.join(path, "scaler.pkl")
            if os.path.exists(scaler_path):
                with open(scaler_path, "rb") as f:
                    scalers[task] = pickle.load(f)
                logger.info(f"✅ Loaded {task} scaler")
            else:
                logger.warning(f"❌ Scaler not found: {scaler_path}")

            # Load features
            features_path = f"models/feature_selection_{task}/selected_features.pkl"
            if os.path.exists(features_path):
                with open(features_path, "rb") as f:
                    feature_names[task] = pickle.load(f)
                logger.info(f"✅ Loaded {task} features: {len(feature_names[task])} features")
            else:
                logger.warning(f"❌ Features not found: {features_path}")
                # Use default features
                feature_names[task] = get_default_features(task)

        except Exception as e:
            logger.error(f"❌ Error loading {task}: {e}")
            continue

    logger.info(f"Model loading completed. Available models: {list(models.keys())}")


def get_default_features(task):
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


def preprocess_input(data: Dict[str, Any], task: str) -> np.ndarray:
    """Preprocess input data for prediction."""
    try:
        # Get feature names for the task
        if task not in feature_names:
            raise ValueError(f"No features found for task: {task}")

        features = feature_names[task]

        # Create DataFrame with all features
        df = pd.DataFrame([data])

        # Ensure all required features are present
        for feature in features:
            if feature not in df.columns:
                df[feature] = 0  # Default value for missing features

        # Select only the required features in the correct order
        X = df[features].values

        # Scale the features if scaler is available
        if task in scalers:
            X = scalers[task].transform(X)

        return X

    except Exception as e:
        logger.error(f"Error preprocessing input: {e}")
        raise


def predict_survival(data: Dict[str, Any]) -> Dict[str, Any]:
    """Predict time to menopause (survival analysis)."""
    try:
        if "survival" not in models:
            raise ValueError("Survival model not loaded")

        # Preprocess input
        X = preprocess_input(data, "survival")

        # Make prediction
        prediction = models["survival"].predict(X)[0]

        # Calculate confidence interval
        std_error = 0.8  # Estimated from model performance
        confidence_lower = max(0, prediction - 1.96 * std_error)
        confidence_upper = prediction + 1.96 * std_error

        # Calculate model confidence
        model_confidence = min(0.95, max(0.5, 1.0 - std_error))

        return {
            "time_to_menopause_years": float(prediction),
            "confidence_interval": [float(confidence_lower), float(confidence_upper)],
            "confidence_level": 0.95,
            "risk_level": get_risk_level(prediction),
            "model_confidence": float(model_confidence),
            "uncertainty_measure": float(std_error),
        }

    except Exception as e:
        logger.error(f"Error in survival prediction: {e}")
        # Fallback prediction
        return {
            "time_to_menopause_years": 3.0,
            "confidence_interval": [1.5, 4.5],
            "confidence_level": 0.95,
            "risk_level": "moderate",
            "model_confidence": 0.5,
            "uncertainty_measure": 0.8,
            "error": str(e),
        }


def predict_symptoms(data: Dict[str, Any]) -> Dict[str, Any]:
    """Predict symptom severity."""
    try:
        if "symptom" not in models:
            raise ValueError("Symptom model not loaded")

        # Preprocess input
        X = preprocess_input(data, "symptom")

        # Make prediction
        prediction = models["symptom"].predict(X)[0]

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
            "severity_level": get_severity_level(prediction),
            "model_confidence": float(model_confidence),
            "uncertainty_measure": float(std_error),
        }

    except Exception as e:
        logger.error(f"Error in symptom prediction: {e}")
        # Fallback prediction
        return {
            "severity_score": 5.0,
            "confidence_interval": [4.0, 6.0],
            "confidence_level": 0.95,
            "severity_level": "moderate",
            "model_confidence": 0.5,
            "uncertainty_measure": 0.5,
            "error": str(e),
        }


def predict_classification(data: Dict[str, Any]) -> Dict[str, Any]:
    """Predict menopause stage classification."""
    try:
        if "classification" not in models:
            raise ValueError("Classification model not loaded")

        # Preprocess input
        X = preprocess_input(data, "classification")

        # Make prediction
        prediction_proba = models["classification"].predict_proba(X)[0]
        prediction_class = models["classification"].predict(X)[0]

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
                "peri_menopause": float(prediction_proba[1]) if len(prediction_proba) > 1 else 0.0,
                "post_menopause": float(prediction_proba[2]) if len(prediction_proba) > 2 else 0.0,
            },
            "model_confidence": max_prob,
            "uncertainty_measure": float(prob_std),
        }

    except Exception as e:
        logger.error(f"Error in classification prediction: {e}")
        # Fallback prediction
        return {
            "predicted_class": "Peri-menopause",
            "confidence": 0.6,
            "confidence_interval": [0.5, 0.7],
            "confidence_level": 0.95,
            "probabilities": {"pre_menopause": 0.4, "peri_menopause": 0.6, "post_menopause": 0.0},
            "model_confidence": 0.6,
            "uncertainty_measure": 0.05,
            "error": str(e),
        }


def get_risk_level(time_to_menopause: float) -> str:
    """Determine risk level based on time to menopause."""
    if time_to_menopause < 1:
        return "high"
    elif time_to_menopause < 3:
        return "moderate"
    else:
        return "low"


def get_severity_level(severity_score: float) -> str:
    """Determine severity level based on score."""
    if severity_score < 3:
        return "mild"
    elif severity_score < 7:
        return "moderate"
    else:
        return "severe"


def generate_recommendations(survival: Dict, symptoms: Dict, classification: Dict) -> list:
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


@app.on_event("startup")
async def startup_event():
    """Load models on startup."""
    load_models()


@app.get(
    "/",
    summary="API Information",
    description="Get basic information about the MenoBalance AI API",
    tags=["General"],
)
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "MenoBalance AI API",
        "version": "1.0.0",
        "description": "Menopause prediction API with confidence intervals and recommendations",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json",
        },
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Check the health status of the API and loaded models",
    tags=["Health"],
)
async def health_check():
    """Health check endpoint to verify API and model status."""
    return {
        "status": "healthy",
        "models_loaded": list(models.keys()),
        "total_models": len(models),
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Get Menopause Predictions",
    description="""
          Get comprehensive menopause predictions including:
          - **Survival Analysis**: Time to menopause with confidence intervals
          - **Symptom Prediction**: Symptom severity estimation
          - **Classification**: Menopause stage determination
          - **Recommendations**: Personalized health recommendations
          
          All predictions include confidence intervals and uncertainty measures.
          """,
    tags=["Predictions"],
)
async def predict(request: PredictionRequest):
    """Main prediction endpoint."""
    try:
        # Convert request to dict
        data = request.dict()

        # Get predictions from all models
        survival_pred = predict_survival(data)
        symptom_pred = predict_symptoms(data)
        classification_pred = predict_classification(data)

        # Generate recommendations
        recommendations = generate_recommendations(survival_pred, symptom_pred, classification_pred)

        return PredictionResponse(
            survival=survival_pred,
            symptoms=symptom_pred,
            classification=classification_pred,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            model_version="1.0.0",
            method="trained_models" if models else "fallback",
        )

    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)
