# 🚀 CryptoInvestor - DCA Strategy Analysis Suite v2.1

A comprehensive cryptocurrency investment analysis toolkit implementing and comparing multiple Dollar Cost Averaging (DCA) strategies with **statistically rigorous** performance evaluation.

> **v2.1 Update**: Optimized to 378 simulations (3x more data) using monthly rolling windows. See [What's New](#-whats-new-in-v21) below.

---

## ✨ Key Features

### 🎯 **Three Analysis Approaches**
- **Duration Simulator**: 1,512 simulations for pattern exploration
- **Balanced Rolling** ⭐: Recommended for standard analysis with risk metrics
- **Advanced Non-Overlapping**: Academic-grade statistical rigor

### 📊 **Comprehensive Metrics**
- Raw returns (mean, median, volatility)
- Risk-adjusted performance (Sharpe, Sortino, Calmar ratios)
- Tail risk analysis (VaR, CVaR, maximum drawdown)
- Statistical significance testing (t-tests, effect sizes, p-values)
- Bootstrap confidence intervals

### 💯 **Production Ready**
- Standalone implementation (no Excel dependency)
- Fully tested (21 comprehensive tests, 100% pass rate)
- Professional documentation and methodology papers
- Clean project structure following Python best practices

---

## 🎯 Quick Start

### Installation

```bash
# Clone repository
git clone <repository-url>
cd CryptoInvestor

# Install dependencies
pip install -r requirements/base.txt

# Optional: Install development dependencies
pip install -r requirements/dev.txt
```

### Run Analysis (Choose One)

```bash
# RECOMMENDED: Balanced approach with risk metrics
python tools/balanced_rolling_analyzer.py

# Exploration: Maximum historical data
python tools/duration_simulator.py

# Academic rigor: Perfect statistical independence
python tools/advanced_duration_analyzer.py

# Compare all three methods
python tools/comprehensive_comparison.py
```

### View Results

```bash
# Main comparison report
cat reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT.txt

# Tool selection guide
cat docs/guides/ANALYSIS_TOOL_GUIDE.md

# Statistical methodology
cat docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md
```

---

## 📊 Key Findings

### 🎯 **Key Finding: No Statistically Significant Advantage**

Despite the complexity of Optimum DCA, there's **NO statistically significant difference** between Optimum and Simple DCA strategies across most investment horizons when properly accounting for autocorrelation.

### 🏆 **Performance Summary** (Monthly Rolling v2.1 - Recommended)

| Duration | Optimum Avg | Simple Avg | Winner | Sharpe Ratio | P-Value | Win Rate |
|----------|-------------|------------|--------|--------------|---------|----------|
| **1-Year** | 65.3% | 70.7% | Simple | O: 0.169, S: 0.566 | 0.881 ❌ | S: 77%, O: 39% |
| **2-Year** | 64.2% | 152.8% | Simple | O: 0.195, S: 0.421 | 0.008 ✅ | S: 84%, O: 37% |
| **3-Year** | 209.2% | 174.2% | Mixed | O: 0.167, S: 0.568 | 0.596 ❌ | S: 95%, O: 35% |
| **4-Year** | 165.2% | 248.4% | Simple | O: 0.140, S: 0.586 | 0.193 ❌ | S: 100%, O: 19% |

✅ = Statistically significant | ❌ = Not statistically significant | O = Optimum, S = Simple

**Critical Finding**: Simple DCA is **statistically significantly better** for 2-year horizons (p=0.008)

### 🛡️ **Risk Analysis**

**Optimum DCA Characteristics:**
- ✅ Better downside protection (lower VaR: -27.7% vs -40.3% at 1-year)
- ✅ Superior Sortino ratios (downside-risk-adjusted returns)
- ✅ Lower maximum drawdowns in most periods
- ❌ Extremely high volatility (362% vs 118% at 1-year)
- ❌ Low win rates (18-39% vs Simple's 77-100%)

**Simple DCA Characteristics:**
- ✅ Superior Sharpe ratios (0.421-0.586 vs Optimum's 0.140-0.195)
- ✅ More consistent returns (lower standard deviation)
- ✅ Higher win rates (77-100% success rate)
- ✅ Much lower volatility
- ❌ Higher tail risk in extreme downturns

### 💡 **Practical Recommendations**

**Choose Simple DCA if you:**
- Want predictable, consistent returns
- Prefer lower volatility (risk-averse)
- Have 2-4 year investment horizon
- Value simplicity in execution
- Need reliable performance metrics

**Consider Optimum DCA if you:**
- Can tolerate extreme volatility (362%+ annual)
- Want tail risk protection
- Seek potential for extreme upside (lottery-ticket returns)
- Have very short horizons during confirmed bull markets
- Can actively monitor and adjust positions

### 📊 **Statistical Reality Check**

The analysis used three methodologies to ensure robust conclusions:

1. **Weekly Rolling** (1,512 simulations) - ⚠️ Misleading due to 98% overlap
2. **Monthly Rolling** (378 simulations) - ✅ Best balance, ~8% autocorrelation (**RECOMMENDED**)
3. **Non-Overlapping** (18 simulations) - ✅ Perfect independence but low statistical power

**Bottom Line**: When properly accounting for statistical dependencies, **Simple DCA performs as well or better than Optimum DCA** with significantly less complexity and risk.

### 🏆 **Final Verdict**

**Simple DCA is the practical winner** for most investors:
- Statistically equivalent or better returns in most periods
- **Significantly outperforms in 2-year windows** (p=0.008)
- Much simpler to implement and maintain
- Lower volatility and more predictable outcomes
- No complex VWAP calculations or volatility adjustments needed

The added complexity of Optimum DCA (VWAP bands, volatility adjustments, dynamic multipliers) **does not translate to statistically significant outperformance** and actually underperforms significantly in 2-year windows.

---

## 📁 Project Structure

```
CryptoInvestor/
├── src/                    # Core implementation
│   └── optimum_dca_analyzer.py
├── tools/                  # Analysis tools
│   ├── balanced_rolling_analyzer.py ⭐ (recommended)
│   ├── duration_simulator.py
│   ├── advanced_duration_analyzer.py
│   └── comprehensive_comparison.py
├── reports/                # Generated outputs
│   ├── simulations/
│   ├── comparisons/
│   └── analysis/
├── docs/                   # Documentation
│   ├── guides/
│   └── methodology/
├── tests/                  # Test suite (21 tests)
├── data/                   # Bitcoin price data
└── examples/               # Usage examples
```

**See**: [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for complete details.

---

## 🔬 Analysis Tools Comparison

| Tool | Simulations | Independence | Risk Metrics | Best For |
|------|-------------|--------------|--------------|----------|
| **Duration Simulator** | 1,512 | ❌ Low (~2%) | ❌ No | Pattern exploration |
| **Balanced Rolling** ⭐ | **378** | ⚠️ Manageable (~8%) | ✅ Yes | **Standard analysis** |
| **Advanced Non-Overlapping** | 18 | ✅ Perfect (100%) | ✅ Yes | Academic rigor |

**v2.1 Optimization**: Balanced Rolling now uses monthly (4-week) steps instead of quarterly, providing 3x more simulations with similar statistical validity.

### Which Tool Should I Use?

```
Exploring historical patterns?
  → duration_simulator.py

Standard investment analysis? (RECOMMENDED)
  → balanced_rolling_analyzer.py ⭐

Publishing research paper?
  → advanced_duration_analyzer.py

Want comprehensive comparison?
  → comprehensive_comparison.py
```

**See**: [docs/guides/ANALYSIS_TOOL_GUIDE.md](docs/guides/ANALYSIS_TOOL_GUIDE.md)

---

## 📊 Example Usage

### Quick Analysis

```python
from src.optimum_dca_analyzer import FlexibleOptimumDCA
from datetime import date

# Create analyzer
analyzer = FlexibleOptimumDCA(
    weekly_budget=250.0,
    start_date=date(2022, 1, 10),
    end_date=date(2025, 9, 22)
)

# Run both strategies
optimum = analyzer.run_optimum_dca_simulation()
simple = analyzer.run_simple_dca_simulation()

print(f"Optimum DCA: {optimum['profit_pct']:.1f}% return")
print(f"Simple DCA: {simple['profit_pct']:.1f}% return")
```

### Custom Period Analysis

```python
from tools.balanced_rolling_analyzer import AdvancedDurationAnalyzer
from datetime import date

# Analyze custom period
analyzer = AdvancedDurationAnalyzer(
    weekly_budget=500.0,  # Custom budget
    overall_start=date(2020, 1, 1),
    overall_end=date(2024, 12, 31),
    risk_free_rate=0.04  # 4% risk-free rate
)

results = analyzer.run_comprehensive_analysis(
    use_non_overlapping=False,
    rolling_step_weeks=13  # Quarterly
)

analyzer.print_analysis_report(results)
```

---

## 🧪 Testing

```bash
# Run all tests
python scripts/run_tests.py

# Run with coverage report
python scripts/run_tests.py --coverage

# Run specific test categories
python scripts/run_tests.py --validation   # Core validation tests
python scripts/run_tests.py --unit         # Unit tests
python scripts/run_tests.py --performance  # Performance tests
```

**Test Results**: 21 tests, 100% pass rate

**See**: [docs/TEST_SUMMARY.md](docs/TEST_SUMMARY.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | Complete project organization |
| [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) | Quick commands and tips |
| [ANALYSIS_TOOL_GUIDE.md](docs/guides/ANALYSIS_TOOL_GUIDE.md) | Which tool to use when |
| [REPORTS_GUIDE.md](docs/guides/REPORTS_GUIDE.md) | Understanding report outputs |
| [STATISTICAL_METHODOLOGY_COMPARISON.md](docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md) | Statistical methods explained |
| [DURATION_SIMULATION_README.md](docs/guides/DURATION_SIMULATION_README.md) | Simulation results |
| [TEST_SUMMARY.md](docs/TEST_SUMMARY.md) | Test documentation |

---

## 🆕 What's New in v2.1

### Sample Size Optimization ⭐
- ✅ **3x more simulations** (378 vs 120) using monthly rolling windows
- ✅ **Higher statistical power** (90% vs 35%)
- ✅ **Narrower confidence intervals** (3.2x more precise)
- ✅ **Better effect detection** (d=0.38 vs d=0.70)

### Updated Analysis
- ✅ **Monthly (4-week) rolling** now default instead of quarterly
- ✅ **Balanced rolling analyzer** optimized for maximum useful data
- ✅ **Quarterly vs monthly comparison** tool added
- ✅ **All reports regenerated** with new monthly analysis

### v2.0 Features (Still Included)
- ✅ **Three analysis methodologies** with statistical rigor
- ✅ **Risk-adjusted metrics** (Sharpe, Sortino, Calmar, VaR, CVaR)
- ✅ **Statistical testing** (t-tests, effect sizes, bootstrap CIs)
- ✅ **Comprehensive reporting** across all methodologies
- ✅ **Professional project structure** following Python best practices

### Key Insights
- ⚠️ **No statistically significant difference** between Optimum and Simple DCA
- ✅ **Choice depends on risk tolerance** and investment horizon
- ✅ **Methodology matters** - monthly rolling provides optimal balance
- ✅ **Simple DCA**: Better Sharpe (risk-adjusted), more consistent
- ✅ **Optimum DCA**: Better Sortino (downside protection), higher upside

---

## 🎯 Recommended Workflow

### For Investment Analysis

```bash
# 1. Run balanced analysis (recommended)
python tools/balanced_rolling_analyzer.py > reports/analysis/my_analysis.txt

# 2. Review results
cat reports/analysis/my_analysis.txt

# 3. Understand the statistics
cat docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md
```

### For Research

```bash
# 1. Explore patterns
python tools/duration_simulator.py

# 2. Rigorous analysis
python tools/balanced_rolling_analyzer.py

# 3. Validate findings
python tools/advanced_duration_analyzer.py

# 4. Compare all methods
python tools/comprehensive_comparison.py
```

---

## 📊 Performance Metrics Explained

### Raw Returns
- **Mean Return**: Average return across all periods
- **Median Return**: Middle value (less affected by outliers)
- **Volatility (σ)**: Standard deviation of returns

### Risk-Adjusted Returns
- **Sharpe Ratio**: Return per unit of total risk (higher is better)
- **Sortino Ratio**: Return per unit of downside risk (higher is better)
- **Calmar Ratio**: Return per unit of maximum drawdown

### Risk Metrics
- **Max Drawdown**: Worst peak-to-trough decline
- **VaR (95%)**: Maximum expected loss at 95% confidence
- **CVaR (95%)**: Average loss in worst 5% of cases

### Statistical Tests
- **P-Value**: Probability of false positive (< 0.05 is significant)
- **Effect Size (Cohen's d)**: Magnitude of difference (0.2=small, 0.5=medium, 0.8=large)
- **Confidence Interval**: Range of likely true values

---

## ⚙️ Configuration

### Custom Budget and Dates

```python
analyzer = FlexibleOptimumDCA(
    weekly_budget=500.0,         # Your budget
    start_date=date(2020, 1, 1), # Custom start
    end_date=date(2024, 12, 31), # Custom end
    final_btc_price=100000.0,    # Custom BTC price for valuation
    verbose=True                 # Show details
)
```

### Analysis Parameters

```python
analyzer = AdvancedDurationAnalyzer(
    weekly_budget=250.0,
    overall_start=date(2016, 1, 1),
    overall_end=date(2025, 9, 24),
    risk_free_rate=0.04,  # 4% annual risk-free rate
    verbose=True
)

# Quarterly rolling (recommended)
results = analyzer.run_comprehensive_analysis(
    use_non_overlapping=False,
    rolling_step_weeks=13
)

# Or non-overlapping (maximum rigor)
results = analyzer.run_comprehensive_analysis(
    use_non_overlapping=True
)
```

---

## 🔧 Dependencies

### Core Requirements
```
pandas >= 1.5.0
numpy >= 1.21.0
scipy >= 1.9.0
```

### Optional (Testing)
```
pytest >= 7.0.0
pytest-cov >= 3.0.0
```

Install all:
```bash
pip install -r requirements/base.txt   # Core only
pip install -r requirements/dev.txt    # Everything
```

---

## 📝 Citing This Work

If you use this analysis in research, please cite:

```
CryptoInvestor DCA Analysis Suite v2.0
Statistical Analysis of Dollar Cost Averaging Strategies for Bitcoin
September 2025
```

And reference the methodology paper:
- [STATISTICAL_METHODOLOGY_COMPARISON.md](docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Follow the coding guidelines in [.cursorrules](.cursorrules)
2. Add tests for new features
3. Update documentation
4. Run test suite before submitting

---

## 📜 License

[Specify your license here]

---

## 🙏 Acknowledgments

- Original Optimum DCA Excel strategy concept
- Statistical methodology based on quantitative finance best practices
- Bootstrap resampling implementation based on Efron & Tibshirani (1993)

---

## 📞 Support

**Documentation**:
- Tool Selection: [docs/guides/ANALYSIS_TOOL_GUIDE.md](docs/guides/ANALYSIS_TOOL_GUIDE.md)
- Statistics: [docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md](docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md)
- Project Structure: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

**Reports**:
- Comprehensive Comparison: `reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT.txt`
- Method Comparison: `reports/comparisons/method_comparison_summary.csv`

---

**Version**: 2.1.0  
**Last Updated**: September 30, 2025  
**Recommended Tool**: `balanced_rolling_analyzer.py` ⭐ (now with monthly rolling)  
**Key Insight**: No significant difference - choose based on YOUR risk tolerance!
