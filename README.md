# 🚀 CryptoInvestor - Optimum DCA Strategy Implementation

A powerful cryptocurrency investment tool that implements an advanced Dollar Cost Averaging (DCA) strategy based on market volatility and technical analysis. This tool replicates and enhances the "Optimum DCA" Excel strategy, delivering **462% returns vs 209% for Simple DCA** during the 2022-2025 period.

## ✨ Key Features

- **🎯 Advanced DCA Strategy**: Market-timing based on VWAP bands and volatility
- **📊 Multiple Strategy Comparison**: Optimum DCA vs Simple DCA vs Buy & HODL
- **💯 Standalone Implementation**: No Excel dependency required
- **🔬 Backtesting**: Historical performance analysis from 2022-2025
- **📈 Proven Results**: 462.1% return (vs 209.4% Simple DCA, 177.8% Buy & HODL)

## 🚀 Quick Start

### Installation & Usage

1. **Clone the repository**:
```bash
git clone <repository-url>
cd CryptoInvestor
```

2. **Install dependencies**:
```bash
pip install pandas numpy openpyxl
```

3. **Run the analysis**:
```bash
# Quick start example
python examples/quick_start.py

# Or run the main analyzer directly
python src/optimum_dca_analyzer.py
```

### Expected Output

```
🎯 OPTIMUM DCA:
   Total BTC: 2.26483845
   Investment: $46,806.51
   Value: $263,077.09
   Return: 462.1% ✅

🎯 SIMPLE DCA:
   Total BTC: 1.29177345
   Investment: $48,500.00
   Value: $150,048.67
   Return: 209.4% ✅
```

## 📁 Key Files

## 📂 Project Structure

```
CryptoInvestor/
├── src/                               # 💻 Source code
│   └── optimum_dca_analyzer.py        #     Main DCA implementation
├── tools/                             # 🔧 Utility tools  
│   └── excel_validator.py             #     Excel validation tool
├── data/                              # 📊 Data files
│   └── bitcoin_prices.csv             #     Historical Bitcoin prices
├── docs/                              # 📚 Documentation
│   └── analysis_report.md             #     Comprehensive analysis
├── reference/                         # 📋 Reference materials
│   ├── excel_file.xlsx                #     Original Excel strategy
│   └── legacy_implementation.py       #     Legacy code
├── examples/                          # 🎯 Usage examples
│   └── quick_start.py                 #     Simple usage example
├── README.md                          # 📖 Main documentation
└── .cursorrules                       # 🧭 Development guidelines
```

| File | Purpose |
|------|---------|
| `src/optimum_dca_analyzer.py` | **Main implementation** - Standalone DCA analysis |
| `examples/quick_start.py` | **Quick start** - Simple usage example |
| `data/bitcoin_prices.csv` | **Data source** - Historical Bitcoin prices (only dependency) |
| `docs/analysis_report.md` | **Analysis report** - Comprehensive results and insights |
| `tools/excel_validator.py` | **Validation tool** - Compares against Excel reference |
| `reference/legacy_implementation.py` | **Legacy code** - Original complex implementation |
| `reference/excel_file.xlsx` | **Reference Excel** - Original strategy implementation |

## 🎯 How It Works

The Optimum DCA strategy uses sophisticated market timing:

1. **VWAP Analysis**: 14-week Volume Weighted Average Price calculation
2. **Volatility Bands**: 2σ, 3σ, 4σ bands around VWAP for entry/exit signals
3. **Dynamic Allocation**: 2x-4x multipliers during market dips, selling during peaks
4. **Market Timing**: Counter-cyclical investing based on technical indicators

### Strategy Logic

```
Investment Amount = (Investment Multiple + Buy/Sell Multiplier) × $250

Where:
- Buy signals: Price < VWAP bands → 2x, 3x, 4x multipliers
- Sell signals: Price > VWAP bands → Negative multipliers (selling)
- Neutral: Price within normal range → 1x multiplier
```

## 📊 Performance Summary

**Period**: January 10, 2022 - September 22, 2025 (194 weeks)

| Strategy | Return | Total BTC | Investment | Final Value |
|----------|--------|-----------|------------|-------------|
| **Optimum DCA** | **462.1%** | 2.26 | $46,807 | $263,077 |
| Simple DCA | 209.4% | 1.29 | $48,500 | $150,049 |
| Buy & HODL | 177.8% | 1.24 | $52,000 | $144,443 |

