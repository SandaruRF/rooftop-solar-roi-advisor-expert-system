"""
Full-Screen Chatbot Interface for Solar ROI Advisor
Main chatbot UI component with Gemini API integration
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict
import time

from gemini_api import get_chatbot_response, test_api_connection
from chat_utils import (
    format_timestamp, 
    validate_message, 
    get_welcome_message,
    get_quick_actions,
    format_message_for_display
)


def initialize_chat_session():
    """Initialize chat session state variables"""
    if "show_chatbot" not in st.session_state:
        st.session_state.show_chatbot = False
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "waiting_for_response" not in st.session_state:
        st.session_state.waiting_for_response = False
    
    if "show_api_key_input" not in st.session_state:
        st.session_state.show_api_key_input = False
    
    if "last_processed_message" not in st.session_state:
        st.session_state.last_processed_message = None


def inject_chatbot_styles():
    """Inject custom CSS for chatbot interface"""
    st.markdown("""
    <style>
    /* Simple Chat Container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Message Bubbles */
    .message-bubble {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        max-width: 70%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        text-align: left;
    }
    
    .assistant-message {
        background: #f0f0f0;
        color: #333;
        margin-right: auto;
    }
    
    /* Input Area */
    .stTextInput input {
        border-radius: 20px !important;
        padding: 0.75rem 1rem !important;
        border: 2px solid #ddd !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
    }
    </style>
    """, unsafe_allow_html=True)


def display_message(role: str, content: str, timestamp: str = None):
    """
    Display a single chat message bubble
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        timestamp: Optional timestamp string
    """
    css_class = "user-message" if role == "user" else "assistant-message"
    formatted_content = format_message_for_display(content)
    
    message_html = f"""
    <div style="display: flex; justify-content: {'flex-end' if role == 'user' else 'flex-start'}; margin: 0.5rem 0;">
        <div class="message-bubble {css_class}">
            {formatted_content}
        </div>
    </div>
    """
    
    st.markdown(message_html, unsafe_allow_html=True)


def display_typing_indicator():
    """Display animated typing indicator"""
    st.markdown("""
    <div class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
    </div>
    """, unsafe_allow_html=True)


def display_chat_history():
    """Render all chat messages"""
    if not st.session_state.chat_history:
        # Show simple welcome message
        st.info("👋 **Welcome!** Ask me anything about solar panel installations, costs, and ROI.")
    else:
        # Display message history
        for msg in st.session_state.chat_history:
            display_message(
                role=msg["role"],
                content=msg["content"]
            )
        
        # Show typing indicator if waiting for response
        if st.session_state.waiting_for_response:
            st.markdown("💭 *Thinking...*")


def handle_quick_action(prompt: str):
    """Handle quick action button click"""
    # Prevent duplicate requests
    if st.session_state.waiting_for_response:
        return
    
    # Add user message
    timestamp = format_timestamp()
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Set flag to trigger AI response
    st.session_state.waiting_for_response = True
    st.session_state.pending_message = prompt
    st.rerun()


def handle_user_input(user_message: str):
    """
    Process user message and get AI response
    
    Args:
        user_message: User's input message
    """
    # Prevent duplicate processing of same message
    if st.session_state.last_processed_message == user_message:
        return
    
    # Prevent duplicate requests
    if st.session_state.waiting_for_response:
        return
    
    # Validate message
    is_valid, error_msg = validate_message(user_message)
    if not is_valid:
        st.error(error_msg)
        return
    
    # Mark this message as processed
    st.session_state.last_processed_message = user_message
    
    # Add user message to history
    timestamp = format_timestamp()
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_message,
        "timestamp": timestamp
    })
    
    # Set flag to trigger AI response
    st.session_state.waiting_for_response = True
    st.session_state.pending_message = user_message


def render_chatbot_header():
    """Render simple chatbot header with back button"""
    col1, col2 = st.columns([1, 6])
    
    with col1:
        if st.button("← Back", key="back_to_dashboard"):
            st.session_state.show_chatbot = False
            st.rerun()
    
    with col2:
        st.title("🤖 Solar Assistant")


def render_api_key_input():
    """Render API key input section if not configured"""
    if st.session_state.show_api_key_input:
        with st.expander("⚙️ Configure Gemini API Key", expanded=True):
            st.info("To use the AI assistant, you need a Gemini API key. Get one free at https://makersuite.google.com/app/apikey")
            
            api_key = st.text_input(
                "Enter your Gemini API Key:",
                type="password",
                key="api_key_input",
                placeholder="AIza..."
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save API Key", type="primary"):
                    if api_key:
                        st.session_state.GEMINI_API_KEY = api_key
                        st.session_state.show_api_key_input = False
                        st.success("API Key saved! You can now use the chatbot.")
                        st.rerun()
                    else:
                        st.error("Please enter a valid API key")
            
            with col2:
                if st.button("Cancel"):
                    st.session_state.show_api_key_input = False
                    st.rerun()


def render_chat_input():
    """Render simple chat input at bottom"""
    st.markdown("---")
    
    # Use a form to handle Enter key press
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your message:",
            placeholder="Ask about solar panels, costs, ROI...",
            key="chat_input_field",
            label_visibility="collapsed"
        )
        
        submit_button = st.form_submit_button("Send", type="primary", use_container_width=True)
        
        if submit_button and user_input:
            handle_user_input(user_input)


def render_chatbot_interface():
    """
    Main function to render simplified chatbot interface
    Call this from main app when show_chatbot is True
    """
    # Initialize session
    initialize_chat_session()
    
    # Process pending message if waiting for response (ONCE)
    if (st.session_state.waiting_for_response and 
        hasattr(st.session_state, 'pending_message') and
        st.session_state.pending_message is not None):
        
        pending_msg = st.session_state.pending_message
        
        # Clear the pending message immediately to prevent re-processing
        st.session_state.pending_message = None
        
        with st.spinner("Getting response..."):
            response = get_chatbot_response(
                user_message=pending_msg,
                chat_history=st.session_state.chat_history[:-1]  # Exclude current message
            )
        
        # Add assistant response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response["message"],
            "timestamp": format_timestamp()
        })
        
        # Clear flags
        st.session_state.waiting_for_response = False
        st.session_state.last_processed_message = None
        st.rerun()
    
    # Inject styles
    inject_chatbot_styles()
    
    # Render header
    render_chatbot_header()
    
    st.markdown("---")
    
    # Chat display area
    display_chat_history()
    
    # Input section
    render_chat_input()
