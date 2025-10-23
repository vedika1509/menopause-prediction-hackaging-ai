"""
Nebius AI Integration Service for MenoBalance AI
Provides chatbot, health recommendations, and educational content generation.
"""

import logging
import os
import random
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NebiusAIService:
    """
    Service for integrating with Nebius AI for chatbot, recommendations, and educational content.
    """

    def __init__(self):
        """Initialize the Nebius AI service."""
        self.api_key = os.getenv("NEBIUS_AI_API_KEY")
        self.base_url = "https://nebius-inference.eu.auth0.com/api/v2"  # Nebius AI endpoint from JWT token
        self.session_context = {}

        # Fallback content for when Nebius AI is unavailable
        self.fallback_responses = self._load_fallback_content()

        if not self.api_key:
            logger.warning("NEBIUS_AI_API_KEY not found. Using fallback responses.")

    def _load_fallback_content(self) -> Dict[str, Any]:
        """Load fallback content for when Nebius AI is unavailable."""
        return {
            "chat_responses": [
                "I understand you're going through a challenging time. How can I help support you today?",
                "It's completely normal to have questions about menopause. I'm here to listen and provide guidance.",
                "Your health and wellbeing matter. What specific concerns would you like to discuss?",
                "Every woman's experience is unique. Let's work together to find what helps you feel your best.",
                "I'm here to provide compassionate support and evidence-based information. What's on your mind?",
            ],
            "recommendations": {
                "pre_menopause": [
                    "Focus on maintaining regular menstrual cycles through balanced nutrition and stress management.",
                    "Consider tracking your cycles to understand your body's patterns better.",
                    "Regular exercise can help support hormonal balance and overall health.",
                ],
                "peri_menopause": [
                    "Monitor symptoms closely and consider keeping a symptom diary.",
                    "Cooling strategies like fans, light clothing, and cool drinks can help with hot flashes.",
                    "Stress management techniques such as meditation or yoga may help with mood changes.",
                ],
                "post_menopause": [
                    "Prioritize bone health with calcium-rich foods and weight-bearing exercise.",
                    "Focus on cardiovascular health through regular physical activity and heart-healthy diet.",
                    "Continue monitoring your overall health and discuss any concerns with your healthcare provider.",
                ],
            },
            "educational_content": {
                "menopause_stages": {
                    "title": "Understanding Menopause Stages",
                    "content": "Menopause is a natural biological process that occurs in three stages: Pre-menopause (regular cycles), Peri-menopause (transition with irregular cycles), and Post-menopause (12+ months without periods).",
                },
                "symptoms": {
                    "title": "Common Menopause Symptoms",
                    "content": "Common symptoms include hot flashes, night sweats, mood changes, sleep disturbances, vaginal dryness, and changes in menstrual cycles. Each woman's experience is unique.",
                },
                "lifestyle": {
                    "title": "Lifestyle Management",
                    "content": "Regular exercise, balanced nutrition, stress management, adequate sleep, and avoiding smoking can help manage menopause symptoms and support overall health.",
                },
            },
        }

    def _make_api_request(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make a request to Nebius AI API."""
        if not self.api_key:
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                f"{self.base_url}/{endpoint}", headers=headers, json=data, timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Nebius AI API error: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error making Nebius AI request: {e}")
            return None

    def chat(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a chatbot response using Nebius AI.

        Args:
            user_message: User's message
            context: Additional context about user's health data

        Returns:
            AI-generated response
        """
        try:
            # Prepare context for Nebius AI
            context_data = {
                "message": user_message,
                "context": context or {},
                "timestamp": datetime.now().isoformat(),
                "session_id": context.get("session_id") if context else None,
            }

            # Try Nebius AI first
            response = self._make_api_request("chat", context_data)

            if response and "message" in response:
                return response["message"]

            # Fallback to local responses
            return self._get_fallback_chat_response(user_message, context)

        except Exception as e:
            logger.error(f"Chat error: {e}")
            return self._get_fallback_chat_response(user_message, context)

    def _get_fallback_chat_response(
        self, user_message: str, context: Optional[Dict[str, Any]]
    ) -> str:
        """Get fallback chat response when Nebius AI is unavailable."""
        # Simple keyword-based responses
        message_lower = user_message.lower()

        if any(word in message_lower for word in ["hot flash", "hot flush", "sweating"]):
            return "Hot flashes can be challenging. Try wearing layers, using a fan, drinking cool water, and avoiding triggers like spicy foods and stress. If they're severe, consider discussing options with your healthcare provider."

        elif any(word in message_lower for word in ["sleep", "insomnia", "tired"]):
            return "Sleep disturbances are common during menopause. Try maintaining a regular sleep schedule, keeping your bedroom cool, avoiding caffeine in the afternoon, and practicing relaxation techniques before bed."

        elif any(word in message_lower for word in ["mood", "depression", "anxiety", "emotional"]):
            return "Mood changes are a normal part of menopause. Regular exercise, stress management, social support, and adequate sleep can help. If you're experiencing persistent mood changes, please consider speaking with a healthcare provider."

        elif any(word in message_lower for word in ["weight", "gain", "lose"]):
            return "Weight changes during menopause are common due to hormonal shifts. Focus on a balanced diet, regular exercise, and maintaining muscle mass through strength training. Remember, your worth isn't defined by your weight."

        elif any(word in message_lower for word in ["exercise", "workout", "fitness"]):
            return "Regular exercise is excellent for menopause management! Aim for a mix of cardio, strength training, and flexibility exercises. Even 30 minutes of moderate activity most days can make a significant difference."

        elif any(word in message_lower for word in ["diet", "nutrition", "food", "eat"]):
            return "A balanced diet rich in fruits, vegetables, whole grains, lean proteins, and healthy fats can help manage menopause symptoms. Focus on calcium-rich foods for bone health and stay hydrated."

        else:
            return random.choice(self.fallback_responses["chat_responses"])

    def generate_recommendations(self, health_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate personalized health recommendations using Nebius AI.

        Args:
            health_data: User's health data and predictions

        Returns:
            List of personalized recommendations
        """
        try:
            # Prepare data for Nebius AI
            recommendation_data = {
                "health_data": health_data,
                "timestamp": datetime.now().isoformat(),
                "request_type": "recommendations",
            }

            # Try Nebius AI first
            response = self._make_api_request("recommendations", recommendation_data)

            if response and "recommendations" in response:
                return response["recommendations"]

            # Fallback to local recommendations
            return self._get_fallback_recommendations(health_data)

        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
            return self._get_fallback_recommendations(health_data)

    def _get_fallback_recommendations(self, health_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get fallback recommendations when Nebius AI is unavailable."""
        recommendations = []

        # Get stage from predictions
        stage = health_data.get("predictions", {}).get("classification", {}).get("stage", "Unknown")

        # Stage-based recommendations
        if stage in self.fallback_responses["recommendations"]:
            for rec in self.fallback_responses["recommendations"][stage]:
                recommendations.append(
                    {
                        "category": "Stage-specific",
                        "title": f"Recommendations for {stage}",
                        "description": rec,
                        "priority": "medium",
                    }
                )

        # Symptom-based recommendations
        symptoms = health_data.get("predictions", {}).get("symptom", {}).get("symptoms", {})
        overall_severity = (
            health_data.get("predictions", {}).get("symptom", {}).get("overall_severity", 0)
        )

        if overall_severity > 6:
            recommendations.append(
                {
                    "category": "Symptom Management",
                    "title": "High Symptom Severity",
                    "description": "Consider discussing your symptoms with a healthcare provider for personalized management strategies.",
                    "priority": "high",
                }
            )

        # Time-based recommendations
        time_to_menopause = (
            health_data.get("predictions", {}).get("survival", {}).get("time_to_menopause", 0)
        )
        if time_to_menopause < 3:
            recommendations.append(
                {
                    "category": "Timeline",
                    "title": "Transition Preparation",
                    "description": "Menopause transition may occur soon. Consider preparing by learning about symptoms and management strategies.",
                    "priority": "medium",
                }
            )

        # General recommendations
        recommendations.extend(
            [
                {
                    "category": "General Health",
                    "title": "Regular Healthcare",
                    "description": "Maintain regular check-ups with your healthcare provider for preventive care and monitoring.",
                    "priority": "high",
                },
                {
                    "category": "Lifestyle",
                    "title": "Stress Management",
                    "description": "Practice stress-reduction techniques such as meditation, deep breathing, or gentle yoga.",
                    "priority": "medium",
                },
            ]
        )

        return recommendations

    def generate_educational_content(self, topic: str) -> Dict[str, str]:
        """
        Generate educational content using Nebius AI.

        Args:
            topic: Educational topic to generate content for

        Returns:
            Educational content dictionary
        """
        try:
            # Prepare data for Nebius AI
            content_data = {
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "request_type": "educational_content",
            }

            # Try Nebius AI first
            response = self._make_api_request("education", content_data)

            if response and "content" in response:
                return response["content"]

            # Fallback to local content
            return self._get_fallback_educational_content(topic)

        except Exception as e:
            logger.error(f"Educational content generation error: {e}")
            return self._get_fallback_educational_content(topic)

    def _get_fallback_educational_content(self, topic: str) -> Dict[str, str]:
        """Get fallback educational content when Nebius AI is unavailable."""
        topic_lower = topic.lower()

        # Check for specific topics
        if any(word in topic_lower for word in ["stage", "phases", "pre", "peri", "post"]):
            return self.fallback_responses["educational_content"]["menopause_stages"]
        elif any(word in topic_lower for word in ["symptom", "hot flash", "mood", "sleep"]):
            return self.fallback_responses["educational_content"]["symptoms"]
        elif any(word in topic_lower for word in ["lifestyle", "exercise", "diet", "stress"]):
            return self.fallback_responses["educational_content"]["lifestyle"]
        else:
            return {
                "title": "Menopause Information",
                "content": "Menopause is a natural transition that every woman experiences. It's important to understand your body's changes and work with healthcare providers to manage symptoms and maintain health.",
            }

    def update_session_context(self, session_id: str, context: Dict[str, Any]):
        """Update session context for conversation continuity."""
        self.session_context[session_id] = {
            **self.session_context.get(session_id, {}),
            **context,
            "last_updated": datetime.now().isoformat(),
        }

    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """Get session context for conversation continuity."""
        return self.session_context.get(session_id, {})


# Global instance for easy access
nebius_service = None


def get_nebius_service():
    """Get or create the global Nebius AI service instance."""
    global nebius_service
    if nebius_service is None:
        nebius_service = NebiusAIService()
    return nebius_service
