# Solar ROI Calculation Logic Explained

## Understanding the Numbers

### Your Question: Why is yearly generation not 550 × 12?

**Great observation!** Here's the complete explanation:

## The Two Different Values

### 1. Your Electricity Consumption
- **Monthly:** 550 kWh
- **Annual:** 550 × 12 = **6,600 kWh/year**
- This is how much electricity YOU USE

### 2. Solar System Generation
- **Annual:** 4,033 kWh/year
- This is how much electricity the SOLAR SYSTEM PRODUCES

## Why Are They Different?

The solar system generation (4,033 kWh) is LESS than your consumption (6,600 kWh) because:

### Your system is UNDERSIZED due to constraints!

Let me walk through the calculations:

## Step-by-Step Calculation

### Step 1: Calculate Required System Size

**What you NEED:**
```
Daily consumption = 550 kWh ÷ 30 days = 18.33 kWh/day
Sun hours (Colombo) = 5.2 hours/day
System efficiency = 0.85 (accounts for inverter losses, dust, shading, etc.)
Oversizing factor = 1.15 (safety margin)

Required kW = (Daily consumption ÷ (Sun hours × Efficiency)) × Oversizing
Required kW = (18.33 ÷ (5.2 × 0.85)) × 1.15
Required kW = (18.33 ÷ 4.42) × 1.15
Required kW = 4.15 × 1.15
Required kW = 4.77 kW ← THIS IS WHAT YOU ACTUALLY NEED!
```

### Step 2: Apply Constraints

The expert system then checks:
- ✓ Budget: LKR 500,000
- ✓ Roof space available
- ⚠️ **Budget constraint limits you to 2.5 kW system**

**Why 2.5 kW?**
```
Cost per kW = ~200,000 LKR/kW
Budget = 500,000 LKR
Maximum affordable = 500,000 ÷ 200,000 = 2.5 kW
```

### Step 3: Calculate Annual Generation

**What the 2.5 kW system PRODUCES:**
```
Daily generation = System size × Sun hours × Efficiency
Daily generation = 2.5 kW × 5.2 hours × 0.85
Daily generation = 11.05 kWh/day

Annual generation = Daily generation × 365 days
Annual generation = 11.05 × 365
Annual generation = 4,033 kWh/year ← THIS IS WHAT YOU SAW!
```

## The Coverage Gap

```
Your consumption:    6,600 kWh/year (100%)
Solar generation:    4,033 kWh/year (61%)
Still from grid:     2,567 kWh/year (39%)
```

**The 2.5 kW system covers only 61% of your electricity needs!**

## Why This Happens

The expert system is working correctly:

1. **Calculates ideal size:** 4.77 kW to fully cover your needs
2. **Applies constraints:** Budget limits you to 2.5 kW
3. **Shows realistic output:** 2.5 kW generates 4,033 kWh/year
4. **Calculates savings:** Only on the 4,033 kWh you generate

## What the Numbers Mean

### Installation Cost: LKR 500,000
- This is the TOTAL cost to install the 2.5 kW system
- Includes panels, inverter, mounting, labor, etc.

### Annual Savings: LKR 115,748/year
- This is calculated on the 4,033 kWh you GENERATE (not consume)
- Formula: `Generated kWh × Self-consumption rate × Tariff rate - Maintenance`
- The remaining 2,567 kWh you still pay for from the grid

### Payback Period: 4.3 years
- How long to recover your LKR 500,000 investment
- Formula: `Installation cost ÷ Annual savings`
- 500,000 ÷ 115,748 = 4.3 years

## The Logic is Correct!

The system is NOT showing you can generate 550 kWh/month. Instead:

**Your consumption:** 550 kWh/month (6,600/year)  
**Your system generates:** 336 kWh/month (4,033/year)  
**Deficit from grid:** 214 kWh/month (2,567/year)

## How to Get 100% Coverage

To cover all 6,600 kWh/year, you would need:

### Option 1: Increase Budget
- Need 4.77 kW system
- Cost: ~LKR 950,000+
- Would generate: ~7,700 kWh/year (117% coverage)

### Option 2: Reduce Consumption
- Reduce to ~336 kWh/month
- The 2.5 kW system would then cover 100%

### Option 3: Phased Installation
- Install 2.5 kW now
- Add 2.3 kW later when budget allows
- Total: 4.8 kW system

## Updated Display

The app now shows:

✓ **Annual Energy Generation:** 4,033 kWh/year  
✓ **Your Annual Consumption:** 6,600 kWh/year  
✓ **Solar Coverage:** 61.1% of your electricity needs  

This makes it crystal clear that the system is undersized!

## Why System Efficiency Matters

The 0.85 efficiency factor accounts for:
- Inverter losses: ~5%
- Cable losses: ~2%
- Dust and dirt: ~3-5%
- Temperature effects: ~5-10%
- Shading: Variable
- Panel degradation: ~0.5%/year

**This is realistic and industry-standard!**

## Summary

**Your observation was correct!** The annual generation (4,033 kWh) is NOT equal to your annual consumption (6,600 kWh) because:

1. The expert system calculated you need 4.77 kW
2. Your budget constrains you to 2.5 kW
3. The 2.5 kW system can only generate 4,033 kWh/year
4. This covers 61% of your needs
5. You'll still draw 2,567 kWh/year from the grid

**The calculations are accurate and realistic!** The system is being honest about what you can achieve with your budget constraints.
