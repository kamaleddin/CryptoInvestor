# 🚀 CryptoInvestor - DCA Strategy Analysis Suite v2.0

A comprehensive cryptocurrency investment analysis toolkit implementing and comparing multiple Dollar Cost Averaging (DCA) strategies with **statistically rigorous** performance evaluation.

> **v2.0 Update**: Now includes three analysis methodologies with proper statistical testing, risk-adjusted metrics, and comprehensive reporting. See [What's New](#-whats-new-in-v20) below.

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

### ⚠️ **Statistical Reality**

Using proper statistical methods (non-overlapping periods):

- **No statistically significant difference** between Optimum and Simple DCA (p > 0.05 for all durations)
- Weekly rolling results are **misleading** due to 98% autocorrelation
- Methodology choice **dramatically affects conclusions**

### 🏆 **Performance Summary** (Quarterly Rolling - Recommended)

| Duration | Optimum Avg | Simple Avg | Winner (Risk-Adj) | P-Value |
|----------|-------------|------------|-------------------|---------|
| 1-Year | 272.34% | 65.58% | Simple (Sharpe: 0.495) | 0.38 ❌ |
| 2-Year | 149.45% | 159.50% | Optimum (Sharpe: 0.397) | 0.88 ❌ |
| 3-Year | 243.81% | 165.98% | Simple (Sharpe: 0.568) | 0.17 ❌ |
| 4-Year | 162.27% | 233.33% | Simple (Sharpe: 0.610) | 0.62 ❌ |

❌ = Not statistically significant

### 💡 **Practical Insights**

**Optimum DCA Advantages:**
- ✅ Better downside protection (Sortino ratio)
- ✅ Superior tail risk metrics (lower VaR, CVaR)
- ✅ Higher upside potential in bull markets

**Simple DCA Advantages:**
- ✅ Better risk-adjusted returns (Sharpe ratio)
- ✅ More consistent performance
- ✅ 100% win rate over 2+ years (non-overlapping data)
- ✅ Lower volatility

**Recommendation**: Choice depends on risk tolerance and investment horizon.

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

**See**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete details.

---

## 🔬 Analysis Tools Comparison

| Tool | Simulations | Independence | Risk Metrics | Best For |
|------|-------------|--------------|--------------|----------|
| **Duration Simulator** | 1,512 | ❌ Low (~2%) | ❌ No | Pattern exploration |
| **Balanced Rolling** ⭐ | 120 | ⚠️ Moderate (~40%) | ✅ Yes | Standard analysis |
| **Advanced Non-Overlapping** | 18 | ✅ Perfect (100%) | ✅ Yes | Academic rigor |

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
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Complete project organization |
| [ANALYSIS_TOOL_GUIDE.md](docs/guides/ANALYSIS_TOOL_GUIDE.md) | Which tool to use when |
| [STATISTICAL_METHODOLOGY_COMPARISON.md](docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md) | Statistical methods explained |
| [DURATION_SIMULATION_README.md](docs/guides/DURATION_SIMULATION_README.md) | Simulation results |
| [TEST_SUMMARY.md](docs/TEST_SUMMARY.md) | Test documentation |
| [.cursorrules](.cursorrules) | Development guidelines |

---

## 🆕 What's New in v2.0

### Statistical Rigor
- ✅ **Three analysis methodologies** (overlapping, quarterly, non-overlapping)
- ✅ **Risk-adjusted metrics** (Sharpe, Sortino, Calmar ratios)
- ✅ **Statistical testing** (t-tests, Mann-Whitney U, effect sizes)
- ✅ **Confidence intervals** (bootstrap resampling)
- ✅ **Distribution analysis** (skewness, kurtosis, normality tests)
- ✅ **Tail risk analysis** (VaR, CVaR, maximum drawdown)

### Improved Reporting
- ✅ **Comprehensive comparison report** across all methodologies
- ✅ **Organized output structure** (reports/ directory)
- ✅ **Method comparison CSV** for easy analysis
- ✅ **Statistical methodology paper** explaining approaches

### Better Project Structure
- ✅ **Reorganized directories** following Python best practices
- ✅ **Separated reports** from code
- ✅ **Comprehensive documentation** with guides and methodology papers
- ✅ **Clear tool selection guidance**

### Key Insights
- ⚠️ **Original weekly rolling results were statistically invalid** (high autocorrelation)
- ✅ **Proper analysis shows no significant difference** between strategies
- ✅ **Choice depends on risk tolerance** and investment horizon
- ✅ **Methodology matters** - different approaches give different conclusions

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
- Project Structure: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

**Reports**:
- Comprehensive Comparison: `reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT.txt`
- Method Comparison: `reports/comparisons/method_comparison_summary.csv`

---

**Version**: 2.0.0  
**Last Updated**: September 30, 2025  
**Recommended Tool**: `balanced_rolling_analyzer.py` ⭐  
**Key Insight**: Methodology matters - use proper statistical methods!
