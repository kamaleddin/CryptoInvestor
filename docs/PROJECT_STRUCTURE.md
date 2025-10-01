# CryptoInvestor Project Structure

## 📁 Directory Organization

```
CryptoInvestor/
│
├── 📊 src/                          # Core implementation
│   ├── __init__.py
│   └── optimum_dca_analyzer.py      # Main DCA analyzer (standalone)
│
├── 🔧 tools/                        # Analysis tools
│   ├── duration_simulator.py        # Weekly rolling simulator (1,512 simulations)
│   ├── balanced_rolling_analyzer.py # Quarterly rolling (recommended) ⭐
│   ├── advanced_duration_analyzer.py # Statistical rigor (non-overlapping)
│   ├── comprehensive_comparison.py  # Compare all three methods
│   ├── analyze_simulation_results.py # Explore simulation data
│   └── excel_validator.py          # Excel validation tool
│
├── 📊 reports/                      # Generated reports & outputs
│   ├── simulations/                 # Simulation outputs
│   │   ├── duration_simulation_detailed_report.csv
│   │   ├── duration_simulation_summary_report.txt
│   │   └── top_investment_opportunities.csv
│   ├── comparisons/                 # Method comparisons
│   │   ├── COMPREHENSIVE_COMPARISON_REPORT.txt
│   │   └── method_comparison_summary.csv
│   └── analysis/                    # Custom analysis reports
│
├── 📚 docs/                         # Documentation
│   ├── guides/                      # User guides
│   │   ├── ANALYSIS_TOOL_GUIDE.md   # Which tool to use
│   │   └── DURATION_SIMULATION_README.md
│   ├── methodology/                 # Technical documentation
│   │   └── STATISTICAL_METHODOLOGY_COMPARISON.md
│   └── TEST_SUMMARY.md             # Test documentation
│
├── 🧪 tests/                        # Test suite (pytest)
│   ├── __init__.py
│   └── test_dca_analyzer.py        # Comprehensive tests (21 tests)
│
├── 🚀 scripts/                      # Automation scripts
│   ├── __init__.py
│   └── run_tests.py                # Test runner
│
├── 💡 examples/                     # Usage examples
│   └── quick_start.py              # Simple usage example
│
├── 📦 requirements/                 # Dependencies
│   ├── base.txt                    # Core dependencies
│   ├── test.txt                    # Testing dependencies
│   └── dev.txt                     # Development dependencies
│
├── 📖 reference/                    # Reference materials
│   ├── legacy_optimum_dca.py       # Original Excel-dependent version
│   └── Optimum DCA.xlsx            # Excel reference file for validation
│
├── 💾 data/                         # Data files
│   └── bitcoin_prices.csv          # Historical Bitcoin prices
│
├── ⚙️  Configuration Files
│   ├── pyproject.toml              # Modern Python project config
│   ├── pytest.ini                  # Pytest configuration
│   ├── .cursorrules                # Development guidelines
│   └── README.md                   # Main project README
│
└── 📋 This File
    └── PROJECT_STRUCTURE.md         # Project organization guide
```

---

## 🎯 Quick Start

### Run Analysis (Choose One)

```bash
# 1. RECOMMENDED: Balanced approach (quarterly rolling)
python tools/balanced_rolling_analyzer.py

# 2. Exploration: Maximum data (weekly rolling) 
python tools/duration_simulator.py

# 3. Academic rigor: Non-overlapping periods
python tools/advanced_duration_analyzer.py

# 4. Compare all three methods
python tools/comprehensive_comparison.py
```

### View Results

```bash
# Main comparison report
cat reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT.txt

# Simulation details
cat reports/simulations/duration_simulation_summary_report.txt

# Method comparison data
open reports/comparisons/method_comparison_summary.csv
```

### Read Documentation

```bash
# Which tool should I use?
cat docs/guides/ANALYSIS_TOOL_GUIDE.md

# Understanding the statistics
cat docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md

# Simulation results explained
cat docs/guides/DURATION_SIMULATION_README.md
```

---

## 📊 Core Components

### 1. **Main Implementation** (`src/`)

**File**: `optimum_dca_analyzer.py`
- Standalone DCA analyzer
- Supports custom date ranges and budgets
- No Excel dependencies
- Validated against test case (462.1% return)

