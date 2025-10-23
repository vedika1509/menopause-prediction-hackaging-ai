"""
AI Chatbot Page - Conversational interface with Nebius.ai integration
"""

import os
import sys
from datetime import datetime

import streamlit as st

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def render_chatbot_page():
    """Render the AI chatbot page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Page header
    st.markdown(
        """
    <div class="main-header">
        <h1>💬 AI Health Assistant</h1>
        <p style="color: var(--medium-gray);">Your personalized menopause health companion</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize chat session
    if "chat_session_id" not in st.session_state:
        try:
            from chatbot_nebius import NebiusChatbot

            chatbot = NebiusChatbot()

            # Create user context
            user_context = st.session_state.get("user_data", {})
            if "predictions" in st.session_state:
                user_context["predictions"] = st.session_state.predictions

            # Create chat session
            session_id = chatbot.create_chat_session(user_context)
            st.session_state.chat_session_id = session_id
            st.session_state.chatbot = chatbot
        except ImportError:
            st.error("AI Assistant not available. Please ensure all dependencies are installed.")
            return

    # Chat interface
    render_chat_interface()


def render_chat_interface():
    """Render the chat interface."""
    chatbot = st.session_state.get("chatbot")
    session_id = st.session_state.get("chat_session_id")

    if not chatbot or not session_id:
        st.error("Chat session not initialized. Please try again.")
        return

    # Chat container
    chat_container = st.container()

    with chat_container:
        # Display chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Show chat messages
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f"""
                <div class="chat-message chat-user">
                    <strong>You:</strong> {message["content"]}
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class="chat-message chat-assistant">
                    <strong>🌸 AI Assistant:</strong> {message["content"]}
                </div>
                """,
                    unsafe_allow_html=True,
                )

    # Input area
    st.markdown("---")

    # Suggested questions
    st.markdown("### 💡 Suggested Questions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Explain my prediction", use_container_width=True):
            send_message("Can you explain my prediction results?", chatbot, session_id)

        if st.button("🩺 What about my symptoms?", use_container_width=True):
            send_message("What can you tell me about my symptoms?", chatbot, session_id)

    with col2:
        if st.button("🏥 When should I see a doctor?", use_container_width=True):
            send_message("When should I see a doctor about my symptoms?", chatbot, session_id)

        if st.button("💡 How can I improve my health?", use_container_width=True):
            send_message("What lifestyle changes can help me?", chatbot, session_id)

    # Manual input
    st.markdown("### 💬 Ask me anything")

    with st.form("chat_form"):
        user_input = st.text_area(
            "Type your question here...",
            placeholder="Ask about your predictions, symptoms, lifestyle recommendations, or any menopause-related questions...",
            height=100,
        )

        col1, col2 = st.columns([1, 4])

        with col1:
            send_button = st.form_submit_button("Send", use_container_width=True)

        with col2:
            if st.form_submit_button("Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        if send_button and user_input:
            send_message(user_input, chatbot, session_id)

    # Medical disclaimer
    st.markdown(
        """
    <div class="info-card" style="margin-top: 2rem;">
        <h4>⚠️ Medical Disclaimer</h4>
        <p style="font-size: 0.9rem; margin: 0;">
            This AI assistant provides educational information only. It is not a substitute for professional medical advice, 
            diagnosis, or treatment. Always consult your healthcare provider for medical decisions.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def send_message(message, chatbot, session_id):
    """Send a message to the chatbot and display response."""
    if not message.strip():
        return

    # Add user message to history
    st.session_state.chat_history.append(
        {"role": "user", "content": message, "timestamp": datetime.now().isoformat()}
    )

    # Get AI response
    try:
        with st.spinner("🤖 AI is thinking..."):
            response = chatbot.send_message(message, session_id)

        # Add AI response to history
        st.session_state.chat_history.append(
            {"role": "assistant", "content": response, "timestamp": datetime.now().isoformat()}
        )

        # Rerun to show new messages
        st.rerun()

    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")

        # Add error message to history
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": "I'm sorry, I'm having trouble connecting right now. Please try again later or contact support if the issue persists.",
                "timestamp": datetime.now().isoformat(),
            }
        )


# This file is imported by the main app
