# Solar ROI Advisor - AI Chatbot Setup Guide

## Overview
The Solar ROI Advisor now includes a full-screen AI chatbot powered by Google Gemini API. Users can ask questions about solar installations, costs, ROI calculations, and get personalized advice.

## Features
- 🤖 **AI-Powered Responses** - Natural language understanding using Gemini Pro
- 💬 **Full-Screen Interface** - Clean, professional chat experience
- 🚀 **Quick Actions** - Pre-defined prompts for common questions
- 📊 **Context-Aware** - Maintains conversation history
- 🎨 **Beautiful UI** - Gradient purple theme matching dashboard
- ⚡ **Fast Responses** - Typically under 3 seconds
- 🔒 **Secure** - API key stored in secrets

## Setup Instructions

### 1. Get Gemini API Key (Free)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Configure API Key

**Option A: Using Streamlit Secrets (Recommended)**
1. Create a `.streamlit` folder in your project root if it doesn't exist
2. Create a `secrets.toml` file inside `.streamlit` folder
3. Add your API key:
```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

**Option B: Using the UI**
1. Run the app
2. Click "💬 Chat Assistant" button
3. Enter your API key when prompted
4. Click "Save API Key"

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

The main dependency is:
- `google-generativeai>=0.3.0`

### 4. Run the Application
```bash
streamlit run app.py
```

## Usage

### Accessing the Chatbot
1. Open the Solar ROI Advisor dashboard
2. Click the "💬 Chat Assistant" button in the header
3. The full-screen chat interface will open

### Quick Actions
Click any of the pre-defined prompts:
- 💰 Calculate ROI for 3kW
- ⚡ Current CEB Tariff Rates
- 📏 How to Size My System
- ⚖️ Compare 3kW vs 5kW
- 🎁 Government Subsidies
- 🔌 Net Metering Info

### Asking Questions
Type your question in the input box at the bottom and press Send or Enter.

**Example Questions:**
- "What is the cost of a 5kW solar system in Colombo?"
- "How do I calculate ROI for my 300 unit monthly consumption?"
- "What are the CEB tariff rates for residential customers?"
- "How many panels do I need for a 4kW system?"
- "What government incentives are available for solar?"

### Navigation
- **Back Button** - Return to the main dashboard
- **Clear Button** - Reset chat history and start fresh

## Technical Details

### Architecture
```
app.py                      # Main application entry point
├── chatbot_interface.py    # UI components and rendering
├── gemini_api.py          # Gemini API integration
└── chat_utils.py          # Helper functions
```

### File Descriptions

**chatbot_interface.py**
- `render_chatbot_interface()` - Main render function
- `display_chat_history()` - Message rendering
- `handle_user_input()` - Input processing
- Custom CSS styling and animations

**gemini_api.py**
- `initialize_gemini()` - API setup
- `get_chatbot_response()` - Get AI responses with retry logic
- `format_context_for_gemini()` - Context window management
- Error handling and rate limiting

**chat_utils.py**
- Message validation
- Timestamp formatting
- Quick action definitions
- Welcome message generation
- Export functionality

### Session State Variables
- `show_chatbot` - Toggle between dashboard and chat
- `chat_history` - List of messages
- `waiting_for_response` - Loading state
- `GEMINI_API_KEY` - API key storage

### System Prompt Context
The AI is configured as a Solar Energy Advisor for Sri Lankan households with knowledge of:
- Local solar panel costs and system sizing
- CEB and LECO tariff structures
- ROI calculations and payback periods
- Installation requirements
- Government incentives
- Net metering policies

All responses use LKR currency and are localized for Sri Lanka.

## Features in Detail

### Context Window Management
- Keeps last 5 messages for API context
- Prevents token limit issues
- Maintains conversation coherence

### Error Handling
- API key validation
- Rate limit detection
- Network error retry (3 attempts with exponential backoff)
- User-friendly error messages
- Graceful degradation

### UI/UX Features
- Smooth message animations
- Typing indicator while processing
- Auto-scroll to latest message
- Responsive design
- Mobile-friendly
- Custom scrollbar styling
- Message timestamps
- Distinct user/assistant bubbles

### Performance
- Typical response time: <3 seconds
- Efficient context management
- Minimal re-rendering
- Optimized API calls

## API Rate Limits

**Free Tier:**
- 60 requests per minute
- 1500 requests per day

The chatbot includes rate limit detection and will notify users if limits are reached.

## Troubleshooting

### "API Key Not Configured"
**Solution:** Add your API key using one of the configuration methods above.

### "Invalid API Key"
**Solution:** 
1. Verify your API key is correct
2. Ensure there are no extra spaces
3. Get a new key from Google AI Studio if needed

### "Rate Limit Reached"
**Solution:** Wait a few moments and try again. Consider upgrading to paid tier for higher limits.

### "Connection Error"
**Solution:** 
1. Check your internet connection
2. Verify firewall isn't blocking the API
3. Try again in a moment

### Messages Not Appearing
**Solution:** 
1. Clear chat history and try again
2. Refresh the page
3. Check browser console for errors

## Security Best Practices

1. **Never commit secrets.toml** - Already in .gitignore
2. **Use environment variables in production**
3. **Rotate API keys periodically**
4. **Monitor API usage** in Google Cloud Console
5. **Don't share API keys** in code or screenshots

## Future Enhancements

Potential improvements:
- [ ] Multi-language support (Sinhala, Tamil)
- [ ] Voice input/output
- [ ] Chat history export to PDF
- [ ] Image analysis (roof photos)
- [ ] Integration with live CEB tariff API
- [ ] Personalized recommendations based on user profile
- [ ] Conversation analytics
- [ ] WhatsApp/Telegram bot integration

## Support

For issues or questions:
1. Check this documentation
2. Review error messages carefully
3. Test API key separately
4. Check Google AI Studio status page
5. Contact project maintainer

## Credits

- **UI Framework:** Streamlit
- **AI Model:** Google Gemini Pro
- **Design:** Gradient purple theme
- **Target Market:** Sri Lankan residential solar customers

## License

Same as main project license.

---

**Last Updated:** November 2025
**Version:** 1.0.0