**Usage**:
```python
from src.optimum_dca_analyzer import FlexibleOptimumDCA

analyzer = FlexibleOptimumDCA(
    weekly_budget=250.0,
    start_date=date(2022, 1, 10),
    end_date=date(2025, 9, 22)
)

results = analyzer.run_optimum_dca_simulation()
```

---

### 2. **Analysis Tools** (`tools/`)

#### 🔧 **duration_simulator.py**
- **Simulations**: 1,512 (weekly rolling)
- **Effective Independence**: ~30 periods
- **Best For**: Pattern exploration, finding best periods
- **NOT For**: Statistical inference (high autocorrelation)

#### ⭐ **balanced_rolling_analyzer.py** (RECOMMENDED)
- **Simulations**: 120 (quarterly rolling)
- **Effective Independence**: ~48 periods
- **Best For**: Standard analysis with risk metrics
- **Features**: Sharpe, Sortino, VaR, CVaR, statistical tests

#### 🎓 **advanced_duration_analyzer.py**
- **Simulations**: 18 (non-overlapping)
- **Effective Independence**: 18 periods (perfect)
- **Best For**: Academic rigor, regulatory submissions
- **Features**: Full statistical test suite, bootstrap CIs

#### 📊 **comprehensive_comparison.py**
- Runs all three methods
- Generates comparison report
- Shows how methodology affects conclusions

#### 🔍 **analyze_simulation_results.py**
- Explore simulation data
- Find best/worst periods
- Analyze by year, market conditions

---

### 3. **Reports** (`reports/`)

All generated outputs organized by type:

