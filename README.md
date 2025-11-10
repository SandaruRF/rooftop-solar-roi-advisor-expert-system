# ☀️ Rooftop Solar ROI Advisor for Sri Lanka

An intelligent expert system built with **Python Experta** and **Streamlit** that provides actionable rooftop solar investment recommendations for Sri Lankan households. The system analyzes electricity usage, location, roof characteristics, and budget constraints to deliver personalized solar installation advice with confidence estimates.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Experta](https://img.shields.io/badge/Experta-1.9.4-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Functionality
- **Smart System Sizing**: Calculates optimal solar panel system size based on consumption patterns and location-specific sun hours
- **Cost Estimation**: Provides detailed installation cost estimates with roof-type adjustments
- **ROI Analysis**: Calculates payback period using up-to-date CEB/LECO tariff structures
- **Constraint Handling**: Intelligently adapts recommendations when budget or roof space limitations exist
- **Confidence Assessment**: Reports uncertainty ranges in payback estimates based on multiple factors
- **Expert Reasoning**: Shows step-by-step logic behind recommendations for transparency

### Technical Features
- **Rule-Based Expert System**: Uses Experta framework for forward-chaining inference
- **Progressive Tariff Calculation**: Accurately computes savings using Sri Lankan electricity bracket system
- **Knowledge Base**: Maintainable YAML configuration for regional data, panel specs, and tariffs
- **Interactive UI**: Clean Streamlit interface with real-time analysis
- **Comprehensive Coverage**: Supports 15+ Sri Lankan cities/regions

## 📋 Table of Contents
- [Installation](#-installation)
- [Usage](#-usage)
- [Sample Scenarios](#-sample-scenarios)
- [Project Structure](#-project-structure)
- [Knowledge Base](#-knowledge-base)
- [Expert System Rules](#-expert-system-rules)
- [Screenshots](#-screenshots)
- [Technical Details](#-technical-details)
- [Future Enhancements](#-future-enhancements)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download this repository**
```powershell
cd "c:\Users\sanda\Desktop\Home\BSc hons AI\Sem 5\es\assignment"
```

2. **Create a virtual environment (recommended)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

## 💻 Usage

### Running the Application

1. **Start the Streamlit app**
```powershell
streamlit run app.py
```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in the terminal

3. **Enter your details**
   - Monthly electricity usage (kWh)
   - Location/city
   - Roof type (Tile, Asbestos, Concrete, Other)
   - Available budget (LKR)
   - Optional: Available roof space (sq.ft.)

4. **Get recommendations**
   - Click "Analyze Solar Investment"
   - Review system recommendations, cost estimates, and payback analysis
   - Explore expert reasoning and alternatives

## 📊 Sample Scenarios

### Scenario 1: Average Urban Home (Colombo)
**Inputs:**
- Monthly Usage: 300 kWh
- Location: Colombo
- Roof Type: Tile
- Budget: LKR 500,000
- Roof Space: Not specified

**Expected Recommendation:**
- System Size: ~2.5 kW
- Number of Panels: 6 panels
- Installation Cost: ~LKR 500,000
- Payback Period: ~7-8 years
- Category: Good Investment
- Confidence: Medium-High

**Reasoning:**
- Colombo receives 5.2 sun hours/day on average
- 300 kWh consumption falls in CEB's higher tariff brackets
- Budget is sufficient for optimal system size
- Good ROI due to progressive tariff savings

### Scenario 2: Large Villa (Galle)
**Inputs:**
- Monthly Usage: 600 kWh
- Location: Galle
- Roof Type: Concrete
- Budget: LKR 1,200,000
- Roof Space: 800 sq.ft.

**Expected Recommendation:**
- System Size: ~5.0 kW
- Number of Panels: 12 panels
- Installation Cost: ~LKR 1,000,000
- Payback Period: ~6-7 years
- Category: Good Investment
- Confidence: High

**Reasoning:**
- Galle has excellent sun hours (5.3/day)
- High consumption means significant tariff savings (45 LKR/kWh bracket)
- Sufficient budget and roof space for full system
- Strong ROI from high-tier tariff offsets

### Scenario 3: Budget-Constrained Home (Kandy)
**Inputs:**
- Monthly Usage: 400 kWh
- Location: Kandy
- Roof Type: Asbestos
- Budget: LKR 350,000
- Roof Space: 600 sq.ft.

**Expected Recommendation:**
- System Size: ~1.5 kW (budget-constrained)
- Number of Panels: 4 panels
- Installation Cost: ~LKR 320,000
- Payback Period: ~8-9 years
- Category: Fair Investment
- Confidence: Medium

**Reasoning:**
- Budget limits full system installation
- Recommends scaled-down system within budget
- Suggests phased expansion approach
- Still provides positive ROI despite constraints

### Scenario 4: Excellent Conditions (Hambantota)
**Inputs:**
- Monthly Usage: 450 kWh
- Location: Hambantota
- Roof Type: Tile
- Budget: LKR 900,000
- Roof Space: 700 sq.ft.

**Expected Recommendation:**
- System Size: ~3.5 kW
- Number of Panels: 8 panels
- Installation Cost: ~LKR 680,000
- Payback Period: ~5-6 years
- Category: Excellent Investment
- Confidence: High

**Reasoning:**
- Hambantota has highest sun hours in Sri Lanka (5.8/day)
- Moderate-high consumption with good tariff savings
- Optimal conditions for solar generation
- Fast payback due to excellent solar irradiance

## 📁 Project Structure

```
assignment/
│
├── app.py                  # Streamlit web application (main UI)
├── solar_expert.py         # Experta expert system (rules & reasoning)
├── utils.py                # Utility functions (calculations)
├── config.yaml             # Knowledge base (data & parameters)
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

### File Descriptions

- **`app.py`**: Streamlit user interface with input forms, results visualization, and interactive elements
- **`solar_expert.py`**: Expert system implementation using Experta framework with 10 major rules
- **`utils.py`**: Helper functions for calculations, data loading, and formatting
- **`config.yaml`**: Centralized knowledge base containing:
  - Regional sun hour data (15+ locations)
  - Solar panel specifications
  - Installation cost parameters
  - CEB/LECO electricity tariffs
  - System sizing rules and thresholds

## 🧠 Knowledge Base

The system uses a comprehensive YAML-based knowledge base (`config.yaml`) containing:

### Regional Data (Sun Hours)
- **Coastal Regions**: Colombo, Gampaha, Galle, Matara, Hambantota (5.2-5.8 hrs/day)
- **Hill Country**: Kandy, Badulla, Ratnapura (4.8-5.1 hrs/day)
- **Northern/Eastern**: Jaffna, Trincomalee, Batticaloa (5.5-5.7 hrs/day)
- **Central Plains**: Anuradhapura, Kurunegala, Monaragala (5.4-5.6 hrs/day)

### Panel Specifications
- **Standard Panel**: 450W monocrystalline
- **System Efficiency**: 85% (accounts for inverter losses, dust, temperature)
- **Panel Area**: ~21 sq.ft. per panel
- **Lifespan**: 25 years
- **Degradation**: 0.5% per year

### Cost Structure (2025 Estimates)
- **Base Cost**: LKR 180,000 per kW installed
- **Fixed Costs**: LKR 50,000 (permits, setup)
- **Roof Adjustments**:
  - Asbestos: -5% (easier installation)
  - Tile: Standard
  - Concrete: +5% (structural reinforcement)

### CEB/LECO Tariff Brackets (2025)
| Units (kWh/month) | Rate (LKR/kWh) |
|-------------------|----------------|
| 0-60              | 8.00           |
| 61-90             | 10.00          |
| 91-120            | 27.75          |
| 121-180           | 32.00          |
| 181+              | 45.00          |

*Plus LKR 400 monthly fixed charge*

### Recommendation Thresholds
- **Excellent**: ≤5 years payback
- **Good**: ≤7 years payback
- **Fair**: ≤12 years payback
- **Marginal**: >12 years payback

## ⚙️ Expert System Rules

The system implements 10 major rules using forward-chaining inference:

### Rule 1: Determine Sun Hours
**Trigger**: Location provided  
**Action**: Look up average daily sun hours and uncertainty from regional database  
**Example**: "Colombo → 5.2 hours/day (±0.3 hours)"

### Rule 2: Calculate Required System Size
**Trigger**: Sun hours determined + monthly consumption known  
**Formula**: `(daily_kWh / (sun_hours × efficiency)) × oversizing_factor`  
**Constraints**: Enforce 1.0-10.0 kW range  
**Example**: "300 kWh/month → 2.5 kW system required"

### Rule 3: Check Roof Space Constraint
**Trigger**: System sized + roof space provided  
**Action**: Calculate required area, check if sufficient  
**If insufficient**: Determine maximum system that fits  
**Example**: "Need 150 sq.ft., have 120 sq.ft. → max 2.0 kW"

### Rule 4: Calculate Installation Cost
**Trigger**: System size determined  
**Formula**: `(kW × cost_per_kW × roof_multiplier) + fixed_cost`  
**Example**: "2.5 kW tile roof → LKR 500,000"

### Rule 5: Check Budget Constraint
**Trigger**: Cost calculated + budget provided  
**Action**: Verify budget sufficiency  
**If insufficient**: Calculate maximum affordable system  
**Example**: "Need LKR 500k, have LKR 350k → max 1.5 kW affordable"

### Rule 6a-6d: Determine Final System
**Variants**:
- **6a** - No constraints: Use optimal size
- **6b** - Roof constrained: Use roof-limited size
- **6c** - Budget constrained: Use budget-limited size
- **6d** - Both constrained: Use more restrictive limit

**Action**: Set final system parameters and explain reasoning

### Rule 7: Calculate Energy Generation & Savings
**Trigger**: Final system determined  
**Calculations**:
1. Annual generation = `kW × sun_hours × efficiency × 365`
2. Average tariff = Progressive bracket calculation
3. Annual savings = `(generation × self_consumption × tariff) - maintenance`
4. Payback = `cost / annual_savings`

**Example**: "2.5 kW → 3,800 kWh/year → LKR 65,000 savings/year → 7.7 years payback"

### Rule 8: Determine Confidence Level
**Trigger**: Savings calculated  
**Factors**: Sun hour uncertainty, tariff volatility, cost variability  
**Formula**: `Combined uncertainty = √(sun² + tariff² + cost²)`  
**Levels**:
- High: <20% combined uncertainty
- Medium: 20-35% uncertainty
- Low: >35% uncertainty

**Example**: "±0.3 sun hrs + ±15% tariff → Medium confidence (±1.2 years)"

### Rule 9: Generate Final Recommendation
**Trigger**: Confidence determined  
**Action**: Package all results, categorize recommendation, create output  
**Example**: "Good Investment: 2.5 kW, 7.7 years payback, Medium confidence"

### Rule 10: Handle Infeasible Cases
**Trigger**: Budget insufficient for minimum viable system  
**Action**: Declare infeasible, suggest alternatives  
**Example**: "Budget LKR 100k < minimum LKR 180k → Not feasible"

## 📸 Screenshots

### Main Input Interface
The sidebar collects user inputs with helpful tooltips and validations.

### Recommendation Dashboard
Displays key metrics in an easy-to-read card layout with color-coded categories.

### Expert Reasoning View
Shows step-by-step logic that led to the recommendation for transparency.

### Constraint Warnings
Highlights budget or roof space limitations with alternative suggestions.

*(Screenshots would be added here after running the application)*

## 🔧 Technical Details

### Technologies Used
- **Python 3.8+**: Core programming language
- **Experta 1.9.4**: Rule-based expert system framework
- **Streamlit 1.28.0**: Web application framework
- **PyYAML 6.0.1**: Configuration management
- **Pandas 2.1.0**: Data manipulation
- **NumPy 1.24.3**: Numerical computations

### Expert System Architecture

```
User Input → Fact Base → Rule Engine → Inference → Recommendation
                ↑            ↑
         Knowledge Base   Forward Chaining
```

**Forward Chaining Process**:
1. User inputs declared as initial facts
2. Rules fire based on fact patterns
3. New facts derived and added to fact base
4. Process continues until no more rules fire
5. Final recommendation extracted

### Calculation Methodology

**Progressive Tariff Calculation**:
```python
# Example: 300 kWh consumption
# 0-60: 60 × 8 = 480
# 61-90: 30 × 10 = 300
# 91-120: 30 × 27.75 = 832.5
# 121-180: 60 × 32 = 1,920
# 181-300: 120 × 45 = 5,400
# Fixed: 400
# Total: 9,332.5 LKR
# Average: 31.11 LKR/kWh
```

**Payback Calculation**:
```python
Payback = Total_Cost / (Annual_Energy_Savings - Annual_Maintenance)
```

**Confidence Calculation**:
```python
Uncertainty = sqrt(sun_uncertainty² + tariff_uncertainty² + cost_uncertainty²)
Payback_Uncertainty = Payback_Years × Total_Uncertainty
```

### Data Sources & Assumptions

**Solar Irradiance**: Based on NASA POWER data and Sri Lanka Sustainable Energy Authority reports

**Electricity Tariffs**: Ceylon Electricity Board (CEB) domestic tariff structure as of 2025

**Installation Costs**: Market survey of Sri Lankan solar installers (2025 estimates)

**System Efficiency**: Industry standard 85% accounting for:
- Inverter efficiency: ~96%
- Temperature losses: ~5%
- Dust/soiling: ~2%
- Wiring losses: ~2%

**Self-Consumption**: 80% assumption (20% excess may be exported at lower rates)

**Maintenance**: 1% of installation cost annually

## 🚀 Future Enhancements

### Planned Features (Not in MVP)
- [ ] **Bill Upload & OCR**: Extract usage data from electricity bill photos
- [ ] **Interactive Charts**: Payback timeline, monthly savings projections
- [ ] **Roof Orientation Analysis**: Account for roof direction and tilt angle
- [ ] **Shading Assessment**: Adjust recommendations based on nearby obstacles
- [ ] **Multi-Phase Installation**: Plan phased system expansion over time
- [ ] **Net Metering Calculator**: Detailed export/import analysis for net metering customers
- [ ] **PDF Report Generation**: Download professional recommendation reports
- [ ] **Cost Comparison**: Compare multiple system configurations
- [ ] **Financing Options**: Integrate loan and leasing calculations
- [ ] **Maintenance Scheduling**: Annual service reminders and checklists
- [ ] **Weather Integration**: Real-time weather impact on projections
- [ ] **Installer Directory**: Connect users with certified local installers

### Technical Improvements
- [ ] User authentication and saved recommendations
- [ ] Database backend for historical tracking
- [ ] API for integration with other systems
- [ ] Mobile-responsive design enhancements
- [ ] Multi-language support (Sinhala, Tamil)
- [ ] A/B testing for recommendation strategies
- [ ] Machine learning for cost prediction refinement

## 📝 Configuration Customization

To update the knowledge base, edit `config.yaml`:

### Adding New Locations
```yaml
regions:
  new_city:
    sun_hours: 5.4
    uncertainty: 0.3
```

### Updating Tariff Rates
```yaml
tariffs:
  brackets:
    - max_units: 60
      rate: 8.50  # Updated rate
```

### Modifying Cost Estimates
```yaml
costs:
  cost_per_kw: 200000  # New cost per kW
  fixed_cost: 60000     # Updated fixed cost
```

## ⚠️ Important Notes

- **Estimates Only**: Recommendations are estimates. Always consult certified installers for final quotes.
- **No Data Storage**: All processing is done locally; no user data is stored.
- **Tariff Changes**: Electricity tariffs may change. Update `config.yaml` accordingly.
- **Professional Consultation**: For systems >5kW or complex installations, seek professional engineering consultation.
- **Permits Required**: Check local regulations and obtain necessary permits before installation.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional Sri Lankan cities/regions
- More accurate cost data
- Enhanced UI/UX
- Better mobile experience
- Additional calculation models

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer

Created as part of BSc (Hons) AI - Semester 5 Expert Systems Assignment

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Built with ❤️ for Sri Lankan households seeking sustainable energy solutions**

☀️ **Go Solar. Save Money. Save the Planet.** 🌍
