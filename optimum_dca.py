
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional, Sequence, Tuple

import numpy as np
import pandas as pd


# --------------------------
# Helpers & data containers
# --------------------------

@dataclass
class WeeklyBands:
    """Price bands computed from VWAP MA (H) and rolling vol (F)."""
    lower_2sd: float
    upper_2sd: float
    lower_3sd: float
    upper_3sd: float
    lower_4sd: float
    upper_4sd: float


def _is_monday(d: date) -> bool:
    # Monday == 0 in Python
    return pd.Timestamp(d).weekday() == 0


def _monday_on_or_after(d: date) -> date:
    ts = pd.Timestamp(d)
    return (ts + pd.offsets.Week(weekday=0)).date() if ts.weekday() != 0 else ts.date()


def _last_non_nan(series: pd.Series) -> Optional[float]:
    """Return last non-NaN value from a numeric series, or None if none exist."""
    for v in reversed(series.tolist()):
        if pd.notna(v):
            return float(v)
    return None


# --------------------------
# Core replication functions
# --------------------------

def compute_weekly_table(
    daily: pd.DataFrame,
    today: Optional[date] = None,
) -> pd.DataFrame:
    """
    Replicate the 'weekly price' sheet logic.

    Parameters
    ----------
    daily : DataFrame with columns:
        - 'date' (datetime-like)
        - 'price' (float)
        - 'daily_volume' (float, optional; can be NaN)
    today : date, optional
        Used only for the special case in the sheet's Bn formula:
        IF(AND(TODAY()>=(An-7), An>TODAY()), use most-recent price; ELSE use price on An.
        If None, defaults to today's date on the system.

    Returns
    -------
    DataFrame with columns (exactly mirroring the sheet semantics):
        A Date                         -> 'date' (Mondays, ascending)
        B Weekly Close                 -> 'weekly_close'
        C Weekly Volume                -> 'weekly_volume'
        D Weekly Volatility            -> 'weekly_return'
        E Weekly Variance              -> 'weekly_variance'
        F 14 Week MA Volatility        -> 'rolling_vol'      (STDEV.S per sheet rules)
        G Weekly Weighted Volume       -> 'weighted_volume'  (B * C)
        H 14 Week VWAP MA              -> 'vwap_ma'
        J Multiple calculation         -> 'multiple_calc'    (piecewise formula)
        K Buy/Sell Multiplier          -> 'bs_multiplier'    (discrete bucket per bands)
        M..R Bands                     -> 'lower_2sd','upper_2sd','lower_3sd','upper_3sd','lower_4sd','upper_4sd'
        T AVG (of D)                   -> 'avg_return' (scalar, repeated in each row)
        U MIN (of D)                   -> 'min_return' (scalar, repeated)
        V MAX (of D)                   -> 'max_return' (scalar, repeated)
        W AVG VAR                      -> 'avg_variance' (scalar, repeated)
        X SD                            -> 'sd_global' (scalar, repeated)

    Important: We follow the spreadsheet exactly, including:
      * H and F use a *running* window until the 14th completed row (rows 3..16),
        then switch to a 14-week rolling window from row 17 onward.
      * The 'Multiple calculation' ("J") formula's IF ordering is replicated verbatim,
        even though it makes the 3σ/4σ undervaluation branches unreachable.
      * The neutral zone returns J=1, which causes K="" (blank) per the sheet.
    """
    if today is None:
        today = date.today()

    # Normalize input
    df = daily.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.sort_values("date").reset_index(drop=True)

    # Build Monday anchors from the sheet's approach:
    # The original sheet starts on a Monday and increments by 7 days.
    start_monday = _monday_on_or_after(df["date"].min())
    last_date = df["date"].max()
    mondays = []
    d0 = start_monday
    while d0 <= last_date:
        mondays.append(d0)
        d0 = (pd.Timestamp(d0) + pd.Timedelta(days=7)).date()

    out = pd.DataFrame({"date": mondays})

    # Lookup helpers: map date -> price and date -> weekly_volume (sum of previous 7 daily volumes)
    price_map = {d: v for d, v in zip(df["date"], df["price"])}

    # Weekly volume in 'calculations' sheet is SUM of daily_volume over [An-7, An-1]
    if "daily_volume" in df.columns:
        vol_series = df.set_index("date")["daily_volume"]
    else:
        vol_series = pd.Series(index=pd.Index(df["date"], name="date"), dtype=float)

    def weekly_close_for(anchor: date) -> float:
        # IF(AND(TODAY()>=(An-7), An>TODAY()), INDEX(calculations!B:B, MATCH(143^143, calculations!B:B)),
        #    IF(MATCH(An, calculations!A:A, 0), INDEX(calculations!B:B, MATCH(An, calculations!A:A, 0)), ""))
        window_start = (pd.Timestamp(anchor) - pd.Timedelta(days=7)).date()
        if today >= window_start and anchor > today:
            # use most recent non-NaN price as of 'today'
            # emulate MATCH(143^143, B:B)
            last_price = _last_non_nan(df.loc[df["date"] <= today, "price"])
            return float("nan") if last_price is None else float(last_price)
        # else exact match on anchor date
        return float(price_map.get(anchor, np.nan))

    out["weekly_close"] = [weekly_close_for(d) for d in out["date"]]

    def weekly_volume_for(anchor: date) -> float:
        start = (pd.Timestamp(anchor) - pd.Timedelta(days=7)).date()
        end = (pd.Timestamp(anchor) - pd.Timedelta(days=1)).date()
        window = vol_series.loc[(vol_series.index >= start) & (vol_series.index <= end)]
        if window.empty:
            return np.nan
        # Sum of available daily volumes (NaNs ignored)
        return float(window.sum(skipna=True))

    out["weekly_volume"] = [weekly_volume_for(d) for d in out["date"]]

    # D: Weekly volatility = (B - B_prev)/B_prev
    out["weekly_return"] = out["weekly_close"].pct_change()

    # Placeholders for scalars that the sheet puts in row 2 (T2, U2, V2, W2, X2)
    # We compute them once from the full D/E arrays, then repeat per row to mirror the sheet.
    # T2 = AVERAGEIF($D$4:D591,"<>")
    # Actual sheet excludes blanks; here we use all non-NaN weekly returns.
    returns_non_nan = out["weekly_return"].dropna()
    avg_return = float(returns_non_nan.mean()) if len(returns_non_nan) else float("nan")
    min_return = float(returns_non_nan.min()) if len(returns_non_nan) else float("nan")
    max_return = float(returns_non_nan.max()) if len(returns_non_nan) else float("nan")

    # E: Weekly variance = (D - $T$2)^2
    out["weekly_variance"] = (out["weekly_return"] - avg_return) ** 2

    # W2 = SUM(E) / COUNTIFS(E<>"", B>0)
    # In the sheet, the denominator counts rows where E is non-blank and B>0
    # We replicate exactly:
    mask_valid_var = out["weekly_variance"].notna() & (out["weekly_close"] > 0)
    sum_var = float(out.loc[mask_valid_var, "weekly_variance"].sum()) if mask_valid_var.any() else float("nan")
    count_var = int(mask_valid_var.sum())
    avg_variance = (sum_var / count_var) if count_var > 0 else float("nan")
    sd_global = math.sqrt(avg_variance) if not math.isnan(avg_variance) else float("nan")

    # F: "14 Week MA Volatility"
    # Sheet behavior:
    #  - For rows 1..(start_index+13) it's a *running* STDEV.S from the first valid D to current D
    #  - From the (start_index+14)-th row onward it's a 14-length rolling STDEV.S
    # The sheet's first row of data corresponds to index 0 in this DataFrame.
    def stdev_s(values: np.ndarray) -> float:
        # STDEV.S is sample stdev (ddof=1); require at least 2 points.
        if len(values) < 2:
            return np.nan
        return float(np.nanstd(values, ddof=1))

    rolling_vol = []
    for i in range(len(out)):
        # D indices start at 0; in the sheet D3 is the first 'previous' cell used for stdev.
        # We'll treat the first non-NaN return as start.
        window_returns = out.loc[:i, "weekly_return"].values
        non_nan = window_returns[~np.isnan(window_returns)]
        if i <= 13:  # first 14 rows: running
            rolling_vol.append(stdev_s(non_nan))
        else:        # from 15th row (0-based i=14) onward: 14-week window
            last14 = out.loc[max(0, i - 13):i, "weekly_return"].values
            last14 = last14[~np.isnan(last14)]
            rolling_vol.append(stdev_s(last14))
    out["rolling_vol"] = rolling_vol

    # G: Weekly Weighted Volume = B * C
    out["weighted_volume"] = out["weekly_close"] * out["weekly_volume"]

    # H: "14 Week VWAP MA"
    # Same pattern: running VWAP until 14th row, then 14-week rolling VWAP
    vwap_ma = []
    for i in range(len(out)):
        if i <= 13:
            num = float(out.loc[:i, "weighted_volume"].sum(skipna=True))
            den = float(out.loc[:i, "weekly_volume"].sum(skipna=True))
        else:
            num = float(out.loc[i-13:i, "weighted_volume"].sum(skipna=True))
            den = float(out.loc[i-13:i, "weekly_volume"].sum(skipna=True))
        vwap_ma.append((num / den) if den > 0 else np.nan)
    out["vwap_ma"] = vwap_ma

    # Bands M..R:
    # M = H*(1 - 2F), N = H*(1 + 2F), etc.
    out["lower_2sd"] = out["vwap_ma"] * (1 - 2 * out["rolling_vol"])
    out["upper_2sd"] = out["vwap_ma"] * (1 + 2 * out["rolling_vol"])
    out["lower_3sd"] = out["vwap_ma"] * (1 - 3 * out["rolling_vol"])
    out["upper_3sd"] = out["vwap_ma"] * (1 + 3 * out["rolling_vol"])
    out["lower_4sd"] = out["vwap_ma"] * (1 - 4 * out["rolling_vol"])
    out["upper_4sd"] = out["vwap_ma"] * (1 + 4 * out["rolling_vol"])

    # J: "Multiple calculation" (verbatim order from the sheet)
    # IF(B<M, 1+(2*ABS(D))+(1+$X$2)+F,
    #    IF(B<O, 1+(3*ABS(D))+(1+$X$2)+F,
    #       IF(B<Q, 1+(4*ABS(D))+(1+$X$2)+F,
    #          IF(AND(B>N,B<P), 1-(2*ABS(D))-(1+$X$2)-F,
    #             IF(AND(B>N,B>P), 1-(3*ABS(D))-(1+$X$2)-F,
    #                IF(AND(B>R,B>P,B>N), 1-(4*ABS(D))-(1+$X$2)-F,
    #                   IF(B>=M, 1)
    #                ))))))
    # NOTE: The "B<O" and "B<Q" branches are unreachable because they are nested after B<M.
    # We keep them to match the spreadsheet exactly.
    J = []
    for i in range(len(out)):
        B = out.at[i, "weekly_close"]
        D = out.at[i, "weekly_return"]
        F = out.at[i, "rolling_vol"]
        M = out.at[i, "lower_2sd"]
        N = out.at[i, "upper_2sd"]
        O = out.at[i, "lower_3sd"]
        P = out.at[i, "upper_3sd"]
        Q = out.at[i, "lower_4sd"]
        R = out.at[i, "upper_4sd"]
        if pd.isna(B):
            J.append(np.nan)
            continue
        # replicate blanks/NaNs like the sheet
        val = np.nan
        if not pd.isna(B):
            if (B < M):
                val = 1 + (2 * abs(D)) + (1 + sd_global) + F
            else:
                if (B < O):
                    val = 1 + (3 * abs(D)) + (1 + sd_global) + F
                else:
                    if (B < Q):
                        val = 1 + (4 * abs(D)) + (1 + sd_global) + F
                    else:
                        if (B > N) and (B < P):
                            val = 1 - (2 * abs(D)) - (1 + sd_global) - F
                        else:
                            if (B > N) and (B > P):
                                val = 1 - (3 * abs(D)) - (1 + sd_global) - F
                            else:
                                if (B > R) and (B > P) and (B > N):
                                    val = 1 - (4 * abs(D)) - (1 + sd_global) - F
                                else:
                                    if (B >= M):
                                        val = 1
        J.append(val)
    out["multiple_calc"] = J

    # K: "Buy/Sell Multiplier" (discrete bucket based on J sign and position vs bands)
    K_vals = []
    for i in range(len(out)):
        B = out.at[i, "weekly_close"]
        Jv = out.at[i, "multiple_calc"]
        M = out.at[i, "lower_2sd"]
        N = out.at[i, "upper_2sd"]
        O = out.at[i, "lower_3sd"]
        P = out.at[i, "upper_3sd"]
        Q = out.at[i, "lower_4sd"]
        R = out.at[i, "upper_4sd"]

        if pd.isna(B) or pd.isna(Jv):
            K_vals.append(np.nan)
            continue

        if Jv == 1:
            K_vals.append(np.nan)  # blank in the sheet
            continue

        if Jv < 0:
            # Sell zones (above VWAP bands)
            if (P > B) and (B > N):
                K_vals.append(-2)
            elif (R > B) and (B > P):
                K_vals.append(-3)
            elif B > R:
                K_vals.append(-4)
            else:
                K_vals.append(np.nan)
        else:
            # Buy zones (below VWAP bands)
            if (O < B) and (B < M):
                K_vals.append(2)
            elif (Q < B) and (B < O):
                K_vals.append(3)
            elif B < Q:
                K_vals.append(4)
            else:
                K_vals.append(np.nan)

    out["bs_multiplier"] = K_vals

    # Scalars repeated per row to match the sheet surfaces
    out["avg_return"]   = avg_return
    out["min_return"]   = min_return
    out["max_return"]   = max_return
    out["avg_variance"] = avg_variance
    out["sd_global"]    = sd_global

    return out


