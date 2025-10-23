"""
FastAPI endpoint for MenoBalance AI predictions.
Provides /predict endpoint with confidence intervals and recommendations.
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import our prediction service
from prediction_service import get_prediction_service
from pydantic import BaseModel, Field

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/api.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MenoBalance AI API",
    description="AI-powered menopause prediction and wellness management API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthInput(BaseModel):
    """Input model for health data."""

    age: float = Field(..., ge=18, le=100, description="Age in years")
    bmi: float = Field(..., ge=10, le=80, description="Body Mass Index")
    fsh: Optional[float] = Field(
        None, ge=0, le=200, description="Follicle Stimulating Hormone (mIU/mL)"
    )
    amh: Optional[float] = Field(None, ge=0, le=20, description="Anti-Mullerian Hormone (ng/mL)")
    estradiol: Optional[float] = Field(None, ge=0, le=1000, description="Estradiol (pg/mL)")

    # Lifestyle factors
    exercise_frequency: Optional[int] = Field(
        None, ge=0, le=7, description="Exercise frequency per week"
    )
    sleep_hours: Optional[float] = Field(
        None, ge=0, le=24, description="Average sleep hours per night"
    )
    stress_level: Optional[int] = Field(None, ge=1, le=10, description="Stress level (1-10 scale)")

    # Medical history
    smoking_status: Optional[bool] = Field(None, description="Current smoking status")
    family_history_menopause: Optional[bool] = Field(
        None, description="Family history of early menopause"
    )

    # Additional features
    weight: Optional[float] = Field(None, ge=30, le=300, description="Weight in kg")
    height: Optional[float] = Field(None, ge=100, le=250, description="Height in cm")
    regular_cycles: Optional[bool] = Field(None, description="Regular menstrual cycles")


class PredictionResponse(BaseModel):
    """Response model for predictions."""

    success: bool
    predictions: Dict[str, Any]
    recommendations: list
    timestamp: str
    model_version: str
    confidence_intervals: Dict[str, str]


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    timestamp: str
    version: str
    models_loaded: bool


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with basic API information."""
    return HealthResponse(
        status="healthy", timestamp=datetime.now().isoformat(), version="1.0.0", models_loaded=True
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        prediction_service = get_prediction_service()
        models_loaded = len(prediction_service.models) > 0

        return HealthResponse(
            status="healthy" if models_loaded else "degraded",
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            models_loaded=models_loaded,
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unavailable")


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: Request, health_data: HealthInput):
    """
    Make predictions for menopause stage, time to menopause, and symptom severity.

    Args:
        health_data: Health input data

    Returns:
        Predictions with confidence intervals and recommendations
    """
    try:
        logger.info(f"Received prediction request: {health_data.dict()}")

        # Get prediction service
        prediction_service = get_prediction_service()

        if not prediction_service.models:
            raise HTTPException(status_code=503, detail="Models not loaded")

        # Convert input to dictionary
        input_data = health_data.dict()

        # Make predictions
        results = prediction_service.predict_all(input_data)

        # Extract confidence intervals
        confidence_intervals = {
            "stage": results["predictions"]["classification"].get("confidence_interval", "N/A"),
            "time_to_menopause": results["predictions"]["survival"].get(
                "time_confidence_interval", "N/A"
            ),
            "symptom_severity": results["predictions"]["symptom"].get(
                "severity_confidence_interval", "N/A"
            ),
        }

        response = PredictionResponse(
            success=True,
            predictions=results["predictions"],
            recommendations=results["recommendations"],
            timestamp=results["timestamp"],
            model_version=results["model_version"],
            confidence_intervals=confidence_intervals,
        )

        logger.info("Prediction completed successfully")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/models/status")
async def models_status():
    """Get status of loaded models."""
    try:
        prediction_service = get_prediction_service()

        status = {
            "models_loaded": list(prediction_service.models.keys()),
            "scalers_loaded": list(prediction_service.scalers.keys()),
            "features_loaded": list(prediction_service.features.keys()),
            "insights_loaded": bool(prediction_service.model_insights),
        }

        return status
    except Exception as e:
        logger.error(f"Error getting model status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model status")


@app.get("/features/{task}")
async def get_features(task: str):
    """Get required features for a specific task."""
    try:
        prediction_service = get_prediction_service()

        if task not in prediction_service.features:
            raise HTTPException(status_code=404, detail=f"Task '{task}' not found")

        return {
            "task": task,
            "features": prediction_service.features[task],
            "count": len(prediction_service.features[task]),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting features for task {task}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get features")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "timestamp": datetime.now().isoformat()},
    )


if __name__ == "__main__":
    # Run the API server
    uvicorn.run("api_endpoint:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
