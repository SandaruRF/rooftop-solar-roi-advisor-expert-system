"""
Gemini API Integration for Solar ROI Advisor Chatbot
Handles communication with Google Gemini API
"""

import google.generativeai as genai
import streamlit as st
from typing import List, Dict, Optional
import time


def initialize_gemini() -> Optional[genai.GenerativeModel]:
    """
    Initialize Gemini API with API key from secrets or environment
    Returns configured GenerativeModel or None if setup fails
    """
    try:
        # Try to get API key from Streamlit secrets first, then environment
        api_key = None
        
        if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            api_key = st.secrets['GEMINI_API_KEY']
        elif 'GEMINI_API_KEY' in st.session_state:
            api_key = st.session_state.GEMINI_API_KEY
        
        if not api_key:
            return None
        
        # Configure API
        genai.configure(api_key=api_key)
        
        # Create model - using gemini-2.5-flash (stable, fast, available)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        return model
        
    except Exception as e:
        st.error(f"Failed to initialize Gemini API: {str(e)}")
        return None


def format_context_for_gemini(chat_history: List[Dict], user_message: str) -> str:
    """
    Format conversation history and new message for Gemini API
    
    Args:
        chat_history: List of previous messages
        user_message: New user message
        
    Returns:
        Formatted prompt string with context
    """
    system_context = """You are a helpful Solar Energy Advisor for Sri Lankan households.

Help users with:
- Solar panel sizing and costs (LKR currency)
- ROI and payback calculations
- CEB/LECO electricity tariffs
- Installation guidance
- Government incentives

Key facts:
- Solar cost: ~LKR 250,000/kW
- Payback: 5-7 years
- Sun hours: 5 hours/day
- Panel size: 450W standard

Keep responses brief and helpful."""
    
    # Build conversation context (last 5 messages for context window management)
    conversation = system_context + "\n\n"
    
    if chat_history:
        recent_history = chat_history[-5:]  # Keep last 5 messages for context
        conversation += "Previous conversation:\n"
        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation += f"{role}: {msg['content']}\n"
    
    conversation += f"\nUser: {user_message}\nAssistant:"
    
    return conversation


def get_chatbot_response(user_message: str, chat_history: List[Dict], retry_count: int = 1) -> Dict[str, any]:
    """
    Get response from Gemini API (single attempt, no retry loop)
    
    Args:
        user_message: User's message
        chat_history: Previous conversation history
        retry_count: Number of retries on failure (default 1 for no retry)
        
    Returns:
        Dict with 'success', 'message', and optional 'error' keys
    """
    model = initialize_gemini()
    
    if not model:
        return {
            'success': False,
            'error': 'API_KEY_MISSING',
            'message': "⚠️ Gemini API key not configured. Please add your API key in the settings."
        }
    
    # Format the prompt with context
    prompt = format_context_for_gemini(chat_history, user_message)
    
    try:
        # Generate content without safety settings (let API use defaults)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.7,
                top_p=0.95,
                top_k=40,
            )
        )
        
        # Check if response has text (use try-except to avoid attribute error)
        try:
            if response and response.text:
                return {
                    'success': True,
                    'message': response.text.strip()
                }
        except (ValueError, AttributeError):
            # If response.text fails, try to extract from candidates
            pass
        
        # Try to get text from candidates if direct text access fails
        if response and hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content.parts:
                text = ''.join(part.text for part in candidate.content.parts if hasattr(part, 'text'))
                if text:
                    return {
                        'success': True,
                        'message': text.strip()
                    }
            
            # Check finish reason
            if hasattr(candidate, 'finish_reason'):
                if candidate.finish_reason == 2:  # SAFETY
                    return {
                        'success': False,
                        'error': 'SAFETY_BLOCK',
                        'message': "Response was blocked by safety filters. Please rephrase your question."
                    }
                elif candidate.finish_reason == 3:  # RECITATION
                    return {
                        'success': False,
                        'error': 'RECITATION',
                        'message': "Response blocked due to recitation. Please rephrase."
                    }
        
        # Handle blocked or empty responses
        return {
            'success': False,
            'error': 'BLOCKED_RESPONSE',
            'message': "I couldn't generate a response for that question. Please try rephrasing your question."
        }
            
    except Exception as e:
        error_message = str(e)
        
        # Handle specific errors
        if 'quota' in error_message.lower() or 'rate limit' in error_message.lower():
            return {
                'success': False,
                'error': 'RATE_LIMIT',
                'message': f"⏱️ API rate limit reached. Please wait a moment and try again."
            }
        elif 'api key' in error_message.lower():
            return {
                'success': False,
                'error': 'INVALID_KEY',
                'message': "⚠️ Invalid API key. Please check your Gemini API key configuration."
            }
        else:
            return {
                'success': False,
                'error': 'NETWORK_ERROR',
                'message': f"❌ Error: {error_message}"
            }


def test_api_connection() -> bool:
    """
    Test if Gemini API is properly configured and accessible
    
    Returns:
        True if API is working, False otherwise
    """
    try:
        model = initialize_gemini()
        if not model:
            return False
        
        # Simple test query
        response = model.generate_content("Hello")
        return response and response.text is not None
        
    except Exception:
        return False
