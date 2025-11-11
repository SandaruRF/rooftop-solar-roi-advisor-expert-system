"""Render and manage the floating chat popup using standard Streamlit widgets."""

import streamlit as st


def _ensure_session_state() -> None:
    """Ensure all chat popup state flags exist."""

    if "chat_popup_open" not in st.session_state:
        st.session_state.chat_popup_open = False
    if "chat_popup_minimized" not in st.session_state:
        st.session_state.chat_popup_minimized = False
    if "chat_popup_maximized" not in st.session_state:
        st.session_state.chat_popup_maximized = False


def _handle_control_clicks() -> None:
    """Provide hidden buttons that can be triggered via JavaScript."""

    placeholder = st.empty()
    with placeholder.container():
        close_clicked = st.button(
            "chat_close_hidden",
            key="chat_close_hidden",
            help="chat_close_trigger",
        )
        minimize_clicked = st.button(
            "chat_minimize_hidden",
            key="chat_minimize_hidden",
            help="chat_minimize_trigger",
        )
        maximize_clicked = st.button(
            "chat_maximize_hidden",
            key="chat_maximize_hidden",
            help="chat_maximize_trigger",
        )

    if close_clicked:
        st.session_state.chat_popup_open = False
        st.session_state.chat_popup_minimized = False
        st.session_state.chat_popup_maximized = False
    if minimize_clicked:
        st.session_state.chat_popup_minimized = not st.session_state.chat_popup_minimized
        if st.session_state.chat_popup_minimized:
            st.session_state.chat_popup_maximized = False
    if maximize_clicked:
        st.session_state.chat_popup_maximized = not st.session_state.chat_popup_maximized
        if st.session_state.chat_popup_maximized:
            st.session_state.chat_popup_minimized = False


