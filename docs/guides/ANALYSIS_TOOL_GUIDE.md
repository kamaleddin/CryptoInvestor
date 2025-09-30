# Analysis Tool Selection Guide v2.1

## 📊 Three Approaches to DCA Analysis

This project includes **three different analyzers**, each with specific use cases and trade-offs.

> **v2.1 Update**: Balanced Rolling now uses **monthly (4-week) steps** for 378 simulations (3x more data).

---

## 🔧 Tool Overview

| Tool | Sample Size | Autocorrelation | Statistical Validity | Best For |
|------|-------------|-----------------|---------------------|----------|
| **Duration Simulator** | Maximum (1,512) | Very High | ❌ Invalid | Exploration |
| **Balanced Rolling** ⭐ | **Large (378)** | Manageable | ✅ Excellent with corrections | **Recommended** |
| **Advanced Non-Overlapping** | Small (18) | None | ✅ Perfect | Academic rigor |

---

## 1️⃣ Duration Simulator (`duration_simulator.py`)

### Overview
Runs **1,512 simulations** with weekly rolling windows across 1-4 year durations.

### Strengths
- ✅ **Maximum data utilization** (456 1-year periods)
- ✅ **Great for pattern detection** (identifies best/worst periods)
- ✅ **Shows full range** of possible outcomes
- ✅ **Easy to understand** (simple statistics)
- ✅ **Fast execution** (~30 seconds)

