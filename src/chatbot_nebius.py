"""
Nebius.ai Chatbot Integration for MenoBalance AI.
Provides conversational AI for explaining predictions and health guidance.
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NebiusChatbot:
    """Nebius.ai chatbot integration for medical conversations."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Nebius.ai chatbot."""
        self.api_key = api_key or os.getenv("NEBIUS_API_KEY")
        self.base_url = "https://api.studio.nebius.ai/v1/"
        self.conversation_history = {}
        self.user_profiles = {}  # Store user health profiles
        self.prediction_context = {}  # Store prediction results for context

        if not self.api_key:
            logger.warning("No Nebius.ai API key provided. Chatbot will use fallback responses.")

    def create_chat_session(self, user_context: Dict[str, Any]) -> str:
        """Initialize a new chat session with user context."""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Store user context for this session
        self.conversation_history[session_id] = {
            "context": user_context,
            "messages": [],
            "created_at": datetime.now().isoformat(),
        }

        # Generate welcome message based on context
        welcome_message = self._generate_welcome_message(user_context)
        self.conversation_history[session_id]["messages"].append(
            {
                "role": "assistant",
                "content": welcome_message,
                "timestamp": datetime.now().isoformat(),
            }
        )

        logger.info(f"Created chat session {session_id} for user")
        return session_id

    def send_message(self, message: str, conversation_id: str) -> str:
        """Send message to Nebius.ai and get response."""
        if conversation_id not in self.conversation_history:
            return "Session not found. Please start a new conversation."

        # Add user message to history
        self.conversation_history[conversation_id]["messages"].append(
            {"role": "user", "content": message, "timestamp": datetime.now().isoformat()}
        )

        # Get AI response
        if self.api_key:
            try:
                response = self._call_nebius_api(message, conversation_id)
            except Exception as e:
                logger.error(f"Nebius.ai API error: {e}")
                response = self._get_fallback_response(message, conversation_id)
        else:
            response = self._get_fallback_response(message, conversation_id)

        # Add AI response to history
        self.conversation_history[conversation_id]["messages"].append(
            {"role": "assistant", "content": response, "timestamp": datetime.now().isoformat()}
        )

        return response

    def update_user_profile(self, session_id: str, health_data: Dict[str, Any]):
        """Update user health profile for better context."""
        if session_id not in self.user_profiles:
            self.user_profiles[session_id] = {}
        
        self.user_profiles[session_id].update(health_data)
        logger.info(f"Updated user profile for session {session_id}")

    def update_prediction_context(self, session_id: str, predictions: Dict[str, Any]):
        """Update prediction results for context-aware responses."""
        self.prediction_context[session_id] = predictions
        logger.info(f"Updated prediction context for session {session_id}")

    def get_contextual_response(self, message: str, session_id: str) -> str:
        """Generate context-aware response using user profile and predictions."""
        user_profile = self.user_profiles.get(session_id, {})
        predictions = self.prediction_context.get(session_id, {})
        
        # Build context string
        context_parts = []
        
        if user_profile:
            age = user_profile.get('age', 'unknown')
            symptoms = user_profile.get('symptoms', [])
            if symptoms:
                context_parts.append(f"User is {age} years old with symptoms: {', '.join(symptoms)}")
            else:
                context_parts.append(f"User is {age} years old")
        
        if predictions:
            survival = predictions.get('survival', {})
            symptoms_pred = predictions.get('symptoms', {})
            
            if survival:
                years = survival.get('time_to_menopause_years', 0)
                risk = survival.get('risk_level', 'unknown')
                context_parts.append(f"Predicted menopause in {years:.1f} years with {risk} risk")
            
            if symptoms_pred:
                severity = symptoms_pred.get('severity_level', 'unknown')
                score = symptoms_pred.get('severity_score', 0)
                context_parts.append(f"Current symptom severity: {severity} (score: {score:.1f})")
        
        context = " | ".join(context_parts) if context_parts else "No specific context available"
        
        # Use Nebius AI with context
        if self.api_key:
            try:
                enhanced_message = f"Context: {context}\n\nUser question: {message}"
                return self._call_nebius_api(enhanced_message, session_id)
            except Exception as e:
                logger.error(f"Contextual response error: {e}")
                return self._get_fallback_response(message, session_id)
        else:
            return self._get_fallback_response(message, session_id)

    def explain_prediction(self, prediction_results: Dict[str, Any]) -> str:
        """Convert technical prediction results to friendly explanation."""
        survival = prediction_results.get("survival", {})
        symptoms = prediction_results.get("symptoms", {})

        explanation = "Let me explain your MenoBalance AI results in simple terms:\n\n"

        # Explain survival prediction
        if survival:
            years = survival.get("time_to_menopause_years", 0)
            risk_level = survival.get("risk_level", "unknown")

            if years < 2:
                explanation += f"🌡️ **Menopause Timeline**: You're likely to reach menopause within {years:.1f} years, which is relatively soon. "
            elif years < 5:
                explanation += f"⏰ **Menopause Timeline**: You're predicted to reach menopause in about {years:.1f} years, which is a moderate timeframe. "
            else:
                explanation += f"🕐 **Menopause Timeline**: You're likely to reach menopause in approximately {years:.1f} years, which gives you more time to prepare. "

            explanation += (
                "This is based on your current age, hormone levels, and health factors.\n\n"
            )

        # Explain symptom prediction
        if symptoms:
            severity = symptoms.get("severity_score", 0)
            severity_level = symptoms.get("severity_level", "unknown")
            top_symptoms = symptoms.get("top_symptoms", [])

            if severity_level == "high":
                explanation += f"⚠️ **Symptom Severity**: Your current symptom severity is {severity_level} (score: {severity:.1f}/10). "
            elif severity_level == "moderate":
                explanation += f"📊 **Symptom Severity**: Your symptom severity is {severity_level} (score: {severity:.1f}/10). "
            else:
                explanation += f"✅ **Symptom Severity**: Your symptom severity is {severity_level} (score: {severity:.1f}/10). "

            if top_symptoms:
                explanation += f"Your main concerns are: {', '.join(top_symptoms)}. "

            explanation += "This helps us understand what symptoms to focus on.\n\n"

        # Add recommendations context
        recommendations = prediction_results.get("recommendations", [])
        if recommendations:
            high_priority = [r for r in recommendations if r.get("priority") == "high"]
            if high_priority:
                explanation += f"🎯 **Priority Actions**: Based on your results, I recommend focusing on: {high_priority[0]['title']}. "

            explanation += "I can provide more specific guidance on any of these areas.\n\n"

        explanation += "💡 **Remember**: These are educational insights based on your current health profile. Always consult with your healthcare provider for medical decisions."

        return explanation

    def get_recommendations(self, user_profile: Dict[str, Any]) -> str:
        """Get personalized health recommendations."""
        age = user_profile.get("age", 0)
        stress_level = user_profile.get("stress_level", 0)
        exercise_frequency = user_profile.get("exercise_frequency", 0)

        recommendations = []

        # Age-based recommendations
        if age < 40:
            recommendations.append(
                "Since you're under 40, focus on preventive health measures and maintaining hormonal balance."
            )
        elif age < 50:
            recommendations.append(
                "You're in the typical perimenopause age range. Monitor your symptoms and consider lifestyle adjustments."
            )
        else:
            recommendations.append(
                "You may be in postmenopause. Focus on long-term health maintenance and bone density."
            )

        # Stress management
        if stress_level > 7:
            recommendations.append(
                "Your stress levels are high. Consider meditation, yoga, or counseling to help manage stress."
            )
        elif stress_level > 4:
            recommendations.append(
                "Moderate stress management techniques like deep breathing or regular breaks can help."
            )

        # Exercise recommendations
        if exercise_frequency < 3:
            recommendations.append(
                "Increasing your exercise frequency to 3-4 times per week can help with menopause symptoms."
            )
        elif exercise_frequency >= 5:
            recommendations.append(
                "Great job maintaining regular exercise! This will help with your overall health during menopause."
            )

        if not recommendations:
            recommendations.append("Continue maintaining your current healthy lifestyle habits.")

        return "Here are some personalized recommendations for you:\n\n" + "\n".join(
            [f"• {rec}" for rec in recommendations]
        )

    def _call_nebius_api(self, message: str, conversation_id: str) -> str:
        """Call Nebius.ai API for response."""
        # This is a placeholder for the actual Nebius.ai API integration
        # In a real implementation, you would use the actual API endpoints

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        # Get conversation context
        context = self.conversation_history[conversation_id]["context"]

        # Prepare the prompt with medical context
        system_prompt = f"""You are a helpful AI assistant specializing in menopause and women's health. 
        You provide empathetic, evidence-based guidance while always recommending professional medical consultation.
        
        User Context:
        - Age: {context.get("age", "Not provided")}
        - Current symptoms: {context.get("symptoms", "Not provided")}
        - Health concerns: {context.get("concerns", "Not provided")}
        
        Guidelines:
        - Be empathetic and supportive
        - Use simple, clear language
        - Always recommend consulting healthcare providers for medical decisions
        - Provide evidence-based information
        - Avoid giving specific medical diagnoses
        - Encourage healthy lifestyle choices
        """

        payload = {
            "model": "gpt-3.5-turbo",  # or appropriate Nebius.ai model
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        }

        # Make API call (placeholder - replace with actual Nebius.ai endpoint)
        response = requests.post(
            f"{self.base_url}chat/completions", headers=headers, json=payload, timeout=30
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API call failed with status {response.status_code}")

    def _get_fallback_response(self, message: str, conversation_id: str) -> str:
        """Provide fallback response when API is unavailable."""
        message_lower = message.lower()

        if "prediction" in message_lower or "results" in message_lower:
            return "I'd be happy to help explain your MenoBalance AI results. Could you share what specific aspects you'd like me to clarify?"

        elif "symptoms" in message_lower:
            return "I can help you understand your symptoms better. What specific symptoms are you experiencing, and how are they affecting your daily life?"

        elif "doctor" in message_lower or "medical" in message_lower:
            return "It's always a good idea to consult with your healthcare provider about any health concerns. They can provide personalized medical advice based on your specific situation."

        elif "help" in message_lower:
            return "I'm here to help you understand your menopause health insights. You can ask me about your predictions, symptoms, lifestyle recommendations, or any other health-related questions."

        else:
            return "I understand you have questions about your health. I'm here to provide supportive guidance about menopause and women's health. What would you like to know more about?"

    def _generate_welcome_message(self, user_context: Dict[str, Any]) -> str:
        """Generate personalized welcome message."""
        age = user_context.get("age", 0)
        name = user_context.get("name", "")

        greeting = f"Hi {name}! " if name else "Hello! "

        if age < 40:
            greeting += "I'm here to help you understand your menopause health insights. Even though you're under 40, understanding your hormonal health early can be very beneficial."
        elif age < 50:
            greeting += "I'm here to support you through your menopause journey. You're in a great position to manage your health during this important transition."
        else:
            greeting += "I'm here to help you maintain your health and well-being during and after menopause. Your health insights can guide your ongoing wellness."

        greeting += "\n\nI can help you understand your MenoBalance AI results, answer questions about symptoms, provide lifestyle recommendations, and offer general health guidance. What would you like to know?"

        return greeting

    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        return self.conversation_history.get(conversation_id, {}).get("messages", [])

    def simplify_medical_report(self, model_insights_json: Dict[str, Any]) -> str:
        """Convert technical model insights to conversational explanation."""
        models = model_insights_json.get("models", {})

        explanation = "Here's what your MenoBalance AI models tell us:\n\n"

        # Explain model performance
        if "survival" in models:
            survival_perf = models["survival"]["performance"]
            explanation += f"📊 **Menopause Timeline Model**: This model is {survival_perf['cv_mean']:.1%} accurate at predicting when menopause might occur. "
            explanation += "It considers your age, hormone levels, and health factors to estimate your timeline.\n\n"

        if "symptom" in models:
            symptom_perf = models["symptom"]["performance"]
            explanation += f"🩺 **Symptom Severity Model**: This model is {symptom_perf['cv_mean']:.1%} accurate at predicting symptom severity. "
            explanation += "It helps identify which symptoms might be most concerning for you.\n\n"

        # Explain limitations
        explanation += "⚠️ **Important Notes**:\n"
        explanation += "• These are educational tools, not medical diagnoses\n"
        explanation += "• Always consult your healthcare provider for medical decisions\n"
        explanation += "• Models are based on research data and may not apply to everyone\n"
        explanation += "• Your individual health journey is unique\n\n"

        explanation += "I'm here to help you understand these results and what they mean for your health journey!"

        return explanation

    def generate_personalized_recommendations(self, user_data: Dict[str, Any], predictions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations using Nebius AI."""
        try:
            # Build context for Nebius AI
            context = f"""
            User Profile:
            - Age: {user_data.get('age', 'unknown')}
            - BMI: {user_data.get('bmi', 'unknown')}
            - Symptoms: {user_data.get('symptoms', [])}
            
            Predictions:
            - Menopause Timeline: {predictions.get('survival', {}).get('time_to_menopause_years', 'unknown')} years
            - Risk Level: {predictions.get('survival', {}).get('risk_level', 'unknown')}
            - Symptom Severity: {predictions.get('symptoms', {}).get('severity_level', 'unknown')}
            - Severity Score: {predictions.get('symptoms', {}).get('severity_score', 'unknown')}
            
            Please provide personalized recommendations for:
            1. Stress management
            2. Sleep improvement
            3. Symptom management
            4. Lifestyle modifications
            5. When to consult healthcare provider
            """
            
            if self.api_key:
                try:
                    response = self._call_nebius_api(context, "recommendations")
                    # Parse Nebius response into structured recommendations
                    return self._parse_recommendations_response(response)
                except Exception as e:
                    logger.error(f"Error generating Nebius recommendations: {e}")
                    return self._get_fallback_recommendations(predictions)
            else:
                return self._get_fallback_recommendations(predictions)
                
        except Exception as e:
            logger.error(f"Error in generate_personalized_recommendations: {e}")
            return self._get_fallback_recommendations(predictions)

    def _parse_recommendations_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse Nebius AI response into structured recommendations."""
        # This would parse the Nebius response and structure it
        # For now, return a structured format
        recommendations = []
        
        # Parse response and extract recommendations
        lines = response.split('\n')
        current_priority = 'medium'
        
        for line in lines:
            line = line.strip()
            if 'high' in line.lower() or 'urgent' in line.lower():
                current_priority = 'high'
            elif 'low' in line.lower():
                current_priority = 'low'
            
            if line and not line.startswith('#') and len(line) > 10:
                recommendations.append({
                    'priority': current_priority,
                    'title': line[:50] + '...' if len(line) > 50 else line,
                    'description': line,
                    'source': 'Nebius AI'
                })
        
        return recommendations[:5]  # Limit to 5 recommendations

    def _get_fallback_recommendations(self, predictions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback recommendations when Nebius AI is not available."""
        recommendations = []
        
        survival = predictions.get('survival', {})
        symptoms = predictions.get('symptoms', {})
        
        # Risk-based recommendations
        risk_level = survival.get('risk_level', 'moderate')
        if risk_level == 'high':
            recommendations.append({
                'priority': 'high',
                'title': 'Schedule Healthcare Consultation',
                'description': 'Your risk assessment suggests immediate consultation with a healthcare provider.',
                'source': 'MenoBalance AI'
            })
        
        # Symptom-based recommendations
        severity = symptoms.get('severity_level', 'moderate')
        if severity == 'severe':
            recommendations.append({
                'priority': 'high',
                'title': 'Symptom Management',
                'description': 'Consider discussing symptom management strategies with your healthcare provider.',
                'source': 'MenoBalance AI'
            })
        elif severity == 'moderate':
            recommendations.append({
                'priority': 'medium',
                'title': 'Lifestyle Modifications',
                'description': 'Focus on stress management, regular exercise, and balanced nutrition.',
                'source': 'MenoBalance AI'
            })
        
        # General recommendations
        recommendations.extend([
            {
                'priority': 'medium',
                'title': 'Regular Monitoring',
                'description': 'Continue tracking your symptoms and wellness metrics.',
                'source': 'MenoBalance AI'
            },
            {
                'priority': 'low',
                'title': 'Educational Resources',
                'description': 'Explore our educational resources for menopause information.',
                'source': 'MenoBalance AI'
            }
        ])
        
        return recommendations


def main():
    """Test the Nebius chatbot integration."""
    print("Testing Nebius.ai Chatbot Integration...")

    # Initialize chatbot
    chatbot = NebiusChatbot()

    # Test user context
    user_context = {
        "age": 45,
        "name": "Sarah",
        "symptoms": ["hot_flashes", "sleep_issues"],
        "concerns": ["timeline", "symptom_management"],
    }

    # Create session
    session_id = chatbot.create_chat_session(user_context)
    print(f"Created session: {session_id}")

    # Test conversation
    response1 = chatbot.send_message("Can you explain my prediction results?", session_id)
    print(f"Response 1: {response1}")

    response2 = chatbot.send_message("What can I do about hot flashes?", session_id)
    print(f"Response 2: {response2}")

    # Test prediction explanation
    prediction_results = {
        "survival": {"time_to_menopause_years": 3.2, "risk_level": "moderate"},
        "symptoms": {
            "severity_score": 6.5,
            "severity_level": "moderate",
            "top_symptoms": ["hot_flashes"],
        },
        "recommendations": [{"priority": "high", "title": "Consult Healthcare Provider"}],
    }

    explanation = chatbot.explain_prediction(prediction_results)
    print(f"Prediction explanation: {explanation}")

    print("Chatbot integration test completed!")


if __name__ == "__main__":
    main()
