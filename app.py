"""
Streamlit Web Application for Rooftop Solar ROI Advisor
User interface for the expert system
"""

import streamlit as st
import yaml
from solar_expert import run_expert_system
import utils
import os
from chat_popup import render_chat_popup

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


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
        background-color: #fff3cd20;
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
    
    # Calculate consumption coverage
    annual_consumption = monthly_kwh * 12
    coverage_percentage = (recommendation.annual_generation_kwh / annual_consumption * 100) if annual_consumption > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Annual Energy Generation:**  
        {recommendation.annual_generation_kwh:,.0f} kWh/year
        
        **Your Annual Consumption:**  
        {annual_consumption:,.0f} kWh/year ({monthly_kwh:,.0f} kWh/month)
        
        **Solar Coverage:**  
        {coverage_percentage:.1f}% of your electricity needs
        
        **Annual Electricity Savings:**  
        LKR {recommendation.annual_savings:,.2f}/year
        """)
    
    with col2:
        st.markdown(f"""
        **Installation Cost:**  
        LKR {recommendation.installation_cost:,.0f}
        
        **25-Year Lifetime Savings:**  
        LKR {recommendation.annual_savings * 25:,.2f}
        
        **Roof Space Required:**  
        ~{recommendation.required_roof_space:.0f} sq.ft.
        
        **Confidence Level:**  
        {recommendation.confidence_level.upper()}
        """)
    
    # Show coverage info box
    if coverage_percentage < 100:
        coverage_color = "#FF9800" if coverage_percentage >= 70 else "#f44336"
        st.markdown(f"""
        <div style="background-color: {coverage_color}15; border-left: 5px solid {coverage_color}; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
        <strong style="color: {coverage_color};">ℹ️ System Coverage Notice</strong><br>
        This {recommendation.recommended_system_kw} kW system will generate <strong>{recommendation.annual_generation_kwh:,.0f} kWh/year</strong>, 
        which covers <strong>{coverage_percentage:.1f}%</strong> of your annual consumption of <strong>{annual_consumption:,.0f} kWh/year</strong>.<br>
        <small>The remaining {100 - coverage_percentage:.1f}% ({annual_consumption - recommendation.annual_generation_kwh:,.0f} kWh/year) will still be drawn from the grid. 
        This is likely due to budget or roof space constraints limiting the system size.</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #4CAF5015; border-left: 5px solid #4CAF50; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
        <strong style="color: #4CAF50;">✓ Full Coverage System</strong><br>
        This system will generate <strong>{recommendation.annual_generation_kwh:,.0f} kWh/year</strong>, 
        which covers <strong>{coverage_percentage:.1f}%</strong> of your annual consumption!<br>
        <small>You may even have excess energy that can be sold back to the grid under net metering programs.</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Confidence and Uncertainty
    st.markdown("### 📈 Confidence Assessment")
    confidence_colors = {
        "high": "#4CAF50",  # Green
        "medium": "#FF9800",  # Orange
        "low": "#f44336"  # Red
    }
    confidence_icons = {
        "high": "🟢",
        "medium": "🟡",
        "low": "🔴"
    }
    
    bg_color = confidence_colors.get(recommendation.confidence_level, "#9E9E9E")
    icon = confidence_icons.get(recommendation.confidence_level, "⚪")
    
    st.markdown(f"""
    <div style="background-color: {bg_color}15; border-left: 5px solid {bg_color}; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
    <strong style="color: {bg_color};">{icon} Confidence Level: {recommendation.confidence_level.upper()}</strong><br>
    <strong>Payback Period Uncertainty:</strong> ±{recommendation.confidence_uncertainty} years<br>
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
    
    # Service Provider Alternatives
    st.markdown("### 🏢 Compare Service Providers")
    st.markdown("*Estimated costs for your system from different installers:*")
    
    config = utils.load_config()
    providers = config['costs'].get('providers', [])
    
    if providers:
        # Calculate costs for each provider
        provider_data = []
        for provider in providers:
            provider_cost_per_kw = provider['installation_cost_per_kw']
            provider_fixed = provider['fixed_cost']
            
            # Calculate total cost for this provider
            total_cost = (recommendation.recommended_system_kw * provider_cost_per_kw) + provider_fixed
            
            # Calculate payback with this provider's cost
            if recommendation.annual_savings > 0:
                payback = round(total_cost / recommendation.annual_savings, 1)
            else:
                payback = None
            
            provider_data.append({
                'Provider': provider['name'],
                'Service Tier': provider['service_tier'].capitalize(),
                'Est. Cost (LKR)': f"{total_cost:,.0f}",
                'Warranty (Years)': provider['warranty_years'],
                'Payback (Years)': f"{payback}" if payback else "N/A",
                'Notes': provider['notes']
            })
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["📊 Quick Compare", "📋 Detailed View"])
        
        with tab1:
            # Display as table without notes
            import pandas as pd
            df = pd.DataFrame(provider_data)
            df_display = df[['Provider', 'Service Tier', 'Est. Cost (LKR)', 'Warranty (Years)', 'Payback (Years)']]
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Highlight best options
            st.markdown("**💡 Quick Tips:**")
            col1, col2, col3 = st.columns(3)
            
            # Find best budget option
            budget_provider = min(provider_data, key=lambda x: float(x['Est. Cost (LKR)'].replace(',', '')))
            with col1:
                st.info(f"**Most Affordable:**\n\n{budget_provider['Provider']}\n\n{budget_provider['Est. Cost (LKR)']}")
            
            # Find best warranty
            warranty_provider = max(provider_data, key=lambda x: x['Warranty (Years)'])
            with col2:
                st.success(f"**Best Warranty:**\n\n{warranty_provider['Provider']}\n\n{warranty_provider['Warranty (Years)']} years")
            
            # Find best payback
            valid_paybacks = [p for p in provider_data if p['Payback (Years)'] != 'N/A']
            if valid_paybacks:
                payback_provider = min(valid_paybacks, key=lambda x: float(x['Payback (Years)']))
                with col3:
                    st.warning(f"**Fastest Payback:**\n\n{payback_provider['Provider']}\n\n{payback_provider['Payback (Years)']} years")
        
        with tab2:
            # Detailed cards for each provider
            for i, provider_info in enumerate(provider_data):
                tier_colors = {
                    'Budget': '#2196F3',
                    'Standard': '#4CAF50',
                    'Premium': '#9C27B0'
                }
                tier_color = tier_colors.get(provider_info['Service Tier'], '#757575')
                
                st.markdown(f"""
                <div style="background-color: {tier_color}10; border-left: 5px solid {tier_color}; padding: 1.5rem; border-radius: 5px; margin: 1rem 0;">
                    <h4 style="color: {tier_color}; margin-top: 0;">🏢 {provider_info['Provider']}</h4>
                    <p><strong>Service Tier:</strong> <span style="color: {tier_color};">{provider_info['Service Tier']}</span></p>
                    <p><strong>Estimated Cost:</strong> {provider_info['Est. Cost (LKR)']}</p>
                    <p><strong>Warranty:</strong> {provider_info['Warranty (Years)']} years</p>
                    <p><strong>Estimated Payback:</strong> {provider_info['Payback (Years)']}</p>
                    <p><strong>Details:</strong> <em>{provider_info['Notes']}</em></p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Provider comparison data not available in configuration.")
    
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


def render_floating_button():
    """Render a fixed floating button at bottom-right corner with click handler"""
    
    # Check if button should trigger popup
    if st.session_state.get('open_chat_clicked', False):
        st.session_state.chat_popup_open = True
        st.session_state.open_chat_clicked = False
        st.rerun()
    
    button_html = """
    <style>
    .floating-chat-btn {
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        cursor: pointer !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
        z-index: 9999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        text-decoration: none !important;
    }
    
    .floating-chat-btn:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        50% {
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.8);
        }
    }
    </style>
    
    <form id="chatButtonForm" action="" method="get">
        <input type="hidden" name="action" value="open">
        <button type="submit" class="floating-chat-btn" title="Open Chat Assistant" style="animation: pulse 2s infinite;">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="width: 30px; height: 30px; fill: white;">
                <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
                <circle cx="12" cy="10" r="1.5"/>
                <circle cx="8" cy="10" r="1.5"/>
                <circle cx="16" cy="10" r="1.5"/>
            </svg>
        </button>
    </form>
    """
    st.markdown(button_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    sidebar_footer()
    render_floating_button()  # Add floating button to all pages
    render_chat_popup()  # Add chat popup functionality
