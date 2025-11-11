"""
Chat Popup Interface Component - Simplified Version
Handles the chat window UI and interactions using pure HTML/CSS
"""

import streamlit as st


def render_chat_popup():
    """Render the chat popup window with controls"""
    
    # Initialize session state
    if "chat_popup_open" not in st.session_state:
        st.session_state.chat_popup_open = False
    if "chat_popup_minimized" not in st.session_state:
        st.session_state.chat_popup_minimized = False
    if "chat_popup_maximized" not in st.session_state:
        st.session_state.chat_popup_maximized = False
    
    # Handle query parameter actions (using older API for Streamlit 1.28.0)
    query_params = st.experimental_get_query_params()
    if "action" in query_params:
        action = query_params["action"][0]  # Get first value from list
        if action == "open":
            st.session_state.chat_popup_open = True
            st.session_state.chat_popup_minimized = False
        elif action == "close":
            st.session_state.chat_popup_open = False
            st.session_state.chat_popup_minimized = False
            st.session_state.chat_popup_maximized = False
        elif action == "minimize":
            st.session_state.chat_popup_minimized = not st.session_state.chat_popup_minimized
            if st.session_state.chat_popup_minimized:
                st.session_state.chat_popup_maximized = False
        elif action == "maximize":
            st.session_state.chat_popup_maximized = not st.session_state.chat_popup_maximized
            if st.session_state.chat_popup_maximized:
                st.session_state.chat_popup_minimized = False
        # Clear query param after handling
        st.experimental_set_query_params()
        st.rerun()
    
    # Check for button clicks from components
    if "popup_action" in st.session_state:
        action = st.session_state.popup_action
        if action == "close":
            st.session_state.chat_popup_open = False
            st.session_state.chat_popup_minimized = False
            st.session_state.chat_popup_maximized = False
        elif action == "minimize":
            st.session_state.chat_popup_minimized = not st.session_state.chat_popup_minimized
            if st.session_state.chat_popup_minimized:
                st.session_state.chat_popup_maximized = False
        elif action == "maximize":
            st.session_state.chat_popup_maximized = not st.session_state.chat_popup_maximized
            if st.session_state.chat_popup_maximized:
                st.session_state.chat_popup_minimized = False
        del st.session_state.popup_action
        st.rerun()
    
    # Only render if popup is open
    if not st.session_state.chat_popup_open:
        return
    
    # Determine popup size based on state
    if st.session_state.chat_popup_maximized:
        popup_style = "top: 20px; left: 20px; right: 20px; bottom: 20px; width: calc(100% - 40px); height: calc(100% - 40px);"
        content_display = "flex"
    elif st.session_state.chat_popup_minimized:
        popup_style = "bottom: 100px; right: 30px; width: 350px; height: 60px;"
        content_display = "none"
    else:
        popup_style = "bottom: 100px; right: 30px; width: 400px; height: 550px;"
        content_display = "flex"
    
    maximize_icon = "◲" if st.session_state.chat_popup_maximized else "◱"
    maximize_title = "Restore" if st.session_state.chat_popup_maximized else "Maximize"
    
    # Render the complete popup with inline JavaScript
    popup_html = f"""
    <style>
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        #chatOverlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.3);
            z-index: 9997;
        }}
        
        #chatPopup {{
            position: fixed;
            {popup_style}
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 9998;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            animation: slideIn 0.3s ease-out;
        }}
        
        .chat-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }}
        
        .header-controls {{
            display: flex;
            gap: 8px;
        }}
        
        .control-btn {{
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.2rem;
            transition: background 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .control-btn:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}
        
        .close-btn:hover {{
            background: rgba(255, 77, 77, 0.8) !important;
        }}
        
        .chat-content {{
            display: {content_display};
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
            background: #f8f9fa;
            flex-direction: column;
        }}
        
        .chat-content::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .chat-content::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 10px;
        }}
        
        .chat-content::-webkit-scrollbar-thumb {{
            background: #667eea;
            border-radius: 10px;
        }}
        
        .welcome-box {{
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }}
        
        .message {{
            margin-bottom: 1rem;
        }}
        
        .message.user {{
            text-align: right;
        }}
        
        .message-bubble {{
            display: inline-block;
            padding: 0.75rem 1rem;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
            text-align: left;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .message.user .message-bubble {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }}
        
        .message.assistant .message-bubble {{
            background: white;
            color: #333;
            border-bottom-left-radius: 5px;
        }}
        
        .quick-actions {{
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .quick-btn {{
            padding: 0.5rem 1rem;
            background: #667eea15;
            border: 1px solid #667eea;
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
            margin: 4px;
        }}
        
        .quick-btn:hover {{
            background: #667eea;
            color: white;
        }}
        
        .chat-input {{
            display: {content_display};
            padding: 1rem;
            border-top: 1px solid #e0e0e0;
            background: white;
            border-radius: 0 0 15px 15px;
            gap: 8px;
            align-items: center;
        }}
        
        .input-field {{
            flex: 1;
            padding: 0.75rem;
            border: 2px solid #e0e0e0;
            border-radius: 20px;
            outline: none;
            font-size: 0.95rem;
            transition: border-color 0.2s;
        }}
        
        .input-field:focus {{
            border-color: #667eea;
        }}
        
        .send-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }}
        
        .send-btn:hover {{
            transform: scale(1.1);
        }}
    </style>
    
    <div id="chatOverlay">
        <form action="" method="get" style="width: 100%; height: 100%;">
            <input type="hidden" name="action" value="close">
            <button type="submit" style="width: 100%; height: 100%; background: transparent; border: none; cursor: pointer;"></button>
        </form>
    </div>
    
    <div id="chatPopup">
        <div class="chat-header">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.5rem;">🤖</span>
                <h3 style="margin: 0; font-size: 1.1rem; font-weight: 600;">Solar Assistant</h3>
            </div>
            
            <div class="header-controls">
                <form action="" method="get" style="display: inline-block;">
                    <input type="hidden" name="action" value="minimize">
                    <button type="submit" class="control-btn" title="Minimize">−</button>
                </form>
                <form action="" method="get" style="display: inline-block;">
                    <input type="hidden" name="action" value="maximize">
                    <button type="submit" class="control-btn" title="{maximize_title}">{maximize_icon}</button>
                </form>
                <form action="" method="get" style="display: inline-block;">
                    <input type="hidden" name="action" value="close">
                    <button type="submit" class="control-btn close-btn" title="Close">×</button>
                </form>
            </div>
        </div>
        
        <div class="chat-content">
            <div class="welcome-box">
                <h4 style="margin: 0 0 0.5rem 0; color: #667eea;">👋 Welcome to Solar Assistant!</h4>
                <p style="margin: 0; color: #555; line-height: 1.6;">
                    I'm here to help you understand solar panel installations, costs, and ROI calculations 
                    for Sri Lankan households.
                </p>
            </div>
            
            <div class="message user">
                <div class="message-bubble">
                    How much does a 3kW solar system cost?
                </div>
            </div>
            
            <div class="message assistant">
                <div class="message-bubble">
                    A 3kW solar system in Sri Lanka typically costs around <strong>LKR 600,000 to 750,000</strong>, 
                    depending on the panel quality, roof type, and installation complexity. This includes:
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        <li>Solar panels (6-7 panels of 450W each)</li>
                        <li>Inverter system</li>
                        <li>Mounting structures</li>
                        <li>Installation and labor</li>
                    </ul>
                    Would you like to see a detailed breakdown?
                </div>
            </div>
            
            <div class="message user">
                <div class="message-bubble">
                    What's the payback period?
                </div>
            </div>
            
            <div class="message assistant">
                <div class="message-bubble">
                    For a 3kW system, the typical payback period in Sri Lanka is <strong>5-7 years</strong>, 
                    depending on your electricity consumption. Factors that affect payback:
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        <li>Your monthly electricity usage</li>
                        <li>Location (sun hours per day)</li>
                        <li>Current CEB tariff bracket</li>
                        <li>System efficiency and maintenance</li>
                    </ul>
                    After payback, you'll enjoy free electricity for 18+ years! ☀️
                </div>
            </div>
            
            <div class="quick-actions">
                <p style="margin: 0 0 0.75rem 0; font-weight: 600; color: #667eea;">
                    💡 Quick Actions:
                </p>
                <button class="quick-btn">Calculate ROI</button>
                <button class="quick-btn">CEB Tariffs</button>
                <button class="quick-btn">System Sizing</button>
            </div>
        </div>
        
        <div class="chat-input">
            <input type="text" class="input-field" placeholder="Type your question here...">
            <button class="send-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
            </button>
        </div>
    </div>
    """
    
    st.markdown(popup_html, unsafe_allow_html=True)