def compute_optimum_dca_schedule(
    weekly: pd.DataFrame,
    start_date: date,
    weeks: int,
    weekly_budget: float,
) -> pd.DataFrame:
    """
    Replicate '20222023 WDCA' logic (only the data columns), independent of Excel.

    Inputs
    ------
    weekly : DataFrame returned by `compute_weekly_table`.
    start_date : the first trade-week anchor date (Monday) (e.g., 2022-01-10).
    weeks : number of weeks in the investment period (e.g., 208).
    weekly_budget : weekly budget in dollars (e.g., 50).

    Returns
    -------
    DataFrame with columns matching the WDCA data columns:
      'trade_date', 'week', 'btc_price', 'pct_change_from_first',
      'investment_multiple_optimum', 'buy_sell_multiplier',
      'investment_amount_optimum', 'btc_units_optimum',
      'total_investment_optimum', 'capital_balance_optimum',
      'rolling_weekly_pnl', 'avg_buy_price_optimum',
      'btc_units_simple', 'investment_amount_simple', 'avg_buy_price_simple'
    """
    w = weekly.set_index("date")
    # derive globals used in WDCA P-cells
    # P10 = weekly_budget
    # P13 = weeks
    # P15 = ABS('weekly price'!X2)*2 = 2*abs(sd_global)
    sd_global = float(w["sd_global"].dropna().iloc[0]) if "sd_global" in w.columns and w["sd_global"].notna().any() else float("nan")
    total_investment = weeks * weekly_budget
    reserve_cap = abs(sd_global) * 2.0
    # P3 = P5 * P15 -> not directly used in row computations; here for completeness
    total_reserve_needed = total_investment * reserve_cap

    # Build weekly range
    anchors = [start_date + timedelta(days=7*i) for i in range(weeks)]
    # Data columns
    out = pd.DataFrame({
        "trade_date": anchors,
        "week": [i+1 for i in range(weeks)]
    })

    # C: BTC price (weekly close)
    out["btc_price"] = [float(w.at[d, "weekly_close"]) if d in w.index else np.nan for d in anchors]

    # D: Change from first day of Entry = (C - C3)/C3
    if len(out) > 0 and not np.isnan(out.at[0, "btc_price"]):
        base_price = float(out.at[0, "btc_price"])
    else:
        base_price = np.nan
    out["pct_change_from_first"] = (out["btc_price"] - base_price) / base_price

    # E: Investment Multiple Optimum scenario
    # IF(C<>"", IF(AND(D<-0.4, C<>""),
    #       INDEX(weekly!J) - 2*D,
    #     INDEX(weekly!J) - D), "")
    def j_at(d):
        try:
            return float(w.at[d, "multiple_calc"])
        except KeyError:
            return np.nan

    inv_mult = []
    for i, d in enumerate(anchors):
        C = out.at[i, "btc_price"]
        D = out.at[i, "pct_change_from_first"]
        if pd.isna(C):
            inv_mult.append(np.nan)
            continue
        J = j_at(d)
        if (not pd.isna(D)) and (D < -0.4):
            inv_mult.append(J - 2*D)
        else:
            inv_mult.append(J - D)
    out["investment_multiple_optimum"] = inv_mult

    # F: Buy/Sell Multiplier = INDEX(weekly!K) for the same date
    out["buy_sell_multiplier"] = [float(w.at[d, "bs_multiplier"]) if (d in w.index and pd.notna(w.at[d, "bs_multiplier"])) else np.nan for d in anchors]

    # G: Investment Amount Optimum scenario = (E + F) * weekly_budget
    out["investment_amount_optimum"] = (out["investment_multiple_optimum"] + out["buy_sell_multiplier"]) * weekly_budget

    # H: BTC unit Optimum scenario = G / C
    out["btc_units_optimum"] = out["investment_amount_optimum"] / out["btc_price"]

    # I: Total Investment Optimum scenario = running sum of G
    out["total_investment_optimum"] = out["investment_amount_optimum"].cumsum(skipna=True)

    # J: Capital Balance Optimum scenario
    # J3 = Total Investment - G3
    # Jn = IF(Cn<>"", J(n-1) - G(n-1), "")
    cap_bal = []
    for i in range(len(out)):
        if i == 0:
            cap_bal.append(total_investment - out.at[i, "investment_amount_optimum"])
        else:
            prev = cap_bal[i-1]
            prev_spend = out.at[i-1, "investment_amount_optimum"]
            cap_bal.append(prev - prev_spend if pd.notna(out.at[i, "btc_price"]) else np.nan)
    out["capital_balance_optimum"] = cap_bal

    # K: Rolling Weekly Profit/Loss = IF(L<>"",-1*((L - C)/L),"")
    # L: AVG buying price Optimum DCA = I / SUM(H)
    cum_units = out["btc_units_optimum"].cumsum(skipna=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        out["avg_buy_price_optimum"] = out["total_investment_optimum"] / cum_units
        out["rolling_weekly_pnl"] = np.where(pd.notna(out["avg_buy_price_optimum"]), -1.0 * ((out["avg_buy_price_optimum"] - out["btc_price"]) / out["avg_buy_price_optimum"]), np.nan)

    # M: BTC unit Simple DCA = weekly_budget / C
    out["btc_units_simple"] = weekly_budget / out["btc_price"]

    # N: Investment Amount DCA scenario = weekly_budget (constant)
    out["investment_amount_simple"] = weekly_budget

    # O: AVG buying price Simple DCA = SUM(N)/SUM(M)
    cum_units_simple = out["btc_units_simple"].cumsum(skipna=True)
    cum_invest_simple = out["investment_amount_simple"].cumsum(skipna=True)
    out["avg_buy_price_simple"] = cum_invest_simple / cum_units_simple

    return out


# Convenience end-to-end
def run_optimum_dca(
    daily: pd.DataFrame,
    start_date: date,
    weeks: int = 208,
    weekly_budget: float = 50.0,
    today: Optional[date] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Compute weekly table and the WDCA schedule in one shot.

    Returns
    -------
    (weekly_table, wdca_table)
    """
    weekly = compute_weekly_table(daily, today=today)
    wdca = compute_optimum_dca_schedule(weekly, start_date=start_date, weeks=weeks, weekly_budget=weekly_budget)
    return weekly, wdca
