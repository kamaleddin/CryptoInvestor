# 📊 Reports Guide - Where to Find Everything

## 🎯 **NEW v2.1 Reports** (Monthly Rolling - Optimized)

### **Main Comprehensive Report** ⭐
**File**: `reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt`  
**What**: Complete comparison of all three methods with monthly (4-week) rolling  
**Size**: ~11 KB  
**Contains**:
- Duration Simulator (1,512 simulations)
- Balanced Rolling Monthly (378 simulations) ⭐ NEW
- Non-Overlapping (18 simulations)
- Full statistics for each duration
- Risk-adjusted metrics
- Statistical tests

**View**:
```bash
cat reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt
```

---

## 📁 **All Available Reports**

### Comparison Reports (`reports/comparisons/`)

| File | Version | Sims | Description |
|------|---------|------|-------------|
| **COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt** | **v2.1** | **378** | **Monthly rolling ⭐** |
| COMPREHENSIVE_COMPARISON_REPORT.txt | v2.0 | 120 | Quarterly rolling (old) |
| method_comparison_summary.csv | Updated | Various | Data table |

### Simulation Reports (`reports/simulations/`)

| File | Rows | Description |
|------|------|-------------|
| duration_simulation_detailed_report.csv | 1,512 | All weekly rolling simulations |
| duration_simulation_summary_report.txt | - | Summary statistics |
| top_investment_opportunities.csv | 80 | Best performing periods |

---

## 🔍 **What's in Each Report**

### COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt
```
✅ Executive Summary
✅ 1-Year Duration Comparison
   - Balanced Rolling (Monthly): 114 sims
   - Non-Overlapping: 9 sims
   - Full statistics, risk metrics, tests
✅ 2-Year Duration Comparison
   - Balanced Rolling (Monthly): 101 sims
   - Non-Overlapping: 4 sims
✅ 3-Year Duration Comparison
   - Balanced Rolling (Monthly): 88 sims
   - Non-Overlapping: 3 sims
✅ 4-Year Duration Comparison
   - Balanced Rolling (Monthly): 75 sims
   - Non-Overlapping: 2 sims
✅ Key Findings & Recommendations
```

### duration_simulation_detailed_report.csv
```
1,512 rows × 17 columns
- duration, start_date, end_date
- optimum/simple: btc, investment, value, profit, return_pct
- outperformance_pct, outperformance_ratio
```

### method_comparison_summary.csv
```
Tabular comparison of all methods
- Sample sizes
- Mean/median returns
- P-values, effect sizes
- Sharpe ratios
```

---

## 📊 **Key Differences: v2.0 vs v2.1**

| Aspect | v2.0 (Old) | v2.1 (New) | Improvement |
|--------|------------|------------|-------------|
| **Rolling Step** | 13 weeks | **4 weeks** | Optimized |
| **Total Sims** | 120 | **378** | **+215%** |
| **1-Year Sims** | 36 | **114** | +217% |
| **Power** | 35% | **90%** | +157% |
| **CI Width** | ±243% | **±75%** | 3.2x narrower |

---

## 🚀 **How to Generate Reports**

### Generate All Reports
```bash
# 1. Duration simulator (1,512 sims)
python tools/duration_simulator.py

# 2. Comprehensive comparison (includes monthly rolling)
python tools/comprehensive_comparison.py

# 3. Quarterly vs Monthly comparison (NEW)
python tools/compare_quarterly_vs_monthly.py
```

### View Specific Reports
```bash
# Main v2.1 report (recommended)
cat reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt

# Quarterly vs monthly comparison
python tools/compare_quarterly_vs_monthly.py

# Detailed simulation data
head -20 reports/simulations/duration_simulation_detailed_report.csv
```

---

## 📚 **Documentation**

To understand the reports:
- `docs/guides/ANALYSIS_TOOL_GUIDE.md` - Which tool to use
- `docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md` - Statistics
- `docs/SAMPLE_SIZE_OPTIMIZATION.md` - Why monthly is better
- `V2.1_UPDATE.md` - What changed in v2.1

---

## 🎯 **Recommended Reading Order**

1. **Start**: `reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt`
2. **Understand**: `V2.1_UPDATE.md`
3. **Deep Dive**: `docs/SAMPLE_SIZE_OPTIMIZATION.md`
4. **Compare**: Run `python tools/compare_quarterly_vs_monthly.py`

---

**Version**: 2.1.0  
**Generated**: September 30, 2025  
**Key Update**: Monthly rolling (378 sims) now default ⭐
