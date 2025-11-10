"""
Utility functions for the Solar ROI Advisor
Handles calculations, data loading, and helper functions
"""

import yaml
import math
from typing import Dict, Tuple, Optional


def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def calculate_average_tariff_rate(monthly_kwh: float, config: Dict) -> float:
    """
    Calculate the average tariff rate based on progressive bracket structure
    
    Args:
        monthly_kwh: Monthly electricity consumption in kWh
        config: Configuration dictionary
    
    Returns:
        Average rate per kWh in LKR
    """
    brackets = config['tariffs']['brackets']
    total_cost = 0
    remaining_kwh = monthly_kwh
    previous_max = 0
    
    for bracket in brackets:
        max_units = bracket['max_units']
        rate = bracket['rate']
        
        if max_units is None:
            # Last bracket - all remaining units
            total_cost += remaining_kwh * rate
            break
        else:
            bracket_size = max_units - previous_max
            units_in_bracket = min(remaining_kwh, bracket_size)
            total_cost += units_in_bracket * rate
            remaining_kwh -= units_in_bracket
            previous_max = max_units
            
            if remaining_kwh <= 0:
                break
    
    # Add fixed charge
    total_cost += config['tariffs']['fixed_charge']
    
    # Return average rate
    return total_cost / monthly_kwh if monthly_kwh > 0 else 0


def calculate_required_system_size(
    monthly_kwh: float,
    sun_hours: float,
    config: Dict
) -> float:
    """
    Calculate required system size in kW
    
    Args:
        monthly_kwh: Monthly electricity consumption
        sun_hours: Average daily sun hours
        config: Configuration dictionary
    
    Returns:
        Required system size in kW
    """
    # Daily consumption
    daily_kwh = monthly_kwh / 30
    
    # Panel efficiency
    efficiency = config['panels']['standard']['efficiency']
    
    # Oversizing factor
    oversizing = config['sizing']['oversizing_factor']
    
    # Calculate required kW: (daily_kwh / (sun_hours * efficiency)) * oversizing
    required_kw = (daily_kwh / (sun_hours * efficiency)) * oversizing
    
    # Round to 2 decimal places
    return round(required_kw, 2)


def calculate_number_of_panels(system_kw: float, config: Dict) -> int:
    """Calculate number of panels needed"""
    panel_wattage = config['panels']['standard']['wattage']
    num_panels = math.ceil((system_kw * 1000) / panel_wattage)
    return num_panels


def calculate_required_roof_space(num_panels: int, config: Dict) -> float:
    """Calculate required roof space in square feet"""
    panel_area = config['panels']['standard']['area_sqft']
    buffer = config['sizing']['space_buffer']
    required_space = num_panels * panel_area * buffer
    return round(required_space, 1)


def calculate_installation_cost(
    system_kw: float,
    roof_type: str,
    config: Dict
) -> float:
    """
    Calculate total installation cost
    
    Args:
        system_kw: System size in kW
        roof_type: Type of roof (tile, asbestos, concrete, other)
        config: Configuration dictionary
    
    Returns:
        Total cost in LKR
    """
    cost_per_kw = config['costs']['cost_per_kw']
    fixed_cost = config['costs']['fixed_cost']
    
    # Get roof multiplier
    roof_multiplier = config['costs']['roof_multipliers'].get(
        roof_type.lower(), 1.0
    )
    
    # Calculate total cost
    variable_cost = system_kw * cost_per_kw * roof_multiplier
    total_cost = variable_cost + fixed_cost
    
    return round(total_cost, 2)


def calculate_annual_generation(
    system_kw: float,
    sun_hours: float,
    config: Dict
) -> float:
    """
    Calculate annual energy generation in kWh
    
    Args:
        system_kw: System size in kW
        sun_hours: Average daily sun hours
        config: Configuration dictionary
    
    Returns:
        Annual generation in kWh
    """
    efficiency = config['panels']['standard']['efficiency']
    daily_generation = system_kw * sun_hours * efficiency
    annual_generation = daily_generation * 365
    
    return round(annual_generation, 2)


def calculate_annual_savings(
    annual_generation_kwh: float,
    avg_tariff_rate: float,
    installation_cost: float,
    config: Dict
) -> float:
    """
    Calculate annual electricity cost savings
    
    Args:
        annual_generation_kwh: Annual solar generation in kWh
        avg_tariff_rate: Average tariff rate per kWh
        installation_cost: Total installation cost
        config: Configuration dictionary
    
    Returns:
        Annual savings in LKR
    """
    self_consumption = config['savings']['self_consumption_rate']
    maintenance_rate = config['savings']['annual_maintenance_rate']
    
    # Calculate savings from self-consumed solar energy
    energy_savings = annual_generation_kwh * self_consumption * avg_tariff_rate
    
    # Subtract annual maintenance costs
    maintenance_cost = installation_cost * maintenance_rate
    net_annual_savings = energy_savings - maintenance_cost
    
    return round(net_annual_savings, 2)


