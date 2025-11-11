"""
Utility functions for chatbot interface
Helper functions for formatting, validation, and UI components
"""

from datetime import datetime
from typing import List, Dict


def format_timestamp(dt: datetime = None) -> str:
    """
    Format datetime object to readable time string
    
    Args:
        dt: datetime object (uses current time if None)
        
    Returns:
        Formatted time string like "2:45 PM"
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%I:%M %p")


def validate_message(message: str) -> tuple[bool, str]:
    """
    Validate user message before sending
    
    Args:
        message: User input message
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not message or not message.strip():
        return False, "Message cannot be empty"
    
    if len(message) > 2000:
        return False, "Message too long (max 2000 characters)"
    
    return True, ""


def get_welcome_message() -> str:
    """
    Get welcome message for first-time chat users
    
    Returns:
        Welcome message string
    """
    return """👋 **Welcome to Solar Assistant!**

I'm your AI guide for solar panel installations in Sri Lanka. I can help you with:

✅ **System Sizing** - Calculate the right solar capacity for your needs
💰 **Cost Estimates** - Get accurate pricing for different system sizes  
📊 **ROI Analysis** - Understand payback periods and long-term savings
⚡ **CEB/LECO Tariffs** - Learn about electricity rates and net metering
🏗️ **Installation Guide** - Best practices and requirements

**How can I help you today?**"""


def get_quick_actions() -> List[Dict[str, str]]:
    """
    Get list of quick action prompts
    
    Returns:
        List of dicts with 'label' and 'prompt' keys
    """
    return [
        {
            "label": "💰 Calculate ROI for 3kW",
            "prompt": "I want to install a 3kW solar system. Can you calculate the ROI, payback period, and total savings over 25 years?"
        },
        {
            "label": "⚡ Current CEB Tariff Rates",
            "prompt": "What are the current CEB electricity tariff rates in Sri Lanka for different consumption tiers?"
        },
        {
            "label": "📏 How to Size My System",
            "prompt": "How do I calculate the right solar panel system size for my home? My monthly electricity bill is around 300 units."
        },
        {
            "label": "⚖️ Compare 3kW vs 5kW",
            "prompt": "Can you compare 3kW and 5kW solar systems in terms of cost, energy production, roof space, and ROI?"
        },
        {
            "label": "🎁 Government Subsidies",
            "prompt": "What government subsidies, incentives, or financing options are available for solar installations in Sri Lanka?"
        },
        {
            "label": "🔌 Net Metering Info",
            "prompt": "How does net metering work in Sri Lanka? How do I export excess solar energy to the grid?"
        }
    ]


def truncate_context(chat_history: List[Dict], max_messages: int = 10) -> List[Dict]:
    """
    Truncate chat history to manage context window
    
    Args:
        chat_history: Full chat history
        max_messages: Maximum messages to keep
        
    Returns:
        Truncated chat history
    """
    if len(chat_history) <= max_messages:
        return chat_history
    
    return chat_history[-max_messages:]


def format_message_for_display(content: str) -> str:
    """
    Format message content for better display
    Handles markdown, line breaks, etc.
    
    Args:
        content: Raw message content
        
    Returns:
        Formatted content string
    """
    # Replace ** with bold tags for consistency
    content = content.replace("**", "**")
    
    # Ensure proper line breaks
    content = content.replace("\n", "  \n")
    
    return content


def get_error_message(error_code: str) -> str:
    """
    Get user-friendly error message for error codes
    
    Args:
        error_code: Error code from API
        
    Returns:
        User-friendly error message
    """
    error_messages = {
        'API_KEY_MISSING': "🔑 **API Key Required**\n\nTo use the AI assistant, you need to configure your Gemini API key. Add it in Settings or contact support.",
        'INVALID_KEY': "⚠️ **Invalid API Key**\n\nYour API key appears to be invalid. Please check your configuration.",
        'RATE_LIMIT': "⏱️ **Rate Limit Reached**\n\nToo many requests. Please wait a moment before trying again.",
        'NETWORK_ERROR': "🌐 **Connection Error**\n\nUnable to reach the AI service. Please check your internet connection.",
        'BLOCKED_RESPONSE': "🚫 **Response Blocked**\n\nThe AI couldn't generate a response for that query. Please try rephrasing your question.",
        'UNKNOWN': "❌ **Unexpected Error**\n\nSomething went wrong. Please try again or contact support if the issue persists."
    }
    
    return error_messages.get(error_code, error_messages['UNKNOWN'])


def export_chat_history(chat_history: List[Dict]) -> str:
    """
    Export chat history as formatted text
    
    Args:
        chat_history: Chat history to export
        
    Returns:
        Formatted text string
    """
    output = "# Solar Assistant Chat History\n\n"
    output += f"Exported: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n\n"
    output += "---\n\n"
    
    for i, msg in enumerate(chat_history, 1):
        role = "You" if msg["role"] == "user" else "Solar Assistant"
        timestamp = msg.get("timestamp", "")
        content = msg["content"]
        
        output += f"### Message {i} - {role}"
        if timestamp:
            output += f" ({timestamp})"
        output += f"\n\n{content}\n\n"
    
    return output
