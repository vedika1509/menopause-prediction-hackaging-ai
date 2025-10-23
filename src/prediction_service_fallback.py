"""
Fallback Prediction Service for MenoBalance AI
Works without trained models for Streamlit Cloud deployment
"""

import logging
from datetime import datetime
from typing import Any, Dict

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FallbackPredictionService:
    """Fallback prediction service that works without trained models."""

    def __init__(self):
        """Initialize the fallback prediction service."""
        logger.info("Initializing fallback prediction service")

    def predict_survival(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict time to menopause using rule-based approach."""
        try:
            # Extract key features
            age = data.get("age", 45)
            fsh = data.get("fsh", 15)
            amh = data.get("amh", 1.0)
            bmi = data.get("bmi", 25)
            smoking = data.get("smoking", False)

            # Base prediction based on age
            if age > 50:
                base_prediction = 1.0
            elif age > 45:
                base_prediction = 2.5
            elif age > 40:
                base_prediction = 4.0
            else:
                base_prediction = 6.0

            # Adjust based on biomarkers
            if fsh > 25:
                base_prediction *= 0.7  # Earlier menopause
            elif fsh > 15:
                base_prediction *= 0.9

            if amh < 1.0:
                base_prediction *= 0.8  # Earlier menopause
            elif amh < 2.0:
                base_prediction *= 0.95

            # Adjust for lifestyle factors
            if smoking:
                base_prediction *= 0.85  # Earlier menopause

            if bmi > 30:
                base_prediction *= 1.1  # Slightly later

            # Add some realistic variation
            variation = np.random.normal(0, 0.3)
            prediction = max(0.5, min(10, base_prediction + variation))

            # Calculate confidence interval
            std_error = 1.0
            confidence_lower = max(0, prediction - 1.96 * std_error)
            confidence_upper = prediction + 1.96 * std_error

            return {
                "time_to_menopause_years": float(prediction),
                "confidence_interval": [float(confidence_lower), float(confidence_upper)],
                "confidence_level": 0.95,
                "risk_level": self._get_risk_level(prediction),
                "model_confidence": 0.7,  # Moderate confidence for rule-based
                "uncertainty_measure": float(std_error),
                "method": "rule_based",
            }

        except Exception as e:
            logger.error(f"Error in fallback survival prediction: {e}")
            return {
                "time_to_menopause_years": 3.0,
                "confidence_interval": [1.5, 4.5],
                "risk_level": "moderate",
                "model_confidence": 0.5,
                "uncertainty_measure": 0.8,
                "method": "rule_based",
                "error": str(e),
            }

    def predict_symptoms(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict symptom severity using rule-based approach."""
        try:
            # Extract key features
            age = data.get("age", 45)
            hot_flashes = data.get("hot_flashes", 0)
            mood_changes = data.get("mood_changes", 0)
            sleep_quality = data.get("sleep_quality", 5)
            stress_level = data.get("stress_level", 5)

            # Base severity calculation
            base_severity = 5.0

            # Adjust based on age (perimenopause typically 40-50)
            if 40 <= age <= 50:
                base_severity += 1.0
            elif age > 50:
                base_severity += 0.5

            # Adjust based on current symptoms
            if hot_flashes > 5:
                base_severity += 1.5
            elif hot_flashes > 3:
                base_severity += 0.8

            if mood_changes > 5:
                base_severity += 1.0
            elif mood_changes > 3:
                base_severity += 0.5

            if sleep_quality < 4:
                base_severity += 1.0
            elif sleep_quality < 6:
                base_severity += 0.5

            if stress_level > 6:
                base_severity += 0.8
            elif stress_level > 4:
                base_severity += 0.3

            # Add some variation
            variation = np.random.normal(0, 0.4)
            prediction = max(0, min(10, base_severity + variation))

            # Calculate confidence interval
            std_error = 0.8
            confidence_lower = max(0, prediction - 1.96 * std_error)
            confidence_upper = min(10, prediction + 1.96 * std_error)

            return {
                "severity_score": float(prediction),
                "confidence_interval": [float(confidence_lower), float(confidence_upper)],
                "confidence_level": 0.95,
                "severity_level": self._get_severity_level(prediction),
                "model_confidence": 0.65,  # Lower confidence for rule-based
                "uncertainty_measure": float(std_error),
                "method": "rule_based",
            }

        except Exception as e:
            logger.error(f"Error in fallback symptom prediction: {e}")
            return {
                "severity_score": 5.0,
                "confidence_interval": [4.0, 6.0],
                "severity_level": "moderate",
                "model_confidence": 0.5,
                "uncertainty_measure": 0.5,
                "method": "rule_based",
                "error": str(e),
            }

    def predict_classification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict menopause stage using rule-based approach."""
        try:
            # Extract key features
            age = data.get("age", 45)
            fsh = data.get("fsh", 15)
            amh = data.get("amh", 1.0)
            last_period = data.get("last_period_months", 6)

            # Determine stage based on rules
            if last_period >= 12:
                predicted_class = "Post-menopause"
                confidence = 0.9
            elif age > 50:
                predicted_class = "Peri-menopause"
                confidence = 0.8
            elif fsh > 25 or amh < 1.0:
                predicted_class = "Peri-menopause"
                confidence = 0.75
            elif age > 45 and (fsh > 15 or amh < 2.0):
                predicted_class = "Peri-menopause"
                confidence = 0.7
            else:
                predicted_class = "Pre-menopause"
                confidence = 0.6

            # Calculate probabilities
            if predicted_class == "Post-menopause":
                probabilities = {
                    "pre_menopause": 0.05,
                    "peri_menopause": 0.15,
                    "post_menopause": 0.8,
                }
            elif predicted_class == "Peri-menopause":
                probabilities = {"pre_menopause": 0.2, "peri_menopause": 0.7, "post_menopause": 0.1}
            else:
                probabilities = {"pre_menopause": 0.8, "peri_menopause": 0.2, "post_menopause": 0.0}

            # Calculate confidence interval
            prob_std = 0.1
            confidence_lower = max(0, confidence - 1.96 * prob_std)
            confidence_upper = min(1, confidence + 1.96 * prob_std)

            return {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "confidence_interval": [float(confidence_lower), float(confidence_upper)],
                "confidence_level": 0.95,
                "probabilities": probabilities,
                "model_confidence": confidence,
                "uncertainty_measure": float(prob_std),
                "method": "rule_based",
            }

        except Exception as e:
            logger.error(f"Error in fallback classification prediction: {e}")
            return {
                "predicted_class": "Peri-menopause",
                "confidence": 0.6,
                "confidence_interval": [0.5, 0.7],
                "probabilities": {"pre_menopause": 0.4, "peri_menopause": 0.6},
                "model_confidence": 0.6,
                "uncertainty_measure": 0.05,
                "method": "rule_based",
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
                "model_version": "fallback_1.0",
                "method": "rule_based",
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
                "method": "rule_based",
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


# Global fallback prediction service instance
fallback_service = None


def get_fallback_prediction_service() -> FallbackPredictionService:
    """Get or create the global fallback prediction service instance."""
    global fallback_service
    if fallback_service is None:
        fallback_service = FallbackPredictionService()
    return fallback_service


def predict_menopause_fallback(data: Dict[str, Any]) -> Dict[str, Any]:
    """Main prediction function using fallback service."""
    service = get_fallback_prediction_service()
    return service.get_comprehensive_prediction(data)


if __name__ == "__main__":
    # Test the fallback prediction service
    test_data = {
        "age": 45,
        "bmi": 25.5,
        "fsh": 15.2,
        "amh": 1.5,
        "hot_flashes": 3,
        "mood_changes": 4,
        "sleep_quality": 6,
        "stress_level": 5,
    }

    service = FallbackPredictionService()
    result = service.get_comprehensive_prediction(test_data)
    print("Fallback prediction result:")
    print(result)