def calculate_payback_period(
    installation_cost: float,
    annual_savings: float
) -> Optional[float]:
    """
    Calculate payback period in years
    
    Args:
        installation_cost: Total installation cost
        annual_savings: Annual savings
    
    Returns:
        Payback period in years, or None if savings are non-positive
    """
    if annual_savings <= 0:
        return None
    
    payback_years = installation_cost / annual_savings
    return round(payback_years, 1)


def calculate_confidence(
    payback_years: Optional[float],
    sun_hours_uncertainty: float,
    config: Dict
) -> Tuple[str, float, str]:
    """
    Calculate confidence level in the recommendation
    
    Args:
        payback_years: Calculated payback period
        sun_hours_uncertainty: Uncertainty in sun hours
        config: Configuration dictionary
    
    Returns:
        Tuple of (confidence_level, uncertainty_years, explanation)
    """
    if payback_years is None:
        return ("low", 0, "Unable to calculate payback period")
    
    tariff_uncertainty = config['tariffs']['tariff_uncertainty']
    cost_uncertainty = config['costs']['min_uncertainty']
    
    # Combined uncertainty factor
    total_uncertainty = math.sqrt(
        sun_hours_uncertainty**2 + 
        tariff_uncertainty**2 + 
        cost_uncertainty**2
    )
    
    # Uncertainty in payback period (in years)
    uncertainty_years = round(payback_years * total_uncertainty, 1)
    
    # Determine confidence level
    if total_uncertainty < 0.2:
        confidence_level = "high"
        explanation = "High confidence based on stable regional data and tariffs"
    elif total_uncertainty < 0.35:
        confidence_level = "medium"
        explanation = "Medium confidence due to some variability in conditions"
    else:
        confidence_level = "low"
        explanation = "Lower confidence due to significant uncertainty in factors"
    
    return (confidence_level, uncertainty_years, explanation)


def format_currency(amount: float) -> str:
    """Format amount as Sri Lankan Rupees"""
    return f"LKR {amount:,.2f}"


def format_percentage(value: float) -> str:
    """Format value as percentage"""
    return f"{value * 100:.1f}%"


def get_region_sun_hours(location: str, config: Dict) -> Tuple[float, float]:
    """
    Get sun hours and uncertainty for a location
    
    Args:
        location: Location name
        config: Configuration dictionary
    
    Returns:
        Tuple of (sun_hours, uncertainty)
    """
    location_key = location.lower().strip()
    
    if location_key in config['regions']:
        region_data = config['regions'][location_key]
        return region_data['sun_hours'], region_data['uncertainty']
    else:
        # Default to average values if location not found
        avg_sun_hours = 5.3
        avg_uncertainty = 0.3
        return avg_sun_hours, avg_uncertainty


def check_budget_constraint(
    required_cost: float,
    available_budget: float,
    config: Dict
) -> Tuple[bool, Optional[float]]:
    """
    Check if budget is sufficient and suggest maximum affordable system
    
    Args:
        required_cost: Required installation cost
        available_budget: Available budget
        config: Configuration dictionary
    
    Returns:
        Tuple of (is_sufficient, max_affordable_kw)
    """
    min_budget = config['thresholds']['min_budget_lkr']
    
    if available_budget < min_budget:
        return False, None
    
    if available_budget >= required_cost:
        return True, None
    
    # Calculate maximum affordable system size
    fixed_cost = config['costs']['fixed_cost']
    cost_per_kw = config['costs']['cost_per_kw']
    
    if available_budget <= fixed_cost:
        return False, None
    
    max_affordable_kw = (available_budget - fixed_cost) / cost_per_kw
    max_affordable_kw = max(0, round(max_affordable_kw, 2))
    
    return False, max_affordable_kw


def check_roof_constraint(
    required_space: float,
    available_space: Optional[float]
) -> bool:
    """
    Check if roof space is sufficient
    
    Args:
        required_space: Required roof space in sqft
        available_space: Available roof space in sqft (None if not provided)
    
    Returns:
        True if sufficient or not specified, False otherwise
    """
    if available_space is None:
        return True  # Assume sufficient if not provided
    
    return available_space >= required_space


def get_recommendation_category(payback_years: Optional[float], config: Dict) -> str:
    """
    Categorize the recommendation based on payback period
    
    Args:
        payback_years: Calculated payback period
        config: Configuration dictionary
    
    Returns:
        Recommendation category string
    """
    if payback_years is None:
        return "Not Recommended"
    
    excellent = config['thresholds']['excellent_payback']
    ideal = config['thresholds']['ideal_payback']
    max_acceptable = config['thresholds']['max_payback_acceptable']
    
    if payback_years <= excellent:
        return "Excellent Investment"
    elif payback_years <= ideal:
        return "Good Investment"
    elif payback_years <= max_acceptable:
        return "Fair Investment"
    else:
        return "Marginal Investment"
