# 🚀 CryptoInvestor v2.0 - Quick Reference Card

## ⚡ Most Common Commands

### Run Analysis
```bash
# RECOMMENDED (quarterly rolling, risk metrics)
python tools/balanced_rolling_analyzer.py

# Exploration (1,512 simulations)
python tools/duration_simulator.py

# Academic rigor (non-overlapping)
python tools/advanced_duration_analyzer.py

# Compare all methods
python tools/comprehensive_comparison.py
```

### View Results
```bash
# Main comparison
cat reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT.txt

# Quick summary
cat reports/simulations/duration_simulation_summary_report.txt

# Data table (open in Excel)
open reports/comparisons/method_comparison_summary.csv
```

### Read Docs
```bash
# Which tool to use?
cat docs/guides/ANALYSIS_TOOL_GUIDE.md

# Statistics explained
cat docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md

# Project organization
cat PROJECT_STRUCTURE.md
```

---

## 📊 Three Analysis Methods

| Tool | When to Use | Simulations | Independence |
|------|-------------|-------------|--------------|
| `duration_simulator.py` | Explore patterns | 1,512 | ❌ Low |
| `balanced_rolling_analyzer.py` ⭐ | Standard analysis | 120 | ⚠️ Good |
| `advanced_duration_analyzer.py` | Academic/regulatory | 18 | ✅ Perfect |

---

## 🎯 Decision Tree

```
What do you need?

├─ Find best historical periods?
│  └─ Use: duration_simulator.py
│
├─ Standard investment analysis?
│  └─ Use: balanced_rolling_analyzer.py ⭐
│
├─ Academic paper/regulatory filing?
│  └─ Use: advanced_duration_analyzer.py
│
└─ Compare all approaches?
   └─ Use: comprehensive_comparison.py
```

---

## 📁 File Locations

### Tools
- `tools/balanced_rolling_analyzer.py` ⭐ RECOMMENDED
- `tools/duration_simulator.py`
- `tools/advanced_duration_analyzer.py`
- `tools/comprehensive_comparison.py`

### Reports
- `reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT.txt`
- `reports/comparisons/method_comparison_summary.csv`
- `reports/simulations/duration_simulation_summary_report.txt`

### Documentation
- `docs/guides/ANALYSIS_TOOL_GUIDE.md` - Tool selection
- `docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md` - Statistics
- `PROJECT_STRUCTURE.md` - Organization
- `RESTRUCTURE_SUMMARY.md` - What changed

---

## 🔬 Key Metrics Explained

| Metric | What It Measures | Higher = Better? |
|--------|------------------|------------------|
| **Sharpe Ratio** | Return per unit of total risk | ✅ Yes |
| **Sortino Ratio** | Return per unit of downside risk | ✅ Yes |
| **Max Drawdown** | Worst peak-to-trough decline | ❌ No (lower better) |
| **VaR (95%)** | Max loss at 95% confidence | ❌ No (higher better, less negative) |
| **CVaR (95%)** | Average loss in worst 5% | ❌ No (higher better, less negative) |
| **P-value** | Statistical significance | < 0.05 = significant |

---

## 🎯 Main Finding

**No statistically significant difference** between Optimum and Simple DCA when using proper methods!

- Weekly rolling (misleading): "Optimum wins" ❌
- Quarterly rolling (valid): "No difference" (p=0.38) ✅
- Non-overlapping (rigorous): "No difference" (p=0.83) ✅

**Choice depends on**: Risk tolerance + Investment horizon

---

## ⚙️ Installation

```bash
# Core dependencies
pip install -r requirements/base.txt

# New in v2.0
pip install scipy
```

---

## 🧪 Testing

```bash
# Run all tests
python scripts/run_tests.py

# With coverage
python scripts/run_tests.py --coverage
```

---

## 📞 Need Help?

1. **Tool selection**: `cat docs/guides/ANALYSIS_TOOL_GUIDE.md`
2. **Statistics**: `cat docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md`
3. **Project layout**: `cat PROJECT_STRUCTURE.md`
4. **What changed**: `cat RESTRUCTURE_SUMMARY.md`

---

**Version**: 2.0.0  
**Date**: September 30, 2025  
**Status**: Production Ready ✅
