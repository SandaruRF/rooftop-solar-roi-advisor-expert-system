# 🚀 Installation & Setup Guide

## Complete Setup Instructions for Solar ROI Advisor

### Prerequisites Check
Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager)
- ✅ Internet connection for downloading packages
- ✅ PowerShell or Command Prompt access

To check your Python version:
```powershell
python --version
```

---

## Step-by-Step Installation

### Step 1: Navigate to Project Directory
```powershell
cd "c:\Users\sanda\Desktop\Home\BSc hons AI\Sem 5\es\assignment"
```

### Step 2: Create Virtual Environment (Recommended)
Creating a virtual environment keeps your project dependencies isolated.

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You should see `(venv)` at the start of your command line prompt.

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

This will install:
- `experta==1.9.4` - Expert system framework
- `streamlit==1.28.0` - Web UI framework
- `pyyaml==6.0.1` - Configuration file handling
- `pandas==2.1.0` - Data manipulation
- `numpy==1.24.3` - Numerical operations

Installation should take 1-2 minutes.

### Step 4: Verify Installation
Run the test script to ensure everything is working:

```powershell
python test_system.py
```

You should see output from 6 test scenarios. If all tests pass, you're ready to go! ✅

---

## Running the Application

### Option 1: Web Interface (Recommended)
Start the Streamlit web application:

```powershell
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

If it doesn't open automatically, manually navigate to the URL shown in the terminal.

**To stop the server**: Press `Ctrl+C` in the terminal

### Option 2: Programmatic Usage
Run example scripts to see how to use the system in your own code:

```powershell
python examples.py
```

This demonstrates various ways to use the expert system programmatically.

---

## Quick Test

Once the app is running, try this scenario:

**Test Input:**
- Monthly Usage: 300 kWh
- Location: Colombo
- Roof Type: Tile
- Budget: 500,000 LKR
- (Leave roof space unchecked)

**Click**: "🔍 Analyze Solar Investment"

**Expected Output:**
- System Size: ~2.5 kW
- Panels: ~6 panels
- Cost: ~LKR 500,000
- Payback: ~7-8 years
- Category: Good Investment

---

## Troubleshooting

### Problem: "Python is not recognized"
**Solution**: Python is not in your PATH. Download and install Python from python.org, ensuring you check "Add Python to PATH" during installation.

### Problem: "pip is not recognized"
**Solution**: 
```powershell
python -m ensurepip --upgrade
```

### Problem: Cannot activate virtual environment
**Solution**: 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Module import errors
**Solution**: Ensure you're in the virtual environment and reinstall dependencies:
```powershell
pip install --upgrade -r requirements.txt
```

### Problem: "FileNotFoundError: config.yaml"
**Solution**: Make sure you're running commands from the project directory:
```powershell
cd "c:\Users\sanda\Desktop\Home\BSc hons AI\Sem 5\es\assignment"
```

### Problem: Port 8501 already in use
**Solution**: Use a different port:
```powershell
streamlit run app.py --server.port 8502
```

### Problem: Streamlit shows "ModuleNotFoundError: No module named 'experta'"
**Solution**: Activate virtual environment before running:
```powershell
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

---

## File Structure Overview

```
assignment/
│
├── app.py                 # Streamlit web application (run this!)
├── solar_expert.py        # Expert system rules (Experta)
├── utils.py               # Calculation utilities
├── config.yaml            # Knowledge base configuration
│
├── requirements.txt       # Python dependencies
├── README.md             # Full documentation
├── QUICKSTART.md         # Quick start guide
├── SETUP.md              # This file
│
├── test_system.py        # Test suite
├── examples.py           # Usage examples
│
└── .gitignore            # Git ignore rules
```

---

## Next Steps

1. ✅ **Test the application** with various scenarios
2. ✅ **Read README.md** for detailed documentation
3. ✅ **Customize config.yaml** for your specific needs
4. ✅ **Explore examples.py** to learn programmatic usage
5. ✅ **Review test_system.py** to understand test scenarios

---

## Development Setup (Optional)

If you want to modify the code:

### Install development tools
```powershell
pip install black flake8 mypy
```

### Code formatting
```powershell
black *.py
```

### Linting
```powershell
flake8 *.py
```

---

## Updating Dependencies

To update all packages to latest versions:

```powershell
pip install --upgrade -r requirements.txt
```

---

## Deactivating Virtual Environment

When you're done:

```powershell
deactivate
```

---

## Uninstall

To remove everything:

1. Deactivate and delete virtual environment:
```powershell
deactivate
Remove-Item -Recurse -Force venv
```

2. (Optional) Delete the entire project directory

---

## System Requirements

**Minimum:**
- OS: Windows 10 or later
- Python: 3.8+
- RAM: 2 GB
- Disk Space: 500 MB

**Recommended:**
- OS: Windows 11
- Python: 3.10+
- RAM: 4 GB
- Disk Space: 1 GB

---

## Getting Help

- Check **README.md** for detailed documentation
- Review **QUICKSTART.md** for quick reference
- Run **test_system.py** to verify setup
- Check **examples.py** for usage patterns

---

## Success Checklist

Before using the application, verify:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Test suite passes (`python test_system.py`)
- [ ] Streamlit app launches (`streamlit run app.py`)
- [ ] Can access app in browser (http://localhost:8501)
- [ ] Sample scenario produces results

If all boxes are checked, you're all set! 🎉

---

**Need more help?** Check the main README.md or contact the developer.

Happy analyzing! ☀️
