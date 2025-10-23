"""
AI Chatbot Page for MenoBalance AI
Interactive chatbot with Nebius AI integration for empathetic health support.
"""

import os

# Import Nebius AI service
import sys
import uuid
from datetime import datetime

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatbot_nebius import get_nebius_service


def render_chatbot_page():
    """Render the AI chatbot page."""
    st.markdown(
        """
    <div class="card">
        <h2 class="card-title">💬 AI Health Assistant</h2>
        <p style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            Chat with our empathetic AI assistant for personalized health support, recommendations, and answers to your questions.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize session variables
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Get Nebius AI service
    nebius_service = get_nebius_service()

    # Create two columns: chat interface and quick actions
    col1, col2 = st.columns([2, 1])

    with col1:
        render_chat_interface(nebius_service)

    with col2:
        render_quick_actions(nebius_service)


def render_chat_interface(nebius_service):
    """Render the main chat interface."""
    st.markdown("### 💬 Chat with Your Health Assistant")

    # Chat container
    chat_container = st.container()

    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f"""
                <div style="
                    background: linear-gradient(90deg, #E8DAEF, #F8F4FF);
                    padding: 1rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                    margin-left: 2rem;
                    border-left: 4px solid #9B59B6;
                ">
                    <strong>You:</strong> {message["content"]}
                    <br>
                    <small style="color: #666;">{message["timestamp"]}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div style="
                    background: linear-gradient(90deg, #F0F8FF, #E3F2FD);
                    padding: 1rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                    margin-right: 2rem;
                    border-left: 4px solid #5DADE2;
                ">
                    <strong>🌸 AI Assistant:</strong> {message["content"]}
                    <br>
                    <small style="color: #666;">{message["timestamp"]}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    # Chat input
    user_input = st.text_area(
        "Type your message here...",
        height=100,
        placeholder="Ask me about menopause symptoms, lifestyle tips, or any health concerns...",
    )

    # Send button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Send Message", use_container_width=True, type="primary"):
            if user_input.strip():
                send_message(user_input, nebius_service)
                st.rerun()
            else:
                st.warning("Please enter a message before sending.")

    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


def render_quick_actions(nebius_service):
    """Render quick action buttons."""
    st.markdown("### 🚀 Quick Actions")

    # Quick action buttons
    quick_actions = [
        ("🔥 Hot Flashes", "I'm experiencing hot flashes. What can I do to manage them?"),
        ("😴 Sleep Issues", "I'm having trouble sleeping. Can you help me with sleep strategies?"),
        ("😰 Mood Changes", "I've been feeling moody lately. Is this normal during menopause?"),
        ("🏃‍♀️ Exercise", "What type of exercise is best for menopause management?"),
        ("🥗 Nutrition", "What foods should I eat to help with menopause symptoms?"),
        ("⚖️ Weight Management", "I'm gaining weight during menopause. What can I do?"),
        ("💊 Hormone Therapy", "Can you tell me about hormone therapy options?"),
        ("🧘‍♀️ Stress Relief", "How can I manage stress during menopause?"),
        ("📊 Health Tracking", "How should I track my menopause symptoms?"),
        ("👩‍⚕️ Doctor Questions", "What questions should I ask my doctor about menopause?"),
    ]

    for action_text, message in quick_actions:
        if st.button(action_text, use_container_width=True, key=f"quick_{action_text}"):
            send_message(message, nebius_service)
            st.rerun()

    # Context information
    st.markdown("---")
    st.markdown("### 📋 Your Health Context")

    if st.session_state.health_data:
        st.markdown("**Available Health Data:**")
        if st.session_state.health_data.get("age"):
            st.markdown(f"• Age: {st.session_state.health_data['age']}")
        if st.session_state.health_data.get("bmi"):
            st.markdown(f"• BMI: {st.session_state.health_data['bmi']:.1f}")
        if st.session_state.health_data.get("exercise_frequency"):
            st.markdown(
                f"• Exercise: {st.session_state.health_data['exercise_frequency']} times/week"
            )
        if st.session_state.health_data.get("stress_level"):
            st.markdown(f"• Stress Level: {st.session_state.health_data['stress_level']}/10")
    else:
        st.markdown(
            "No health data available. Complete the Health Input form for personalized responses."
        )

    # Recent predictions context
    if st.session_state.predictions:
        pred_data = st.session_state.predictions.get("predictions", {})
        if pred_data:
            st.markdown("**Recent Predictions:**")
            if "classification" in pred_data:
                stage = pred_data["classification"].get("stage", "Unknown")
                st.markdown(f"• Menopause Stage: {stage}")
            if "survival" in pred_data:
                time_to_menopause = pred_data["survival"].get("time_to_menopause", 0)
                st.markdown(f"• Time to Menopause: {time_to_menopause:.1f} years")


def send_message(user_message, nebius_service):
    """Send a message to the chatbot and get response."""
    # Add user message to history
    user_msg = {
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state.chat_history.append(user_msg)

    # Prepare context for Nebius AI
    context = {
        "session_id": st.session_state.session_id,
        "health_data": st.session_state.health_data,
        "predictions": st.session_state.predictions,
        "chat_history": st.session_state.chat_history[-5:],  # Last 5 messages for context
    }

    # Get response from Nebius AI
    try:
        with st.spinner("🤖 AI is thinking..."):
            ai_response = nebius_service.chat(user_message, context)

        # Add AI response to history
        ai_msg = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        st.session_state.chat_history.append(ai_msg)

        # Update session context
        nebius_service.update_session_context(st.session_state.session_id, context)

    except Exception:
        # Fallback response
        ai_msg = {
            "role": "assistant",
            "content": "I'm sorry, I'm having trouble responding right now. Please try again or contact support if the issue persists.",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        st.session_state.chat_history.append(ai_msg)


def render_chat_guidelines():
    """Render chat guidelines and disclaimers."""
    st.markdown("---")
    st.markdown("### 📋 Chat Guidelines")

    with st.expander("How to get the best help from your AI assistant"):
        st.markdown("""
        **💡 Tips for better conversations:**
        - Be specific about your symptoms or concerns
        - Ask follow-up questions if you need clarification
        - Mention any relevant health information you've shared
        - Use the quick action buttons for common topics
        
        **🔒 Privacy & Safety:**
        - Your conversations are private and not shared
        - The AI provides general health information only
        - Always consult healthcare providers for medical advice
        - Emergency situations require immediate medical attention
        
        **⚖️ Limitations:**
        - AI responses are for educational purposes only
        - Not a replacement for professional medical advice
        - May not address all individual health situations
        - Always discuss health decisions with qualified professionals
        """)

    # Medical disclaimer
    st.markdown(
        """
    <div class="warning-message">
        <h4>⚠️ Medical Disclaimer</h4>
        <p>This AI assistant provides general health information and support only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with questions about your health condition.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_chat_statistics():
    """Render chat statistics and insights."""
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📊 Chat Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Messages Exchanged", len(st.session_state.chat_history))

        with col2:
            user_messages = len(
                [msg for msg in st.session_state.chat_history if msg["role"] == "user"]
            )
            st.metric("Your Messages", user_messages)

        with col3:
            ai_messages = len(
                [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
            )
            st.metric("AI Responses", ai_messages)


# Add the guidelines and statistics to the main render function
def render_chatbot_page_complete():
    """Complete chatbot page with all sections."""
    render_chatbot_page()
    render_chat_guidelines()
    render_chat_statistics()
