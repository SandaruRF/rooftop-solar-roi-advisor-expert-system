# Chat Popup Feature

## Overview
A floating chat assistant button with popup interface for the Solar ROI Advisor application.

## Files
- `chat_popup.py` - Popup component implementation
- `app.py` - Main app with button integration

## Features

### 1. Floating Button
- **Position**: Fixed at bottom-right corner (30px from edges)
- **Size**: 60x60px circle
- **Style**: Purple-blue gradient with pulse animation
- **Icon**: SVG chat bubbles with dots
- **Behavior**: Clicking opens the chat popup

### 2. Chat Popup Window
- **Default Size**: 400x550px
- **Position**: Above floating button (bottom-right)
- **Components**:
  - Header with title and window controls
  - Scrollable content area with dummy chat messages
  - Input area with text field and send button
  - Overlay for click-outside-to-close

### 3. Window Controls

#### Close Button (×)
- Closes the popup completely
- Returns to just the floating button

#### Minimize Button (−)
- Collapses popup to 350x60px title bar only
- Hides content and input areas
- Click again to restore

#### Maximize Button (◱/◲)
- Expands popup to near-fullscreen (fills viewport with 20px margins)
- Icon changes to restore symbol when maximized
- Click again to return to default size

## Implementation Details

### State Management
Uses Streamlit session state:
- `chat_popup_open` - Whether popup is visible
- `chat_popup_minimized` - Whether popup is collapsed
- `chat_popup_maximized` - Whether popup is fullscreen

### Communication
- Button click → Sets query param `?chat=open` → Page reloads with popup open
- Window controls → JavaScript postMessage → Sets query param → Page reloads with new state
- All interactions trigger page reload to update Streamlit state

### Styling
- **Gradient**: Purple (#667eea) to violet (#764ba2)
- **Shadows**: Subtle elevation with blur
- **Animations**: Slide-in on open, pulse on button
- **Scrollbar**: Custom styled purple scrollbar
- **Responsive**: Adapts to maximized/minimized states

## Dummy Content
Current popup displays:
- Welcome message with gradient background
- Sample conversation (user questions + assistant responses)
- Quick action buttons (Calculate ROI, CEB Tariffs, System Sizing)
- Example topics: 3kW system cost, payback periods, solar coverage

## Future Enhancements
- Connect to actual chatbot backend (Gemini API)
- Real-time message streaming
- Chat history persistence
- User authentication
- File uploads for bills
- Image support for roof photos
- Voice input/output
- Multi-language support

## Usage
The popup automatically appears when clicking the floating button. No additional setup required - just import and call:

```python
from chat_popup import render_chat_popup

# At end of main app
render_chat_popup()
```
