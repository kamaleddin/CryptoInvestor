# 📚 Documentation Index - v2.1

Complete guide to all documentation in the CryptoInvestor project.

---

## 🚀 **Start Here**

1. **README.md** - Main project overview and quick start
2. **QUICK_REFERENCE.md** - Quick commands and common tasks
3. **REPORTS_GUIDE.md** - Where to find all reports

---

## 📊 **Core Documentation**

### Getting Started
| Document | Purpose |
|----------|---------|
| **README.md** | Main project documentation |
| **QUICK_REFERENCE.md** | Quick commands cheat sheet |
| **PROJECT_STRUCTURE.md** | Complete project organization |

### Version History
| Document | Purpose |
|----------|---------|
| **V2.1_UPDATE.md** | What's new in v2.1 (monthly rolling optimization) |
| **RESTRUCTURE_SUMMARY.md** | v2.0 project restructure details |
| **IMPLEMENTATION_COMPLETE.md** | v2.0 deliverables summary |

### Reports
| Document | Purpose |
|----------|---------|
| **REPORTS_GUIDE.md** | Where all reports are located |
| **reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt** | Main analysis report ⭐ |
| **reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT.txt** | Old v2.0 report (deprecated) |

---

## 📖 **User Guides** (`docs/guides/`)

| Document | Purpose |
|----------|---------|
| **ANALYSIS_TOOL_GUIDE.md** | Which tool to use when (decision tree) |
| **DURATION_SIMULATION_README.md** | Duration simulation results explained |

---

## 🔬 **Technical Documentation** (`docs/methodology/`)

| Document | Purpose |
|----------|---------|
| **STATISTICAL_METHODOLOGY_COMPARISON.md** | Deep dive into statistical methods |
| **SAMPLE_SIZE_OPTIMIZATION.md** | Why monthly rolling is optimal |

---

## 🧪 **Testing & Validation** (`docs/`)

| Document | Purpose |
|----------|---------|
| **TEST_SUMMARY.md** | Test suite documentation |
| **analysis_report.md** | Historical Excel validation report |

---

## 📁 **Project Organization**

```
Documentation Structure:
├── Root Level (Getting Started)
│   ├── README.md                 ⭐ START HERE
│   ├── QUICK_REFERENCE.md        Quick commands
│   ├── REPORTS_GUIDE.md          Where to find reports
│   └── PROJECT_STRUCTURE.md      Complete organization
│
├── Version History
│   ├── V2.1_UPDATE.md            Latest changes
│   ├── RESTRUCTURE_SUMMARY.md    v2.0 changes
│   └── IMPLEMENTATION_COMPLETE.md v2.0 summary
│
├── docs/guides/ (User Guides)
│   ├── ANALYSIS_TOOL_GUIDE.md    Tool selection
│   └── DURATION_SIMULATION_README.md
│
├── docs/methodology/ (Technical)
│   ├── STATISTICAL_METHODOLOGY_COMPARISON.md
│   └── SAMPLE_SIZE_OPTIMIZATION.md
│
└── docs/ (Testing & Historical)
    ├── TEST_SUMMARY.md
    └── analysis_report.md
```

---

## 🎯 **Documentation by Use Case**

### "I just want to run an analysis"
1. Read: `QUICK_REFERENCE.md`
2. Run: `python tools/balanced_rolling_analyzer.py`
3. View: `reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt`

### "Which tool should I use?"
1. Read: `docs/guides/ANALYSIS_TOOL_GUIDE.md`
2. Decision tree and recommendations

### "I want to understand the statistics"
1. Read: `docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md`
2. Then: `docs/SAMPLE_SIZE_OPTIMIZATION.md`

### "What changed in v2.1?"
1. Read: `V2.1_UPDATE.md`
2. Compare: Run `python tools/compare_quarterly_vs_monthly.py`

### "Where are the reports?"
1. Read: `REPORTS_GUIDE.md`
2. Main report: `reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt`

### "How is the project organized?"
1. Read: `PROJECT_STRUCTURE.md`
2. Complete directory structure and file inventory

---

## 📝 **Deprecated/Archived**

| Document | Status | Replacement |
|----------|--------|-------------|
| `README_v1_ARCHIVED.md` | Archived | `README.md` (v2.1) |
| `reports/.../COMPREHENSIVE_COMPARISON_REPORT.txt` | Deprecated | `..._v2.1.txt` |

---

## 🔄 **Keeping Documentation Updated**

### When to Update Which Files

**Made code changes**:
- Update `PROJECT_STRUCTURE.md` if directory structure changed
- Update `README.md` with new features
- Update relevant guide in `docs/guides/`

**Changed analysis methodology**:
- Add version update doc (like `V2.1_UPDATE.md`)
- Update `STATISTICAL_METHODOLOGY_COMPARISON.md`
- Regenerate reports

**Added new tool**:
- Update `ANALYSIS_TOOL_GUIDE.md`
- Update `QUICK_REFERENCE.md`
- Update `README.md`

---

## 📊 **Documentation Statistics**

| Category | Count | Location |
|----------|-------|----------|
| Root Documentation | 7 | `/` |
| User Guides | 2 | `docs/guides/` |
| Technical Docs | 2 | `docs/methodology/` |
| Test Docs | 2 | `docs/` |
| Reports | 3 | `reports/comparisons/` |
| **Total** | **16** | Various |

---

## 🎯 **Quick Links**

```bash
# View main documentation
cat README.md
cat QUICK_REFERENCE.md

# View latest report
cat reports/comparisons/COMPREHENSIVE_COMPARISON_REPORT_v2.1.txt

# Understand tool selection
cat docs/guides/ANALYSIS_TOOL_GUIDE.md

# Learn the statistics
cat docs/methodology/STATISTICAL_METHODOLOGY_COMPARISON.md

# What changed
cat V2.1_UPDATE.md
```

---

**Last Updated**: September 30, 2025  
**Version**: 2.1.0  
**Total Documentation Files**: 16  
**Status**: Current and Complete ✅