- **simulations/**: Raw simulation results
- **comparisons/**: Method comparison reports  
- **analysis/**: Custom analysis outputs

**Key Files**:
- `COMPREHENSIVE_COMPARISON_REPORT.txt`: Master comparison
- `method_comparison_summary.csv`: Summary data
- `duration_simulation_detailed_report.csv`: All 1,512 runs

---

### 4. **Documentation** (`docs/`)

#### **Guides** (`docs/guides/`)
- **ANALYSIS_TOOL_GUIDE.md**: Decision tree for tool selection
- **DURATION_SIMULATION_README.md**: Simulation results explained

#### **Methodology** (`docs/methodology/`)
- **STATISTICAL_METHODOLOGY_COMPARISON.md**: Deep dive into statistics
  - Autocorrelation issues
  - Risk-adjusted metrics
  - Statistical significance testing
  - Bootstrap confidence intervals

---

## 🔬 Understanding the Three Approaches

### Comparison Matrix

| Aspect | Duration Simulator | Balanced Rolling | Non-Overlapping |
|--------|-------------------|------------------|-----------------|
| **Simulations** | 1,512 | 120 | 18 |
| **Independence** | ❌ Low (~2%) | ⚠️ Moderate (~40%) | ✅ Perfect (100%) |
| **Sample Size** | ✅ Large | ✅ Good | ❌ Small |
| **Risk Metrics** | ❌ No | ✅ Yes | ✅ Yes |
| **Statistical Tests** | ❌ Invalid | ✅ Valid | ✅ Valid |
| **Best Use** | Exploration | Standard Analysis | Academic |
| **Recommendation** | 🔍 Explore | ⭐ Default | 🎓 Validate |

### Which to Use?

```
Need to explore patterns? 
  → duration_simulator.py

Standard investment analysis?
  → balanced_rolling_analyzer.py ⭐

Publishing academic paper?
  → advanced_duration_analyzer.py

Want to compare all methods?
  → comprehensive_comparison.py
```

---

## 🧪 Testing

```bash
# Run all tests
python scripts/run_tests.py

# Run with coverage
python scripts/run_tests.py --coverage

# Run specific test categories
python scripts/run_tests.py --validation
python scripts/run_tests.py --unit
python scripts/run_tests.py --performance
```

---

## 📦 Installation

```bash
# Core dependencies
pip install -r requirements/base.txt

# Testing dependencies
pip install -r requirements/test.txt

# All development dependencies
pip install -r requirements/dev.txt

# Install in development mode
pip install -e .
```

---

## 🎯 Key Findings Summary

### Statistical Reality
- ❌ **No statistically significant difference** between Optimum and Simple DCA
- Weekly rolling results are **misleading** due to autocorrelation
- Proper analysis shows **context-dependent** performance

### Risk-Adjusted Performance
- **Simple DCA**: Better Sharpe ratios (total risk-adjusted)
- **Optimum DCA**: Better Sortino ratios (downside risk-adjusted)
- **Optimum DCA**: Better tail risk protection (VaR, CVaR)

### Practical Recommendations
- **1-2 Years**: Optimum if you tolerate volatility
- **3-4 Years**: Simple for consistency
- **Risk-Averse**: Simple DCA
- **Risk-Tolerant**: Optimum DCA

---

## 📝 File Naming Conventions

- **Analysis Tools**: `*_analyzer.py`, `*_simulator.py`
- **Reports**: `UPPERCASE_REPORT.txt/md`
- **Data**: `lowercase_with_underscores.csv`
- **Documentation**: `UPPERCASE_GUIDE.md`

---

## 🔄 Workflow Examples

### Standard Analysis Workflow

```bash
# 1. Run recommended analysis
python tools/balanced_rolling_analyzer.py > reports/analysis/my_analysis.txt

# 2. View results
cat reports/analysis/my_analysis.txt

# 3. Read interpretation guide
cat docs/guides/ANALYSIS_TOOL_GUIDE.md
```

### Research Workflow

```bash
# 1. Explore patterns
python tools/duration_simulator.py

# 2. Rigorous analysis
python tools/balanced_rolling_analyzer.py

# 3. Validate findings
python tools/advanced_duration_analyzer.py

# 4. Compare all methods
python tools/comprehensive_comparison.py

# 5. Review methodology
cat docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md
```

### Custom Analysis

```python
# Use the core analyzer for custom periods
from src.optimum_dca_analyzer import FlexibleOptimumDCA
from datetime import date

analyzer = FlexibleOptimumDCA(
    weekly_budget=500.0,  # Custom budget
    start_date=date(2020, 1, 1),
    end_date=date(2023, 12, 31)
)

optimum = analyzer.run_optimum_dca_simulation()
simple = analyzer.run_simple_dca_simulation()

print(f"Optimum: {optimum['profit_pct']:.2f}%")
print(f"Simple: {simple['profit_pct']:.2f}%")
```

---

## 🚀 Development

### Adding New Analysis

1. Create tool in `tools/`
2. Generate reports to `reports/analysis/`
3. Document in `docs/guides/`
4. Add tests in `tests/`

### Modifying Core

1. Edit `src/optimum_dca_analyzer.py`
2. Run tests: `python scripts/run_tests.py`
3. Validate: `python tools/excel_validator.py`
4. Update docs in `docs/`

---

## 📖 Documentation Index

| Document | Location | Purpose |
|----------|----------|---------|
| Main README | `README.md` | Project overview |
| This Guide | `PROJECT_STRUCTURE.md` | Directory structure |
| Tool Selection | `docs/guides/ANALYSIS_TOOL_GUIDE.md` | Which tool to use |
| Statistics | `docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md` | Statistical methods |
| Simulation Results | `docs/guides/DURATION_SIMULATION_README.md` | Simulation findings |
| Test Summary | `docs/TEST_SUMMARY.md` | Test documentation |
| Development Rules | `.cursorrules` | Coding guidelines |

---

## 🎓 Best Practices

### For Analysis
1. **Start with balanced_rolling_analyzer.py** (recommended)
2. Use duration_simulator.py for exploration only
3. Validate important findings with advanced_duration_analyzer.py
4. Always report methodology used

### For Reporting
1. Include sample size and independence level
2. Report both raw and risk-adjusted metrics
3. Use confidence intervals, not just point estimates
4. State statistical significance with p-values

### For Development
1. Run tests before committing
2. Update documentation with code changes
3. Follow naming conventions
4. Keep reports organized in `reports/`

---

## 📞 Quick Reference

```bash
# Analysis
python tools/balanced_rolling_analyzer.py              # Default analysis
python tools/comprehensive_comparison.py               # Compare methods

# Reports  
cat reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT.txt
open reports/comparisons/method_comparison_summary.csv

# Documentation
cat docs/guides/ANALYSIS_TOOL_GUIDE.md                # Tool selection
cat docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md  # Statistics

# Testing
python scripts/run_tests.py                           # Run tests
python tools/excel_validator.py                       # Validate accuracy
```

---

**Last Updated**: September 30, 2025  
**Project Version**: 2.0 (Restructured with statistical rigor)  
**Recommended Tool**: `balanced_rolling_analyzer.py`
