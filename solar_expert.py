"""
Solar ROI Expert System using Experta
Implements rule-based reasoning for rooftop solar recommendations
"""

from experta import *
import utils


class SolarFact(Fact):
    """Facts about the solar installation scenario"""
    pass


class SolarRecommendation:
    """Data structure to hold the recommendation output"""
    def __init__(self):
        self.recommended_system_kw = None
        self.num_panels = None
        self.required_roof_space = None
        self.installation_cost = None
        self.annual_generation_kwh = None
        self.annual_savings = None
        self.payback_years = None
        self.confidence_level = None
        self.confidence_uncertainty = None
        self.recommendation_category = None
        self.reasoning_steps = []
        self.warnings = []
        self.alternatives = []
        self.is_feasible = True


class SolarROIExpert(KnowledgeEngine):
    """Expert system for solar ROI recommendations"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.recommendation = SolarRecommendation()
    
    def add_reasoning(self, step: str):
        """Add a reasoning step to the explanation"""
        self.recommendation.reasoning_steps.append(step)
    
    def add_warning(self, warning: str):
        """Add a warning message"""
        self.recommendation.warnings.append(warning)
    
    def add_alternative(self, alternative: str):
        """Add an alternative recommendation"""
        self.recommendation.alternatives.append(alternative)
    
    # ===== RULE 1: Determine Sun Hours =====
    @Rule(
        AS.f1 << SolarFact(stage='input'),
        SolarFact(location=MATCH.location),
        NOT(SolarFact(stage='sun_hours_determined'))
    )
    def determine_sun_hours(self, f1, location):
        """Determine average sun hours based on location"""
        sun_hours, uncertainty = utils.get_region_sun_hours(location, self.config)
        
        self.declare(SolarFact(
            stage='sun_hours_determined',
            sun_hours=sun_hours,
            sun_hours_uncertainty=uncertainty
        ))
        
        self.add_reasoning(
            f"Based on location '{location}', determined average sun hours: "
            f"{sun_hours} hours/day (±{uncertainty} hours uncertainty)"
        )
        
        self.retract(f1)
    
    # ===== RULE 2: Calculate Required System Size =====
    @Rule(
        SolarFact(stage='sun_hours_determined'),
        SolarFact(monthly_kwh=MATCH.monthly_kwh),
        SolarFact(sun_hours=MATCH.sun_hours)
    )
    def calculate_system_size(self, monthly_kwh, sun_hours):
        """Calculate required system size based on consumption"""
        required_kw = utils.calculate_required_system_size(
            monthly_kwh, sun_hours, self.config
        )
        
        # Check against min/max limits
        min_kw = self.config['sizing']['min_system_kw']
        max_kw = self.config['sizing']['max_system_kw']
        
        if required_kw < min_kw:
            required_kw = min_kw
            self.add_warning(
                f"Calculated system size was below minimum ({min_kw}kW). "
                f"Using minimum recommended size."
            )
        elif required_kw > max_kw:
            self.add_warning(
                f"Calculated system size ({required_kw}kW) exceeds maximum "
                f"recommended residential size ({max_kw}kW). Consider splitting "
                f"or consulting for commercial installation."
            )
            required_kw = max_kw
        
        num_panels = utils.calculate_number_of_panels(required_kw, self.config)
        required_space = utils.calculate_required_roof_space(num_panels, self.config)
        
        self.declare(SolarFact(
            stage='system_sized',
            required_system_kw=required_kw,
            num_panels=num_panels,
            required_roof_space=required_space
        ))
        
        self.add_reasoning(
            f"For monthly consumption of {monthly_kwh} kWh, calculated required "
            f"system size: {required_kw} kW ({num_panels} panels, requiring "
            f"~{required_space} sq.ft. of roof space)"
        )
    
    # ===== RULE 3: Check Roof Space Constraint =====
    @Rule(
        SolarFact(stage='system_sized'),
        SolarFact(required_roof_space=MATCH.required_space),
        SolarFact(available_roof_space=MATCH.available_space),
        SolarFact(required_system_kw=MATCH.required_kw)
    )
    def check_roof_space(self, required_space, available_space, required_kw):
        """Check if roof space is sufficient"""
        if available_space is not None and available_space < required_space:
            # Calculate maximum system that fits
            panel_area = self.config['panels']['standard']['area_sqft']
            buffer = self.config['sizing']['space_buffer']
            max_panels = int(available_space / (panel_area * buffer))
            panel_wattage = self.config['panels']['standard']['wattage']
            max_kw = round((max_panels * panel_wattage) / 1000, 2)
            
            self.declare(SolarFact(
                stage='roof_constrained',
                max_system_kw_by_roof=max_kw,
                max_panels_by_roof=max_panels
            ))
            
            self.add_warning(
                f"Available roof space ({available_space} sq.ft.) is insufficient "
                f"for the required system size. Maximum system that fits: {max_kw} kW"
            )
            
            self.add_reasoning(
                f"Roof space constraint detected: can accommodate maximum {max_kw} kW "
                f"({max_panels} panels) on available {available_space} sq.ft."
            )
        else:
            self.declare(SolarFact(stage='roof_ok'))
            self.add_reasoning("Roof space is sufficient for the required system")
    
    # ===== RULE 4: Calculate Installation Cost =====
    @Rule(
        SolarFact(stage='system_sized'),
        SolarFact(required_system_kw=MATCH.system_kw),
        SolarFact(roof_type=MATCH.roof_type)
    )
    def calculate_cost(self, system_kw, roof_type):
        """Calculate installation cost"""
        cost = utils.calculate_installation_cost(system_kw, roof_type, self.config)
        
        self.declare(SolarFact(
            stage='cost_calculated',
            installation_cost=cost
        ))
        
        roof_mult = self.config['costs']['roof_multipliers'].get(roof_type.lower(), 1.0)
        roof_note = ""
        if roof_mult != 1.0:
            roof_note = f" (adjusted for {roof_type} roof)"
        
        self.add_reasoning(
            f"Estimated installation cost for {system_kw} kW system: "
            f"LKR {cost:,.2f}{roof_note}"
        )
    
    # ===== RULE 5: Check Budget Constraint =====
    @Rule(
        SolarFact(stage='cost_calculated'),
        SolarFact(installation_cost=MATCH.cost),
        SolarFact(budget=MATCH.budget),
        SolarFact(required_system_kw=MATCH.required_kw)
    )
    def check_budget(self, cost, budget, required_kw):
        """Check if budget is sufficient"""
        is_sufficient, max_affordable_kw = utils.check_budget_constraint(
            cost, budget, self.config
        )
        
        if not is_sufficient:
            if max_affordable_kw is None or max_affordable_kw < self.config['sizing']['min_system_kw']:
                self.declare(SolarFact(stage='budget_insufficient'))
                self.add_warning(
                    f"Budget (LKR {budget:,.2f}) is insufficient for a viable solar "
                    f"installation. Minimum recommended budget: LKR "
                    f"{self.config['thresholds']['min_budget_lkr']:,.2f}"
                )
                self.recommendation.is_feasible = False
            else:
                self.declare(SolarFact(
                    stage='budget_constrained',
                    max_system_kw_by_budget=max_affordable_kw
                ))
                self.add_warning(
                    f"Budget (LKR {budget:,.2f}) is insufficient for the required "
                    f"system ({required_kw} kW at LKR {cost:,.2f}). Maximum "
                    f"affordable system: {max_affordable_kw} kW"
                )
                self.add_reasoning(
                    f"Budget constraint: can afford maximum {max_affordable_kw} kW "
                    f"system with available budget"
                )
        else:
            self.declare(SolarFact(stage='budget_ok'))
            self.add_reasoning("Budget is sufficient for the required system")
    
    # ===== RULE 6a: Determine Final System (No Constraints) =====
    @Rule(
        SolarFact(stage='roof_ok'),
        SolarFact(stage='budget_ok'),
        SolarFact(required_system_kw=MATCH.required_kw),
        SolarFact(num_panels=MATCH.num_panels),
        SolarFact(installation_cost=MATCH.cost),
        SolarFact(required_roof_space=MATCH.required_space)
    )
    def finalize_unconstrained(self, required_kw, num_panels, cost, required_space):
        """Finalize recommendation when no constraints apply"""
        self.declare(SolarFact(
            stage='system_finalized',
            final_system_kw=required_kw,
            final_num_panels=num_panels,
            final_cost=cost,
            final_roof_space=required_space
        ))
        
        self.add_reasoning(
            f"No major constraints detected. Recommending optimal system size "
            f"of {required_kw} kW to meet energy needs"
        )
    
    # ===== RULE 6b: Determine Final System (Roof Constrained) =====
    @Rule(
        SolarFact(stage='roof_constrained'),
        SolarFact(stage='budget_ok'),
        SolarFact(max_system_kw_by_roof=MATCH.max_kw),
        SolarFact(max_panels_by_roof=MATCH.max_panels),
        SolarFact(roof_type=MATCH.roof_type),
        SolarFact(available_roof_space=MATCH.available_space)
    )
    def finalize_roof_constrained(self, max_kw, max_panels, roof_type, available_space):
        """Finalize recommendation when roof space is limiting"""
        # Recalculate cost for the constrained system
        cost = utils.calculate_installation_cost(max_kw, roof_type, self.config)
        
        self.declare(SolarFact(
            stage='system_finalized',
            final_system_kw=max_kw,
            final_num_panels=max_panels,
            final_cost=cost,
            final_roof_space=available_space,
            constrained_by='roof'
        ))
        
        self.add_reasoning(
            f"Due to roof space limitation, recommending scaled-down system: "
            f"{max_kw} kW ({max_panels} panels)"
        )
        
        self.add_alternative(
            "Consider using higher efficiency panels or optimizing roof layout "
            "to maximize capacity"
        )
    
    # ===== RULE 6c: Determine Final System (Budget Constrained) =====
    @Rule(
        SolarFact(stage='budget_constrained'),
        SolarFact(max_system_kw_by_budget=MATCH.max_kw),
        SolarFact(roof_type=MATCH.roof_type),
        SolarFact(budget=MATCH.budget)
    )
    def finalize_budget_constrained(self, max_kw, roof_type, budget):
        """Finalize recommendation when budget is limiting"""
        # Calculate actual number of panels and cost for budget-constrained system
        num_panels = utils.calculate_number_of_panels(max_kw, self.config)
        required_space = utils.calculate_required_roof_space(num_panels, self.config)
        cost = utils.calculate_installation_cost(max_kw, roof_type, self.config)
        
        # Adjust cost to not exceed budget
        cost = min(cost, budget)
        
        self.declare(SolarFact(
            stage='system_finalized',
            final_system_kw=max_kw,
            final_num_panels=num_panels,
            final_cost=cost,
            final_roof_space=required_space,
            constrained_by='budget'
        ))
        
        self.add_reasoning(
            f"Due to budget limitation, recommending scaled-down system: "
            f"{max_kw} kW ({num_panels} panels) for LKR {cost:,.2f}"
        )
        
        self.add_alternative(
            "Consider financing options or starting with a smaller system "
            "and expanding later"
        )
    
    # ===== RULE 6d: Determine Final System (Both Constrained) =====
    @Rule(
        SolarFact(stage='roof_constrained'),
        SolarFact(stage='budget_constrained'),
        SolarFact(max_system_kw_by_roof=MATCH.max_kw_roof),
        SolarFact(max_system_kw_by_budget=MATCH.max_kw_budget),
        SolarFact(max_panels_by_roof=MATCH.max_panels),
        SolarFact(roof_type=MATCH.roof_type)
    )
    def finalize_both_constrained(self, max_kw_roof, max_kw_budget, max_panels, roof_type):
        """Finalize recommendation when both roof and budget are limiting"""
        # Use the more restrictive constraint
        final_kw = min(max_kw_roof, max_kw_budget)
        
        # Recalculate based on final system
        num_panels = utils.calculate_number_of_panels(final_kw, self.config)
        required_space = utils.calculate_required_roof_space(num_panels, self.config)
        cost = utils.calculate_installation_cost(final_kw, roof_type, self.config)
        
        limiting_factor = "roof" if max_kw_roof < max_kw_budget else "budget"
        
        self.declare(SolarFact(
            stage='system_finalized',
            final_system_kw=final_kw,
            final_num_panels=num_panels,
            final_cost=cost,
            final_roof_space=required_space,
            constrained_by='both'
        ))
        
        self.add_reasoning(
            f"Both roof space and budget are limiting factors. The {limiting_factor} "
            f"is more restrictive. Recommending: {final_kw} kW ({num_panels} panels)"
        )
        
        self.add_alternative(
            "To maximize ROI within constraints, ensure optimal panel placement "
            "and consider energy efficiency measures to reduce consumption"
        )
    
    # ===== RULE 7: Calculate Energy Generation and Savings =====
    @Rule(
        SolarFact(stage='system_finalized'),
        SolarFact(final_system_kw=MATCH.system_kw),
        SolarFact(final_cost=MATCH.cost),
        SolarFact(sun_hours=MATCH.sun_hours),
        SolarFact(monthly_kwh=MATCH.monthly_kwh)
    )
    def calculate_savings(self, system_kw, cost, sun_hours, monthly_kwh):
        """Calculate annual generation and savings"""
        # Calculate annual generation
        annual_generation = utils.calculate_annual_generation(
            system_kw, sun_hours, self.config
        )
        
        # Calculate average tariff rate
        avg_tariff = utils.calculate_average_tariff_rate(monthly_kwh, self.config)
        
        # Calculate annual savings
        annual_savings = utils.calculate_annual_savings(
            annual_generation, avg_tariff, cost, self.config
        )
        
        # Calculate payback period
        payback_years = utils.calculate_payback_period(cost, annual_savings)
        
        self.declare(SolarFact(
            stage='savings_calculated',
            annual_generation_kwh=annual_generation,
            annual_savings=annual_savings,
            payback_years=payback_years
        ))
        
        if payback_years:
            self.add_reasoning(
                f"Expected annual generation: {annual_generation:,.0f} kWh, "
                f"Annual savings: LKR {annual_savings:,.2f}, "
                f"Payback period: {payback_years} years"
            )
        else:
            self.add_reasoning(
                f"Expected annual generation: {annual_generation:,.0f} kWh, "
                f"Unable to calculate positive payback period"
            )
            self.add_warning(
                "Annual savings are insufficient to justify the investment"
            )
    
    # ===== RULE 8: Determine Confidence Level =====
    @Rule(
        SolarFact(stage='savings_calculated'),
        SolarFact(payback_years=MATCH.payback_years),
        SolarFact(sun_hours_uncertainty=MATCH.uncertainty)
    )
    def determine_confidence(self, payback_years, uncertainty):
        """Determine confidence level in the recommendation"""
        confidence_level, confidence_uncertainty, explanation = \
            utils.calculate_confidence(payback_years, uncertainty, self.config)
        
        self.declare(SolarFact(
            stage='confidence_determined',
            confidence_level=confidence_level,
            confidence_uncertainty=confidence_uncertainty
        ))
        
        if payback_years:
            self.add_reasoning(
                f"Confidence level: {confidence_level.upper()} "
                f"(±{confidence_uncertainty} years in payback estimate). {explanation}"
            )
        else:
            self.add_reasoning(f"Confidence level: {confidence_level.upper()}. {explanation}")
    
    # ===== RULE 9: Final Recommendation =====
    @Rule(
        SolarFact(stage='confidence_determined'),
        SolarFact(final_system_kw=MATCH.system_kw),
        SolarFact(final_num_panels=MATCH.num_panels),
        SolarFact(final_cost=MATCH.cost),
        SolarFact(final_roof_space=MATCH.roof_space),
        SolarFact(annual_generation_kwh=MATCH.annual_gen),
        SolarFact(annual_savings=MATCH.annual_savings),
        SolarFact(payback_years=MATCH.payback),
        SolarFact(confidence_level=MATCH.confidence),
        SolarFact(confidence_uncertainty=MATCH.uncertainty)
    )
    def generate_final_recommendation(
        self, system_kw, num_panels, cost, roof_space,
        annual_gen, annual_savings, payback, confidence, uncertainty
    ):
        """Generate the final recommendation"""
        self.recommendation.recommended_system_kw = system_kw
        self.recommendation.num_panels = num_panels
        self.recommendation.installation_cost = cost
        self.recommendation.required_roof_space = roof_space
        self.recommendation.annual_generation_kwh = annual_gen
        self.recommendation.annual_savings = annual_savings
        self.recommendation.payback_years = payback
        self.recommendation.confidence_level = confidence
        self.recommendation.confidence_uncertainty = uncertainty
        
        # Determine recommendation category
        self.recommendation.recommendation_category = \
            utils.get_recommendation_category(payback, self.config)
        
        self.add_reasoning(
            f"FINAL RECOMMENDATION: {self.recommendation.recommendation_category}"
        )
        
        self.declare(SolarFact(stage='complete'))
    
    # ===== RULE 10: Handle Infeasible Case =====
    @Rule(
        SolarFact(stage='budget_insufficient')
    )
    def handle_infeasible(self):
        """Handle cases where installation is not feasible"""
        self.recommendation.is_feasible = False
        self.add_reasoning(
            "Solar installation is not feasible under current constraints. "
            "Consider increasing budget or reducing energy consumption first."
        )
        
        self.declare(SolarFact(stage='complete'))


def run_expert_system(
    monthly_kwh: float,
    location: str,
    roof_type: str,
    budget: float,
    available_roof_space: float = None
) -> SolarRecommendation:
    """
    Run the expert system with given inputs
    
    Args:
        monthly_kwh: Monthly electricity consumption in kWh
        location: Location/city name
        roof_type: Type of roof (tile, asbestos, concrete, other)
        budget: Available budget in LKR
        available_roof_space: Available roof space in sq.ft. (optional)
    
    Returns:
        SolarRecommendation object with results
    """
    # Load configuration
    config = utils.load_config()
    
    # Create expert system
    expert = SolarROIExpert(config)
    expert.reset()
    
    # Declare initial facts
    expert.declare(SolarFact(stage='input'))
    expert.declare(SolarFact(monthly_kwh=monthly_kwh))
    expert.declare(SolarFact(location=location))
    expert.declare(SolarFact(roof_type=roof_type))
    expert.declare(SolarFact(budget=budget))
    expert.declare(SolarFact(available_roof_space=available_roof_space))
    
    # Run the expert system
    expert.run()
    
    return expert.recommendation