**Key Insight**: Optimum DCA delivered **2.2x better returns** than Simple DCA by buying aggressively during market downturns and selling during peaks.

## 🔧 Configuration

Modify key parameters in `src/optimum_dca_analyzer.py`:

```python
# Investment settings
weekly_budget = 250.0      # Weekly investment amount
total_capital = 52000.0    # Total available capital

# Period settings  
START_DATE = date(2022, 1, 10)  # Analysis start date
END_DATE = date(2025, 9, 22)    # Analysis end date
```

## 📖 Technical Documentation

For detailed technical documentation, implementation details, and Excel mapping, see below:

---

# Optimum DCA — Excel ↔ Python Mapping & Test Plan

This document explains how the Python implementation in `optimum_dca.py` mirrors the spreadsheet logic, and how to validate it by comparing against CSVs exported from Excel.

## Contents
- [1. Files](#1-files)
- [2. Inputs & Outputs](#2-inputs--outputs)
- [3. Excel → Python Mapping](#3-excel--python-mapping)
  - [3.1 Weekly Price table](#31-weekly-price-table)
  - [3.2 WDCA (20222023 WDCA sheet)](#32-wdca-20222023-wdca-sheet)
- [4. Configuration & Assumptions](#4-configuration--assumptions)
- [5. Validation Workflow](#5-validation-workflow)
  - [5.1 Export expected CSVs from Excel](#51-export-expected-csvs-from-excel)
  - [5.2 Run Python to compute results](#52-run-python-to-compute-results)
  - [5.3 Compare with pytest](#53-compare-with-pytest)
- [6. Troubleshooting & Pitfalls](#6-troubleshooting--pitfalls)
- [Appendix A — Fixed Excel formula for J](#appendix-a--fixed-excel-formula-for-j)

---

## 1. Files

- **`optimum_dca.py`** — Standalone Python module implementing your workbook logic (no Excel dependency).
- **`tests/`** — Pytest suite to compare Python outputs to Excel CSV snapshots.
- **`data/`** — CSV snapshots exported from the workbook for validation.

Suggested layout:
```
project/
  optimum_dca.py
  tests/
    test_weekly_price.py
    test_wdca.py
  data/
    daily.csv (use bitcoin_prices.csv formatting is different)
    expected_weekly_price.csv
    expected_wdca.csv
```
> Export **values-only** CSVs with ISO dates (yyyy-mm-dd).

---

## 2. Inputs & Outputs

### Input (Python)
- **Daily price series**: DataFrame with columns
  - `date` (datetime or ISO date string)
  - `price` (float)
  - `daily_volume` (float; optional but recommended)

### Outputs (Python)
- **Weekly table** (replicates the `weekly price` sheet).
- **WDCA schedule** (replicates the `20222023 WDCA` sheet).

Produced via:
```python
import pandas as pd
from datetime import date
import optimum_dca

daily = pd.read_csv("data/daily.csv", parse_dates=["date"])

weekly, wdca = optimum_dca.run_optimum_dca(
    daily,
    start_date=date(2022, 1, 10),
    weeks=208,
    weekly_budget=50.0,
    today=date(2100, 1, 1),  # set > all anchors for deterministic tests
    j_logic="fixed",         # or "excel" to match the original workbook ordering
)
```

---

## 3. Excel → Python Mapping

### 3.1 Weekly Price table

**Sheet:** `weekly price`  
**Python:** `compute_weekly_table(daily, today, j_logic)`

| Excel | Name in sheet               | Python column         | Exact definition implemented |
|------:|-----------------------------|-----------------------|------------------------------|
| **A** | Date (Mondays)              | `date`                | Mondays from first Monday ≥ min(daily.date) to max(daily.date). |
| **B** | Weekly Close                | `weekly_close`        | If `today ∈ [A-7, A)`: latest available close; else exact close at `A`. |
| **C** | Weekly Volume               | `weekly_volume`       | Sum of `daily_volume` from `A-7` through `A-1`. |
| **D** | Weekly Volatility           | `weekly_return`       | `(B_n - B_{n-1}) / B_{n-1}`. |
| **E** | Weekly Variance             | `weekly_variance`     | `(D_n - T)^2`, `T` = mean of non-blank `D`. |
| **F** | 14 Week MA Volatility       | `rolling_vol`         | `STDEV.S`: **running** until row 14, then **14-week rolling**. |
| **G** | Weekly Weighted Volume      | `weighted_volume`     | `B_n * C_n`. |
| **H** | 14 Week VWAP MA             | `vwap_ma`             | `sum(G) / sum(C)`: running then 14-week rolling. |
| **M** | Lower 2σ                    | `lower_2sd`           | `H * (1 - 2F)`. |
| **N** | Upper 2σ                    | `upper_2sd`           | `H * (1 + 2F)`. |
| **O** | Lower 3σ                    | `lower_3sd`           | `H * (1 - 3F)`. |
| **P** | Upper 3σ                    | `upper_3sd`           | `H * (1 + 3F)`. |
| **Q** | Lower 4σ                    | `lower_4sd`           | `H * (1 - 4F)`. |
| **R** | Upper 4σ                    | `upper_4sd`           | `H * (1 + 4F)`. |
| **J** | Multiple calculation        | `multiple_calc`       | See two modes below. |
| **K** | Buy/Sell Multiplier         | `bs_multiplier`       | Discrete buckets from band zones. |
| **T** | AVG (of D)                  | `avg_return`          | Scalar repeated per row. |
| **U** | MIN (of D)                  | `min_return`          | Scalar repeated. |
| **V** | MAX (of D)                  | `max_return`          | Scalar repeated. |
| **W** | AVG VAR                     | `avg_variance`        | `sum(E)/count(E where B>0)`, repeated. |
| **X** | SD                          | `sd_global`           | `sqrt(W)`, repeated. |

**Weekly Close (B) exception**  
Excel: `IF(AND(TODAY()>=(A-7), A>TODAY()), latest close so far, exact close at A)`  
Tests: set `today` far in the future to avoid this branch.

**Multiple calculation (J)**

- **Workbook (original) ordering** — `j_logic="excel"` (keeps quirk):  
  Buy-side `<3σ` and `<4σ` branches are unreachable because they come after `<2σ`.
- **Fixed ordering** — `j_logic="fixed"` (default in code):
  ```text
  if B < Q:  J = 1 + (4*|D|) + (1+X) + F
  elif B < O: J = 1 + (3*|D|) + (1+X) + F
  elif B < M: J = 1 + (2*|D|) + (1+X) + F
  elif B > R: J = 1 - (4*|D|) - (1+X) - F
  elif B > P: J = 1 - (3*|D|) - (1+X) - F
  elif B > N: J = 1 - (2*|D|) - (1+X) - F
  else:       J = 1
  ```
  Where `B`=close, `D`=weekly return, `F`=rolling vol, `X`=global SD, and `M/N/O/P/Q/R` are VWAP ± (2/3/4)σ.

**Buy/Sell Multiplier (K)**  
- If `J=1` → blank.  
- If `J<0` (overbought): `-2` for `N < B < P`, `-3` for `P < B < R`, `-4` for `B > R`.  
- If `J>0` (oversold):  `+2` for `O < B < M`, `+3` for `Q < B < O`, `+4` for `B < Q`.

---

### 3.2 WDCA (20222023 WDCA sheet)

**Sheet:** `20222023 WDCA`  
**Python:** `compute_optimum_dca_schedule(weekly, start_date, weeks, weekly_budget)`

| Excel | Column label                      | Python column                 | Definition |
|------:|-----------------------------------|-------------------------------|------------|
| **A** | Trade Date                        | `trade_date`                  | `start_date + 7*i days`, i=0..weeks-1. |
| **B** | Week                              | `week`                        | 1-based week index. |
| **C** | BTC price                         | `btc_price`                   | Weekly close on that date (from weekly table). |
| **D** | Change from first day of Entry    | `pct_change_from_first`       | `(C_n - C_1)/C_1`. |
| **E** | Investment Multiple (Optimum)     | `investment_multiple_optimum` | If `D < -0.4`: `J - 2*D`; else `J - D`. |
| **F** | Buy/Sell Multiplier               | `buy_sell_multiplier`         | From weekly `K`. |
| **G** | Investment Amount (Optimum)       | `investment_amount_optimum`   | `(E + F) * weekly_budget`. |
| **H** | BTC units (Optimum)               | `btc_units_optimum`           | `G / C`. |
| **I** | Total Investment (Optimum)        | `total_investment_optimum`    | Cumulative sum of `G`. |
| **J** | Capital Balance (Optimum)         | `capital_balance_optimum`     | Week1: `TotalBudget - G1`; Week≥2: `J_{n-1} - G_{n-1}` (lagged). |
| **K** | Rolling Weekly P/L                | `rolling_weekly_pnl`          | `-((L - C)/L)`. |
| **L** | AVG buying price (Optimum)        | `avg_buy_price_optimum`       | `(sum G)/(sum H)`. |
| **M** | BTC units (Simple DCA)            | `btc_units_simple`            | `weekly_budget / C`. |
| **N** | Investment Amount (Simple DCA)    | `investment_amount_simple`    | `weekly_budget` (constant). |
| **O** | AVG buying price (Simple DCA)     | `avg_buy_price_simple`        | `(sum N)/(sum M)`. |

Right-panel parameters:
- Total Investment = `weeks * weekly_budget`  
- Reserve cap = `2 * sd_global` (from weekly `X`)  
- Total reserve = `Total Investment * Reserve cap` (kept for parity; not used downstream)

---

## 4. Configuration & Assumptions

- **`j_logic`**: `"fixed"` *(default)* for corrected J ordering; `"excel"` to mirror the original workbook logic.
- **Windowing**: F and H are **running** until the 14th populated row, then **14-week rolling** thereafter.
- **NaN / blanks**: Sums ignore NaNs; divide-by-zero → NaN. Coerce `#REF!`/`#N/A` to NaN when reading CSVs.
- **Deterministic tests**: Set `today` to a far-future date so the “current week” exception for B never triggers.

---

## 5. Validation Workflow

### 5.1 Export expected CSVs from Excel

1) **Daily source** (from `calculations` → values-only) → `data/daily.csv`
```csv
date,price,daily_volume
2012-01-01,42934.12,123456789
...
```

2) **Weekly price expected** → `data/expected_weekly_price.csv`
```csv
date,weekly_close,weekly_volume,weekly_return,weekly_variance,rolling_vol,weighted_volume,vwap_ma,multiple_calc,bs_multiplier,lower_2sd,upper_2sd,lower_3sd,upper_3sd,lower_4sd,upper_4sd,avg_return,avg_variance,sd_global
```

3) **WDCA expected** → `data/expected_wdca.csv`
```csv
trade_date,week,btc_price,pct_change_from_first,investment_multiple_optimum,buy_sell_multiplier,investment_amount_optimum,btc_units_optimum,total_investment_optimum,capital_balance_optimum,rolling_weekly_pnl,avg_buy_price_optimum,btc_units_simple,investment_amount_simple,avg_buy_price_simple
```

> Ensure ISO dates and exact header names.

---

### 5.2 Run Python to compute results

Example (`scripts/compute.py`):
```python
import pandas as pd
from datetime import date
import optimum_dca

daily = pd.read_csv("data/daily.csv", parse_dates=["date"])

weekly, wdca = optimum_dca.run_optimum_dca(
    daily,
    start_date=date(2022, 1, 10),
    weeks=208,
    weekly_budget=50.0,
    today=date(2100, 1, 1),
    j_logic="excel"  # use "excel" to match workbook baseline bit-for-bit
)

weekly.to_csv("data/weekly_python.csv", index=False)
wdca.to_csv("data/wdca_python.csv", index=False)
```

---

### 5.3 Compare with pytest

Install:
```
pip install pytest
```

**`tests/test_weekly_price.py`**
```python
import pandas as pd
import numpy as np
from datetime import date
import optimum_dca

ABS_TOL = 1e-8
REL_TOL = 1e-8

COLUMNS = [
    "weekly_close","weekly_volume","weekly_return","weekly_variance","rolling_vol",
    "weighted_volume","vwap_ma","multiple_calc","bs_multiplier",
    "lower_2sd","upper_2sd","lower_3sd","upper_3sd","lower_4sd","upper_4sd",
    "avg_return","avg_variance","sd_global"
]

def to_float(s):
    return pd.to_numeric(s, errors="coerce")

def test_weekly_price_matches_excel():
    daily = pd.read_csv("data/daily.csv", parse_dates=["date"])
    weekly_py, _ = optimum_dca.run_optimum_dca(
        daily,
        start_date=date(2022, 1, 10),
        weeks=208,
        weekly_budget=50.0,
        today=date(2100, 1, 1),
        j_logic="excel"
    )
    exp = pd.read_csv("data/expected_weekly_price.csv", parse_dates=["date"])

    left  = weekly_py.set_index("date").loc[exp["date"]].reset_index()
    right = exp.copy()

    for col in COLUMNS:
        a = to_float(left[col])
        b = to_float(right[col])
        both_nan = a.isna() & b.isna()
        diff = (a - b).abs()
        ok = (both_nan) | (diff <= (ABS_TOL + REL_TOL * b.abs()))
        if not ok.all():
            bad = pd.DataFrame({"date": left["date"], "py": a, "exp": b, "abs_diff": diff})[~ok]
            print("\nMismatches in", col)
            print(bad.head(10).to_string(index=False))
        assert ok.all(), f"Column {col} has mismatches"
```

**`tests/test_wdca.py`**
```python
import pandas as pd
import numpy as np
from datetime import date
import optimum_dca

ABS_TOL = 1e-8
REL_TOL = 1e-8

COLUMNS = [
    "btc_price","pct_change_from_first","investment_multiple_optimum","buy_sell_multiplier",
    "investment_amount_optimum","btc_units_optimum","total_investment_optimum","capital_balance_optimum",
    "rolling_weekly_pnl","avg_buy_price_optimum","btc_units_simple","investment_amount_simple","avg_buy_price_simple"
]

def to_float(s):
    return pd.to_numeric(s, errors="coerce")

def test_wdca_matches_excel():
    daily = pd.read_csv("data/daily.csv", parse_dates=["date"])
    weekly, wdca_py = optimum_dca.run_optimum_dca(
        daily,
        start_date=date(2022, 1, 10),
        weeks=208,
        weekly_budget=50.0,
        today=date(2100, 1, 1),
        j_logic="excel"
    )
    exp = pd.read_csv("data/expected_wdca.csv", parse_dates=["trade_date"])

    left  = wdca_py.set_index("trade_date").loc[exp["trade_date"]].reset_index()
    right = exp.copy()

    for col in COLUMNS:
        a = to_float(left[col])
        b = to_float(right[col])
        both_nan = a.isna() & b.isna()
        diff = (a - b).abs()
        ok = (both_nan) | (diff <= (ABS_TOL + REL_TOL * b.abs()))
        if not ok.all():
            bad = pd.DataFrame({"trade_date": left["trade_date"], "py": a, "exp": b, "abs_diff": diff})[~ok]
            print("\nMismatches in", col)
            print(bad.head(10).to_string(index=False))
        assert ok.all(), f"Column {col} has mismatches"
```

Run:
```
pytest -q
```

> To validate the **fixed** J ordering instead, export a new *expected* CSV from Excel after updating J’s formula, or compare Python `j_logic="fixed"` vs `j_logic="excel"` and manually review deep buy-zone differences.

---

## 6. Troubleshooting & Pitfalls

- **Band ties**: J uses strict inequalities; values exactly on a band are neutral (`J=1`). K already uses open intervals.
- **Current week exception**: Set `today` far in the future for stable tests so Weekly Close doesn’t use “latest so far” logic.
- **Excel error strings**: Coerce `#REF!`/`#N/A` to NaN.
- **Window boundaries**: F and H match the sheet (“running until row 14, then rolling 14”). Ensure your exports reflect a fresh recalc.
- **Precision**: Tiny float differences are normal; `1e-8` tolerances are strict—loosen if your CSVs are rounded.

---

## Appendix A — Fixed Excel formula for J

To make Excel match the **fixed** ordering used in Python, put this in **J9** and fill down:

```excel
=IF(B9="","",
 IF(B9<Q9, 1+(4*ABS(D9))+(1+$X$2)+F9,
 IF(B9<O9, 1+(3*ABS(D9))+(1+$X$2)+F9,
 IF(B9<M9, 1+(2*ABS(D9))+(1+$X$2)+F9,
 IF(B9>R9, 1-(4*ABS(D9))-(1+$X$2)-F9,
 IF(B9>P9, 1-(3*ABS(D9))-(1+$X$2)-F9,
 IF(B9>N9, 1-(2*ABS(D9))-(1+$X$2)-F9,
 1)))))))
```
