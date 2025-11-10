"""
Streamlit Web Application for Rooftop Solar ROI Advisor
User interface for the expert system
"""

import streamlit as st
import yaml
from solar_expert import run_expert_system
import utils


# Page configuration
st.set_page_config(
    page_title="Solar ROI Advisor - Sri Lanka",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B00;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-box {
        background-color: #f0f8ff;
        border-left: 5px solid #4CAF50;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 5px solid #2196F3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


def load_locations():
    """Load available locations from config"""
    config = utils.load_config()
    locations = list(config['regions'].keys())
    # Capitalize first letter of each location
    return [loc.capitalize() for loc in locations]


def main():
    # Header
    st.markdown('<div class="main-header">☀️ Rooftop Solar ROI Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Smart Solar Investment Recommendations for Sri Lankan Households</div>', 
                unsafe_allow_html=True)
    
    # Sidebar - Input Form
    with st.sidebar:
        st.header("📋 Enter Your Details")
        
        st.markdown("---")
        
        # Monthly electricity usage
        monthly_kwh = st.number_input(
            "Monthly Electricity Usage (kWh)",
            min_value=0.0,
            max_value=2000.0,
            value=300.0,
            step=10.0,
            help="Check your electricity bill for your average monthly consumption in kilowatt-hours (kWh)"
        )
        
        # Location
        locations = load_locations()
        location = st.selectbox(
            "Location (City/Region)",
            options=locations,
            help="Select your city or nearest major city"
        )
        
        # Roof type
        roof_type = st.selectbox(
            "Roof Type",
            options=["Tile", "Asbestos", "Concrete", "Other"],
            help="Select the material of your roof. This affects installation cost."
        )
        
        # Roof size (optional)
        roof_size_provided = st.checkbox(
            "I know my available roof space",
            value=False
        )
        
        roof_size = None
        if roof_size_provided:
            roof_size = st.number_input(
                "Available Roof Space (sq.ft.)",
                min_value=0.0,
                max_value=5000.0,
                value=500.0,
                step=50.0,
                help="Estimate the flat roof area available for solar panels"
            )
        
        # Budget
        budget = st.number_input(
            "Budget (LKR)",
            min_value=0.0,
            max_value=5000000.0,
            value=500000.0,
            step=10000.0,
            help="Enter your available budget for solar installation"
        )
        
        st.markdown("---")
        
        # Submit button
        analyze_button = st.button("🔍 Analyze Solar Investment", type="primary", use_container_width=True)
    
    # Main content area
    if analyze_button:
        with st.spinner("🔄 Running expert system analysis..."):
            try:
                # Run expert system
                recommendation = run_expert_system(
                    monthly_kwh=monthly_kwh,
                    location=location.lower(),
                    roof_type=roof_type.lower(),
                    budget=budget,
                    available_roof_space=roof_size
                )
                
                # Display results
                display_results(recommendation, monthly_kwh, location, roof_type, budget, roof_size)
                
            except Exception as e:
                st.error(f"❌ Error running analysis: {str(e)}")
                st.exception(e)
    else:
        # Welcome screen
        display_welcome()


def display_welcome():
    """Display welcome screen with instructions"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🌟 Welcome to the Solar ROI Advisor!")
        st.markdown("""
        This expert system helps you make informed decisions about rooftop solar investments 
        in Sri Lanka. 
        
        **How it works:**
        1. Enter your electricity usage and location details in the sidebar
        2. Provide your roof type and available budget
        3. Click "Analyze Solar Investment" to get personalized recommendations
        
        **What you'll get:**
        - Recommended solar system size and specifications
        - Detailed cost estimate and payback analysis
        - Expert reasoning behind the recommendation
        - Confidence level in the projections
        - Alternative options if constraints apply
        
        **Ready to get started?** Fill in your details on the left sidebar! 👈
        """)
        
        # Display sample scenarios
        with st.expander("📊 View Sample Scenarios"):
            st.markdown("""
            **Scenario 1: Average Urban Home**
            - Monthly Usage: 300 kWh
            - Location: Colombo
            - Roof: Tile
            - Budget: LKR 500,000
            
            **Scenario 2: Large Villa**
            - Monthly Usage: 600 kWh
            - Location: Galle
            - Roof: Concrete
            - Budget: LKR 1,200,000
            
            **Scenario 3: Small Apartment**
            - Monthly Usage: 150 kWh
            - Location: Kandy
            - Roof: Asbestos
            - Budget: LKR 300,000
            """)


def display_results(recommendation, monthly_kwh, location, roof_type, budget, roof_size):
    """Display the expert system results"""
    
    # Check if feasible
    if not recommendation.is_feasible:
        st.error("❌ Solar installation is not currently feasible with the given constraints.")
        
        # Display warnings
        if recommendation.warnings:
            st.markdown("### ⚠️ Constraints")
            for warning in recommendation.warnings:
                st.warning(warning)
        
        # Display reasoning
        if recommendation.reasoning_steps:
            with st.expander("🧠 Expert System Reasoning"):
                for step in recommendation.reasoning_steps:
                    st.markdown(f"- {step}")
        
        return
    
    # Header with recommendation category
    category = recommendation.recommendation_category
    category_colors = {
        "Excellent Investment": "🟢",
        "Good Investment": "🟢",
        "Fair Investment": "🟡",
        "Marginal Investment": "🟠",
        "Not Recommended": "🔴"
    }
    
    emoji = category_colors.get(category, "⚪")
    st.markdown(f"## {emoji} {category}")
    
    # Key Metrics
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="System Size",
            value=f"{recommendation.recommended_system_kw} kW",
            help="Recommended solar panel system capacity"
        )
    
    with col2:
        st.metric(
            label="Number of Panels",
            value=f"{recommendation.num_panels}",
            help="Total solar panels needed"
        )
    
    with col3:
        st.metric(
            label="Installation Cost",
            value=f"LKR {recommendation.installation_cost:,.0f}",
            help="Total estimated installation cost"
        )
    
    with col4:
        if recommendation.payback_years:
            payback_display = f"{recommendation.payback_years} years"
            if recommendation.confidence_uncertainty:
                payback_display += f" (±{recommendation.confidence_uncertainty})"
        else:
            payback_display = "N/A"
        
        st.metric(
            label="Payback Period",
            value=payback_display,
            help="Time to recover your investment through savings"
        )
    
    # Financial Details
    st.markdown("### 💰 Financial Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Annual Energy Generation:**  
        {recommendation.annual_generation_kwh:,.0f} kWh/year
        
        **Annual Electricity Savings:**  
        LKR {recommendation.annual_savings:,.2f}/year
        
        **25-Year Lifetime Savings:**  
        LKR {recommendation.annual_savings * 25:,.2f}
        """)
    
    with col2:
        st.markdown(f"""
        **Roof Space Required:**  
        ~{recommendation.required_roof_space:.0f} sq.ft.
        
        **Confidence Level:**  
        {recommendation.confidence_level.upper()}
        
        **Monthly Consumption:**  
        {monthly_kwh} kWh
        """)
    
    # Confidence and Uncertainty
    st.markdown("### 📈 Confidence Assessment")
    confidence_color = {
        "high": "green",
        "medium": "orange",
        "low": "red"
    }
    color = confidence_color.get(recommendation.confidence_level, "gray")
    
    st.markdown(f"""
    <div class="info-box">
    <strong>Confidence Level: {recommendation.confidence_level.upper()}</strong><br>
    Payback Period Uncertainty: ±{recommendation.confidence_uncertainty} years<br>
    <small>This accounts for variations in sun hours, electricity tariffs, and installation costs.</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Warnings
    if recommendation.warnings:
        st.markdown("### ⚠️ Important Considerations")
        for warning in recommendation.warnings:
            st.markdown(f"""
            <div class="warning-box">
            {warning}
            </div>
            """, unsafe_allow_html=True)
    
    # Alternative Recommendations
    if recommendation.alternatives:
        st.markdown("### 💡 Alternative Options")
        for alternative in recommendation.alternatives:
            st.info(alternative)
    
    # Reasoning Steps
    with st.expander("🧠 Expert System Reasoning Process"):
        st.markdown("**Step-by-step analysis:**")
        for i, step in enumerate(recommendation.reasoning_steps, 1):
            st.markdown(f"{i}. {step}")
    
    # Input Summary
    with st.expander("📝 Input Summary"):
        st.markdown(f"""
        - **Monthly Electricity Usage:** {monthly_kwh} kWh
        - **Location:** {location}
        - **Roof Type:** {roof_type}
        - **Available Budget:** LKR {budget:,.2f}
        - **Roof Space:** {f'{roof_size} sq.ft.' if roof_size else 'Not specified'}
        """)
    
    # Resources
    st.markdown("### 📚 Helpful Resources")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **[Ceylon Electricity Board](https://www.ceb.lk/)**  
        Official CEB solar programs
        """)
    
    with col2:
        st.markdown("""
        **[Sustainable Energy Authority](https://www.energy.gov.lk/)**  
        Government energy resources
        """)
    
    with col3:
        st.markdown("""
        **Local Solar Installers**  
        Get quotes from certified installers
        """)
    
    # Download option
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📄 Generate PDF Report (Coming Soon)", use_container_width=True):
            st.info("PDF report generation feature will be added in future updates!")


# Sidebar footer
def sidebar_footer():
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <small>
    💡 **Tip:** Keep your electricity bill handy for accurate inputs!
    
    🔒 Your data is processed locally and not stored.
    
    ⚠️ These are estimates. Consult certified installers for final quotes.
    </small>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    sidebar_footer()
