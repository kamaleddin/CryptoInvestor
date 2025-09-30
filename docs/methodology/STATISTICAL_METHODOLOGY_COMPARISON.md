# Statistical Methodology Comparison

## Executive Summary

This document compares two approaches to analyzing DCA strategy performance and explains the mathematical and statistical improvements in the advanced analyzer.

---

## 🔬 Key Statistical Issues Identified

### Original Approach (`duration_simulator.py`)

| Issue | Description | Impact |
|-------|-------------|--------|
| **Severe Autocorrelation** | Weekly overlapping periods share 51/52 weeks of data | Violates independence assumption |
| **Inflated Sample Size** | 456 "independent" 1-year periods, but only ~9 truly independent | False confidence in results |
| **No Risk Adjustment** | Only raw returns, ignores volatility | Can't compare risk-adjusted performance |
| **Missing Statistical Tests** | No significance testing | Can't prove if differences are real vs. random |
| **No Distribution Analysis** | Skewness, kurtosis, tail risk ignored | Missing key risk characteristics |
| **No Confidence Intervals** | Point estimates only | No uncertainty quantification |

### ⚠️ **Critical Statistical Flaw**

When periods overlap by 98% (weekly rolling), observations are **NOT independent**. This means:
- Standard errors are **severely underestimated**
- P-values are **artificially low**  
- Confidence intervals are **too narrow**
- Statistical significance is **misleading**

**Example**: 456 weekly-rolling 1-year periods ≈ only **9 independent observations**

---

## ✅ Improvements in Advanced Analyzer

### 1. **Non-Overlapping Periods** (Statistical Independence)

```python
# Original: Weekly rolling (severe overlap)
start_dates = [2016-01-01, 2016-01-08, 2016-01-15, ...]  # 456 periods
# Actual independence: ~9 periods

# Improved: Non-overlapping (true independence)
start_dates = [2016-01-01, 2017-01-01, 2018-01-01, ...]  # 9 periods  
# Actual independence: 9 periods
```

**Trade-off**: Fewer observations (9 vs 456), but **statistically valid**

### 2. **Risk-Adjusted Performance Metrics**

| Metric | Formula | What It Measures | Why Important |
|--------|---------|------------------|---------------|
| **Sharpe Ratio** | (Return - RF) / σ | Return per unit of total risk | Standard in finance, risk-adjusted performance |
| **Sortino Ratio** | (Return - RF) / Downside σ | Return per unit of downside risk | Better for asymmetric returns |
| **Calmar Ratio** | Annual Return / Max Drawdown | Return per unit of max loss | Risk of ruin |
| **Max Drawdown** | Max peak-to-trough decline | Worst historical loss | Investor psychology |

**Key Insight**: A strategy with 200% return but 300% volatility may be **worse** than one with 100% return and 50% volatility.

### 3. **Statistical Significance Testing**

#### Paired T-Test
```
H₀: Mean(Optimum) = Mean(Simple)
H₁: Mean(Optimum) ≠ Mean(Simple)

Result: p-value = 0.83 (1-year) → Cannot reject H₀
```

**Conclusion**: Despite Optimum showing higher average returns (114.84% vs 94.07%), this difference is **NOT statistically significant** (p > 0.05).

#### Effect Size (Cohen's d)
```
d = (Mean₁ - Mean₂) / Pooled SD

d = 0.101 (1-year) → "Negligible" effect
d = -0.271 (2-year) → "Small" effect (favors Simple)
d = 0.489 (3-year) → "Medium" effect (favors Optimum)
d = -0.984 (4-year) → "Large" effect (favors Simple)
```

**Interpretation**:
- d < 0.2: Negligible
- d = 0.2-0.5: Small
- d = 0.5-0.8: Medium  
- d > 0.8: Large

### 4. **Bootstrap Confidence Intervals**

Instead of assuming normality, **resample** data 10,000 times to estimate uncertainty:

```
1-Year Optimum: 114.84% [95% CI: 10.53%, 272.72%]
1-Year Simple:   94.07% [95% CI:  7.30%, 227.77%]
```