### Weaknesses  
- ❌ **Severe autocorrelation** (98% overlap between consecutive periods)
- ❌ **Invalid statistical inference** (can't claim significance)
- ❌ **Inflated sample size** (456 periods ≈ only 9 independent)
- ❌ **No risk-adjusted metrics**
- ❌ **Missing tail risk analysis**

### When to Use
- **Exploratory analysis**: Understanding historical patterns
- **Best-case scenarios**: Finding optimal entry/exit periods  
- **Hypothesis generation**: Identifying trends to test
- **Client presentations**: Showing range of outcomes
- **Backtesting ideas**: Quick iteration

### When NOT to Use
- ❌ **Statistical significance claims**
- ❌ **Academic research**
- ❌ **Regulatory submissions**
- ❌ **Risk assessment**

### Example Output
```
1-Year Duration (456 simulations):
- Optimum DCA: 168.68% avg, 59.9% win rate
- Simple DCA: 70.43% avg, 77.2% win rate
- Best period: Dec 2022 - Dec 2023 (52,535% return!)
```

### Usage
```bash
python tools/duration_simulator.py
```

---

## 2️⃣ Balanced Rolling Analyzer (`balanced_rolling_analyzer.py`) ⭐ **RECOMMENDED**

### Overview
Uses **monthly rolling windows** (4-week steps) for **378 total simulations** (v2.1 optimized).

### Strengths
- ✅ **Large sample sizes** (144 1-year, 126 2-year, 108 3-year, 90 4-year) - 3x more!
- ✅ **Manageable autocorrelation** (~92% overlap, correctable with Newey-West)
- ✅ **Risk-adjusted metrics** (Sharpe, Sortino, Calmar)
- ✅ **Statistical testing** (t-tests, Mann-Whitney U)
- ✅ **Bootstrap confidence intervals**
- ✅ **VaR and CVaR** analysis
- ✅ **Practical balance** between rigor and power

### Weaknesses
- ⚠️ **Moderate autocorrelation** (requires Newey-West corrections)
- ⚠️ **Some conservatism needed** (effective N ≈ 40% of actual)

### When to Use (Most Scenarios)
- ✅ **Standard analysis**: Default choice for most studies
- ✅ **Risk assessment**: Comprehensive risk metrics
- ✅ **Strategy comparison**: Statistically sound comparisons
- ✅ **Investment decisions**: Balances rigor with practicality
- ✅ **Client reports**: Professional-grade analysis
- ✅ **Performance attribution**: Understanding sources of return

### Example Output
```
1-Year Duration (36 periods, ~14 effective independent):
- Optimum: 272.34% avg [CI: 19.70%, 740.08%]
- Simple: 65.58% avg [CI: 30.24%, 111.04%]
- Sharpe Ratio: 0.193 vs 0.495 (Simple wins)
- Sortino Ratio: 29.634 vs 3.792 (Optimum wins)
- P-value: 0.38 (not significant at 5%)
- Effect Size: d=0.21 (small)
```

### Usage
```bash
python tools/balanced_rolling_analyzer.py
```

---

## 3️⃣ Advanced Non-Overlapping Analyzer (`advanced_duration_analyzer.py`)

### Overview
Uses **completely non-overlapping** periods for perfect statistical independence.

### Strengths
- ✅ **Perfect independence** (zero autocorrelation)
- ✅ **Unbiased standard errors**
- ✅ **Valid p-values**
- ✅ **Publication-ready** methodology
- ✅ **All risk metrics** (Sharpe, Sortino, VaR, CVaR, etc.)
- ✅ **Distribution analysis** (skewness, kurtosis)

### Weaknesses
- ❌ **Very small samples** (9, 4, 3, 2 periods)
- ❌ **Low statistical power** (can't detect small/medium effects)
- ❌ **High sensitivity** to outliers
- ❌ **Wide confidence intervals**

### When to Use
- ✅ **Academic research**: Peer-reviewed publications
- ✅ **Regulatory filings**: Requires unbiased estimates  
- ✅ **Conservative estimates**: Maximum rigor needed
- ✅ **Methodological gold standard**: Teaching/benchmarking

### When NOT to Use
- ❌ **Exploratory analysis** (insufficient power)
- ❌ **Detecting small effects** (underpowered)
- ❌ **Quick iterations** (too conservative)

### Example Output
```
1-Year Duration (9 independent periods):
- Optimum: 114.84% [CI: 10.53%, 272.72%]
- Simple: 94.07% [CI: 7.30%, 227.77%]
- P-value: 0.83 (not significant)
- Conclusion: Cannot prove difference exists
```

### Usage
```bash
python tools/advanced_duration_analyzer.py
```

---

## 🎯 Decision Tree: Which Tool Should I Use?

```
START
  │
  ├─ Need maximum statistical rigor? (academic/regulatory)
  │   └─ YES → Advanced Non-Overlapping Analyzer
  │
  ├─ Want to explore historical patterns only?
  │   └─ YES → Duration Simulator
  │
  └─ Standard analysis for decision-making?
      └─ YES → Balanced Rolling Analyzer ⭐
```

---

## 📊 Detailed Comparison

### Sample Sizes

| Duration | Duration Sim | Balanced Rolling | Non-Overlapping |
|----------|--------------|------------------|-----------------|
| 1-Year | 456 | 36 (~14 effective) | 9 |
| 2-Year | 404 | 32 (~13 effective) | 4 |
| 3-Year | 352 | 28 (~11 effective) | 3 |
| 4-Year | 300 | 24 (~10 effective) | 2 |
| **Total** | **1,512** | **120 (~48)** | **18** |

### Autocorrelation

| Method | Overlap % | Correlation | Independence |
|--------|-----------|-------------|--------------|
| Weekly Rolling | 98% | Very High | ❌ Invalid |
| Bi-weekly Rolling | 96% | Very High | ❌ Invalid |
| Monthly Rolling | 92% | High | ⚠️ Weak |
| **Quarterly Rolling** | **75%** | **Moderate** | ⚠️ **Good** |
| Semi-annual Rolling | 50% | Low | ✅ Good |
| **Non-Overlapping** | **0%** | **None** | ✅ **Perfect** |

### Statistical Power

Assuming small effect size (d=0.3) and α=0.05:

| Method | Sample Size | Power | Can Detect? |
|--------|-------------|-------|-------------|
| Duration Sim* | 456 (9 effective) | 23% | ❌ No |
| Balanced Rolling | 36 (14 effective) | 40% | ⚠️ Weak |
| Non-Overlapping | 9 | 23% | ❌ No |

*Overstates power due to autocorrelation

### Risk Metrics Comparison

| Metric | Duration Sim | Balanced | Non-Overlapping |
|--------|--------------|----------|-----------------|
| Mean Return | ✅ | ✅ | ✅ |
| Median Return | ✅ | ✅ | ✅ |
| Volatility | ❌ | ✅ | ✅ |
| Sharpe Ratio | ❌ | ✅ | ✅ |
| Sortino Ratio | ❌ | ✅ | ✅ |
| Max Drawdown | ❌ | ✅ | ✅ |
| VaR / CVaR | ❌ | ✅ | ✅ |
| Skewness / Kurtosis | ❌ | ✅ | ✅ |
| Confidence Intervals | ❌ | ✅ (Bootstrap) | ✅ (Bootstrap) |
| P-values | ❌ Invalid | ✅ | ✅ |

---

## 💡 Best Practices

### 1. **Use All Three for Comprehensive Analysis**

```python
# Step 1: Explore patterns
python tools/duration_simulator.py
# Outcome: Find best periods, understand range

# Step 2: Rigorous analysis  
python tools/balanced_rolling_analyzer.py
# Outcome: Statistical significance, risk metrics

# Step 3: Validate with gold standard
python tools/advanced_duration_analyzer.py
# Outcome: Confirm findings with perfect independence
```

### 2. **Report Methodology Clearly**

**Bad**: "Optimum DCA beats Simple DCA (p<0.001)"
- Doesn't mention overlapping data
- P-value likely invalid

**Good**: "Using quarterly rolling windows (n=36, ~14 effective), Optimum DCA showed higher average returns (272% vs 66%), but the difference was not statistically significant (p=0.38). However, Optimum had superior downside protection (Sortino: 29.6 vs 3.8)."

### 3. **Match Tool to Audience**

| Audience | Recommended Tool | Why |
|----------|------------------|-----|
| Clients | Balanced Rolling | Professional metrics, understandable |
| Researchers | Non-Overlapping | Rigorous methodology |
| Yourself | Duration Simulator | Fast exploration |
| Regulators | Non-Overlapping | Conservative, unbiased |
| Media | Duration Simulator | Compelling stories |

### 4. **Adjust for Multiple Testing**

If testing 4 durations:
- Bonferroni correction: α = 0.05 / 4 = 0.0125
- FDR correction: Less conservative
- Report all p-values and let readers judge

### 5. **Focus on Effect Sizes**

P-values alone insufficient:
- **Always report Cohen's d**
- **Include confidence intervals**
- **Show practical significance**

Example:
- d = 0.1: Negligible (don't bother)
- d = 0.3: Small (maybe interesting)
- d = 0.5: Medium (worth pursuing)
- d = 0.8: Large (strong effect)

---

## 🎓 Conclusion

### For Most Users: **Balanced Rolling Analyzer** ⭐

Provides the best trade-off between:
- Statistical rigor
- Practical sample sizes
- Comprehensive risk metrics
- Decision-relevant insights

### Quick Reference

```bash
# Exploration & Pattern Finding
python tools/duration_simulator.py

# Standard Analysis (RECOMMENDED)
python tools/balanced_rolling_analyzer.py

# Maximum Statistical Rigor
python tools/advanced_duration_analyzer.py

# Compare Methodologies
python tools/analyze_simulation_results.py
```

### Key Takeaway

**The tool you choose changes your conclusions!**

- Duration Simulator: Suggests Optimum beats Simple
- Balanced Rolling: Suggests no significant difference, context-dependent
- Non-Overlapping: Suggests insufficient evidence to choose

**Truth**: All are correct for their assumptions. Choose based on your needs for rigor vs. power.

---

**Last Updated**: September 30, 2025  
**Recommended Default**: Balanced Rolling Analyzer  
**For Publications**: Advanced Non-Overlapping Analyzer
