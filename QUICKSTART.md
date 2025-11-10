# Quick Start Guide - Rooftop Solar ROI Advisor

## Installation & Setup

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Run the Application
```powershell
streamlit run app.py
```

### Step 3: Access the App
Open your browser and navigate to:
```
http://localhost:8501
```

## Quick Test Scenarios

### Test 1: Basic Urban Home
- Monthly Usage: 300 kWh
- Location: Colombo
- Roof: Tile
- Budget: 500,000 LKR

Expected: ~2.5 kW system, 7-8 year payback

### Test 2: Large Home with High Usage
- Monthly Usage: 600 kWh
- Location: Galle
- Roof: Concrete
- Budget: 1,200,000 LKR
- Roof Space: 800 sq.ft.

Expected: ~5 kW system, 6-7 year payback

### Test 3: Budget Constrained
- Monthly Usage: 400 kWh
- Location: Kandy
- Roof: Asbestos
- Budget: 350,000 LKR

Expected: Scaled-down recommendation, alternative suggestions

## Troubleshooting

### Issue: Import errors when running
**Solution**: Ensure all dependencies are installed
```powershell
pip install --upgrade -r requirements.txt
```

### Issue: Config file not found
**Solution**: Make sure you're running from the project directory
```powershell
cd "c:\Users\sanda\Desktop\Home\BSc hons AI\Sem 5\es\assignment"
streamlit run app.py
```

### Issue: Port already in use
**Solution**: Use a different port
```powershell
streamlit run app.py --server.port 8502
```

## Project Files Overview

- **app.py** - Main Streamlit web application
- **solar_expert.py** - Experta expert system with rules
- **utils.py** - Helper functions and calculations
- **config.yaml** - Knowledge base with regional data
- **requirements.txt** - Python dependencies

## Key Features to Test

1. **System Sizing** - Enter different usage levels and see recommended sizes
2. **Budget Constraints** - Test with insufficient budgets to see alternatives
3. **Roof Limitations** - Provide small roof sizes to see scaled recommendations
4. **Location Variations** - Try different cities to see sun hour impacts
5. **Expert Reasoning** - Expand the reasoning section to see rule execution

## Customization

### Update Electricity Tariffs
Edit `config.yaml` section:
```yaml
tariffs:
  brackets:
    - max_units: 60
      rate: 8.00  # Update here
```

### Add New Locations
Edit `config.yaml` section:
```yaml
regions:
  your_city:
    sun_hours: 5.5
    uncertainty: 0.3
```

### Modify Cost Estimates
Edit `config.yaml` section:
```yaml
costs:
  cost_per_kw: 180000  # LKR per kW
  fixed_cost: 50000    # Fixed installation cost
```

## Next Steps

1. Test the application with various scenarios
2. Review the expert system reasoning for different inputs
3. Customize the knowledge base for your needs
4. Explore the code to understand the rule execution
5. Consider adding new features from the README

Enjoy your Solar ROI Advisor! ☀️