**Key Finding**: Confidence intervals **overlap significantly** → No statistical difference

### 5. **Distribution Analysis**

| Metric | 1-Year Optimum | 1-Year Simple | Interpretation |
|--------|----------------|---------------|----------------|
| **Skewness** | 1.912 | 1.927 | Right-skewed (long tail of extreme gains) |
| **Kurtosis** | 2.431 | 2.515 | Fat tails (more extreme outcomes) |
| **Normality** | False | False | Returns NOT normally distributed |

**Implication**: Traditional mean/std analysis **insufficient**; need VaR, CVaR for tail risk.

### 6. **Value at Risk (VaR) & Conditional VaR**

```
1-Year Optimum VaR₉₅: -33.33%
→ 95% confident won't lose more than 33.33%

1-Year Optimum CVaR₉₅: -33.70%  
→ If you hit the worst 5% of outcomes, average loss is 33.70%
```

**Simple DCA has worse tail risk**: -44.39% worst case vs -33.70%

---

## 📊 Comparison of Results

### Original Simulator (Overlapping)
```
1-Year Duration (456 simulations):
- Optimum: 168.68% avg return
- Simple: 70.43% avg return
- Outperformance: 98.25 pp
- Optimum wins: 59.9%
```

### Advanced Analyzer (Non-Overlapping)
```
1-Year Duration (9 independent periods):
- Optimum: 114.84% avg return [CI: 10.53%, 272.72%]
- Simple: 94.07% avg return [CI: 7.30%, 227.77%]
- Outperformance: 20.78 pp
- Optimum wins: 66.7%
- Statistical significance: NO (p=0.83)
- Effect size: Negligible (d=0.10)
```

### Why Different Results?

1. **Sample selection bias**: Original includes many overlapping bull market periods
2. **Autocorrelation**: Overlapping periods count same events multiple times
3. **Outlier sensitivity**: Small independent sample more affected by extreme periods

---

## 🎯 Statistical Best Practices Implemented

### 1. **Sample Size Considerations**
- **Rule of thumb**: Need n≥30 for CLT, n≥8 for t-tests
- **Our data**: 9, 4, 3, 2 non-overlapping periods
- **Solution**: Bootstrap for confidence intervals, use non-parametric tests

### 2. **Multiple Hypothesis Testing**
- Testing 4 durations → Bonferroni correction: α = 0.05/4 = 0.0125
- None of our p-values pass even uncorrected α = 0.05

### 3. **Effect Size Reporting**
- P-values alone insufficient
- Report Cohen's d for practical significance
- Use confidence intervals over point estimates

### 4. **Assumption Checking**
- Test for normality (Jarque-Bera)
- Use non-parametric tests when violated
- Bootstrap when sample size small

### 5. **Risk-Adjusted Metrics**
- Sharpe ratio industry standard
- Sortino better for asymmetric returns
- Max drawdown for behavioral finance

---

## 🔍 Key Findings from Advanced Analysis

### 1-Year Duration
- **No statistical difference** between strategies (p=0.83)
- Optimum has **better downside protection** (VaR: -33% vs -44%)
- **Much better Sortino** (168.8 vs 11.6) → Optimum's volatility is upside
- Simple has better win rate (78% vs 44%)

### 2-Year Duration  
- **No statistical difference** (p=0.76)
- Simple DCA actually performs better on average (481% vs 303%)
- Both have 100% win rate in non-overlapping periods
- Simple has higher volatility (770% vs 522%)

### 3-Year Duration
- **No statistical difference** (p=0.54)
- Optimum shows higher average (462% vs 267%)
- But **much higher volatility** (556% vs 101%)
- Simple has **better Sharpe ratio** (1.46 vs 0.47) → Better risk-adjusted
- Medium effect size (d=0.49) suggests potential real difference

### 4-Year Duration
- **Only 2 independent periods** (insufficient data)
- Simple DCA dominates (252% vs 44%)
- Large negative effect size (d=-0.98)
- Both periods positive for Simple, one negative for Optimum

---

## 💡 Recommendations

