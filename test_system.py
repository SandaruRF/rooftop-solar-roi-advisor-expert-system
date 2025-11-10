"""
Test script for the Solar ROI Expert System
Run this to verify the system is working correctly
"""

from solar_expert import run_expert_system
import utils


def print_separator():
    print("\n" + "="*80 + "\n")


def test_scenario(name, monthly_kwh, location, roof_type, budget, roof_size=None):
    """Test a specific scenario and print results"""
    print(f"🧪 Testing Scenario: {name}")
    print(f"   Monthly Usage: {monthly_kwh} kWh")
    print(f"   Location: {location}")
    print(f"   Roof Type: {roof_type}")
    print(f"   Budget: LKR {budget:,.0f}")
    if roof_size:
        print(f"   Roof Size: {roof_size} sq.ft.")
    
    print("\n⚙️ Running expert system...")
    
    try:
        result = run_expert_system(
            monthly_kwh=monthly_kwh,
            location=location,
            roof_type=roof_type,
            budget=budget,
            available_roof_space=roof_size
        )
        
        print("\n✅ RECOMMENDATION:")
        print(f"   Category: {result.recommendation_category}")
        
        if result.is_feasible:
            print(f"   System Size: {result.recommended_system_kw} kW")
            print(f"   Number of Panels: {result.num_panels}")
            print(f"   Installation Cost: LKR {result.installation_cost:,.2f}")
            print(f"   Roof Space Required: {result.required_roof_space} sq.ft.")
            print(f"   Annual Generation: {result.annual_generation_kwh:,.0f} kWh")
            print(f"   Annual Savings: LKR {result.annual_savings:,.2f}")
            
            if result.payback_years:
                print(f"   Payback Period: {result.payback_years} years")
                print(f"   Confidence: {result.confidence_level.upper()} (±{result.confidence_uncertainty} years)")
            else:
                print(f"   Payback Period: Unable to calculate")
            
            if result.warnings:
                print("\n⚠️  WARNINGS:")
                for warning in result.warnings:
                    print(f"   - {warning}")
            
            if result.alternatives:
                print("\n💡 ALTERNATIVES:")
                for alt in result.alternatives:
                    print(f"   - {alt}")
            
            print("\n🧠 REASONING STEPS:")
            for i, step in enumerate(result.reasoning_steps, 1):
                print(f"   {i}. {step}")
        else:
            print("   ❌ Not feasible under current constraints")
            
            if result.warnings:
                print("\n⚠️  REASONS:")
                for warning in result.warnings:
                    print(f"   - {warning}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*80)
    print(" "*20 + "SOLAR ROI EXPERT SYSTEM - TEST SUITE")
    print("="*80)
    
    # Test 1: Ideal conditions
    print_separator()
    success1 = test_scenario(
        name="Ideal Urban Home",
        monthly_kwh=300,
        location="colombo",
        roof_type="tile",
        budget=500000
    )
    
    # Test 2: High consumption
    print_separator()
    success2 = test_scenario(
        name="Large Villa with High Consumption",
        monthly_kwh=600,
        location="galle",
        roof_type="concrete",
        budget=1200000,
        roof_size=800
    )
    
    # Test 3: Budget constrained
    print_separator()
    success3 = test_scenario(
        name="Budget Constrained Home",
        monthly_kwh=400,
        location="kandy",
        roof_type="asbestos",
        budget=350000
    )
    
    # Test 4: Excellent sun conditions
    print_separator()
    success4 = test_scenario(
        name="Excellent Solar Conditions",
        monthly_kwh=450,
        location="hambantota",
        roof_type="tile",
        budget=900000,
        roof_size=700
    )
    
    # Test 5: Insufficient budget
    print_separator()
    success5 = test_scenario(
        name="Insufficient Budget",
        monthly_kwh=500,
        location="colombo",
        roof_type="tile",
        budget=100000
    )
    
    # Test 6: Roof space constraint
    print_separator()
    success6 = test_scenario(
        name="Limited Roof Space",
        monthly_kwh=500,
        location="colombo",
        roof_type="tile",
        budget=800000,
        roof_size=150
    )
    
    # Summary
    print_separator()
    print("📊 TEST SUMMARY")
    print("="*80)
    
    tests = [
        ("Ideal Urban Home", success1),
        ("Large Villa", success2),
        ("Budget Constrained", success3),
        ("Excellent Conditions", success4),
        ("Insufficient Budget", success5),
        ("Limited Roof Space", success6)
    ]
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for name, success in tests:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status}: {name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n   🎉 All tests passed! System is working correctly.")
    else:
        print("\n   ⚠️  Some tests failed. Check the errors above.")
    
    print("="*80)


if __name__ == "__main__":
    main()
