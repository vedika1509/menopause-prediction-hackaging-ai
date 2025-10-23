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
from dotenv import load_dotenv

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    logger.warning(f"Could not load .env file: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NebiusAIService:
    """
    Service for integrating with Nebius AI for chatbot, recommendations, and educational content.
    """

    def __init__(self):
        """Initialize the Nebius AI service."""
        self.api_key = os.getenv("NEBIUS_AI_API_KEY") or os.getenv("NEBIUS_API_KEY")
        self.base_url = "https://api.studio.nebius.com/v1"  # Correct Nebius AI endpoint
        self.session_context = {}

        # Fallback content for when Nebius AI is unavailable
        self.fallback_responses = self._load_fallback_content()

        if self.api_key:
            logger.info("NEBIUS_AI_API_KEY found. Nebius AI integration enabled.")
        else:
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

            # Format the request for Nebius AI chat completion
            if endpoint == "chat":
                # Create the proper request format for Nebius AI based on their documentation
                request_data = {
                    "model": "deepseek-ai/DeepSeek-R1-0528",  # Using the model from Nebius AI docs
                    "messages": [
                        {
                            "role": "system",
                            "content": data.get("system_prompt", "You are a helpful assistant."),
                        },
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": data.get("user_message", "")}],
                        },
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7,
                }
            else:
                request_data = data

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=request_data,
                timeout=90,
            )

            if response.status_code == 200:
                result = response.json()
                # Extract the message from Nebius AI response
                if endpoint == "chat" and "choices" in result:
                    return {"message": result["choices"][0]["message"]["content"]}
                return result
            else:
                logger.error(f"Nebius AI API error: {response.status_code} - {response.text}")
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
            # Create counseling prompt for Nebius AI
            counseling_prompt = """You are a compassionate and knowledgeable menopause counselor and women's health specialist. 
            
            The user may be experiencing menopause-related issues and needs empathetic support and guidance. 
            
            Please respond as a caring counselor who:
            - Shows empathy and understanding
            - Provides evidence-based information about menopause
            - Offers practical coping strategies
            - Encourages professional medical consultation when appropriate
            - Uses a warm, supportive tone
            - Validates their experiences and concerns
            
            Remember to be sensitive to the personal nature of their questions and maintain a professional yet caring demeanor."""

            # Prepare context for Nebius AI with counseling prompt
            context_data = {
                "system_prompt": counseling_prompt,
                "user_message": user_message,
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
        # Simple keyword-based responses with counseling tone
        message_lower = user_message.lower()

        if any(word in message_lower for word in ["hot flash", "hot flush", "sweating"]):
            return "I understand that hot flashes can be really challenging and disruptive to your daily life. You're not alone in this experience. Try wearing layers that you can easily remove, using a fan, drinking cool water, and avoiding triggers like spicy foods and stress. If they're severely impacting your quality of life, I'd encourage you to discuss treatment options with your healthcare provider. Remember, there are effective ways to manage this symptom."

        elif any(word in message_lower for word in ["sleep", "insomnia", "tired"]):
            return "Sleep disturbances during menopause are unfortunately very common, and I know how frustrating this can be. Your body is going through significant hormonal changes that affect sleep. Try maintaining a regular sleep schedule, keeping your bedroom cool and dark, avoiding caffeine in the afternoon, and practicing relaxation techniques like deep breathing before bed. If sleep issues persist, consider discussing this with your healthcare provider as there are treatments that can help."

        elif any(word in message_lower for word in ["mood", "depression", "anxiety", "emotional"]):
            return "I want you to know that mood changes during menopause are completely normal and you're not alone in experiencing this. The hormonal fluctuations can significantly impact your emotional well-being. It's important to be gentle with yourself during this time. Regular exercise, stress management techniques, maintaining social connections, and ensuring adequate sleep can all help support your emotional health. If you're experiencing persistent mood changes that are affecting your daily life, I strongly encourage you to speak with a healthcare provider or mental health professional who can provide additional support and treatment options."

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
            # Create counseling prompt for recommendations
            counseling_prompt = """You are a compassionate menopause counselor and women's health specialist. 
            
            Based on the user's health data and predictions, provide personalized, empathetic recommendations that:
            - Show understanding and validation of their experience
            - Offer practical, evidence-based coping strategies
            - Consider their specific menopause stage and symptoms
            - Encourage professional medical consultation when appropriate
            - Use a warm, supportive tone
            - Prioritize their wellbeing and quality of life
            
            Format your response as a list of recommendations with categories, titles, descriptions, and priority levels."""

            # Prepare data for Nebius AI with counseling prompt
            recommendation_data = {
                "system_prompt": counseling_prompt,
                "user_message": f"Please provide personalized recommendations based on this health data: {health_data}",
                "health_data": health_data,
                "timestamp": datetime.now().isoformat(),
                "request_type": "recommendations",
            }

            # Try Nebius AI first
            response = self._make_api_request("chat", recommendation_data)

            if response and "message" in response:
                # Parse the AI response into recommendation format
                ai_response = response["message"]
                # For now, return fallback recommendations with AI-enhanced descriptions
                recommendations = self._get_fallback_recommendations(health_data)
                # Add AI insight to the first recommendation
                if recommendations:
                    recommendations[0]["ai_insight"] = ai_response
                return recommendations

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
            # Create counseling prompt for educational content
            counseling_prompt = """You are a compassionate menopause counselor and women's health educator. 
            
            Provide educational content about the requested topic that:
            - Uses clear, accessible language that's easy to understand
            - Shows empathy and understanding for women's experiences
            - Provides evidence-based information
            - Offers practical tips and strategies
            - Encourages professional medical consultation when appropriate
            - Uses a warm, supportive tone
            - Validates that menopause experiences are normal and manageable
            
            Structure your response with a clear title and comprehensive, empathetic content."""

            # Prepare data for Nebius AI with counseling prompt
            content_data = {
                "system_prompt": counseling_prompt,
                "user_message": f"Please provide educational content about: {topic}",
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "request_type": "educational_content",
            }

            # Try Nebius AI first
            response = self._make_api_request("chat", content_data)

            if response and "message" in response:
                # Parse the AI response into educational content format
                ai_response = response["message"]
                return {
                    "title": f"Understanding {topic.title()}",
                    "content": ai_response,
                    "ai_enhanced": True,
                }

            # Fallback to local content
            return self._get_fallback_educational_content(topic)

        except Exception as e:
            logger.error(f"Educational content generation error: {e}")
            return self._get_fallback_educational_content(topic)

    def _get_fallback_educational_content(self, topic: str) -> Dict[str, str]:
        """Get fallback educational content when Nebius AI is unavailable."""
        topic_lower = topic.lower()

        # Check for specific topics with counseling tone
        if any(word in topic_lower for word in ["stage", "phases", "pre", "peri", "post"]):
            content = self.fallback_responses["educational_content"]["menopause_stages"]
            content["content"] = (
                f"I understand you're seeking information about menopause stages. {content['content']} Remember, every woman's journey is unique, and it's completely normal to have questions about what to expect during this transition."
            )
            return content
        elif any(word in topic_lower for word in ["symptom", "hot flash", "mood", "sleep"]):
            content = self.fallback_responses["educational_content"]["symptoms"]
            content["content"] = (
                f"I know that menopause symptoms can be challenging and disruptive. {content['content']} Please remember that you're not alone in experiencing these symptoms, and there are many effective ways to manage them with support from healthcare providers."
            )
            return content
        elif any(word in topic_lower for word in ["lifestyle", "exercise", "diet", "stress"]):
            content = self.fallback_responses["educational_content"]["lifestyle"]
            content["content"] = (
                f"Taking care of your overall wellbeing during menopause is so important. {content['content']} Making small, sustainable changes can have a big impact on how you feel during this transition."
            )
            return content
        else:
            return {
                "title": "Menopause Information",
                "content": "I want you to know that menopause is a natural transition that every woman experiences, and it's completely normal to have questions or concerns. Understanding your body's changes and working with healthcare providers to manage symptoms and maintain health is an important part of this journey. Remember, you're not alone, and there are many resources and support systems available to help you through this transition.",
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