### For Academic/Statistical Rigor
**Use: Advanced Analyzer (`advanced_duration_analyzer.py`)**
- Statistically valid inference
- Risk-adjusted metrics
- Proper uncertainty quantification
- Publication-ready methodology

### For Exploratory Analysis  
**Use: Duration Simulator (`duration_simulator.py`)**
- Identify patterns and trends
- Find best historical periods
- Generate hypotheses
- Understand range of outcomes

**BUT**: Don't claim statistical significance from overlapping data

### Combined Approach
1. **Explore** with duration simulator (1,512 scenarios)
2. **Validate** with advanced analyzer (18 independent periods)
3. **Report** both with caveats about methodology

---

## 📈 Recommended Additional Analyses

### 1. **Monte Carlo Simulation**
- Simulate future scenarios with bootstrapped returns
- Estimate probability distributions of outcomes
- Stress testing under different market conditions

### 2. **Rolling Window Analysis**
```python
# Use 4-week or 13-week steps (quarterly)
# Provides balance: more data than non-overlapping, less correlation than weekly
```

### 3. **Regime Detection**
- Identify bull/bear/sideways markets using Hidden Markov Models
- Analyze strategy performance by regime
- Time-varying performance

### 4. **Bayesian Analysis**
- Incorporate prior beliefs
- Update beliefs with data
- Posterior probability that Optimum > Simple

### 5. **Walk-Forward Analysis**
- Train on in-sample data
- Test on out-of-sample data
- Avoid overfitting

---

## 📊 Summary Statistics Table

| Metric | 1-Year | 2-Year | 3-Year | 4-Year |
|--------|--------|--------|--------|--------|
| **Independent Periods** | 9 | 4 | 3 | 2 |
| **Optimum Mean Return** | 114.84% | 302.61% | 462.24% | 44.35% |
| **Simple Mean Return** | 94.07% | 480.56% | 266.83% | 252.14% |
| **Optimum Sharpe** | 0.488 | 0.399 | 0.468 | 0.061 |
| **Simple Sharpe** | 0.493 | 0.434 | 1.462 | 0.631 |
| **Winner (Risk-Adj)** | Simple | Simple | Simple | Simple |
| **P-value** | 0.83 | 0.76 | 0.54 | 0.61 |
| **Statistical Sig?** | ❌ No | ❌ No | ❌ No | ❌ No |
| **Effect Size** | 0.10 (Neg) | -0.27 (Sm) | 0.49 (Med) | -0.98 (Lg) |

---

## 🎓 Conclusion

### Original Simulator Findings
- ✅ Good for exploration and pattern identification
- ✅ Shows range of historical outcomes
- ❌ **Statistically invalid** for inference
- ❌ Overstates significance due to overlapping data
- ❌ Missing risk-adjusted metrics

### Advanced Analyzer Findings  
- ✅ Statistically rigorous methodology
- ✅ Risk-adjusted performance metrics
- ✅ Proper uncertainty quantification
- ✅ Valid statistical inference
- ⚠️ Small sample sizes limit power
- ⚠️ Cannot detect all but very large effects

### **The Truth**
With proper statistical analysis, we find **no statistically significant difference** between Optimum and Simple DCA strategies. The differences observed could easily be due to:
- Random variation
- Small sample size
- Selection of specific time periods
- Market regime changes

### **However**
- Optimum shows **better downside protection** (lower VaR, CVaR)
- Optimum has **better Sortino ratio** (upside volatility)
- Simple has **more consistent returns** (better Sharpe on longer durations)
- Simple has **100% win rate** over 2+ years

**Bottom Line**: The "best" strategy depends on:
1. Investment horizon (1-3 years favors risk-taking Optimum, 4+ years favors consistent Simple)
2. Risk tolerance (Optimum more volatile but better downside)
3. Market regime (bull markets favor Optimum, bear markets favor Simple)

---

**Generated**: September 30, 2025  
**Methodology**: Frequentist statistics with bootstrap resampling  
**Significance Level**: α = 0.05 (two-tailed)  
**Software**: Python 3.x, SciPy 1.x, NumPy 1.x