def render_chat_popup() -> None:
    """Render the floating chat popup with minimize/maximize controls."""

    _ensure_session_state()
    _handle_control_clicks()

    if not st.session_state.chat_popup_open:
        return

    state_class = (
        "maximized"
        if st.session_state.chat_popup_maximized
        else "minimized"
        if st.session_state.chat_popup_minimized
        else "open"
    )
    maximize_icon = "◲" if st.session_state.chat_popup_maximized else "◱"

    welcome_section = """
        <div class="welcome-box">
            <h4>👋 Welcome to Solar Assistant!</h4>
            <p>
                I'm here to help you understand solar panel installations, costs,
                and ROI calculations for Sri Lankan households.
            </p>
        </div>
    """

    transcript_section = """
        <div class="message user">
            <div class="message-bubble">
                How much does a 3kW solar system cost?
            </div>
        </div>
        <div class="message assistant">
            <div class="message-bubble">
                A 3kW solar system in Sri Lanka typically costs around
                <strong>LKR 600,000 to 750,000</strong>, depending on the panel quality,
                roof type, and installation complexity. This includes:
                <ul>
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
                For a 3kW system, the typical payback period in Sri Lanka is
                <strong>5-7 years</strong>, depending on your electricity consumption.
                Factors that affect payback:
                <ul>
                    <li>Your monthly electricity usage</li>
                    <li>Location (sun hours per day)</li>
                    <li>Current CEB tariff bracket</li>
                    <li>System efficiency and maintenance</li>
                </ul>
                After payback, you'll enjoy free electricity for 18+ years! ☀️
            </div>
        </div>
    """

    quick_actions_section = """
        <div class="quick-actions">
            <p>💡 Quick Actions:</p>
            <button class="quick-btn" type="button">Calculate ROI</button>
            <button class="quick-btn" type="button">CEB Tariffs</button>
            <button class="quick-btn" type="button">System Sizing</button>
        </div>
    """

    popup_html = f"""
    <style>
    .chat-root {{
        position: fixed;
        inset: 0;
        z-index: 9996;
        pointer-events: none;
        font-family: 'Inter', system-ui, sans-serif;
    }}

    .chat-root .chat-overlay {{
        position: absolute;
        inset: 0;
        background: rgba(15, 23, 42, 0.08);
        pointer-events: none;
    }}

    .chat-popup {{
        position: absolute;
        display: flex;
        flex-direction: column;
        background: #ffffff;
        border-radius: 18px;
        box-shadow: 0 18px 48px rgba(15, 23, 42, 0.28);
        border: 1px solid rgba(102, 126, 234, 0.18);
        overflow: hidden;
        pointer-events: auto;
        backface-visibility: hidden;
        transform-origin: bottom right;
        transition: transform 0.22s ease, opacity 0.22s ease;
    }}

    .chat-root.open .chat-popup {{
        right: 32px;
        bottom: 120px;
        width: min(420px, 92vw);
        height: min(600px, 85vh);
    }}

    .chat-root.minimized .chat-popup {{
        right: 32px;
        bottom: 120px;
        width: 360px;
        height: 92px;
        border-radius: 48px;
    }}

    .chat-root.maximized .chat-popup {{
        top: 24px;
        right: 24px;
        bottom: 24px;
        left: 24px;
        width: auto;
        height: auto;
        border-radius: 22px;
    }}

    .popup-header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 1rem 1.25rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }}

    .chat-root.minimized .popup-header {{
        padding: 0.85rem 1.5rem;
    }}

    .header-title {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .header-title h3 {{
        margin: 0;
        font-size: 1.15rem;
        font-weight: 600;
    }}

    .header-title small {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 500;
        opacity: 0.85;
    }}

    .status-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.18);
    }}

    .header-controls {{
        display: flex;
        gap: 10px;
    }}

    .control-btn {{
        width: 34px;
        height: 34px;
        border-radius: 8px;
        border: none;
        background: rgba(255, 255, 255, 0.24);
        color: inherit;
        font-size: 1.2rem;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: background 0.18s ease, transform 0.18s ease;
    }}

    .control-btn:hover {{
        background: rgba(255, 255, 255, 0.38);
        transform: translateY(-1px);
    }}

    .control-btn.close-btn:hover {{
        background: rgba(255, 77, 77, 0.82);
    }}

    .chat-root.minimized .popup-content,
    .chat-root.minimized .popup-input {{
        display: none;
    }}

    .popup-content {{
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1.5rem;
        background: #f8f9fa;
        overflow-y: auto;
    }}

    .popup-content ul {{
        margin: 0.5rem 0 0 1.25rem;
        padding: 0;
    }}

    .popup-content::-webkit-scrollbar {{ width: 8px; }}
    .popup-content::-webkit-scrollbar-track {{ background: #e9ecef; }}
    .popup-content::-webkit-scrollbar-thumb {{ background: #667eea; border-radius: 10px; }}

    .welcome-box {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.16) 0%, rgba(118, 75, 162, 0.12) 100%);
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 1rem;
        color: #364152;
        box-shadow: 0 6px 18px rgba(102, 126, 234, 0.18);
    }}

    .welcome-box h4 {{
        margin: 0 0 0.5rem 0;
        color: #667eea;
        font-size: 1.05rem;
    }}

    .welcome-box p {{
        margin: 0;
        line-height: 1.6;
        color: #4b5563;
    }}

    .message {{
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }}

    .message-bubble {{
        max-width: 75%;
        padding: 0.85rem 1rem;
        border-radius: 18px;
        line-height: 1.5;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
    }}

    .message.user {{ align-items: flex-end; }}
    .message.user .message-bubble {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border-bottom-right-radius: 6px;
    }}

    .message.assistant {{ align-items: flex-start; }}
    .message.assistant .message-bubble {{
        background: #ffffff;
        color: #303a4b;
        border-bottom-left-radius: 6px;
    }}

    .quick-actions {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        align-items: center;
        background: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
    }}

    .quick-actions p {{
        width: 100%;
        margin: 0 0 0.35rem 0;
        font-weight: 600;
        color: #667eea;
    }}

    .quick-btn {{
        border: 1px solid rgba(102, 126, 234, 0.5);
        color: #4e5ee4;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 999px;
        padding: 0.55rem 1.1rem;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease;
    }}

    .quick-btn:hover {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        transform: translateY(-1px);
    }}

    .popup-input {{
        padding: 1.1rem 1.25rem;
        background: #ffffff;
        border-top: 1px solid rgba(229, 231, 235, 0.9);
        display: flex;
        align-items: center;
    }}

    .input-container {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
    }}

    .input-field {{
        flex: 1;
        padding: 0.85rem 1.1rem;
        border-radius: 24px;
        border: 2px solid rgba(226, 232, 240, 0.9);
        font-size: 0.95rem;
        transition: border 0.18s ease, box-shadow 0.18s ease;
    }}

    .input-field:focus {{
        border-color: rgba(102, 126, 234, 0.85);
        outline: none;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }}

    .send-btn {{
        width: 44px;
        height: 44px;
        border-radius: 50%;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.35);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}

    .send-btn:hover {{
        transform: translateX(2px);
        box-shadow: 0 16px 32px rgba(102, 126, 234, 0.45);
    }}
    </style>

    <div class="chat-root {state_class}">
        <div class="chat-overlay"></div>
        <div class="chat-popup">
            <div class="popup-header">
                <div class="header-title">
                    <span style="font-size:1.6rem;">🤖</span>
                    <div>
                        <h3>Solar Assistant</h3>
                        <small>
                            <span class="status-dot"></span>
                            Online • Replies instantly
                        </small>
                    </div>
                </div>
                <div class="header-controls">
                    <button class="control-btn" data-chat-action="minimize" title="Minimize">−</button>
                    <button class="control-btn" data-chat-action="maximize" title="Toggle size">{maximize_icon}</button>
                    <button class="control-btn close-btn" data-chat-action="close" title="Close">×</button>
                </div>
            </div>
            <div class="popup-content">
                {welcome_section}
                {transcript_section}
                {quick_actions_section}
            </div>
            <div class="popup-input">
                <div class="input-container">
                    <input class="input-field" type="text" placeholder="Type your question here..." />
                    <button class="send-btn" type="button" title="Send message">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
    (function() {{
        const findTrigger = (label) => {{
            const buttons = Array.from(document.querySelectorAll('button[kind]'));
            return buttons.find((btn) => btn.innerText.trim() === label);
        }};

        const hideTrigger = (btn) => {{
            if (!btn) return;
            btn.innerHTML = '';
            const wrapper = btn.closest('div[data-testid="stButton"]');
            if (wrapper) {{
                wrapper.style.position = 'absolute';
                wrapper.style.pointerEvents = 'none';
                wrapper.style.opacity = '0';
                wrapper.style.width = '0';
                wrapper.style.height = '0';
                wrapper.style.overflow = 'hidden';
            }}
        }};

        const initializeTriggers = () => {{
            const triggers = {{
                close: findTrigger('chat_close_hidden'),
                minimize: findTrigger('chat_minimize_hidden'),
                maximize: findTrigger('chat_maximize_hidden')
            }};

            const missing = Object.values(triggers).some((btn) => !btn);
            if (missing) {{
                window.requestAnimationFrame(initializeTriggers);
                return;
            }}

            Object.values(triggers).forEach(hideTrigger);

            document.querySelectorAll('[data-chat-action]').forEach((btn) => {{
                btn.addEventListener('click', (event) => {{
                    event.preventDefault();
                    event.stopPropagation();
                    const action = btn.dataset.chatAction;
                    const trigger = triggers[action];
                    if (trigger) {{
                        trigger.click();
                    }}
                }});
            }});
        }};

        initializeTriggers();
    }})();
    </script>
    """

    st.markdown(popup_html, unsafe_allow_html=True)
