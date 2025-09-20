
# optimum_dca_standalone.py
# --------------------------------------------------------------
# A clean, standalone implementation of an "optimum DCA" strategy
# that uses weekly inputs (date, close, volumes) and computes:
#   - Volatility and rolling stats (mean/std) to form SD bands
#   - A regime-aware base investment multiple (leans in on dips, dials back when hot)
#   - A dip-depth buy multiplier (tiers 0/2/3/4 based on how far below bands price is)
#   - A per-week investment amount from (base multiple - P/L drift + dip multiplier)
#   - Units purchased, cumulative investment, capital balance, average cost
#
# No CSV/Excel reading. You pass in a pandas DataFrame with weekly data.
#
# © You. MIT-style use encouraged.
# --------------------------------------------------------------

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Literal
import numpy as np
import pandas as pd

@dataclass
class StrategyConfig:
    # Budgeting
    weekly_budget: float              # nominal budget per week (e.g., 50.0)
    total_weeks: int                  # horizon in weeks (used only for total capital bookkeeping)

    # Rolling windows for stats
    vol_lookback_weeks: int = 1       # 1-week realized volatility proxy (|return|) by default
    ma_vol_lookback_weeks: int = 14   # moving-average window for volatility
    band_lookback_weeks: int = 14     # rolling mean/std window for SD bands

    # Sigma multipliers for bands
    band_sigma_2: float = 2.0
    band_sigma_3: float = 3.0
    band_sigma_4: float = 4.0

    # Sensitivity parameter that appears in the Excel logic (we expose it clearly)
    sd_sensitivity: float = 0.0       # corresponds to some SD-related constant in Excel (X2)

    # Investment rules
    allow_negative_investment: bool = False   # if True, negative cash implies "selling"; else clipped at 0

    # Output rounding
    rounding: Optional[int] = None    # e.g., 8 for 8 decimal places on units; None means no rounding


def compute_weekly_features(
    weekly_df: pd.DataFrame,
    cfg: StrategyConfig,
    price_col: str = "close",
    weekly_volume_col: Optional[str] = "weekly_volume",
) -> pd.DataFrame:
    """
    Given weekly_df with at least a 'close' column and a DateTimeIndex or 'date' column,
    compute derived features used by the strategy:
      - pct_return, vol_abs (abs return)
      - ma_vol (rolling mean of vol_abs over cfg.ma_vol_lookback_weeks)
      - rolling mean / std on close (for SD bands)
      - lower/upper 2σ, 3σ, 4σ bands

    Returns a copy of weekly_df with new columns added.
    """
    df = weekly_df.copy()
    if "date" in df.columns:
        df = df.set_index("date")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("weekly_df must have a DatetimeIndex or a 'date' column with datetime values.")

    if price_col not in df.columns:
        raise KeyError(f"'{price_col}' column not found in weekly_df.")

    # 1) Week-over-week returns and a simple realized vol proxy
    df["pct_return"] = df[price_col].pct_change(cfg.vol_lookback_weeks)
    df["vol_abs"] = df["pct_return"].abs()

    # 2) Moving average of volatility
    df["ma_vol"] = df["vol_abs"].rolling(cfg.ma_vol_lookback_weeks, min_periods=1).mean()

    # 3) Rolling mean and std for bands
    roll_mean = df[price_col].rolling(cfg.band_lookback_weeks, min_periods=1).mean()
    roll_std  = df[price_col].rolling(cfg.band_lookback_weeks, min_periods=2).std()

    # 2σ, 3σ, 4σ bands (lower & upper)
    for mult, name in [(cfg.band_sigma_2, "2"), (cfg.band_sigma_3, "3"), (cfg.band_sigma_4, "4")]:
        df[f"lower_{name}sigma"] = roll_mean - mult * roll_std
        df[f"upper_{name}sigma"] = roll_mean + mult * roll_std

    return df


def base_regime_multiple(
    price: float,
    lower_2sigma: float,
    upper_2sigma: float,
    vol_abs: float,
    ma_vol: float,
    sd_sensitivity: float,
) -> float:
    """
    A regime-aware base multiple, inspired by the Excel's 'Multiple calculation' (weekly price!J).
    - If price is below the lower 2σ band: overweight (increase multiple)
    - If price is above the upper 2σ band: underweight (decrease multiple)
    - Otherwise: neutral (1.0)

    The scaling uses |volatility|, its moving-average, and a user-set sensitivity constant.
    """
    J = 1.0  # neutral baseline
    if np.isfinite(price) and np.isfinite(lower_2sigma) and price < lower_2sigma:
        # Market is "cheap" vs. band: overweight
        J += 2.0 * abs(vol_abs) + (1.0 + sd_sensitivity) + (ma_vol if np.isfinite(ma_vol) else 0.0)
    elif np.isfinite(price) and np.isfinite(upper_2sigma) and price > upper_2sigma:
        # Market is "hot" vs. band: underweight
        J -= 4.0 * abs(vol_abs) + (1.0 + sd_sensitivity) + (ma_vol if np.isfinite(ma_vol) else 0.0)
    return J


