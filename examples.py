"""
Example usage of the Solar ROI Expert System
This shows how to use the system programmatically without the UI
"""

from solar_expert import run_expert_system


def example_1_basic_usage():
    """Basic usage example"""
    print("="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    # Run the expert system with input parameters
    recommendation = run_expert_system(
        monthly_kwh=300,           # Monthly electricity consumption
        location="colombo",        # City/region
        roof_type="tile",          # Roof material
        budget=500000             # Budget in LKR
    )
    
    # Access the results
    if recommendation.is_feasible:
        print(f"\n✅ Recommendation: {recommendation.recommendation_category}")
        print(f"   System Size: {recommendation.recommended_system_kw} kW")
        print(f"   Cost: LKR {recommendation.installation_cost:,.2f}")
        print(f"   Payback: {recommendation.payback_years} years")
        print(f"   Confidence: {recommendation.confidence_level}")
    else:
        print("\n❌ Installation not feasible")
        for warning in recommendation.warnings:
            print(f"   - {warning}")


def example_2_with_roof_size():
    """Example with roof size constraint"""
    print("\n" + "="*60)
    print("Example 2: With Roof Size Constraint")
    print("="*60)
    
    recommendation = run_expert_system(
        monthly_kwh=500,
        location="galle",
        roof_type="concrete",
        budget=900000,
        available_roof_space=200  # Limited roof space
    )
    
    if recommendation.is_feasible:
        print(f"\n✅ Recommendation: {recommendation.recommendation_category}")
        print(f"   System Size: {recommendation.recommended_system_kw} kW")
        print(f"   Panels: {recommendation.num_panels}")
        print(f"   Required Space: {recommendation.required_roof_space} sq.ft.")
        
        if recommendation.warnings:
            print("\n⚠️ Warnings:")
            for warning in recommendation.warnings:
                print(f"   - {warning}")


def example_3_view_reasoning():
    """Example showing expert reasoning"""
    print("\n" + "="*60)
    print("Example 3: View Expert System Reasoning")
    print("="*60)
    
    recommendation = run_expert_system(
        monthly_kwh=400,
        location="kandy",
        roof_type="asbestos",
        budget=600000
    )
    
    print("\n🧠 Expert System Reasoning:")
    for i, step in enumerate(recommendation.reasoning_steps, 1):
        print(f"{i}. {step}")


def example_4_compare_locations():
    """Compare recommendations for different locations"""
    print("\n" + "="*60)
    print("Example 4: Compare Multiple Locations")
    print("="*60)
    
    locations = ["colombo", "kandy", "hambantota"]
    common_params = {
        "monthly_kwh": 350,
        "roof_type": "tile",
        "budget": 600000
    }
    
    print(f"\nComparing recommendations for {common_params['monthly_kwh']} kWh usage:\n")
    
    for location in locations:
        rec = run_expert_system(location=location, **common_params)
        
        if rec.is_feasible:
            print(f"{location.capitalize():15} → {rec.recommended_system_kw} kW, "
                  f"{rec.payback_years} years payback, "
                  f"{rec.confidence_level} confidence")


def example_5_budget_scenarios():
    """Test different budget scenarios"""
    print("\n" + "="*60)
    print("Example 5: Budget Impact Analysis")
    print("="*60)
    
    budgets = [300000, 500000, 800000, 1200000]
    
    print(f"\nTesting different budgets for 400 kWh monthly usage:\n")
    
    for budget in budgets:
        rec = run_expert_system(
            monthly_kwh=400,
            location="colombo",
            roof_type="tile",
            budget=budget
        )
        
        if rec.is_feasible:
            print(f"LKR {budget:8,} → {rec.recommended_system_kw} kW system, "
                  f"LKR {rec.installation_cost:,.0f} cost")
        else:
            print(f"LKR {budget:8,} → Not feasible")


def example_6_detailed_output():
    """Get detailed output including all fields"""
    print("\n" + "="*60)
    print("Example 6: Detailed Recommendation Output")
    print("="*60)
    
    rec = run_expert_system(
        monthly_kwh=450,
        location="galle",
        roof_type="tile",
        budget=800000,
        available_roof_space=500
    )
    
    if rec.is_feasible:
        print(f"""
📊 DETAILED RECOMMENDATION

System Specifications:
  - System Size: {rec.recommended_system_kw} kW
  - Number of Panels: {rec.num_panels}
  - Required Roof Space: {rec.required_roof_space} sq.ft.

Financial Analysis:
  - Installation Cost: LKR {rec.installation_cost:,.2f}
  - Annual Generation: {rec.annual_generation_kwh:,.0f} kWh
  - Annual Savings: LKR {rec.annual_savings:,.2f}
  - Payback Period: {rec.payback_years} years (±{rec.confidence_uncertainty} years)

Recommendation:
  - Category: {rec.recommendation_category}
  - Confidence Level: {rec.confidence_level.upper()}

25-Year Projections:
  - Total Energy Generated: {rec.annual_generation_kwh * 25:,.0f} kWh
  - Total Savings: LKR {rec.annual_savings * 25:,.2f}
  - Net Profit: LKR {(rec.annual_savings * 25) - rec.installation_cost:,.2f}
  - Return on Investment: {((rec.annual_savings * 25) / rec.installation_cost - 1) * 100:.1f}%
""")
        
        if rec.alternatives:
            print("💡 Alternative Recommendations:")
            for alt in rec.alternatives:
                print(f"   - {alt}")


if __name__ == "__main__":
    # Run all examples
    example_1_basic_usage()
    example_2_with_roof_size()
    example_3_view_reasoning()
    example_4_compare_locations()
    example_5_budget_scenarios()
    example_6_detailed_output()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