def dip_depth_multiplier(
    price: float,
    lower_2sigma: float,
    lower_3sigma: float,
    lower_4sigma: float,
) -> float:
    """
    A discrete buy multiplier (K) based on how deep the price is below lower SD bands.
    - price < lower_4σ  => 4
    - lower_4σ < price < lower_3σ => 3
    - lower_3σ < price < lower_2σ => 2
    - else => 0
    """
    if not all(np.isfinite([price, lower_2sigma, lower_3sigma, lower_4sigma])):
        return 0.0

    if price < lower_4sigma:
        return 4.0
    if lower_4sigma < price < lower_3sigma:
        return 3.0
    if lower_3sigma < price < lower_2sigma:
        return 2.0
    return 0.0


def compute_optimum_dca(
    weekly_features: pd.DataFrame,
    cfg: StrategyConfig,
    price_col: str = "close",
) -> pd.DataFrame:
    """
    Core pipeline—expects the features produced by compute_weekly_features and produces:
      - change_from_entry: (price_t - price_entry)/price_entry
      - base_multiple:     regime-aware multiple J
      - dip_multiplier:    discrete K (0,2,3,4)
      - investment_multiple: base_multiple - change_from_entry
      - weekly_investment: (investment_multiple + dip_multiplier) * weekly_budget
      - units_bought:      weekly_investment / price
      - cum_investment:    cumulative sum of weekly_investment
      - cum_units:         cumulative sum of units_bought
      - capital_balance:   total_capital - cum_investment
      - average_cost:      cum_investment / cum_units
    """
    df = weekly_features.copy()
    if "date" in df.columns:
        df = df.set_index("date")
    price = df[price_col]

    # Entry anchor
    entry_price = price.iloc[0]

    # 1) P/L drift vs entry
    df["change_from_entry"] = (price - entry_price) / entry_price

    # 2) Regime base multiple J
    df["base_multiple"] = [
        base_regime_multiple(
            price=p,
            lower_2sigma=l2,
            upper_2sigma=u2,
            vol_abs=v,
            ma_vol=mav,
            sd_sensitivity=cfg.sd_sensitivity,
        )
        for p, l2, u2, v, mav in zip(
            df[price_col].values,
            df["lower_2sigma"].values,
            df["upper_2sigma"].values,
            df["vol_abs"].values,
            df["ma_vol"].values,
        )
    ]

    # 3) Dip-depth discrete K
    df["dip_multiplier"] = [
        dip_depth_multiplier(p, l2, l3, l4)
        for p, l2, l3, l4 in zip(
            df[price_col].values,
            df["lower_2sigma"].values,
            df["lower_3sigma"].values,
            df["lower_4sigma"].values,
        )
    ]

    # 4) Investment multiple E = J - D
    df["investment_multiple"] = df["base_multiple"] - df["change_from_entry"]

    # 5) Weekly cash allocation = (E + K) * weekly_budget
    weekly_cash = (df["investment_multiple"] + df["dip_multiplier"]) * cfg.weekly_budget
    if not cfg.allow_negative_investment:
        weekly_cash = weekly_cash.clip(lower=0.0)
    df["weekly_investment"] = weekly_cash

    # 6) Units bought each week
    df["units_bought"] = df["weekly_investment"] / price

    # 7) Cumulative cash & units
    df["cum_investment"] = df["weekly_investment"].cumsum()
    df["cum_units"] = df["units_bought"].cumsum()

    # 8) Capital balance (for bookkeeping)
    total_capital = cfg.weekly_budget * cfg.total_weeks
    df["capital_balance"] = total_capital - df["cum_investment"]

    # 9) Average cost
    df["average_cost"] = df["cum_investment"] / df["cum_units"]

    # Optional rounding for nicer displays
    if cfg.rounding is not None:
        for col in ["units_bought", "cum_units", "average_cost"]:
            df[col] = df[col].round(cfg.rounding)

    return df


# ----------------------
# Example usage (commented)
# ----------------------
# import pandas as pd
# import numpy as np
# from optimum_dca_standalone import StrategyConfig, compute_weekly_features, compute_optimum_dca
#
# # Suppose you already have a weekly dataframe with columns:
# # index: weekly DateTimeIndex
# # columns: ['close', 'weekly_volume']
# weekly = pd.DataFrame({
#     "close": ...,
#     "weekly_volume": ...
# }, index=weekly_dates)
#
# cfg = StrategyConfig(
#     weekly_budget=50.0,
#     total_weeks=208,
#     vol_lookback_weeks=1,
#     ma_vol_lookback_weeks=14,
#     band_lookback_weeks=14,
#     sd_sensitivity=0.0,
#     rounding=8,
# )
#
# features = compute_weekly_features(weekly, cfg)
# results  = compute_optimum_dca(features, cfg)
# print(results.tail())
