"""
Technical Indicator Computation Module.
Implements the exact 10 technical indicators specified in Table 10 of:
'Predicting Stock Market Trends Using Machine Learning and Deep Learning Algorithms
Via Continuous and Binary Data; a Comparative Analysis' (Nabipour et al., IEEE Access 2020).
"""

from typing import Optional
import numpy as np
import pandas as pd
from stock_predict.config import IndicatorConfig


def compute_sma(close: pd.Series, period: int = 10) -> pd.Series:
    """
    Simple n-day Moving Average (SMA).
    Formula: SMA_t = (C_t + C_{t-1} + ... + C_{t-n+1}) / n
    """
    return close.rolling(window=period, min_periods=period).mean()


def compute_wma(close: pd.Series, period: int = 10) -> pd.Series:
    """
    Weighted n-day Moving Average (WMA).
    Formula: WMA_t = sum((period - i) * C_{t-i}) / sum(1..period)
    """
    weights = np.arange(1, period + 1)
    weight_sum = weights.sum()

    def calc_wma(window: np.ndarray) -> float:
        return float(np.dot(window, weights) / weight_sum)

    return close.rolling(window=period, min_periods=period).apply(calc_wma, raw=True)


def compute_mom(close: pd.Series, period: int = 10) -> pd.Series:
    """
    Momentum (MOM).
    Formula: MOM_t = C_t - C_{t-n+1} (change over n-1 past periods to current)
    """
    return close.diff(periods=period - 1)


def compute_stck(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10
) -> pd.Series:
    """
    Stochastic %K (STCK).
    Formula: STCK_t = ((C_t - LL_{t-n+1}) / (HH_{t-n+1} - LL_{t-n+1})) * 100
    """
    ll = low.rolling(window=period, min_periods=period).min()
    hh = high.rolling(window=period, min_periods=period).max()
    diff = hh - ll
    diff = diff.replace(0, np.nan)
    stck = ((close - ll) / diff) * 100.0
    return stck.fillna(50.0)


def compute_stcd(stck: pd.Series, period: int = 10) -> pd.Series:
    """
    Stochastic %D (STCD).
    Formula: STCD_t = sum_{i=0}^{n-1} STCK_{t-i} / n
    """
    return stck.rolling(window=period, min_periods=period).mean()


def compute_rsi(close: pd.Series, period: int = 10) -> pd.Series:
    """
    Relative Strength Index (RSI).
    Formula: RSI_t = 100 - (100 / (1 + (sum(UP) / sum(DW))))
    """
    delta = close.diff()
    up = delta.clip(lower=0)
    dw = (-delta).clip(lower=0)

    sum_up = up.rolling(window=period, min_periods=period).sum()
    sum_dw = dw.rolling(window=period, min_periods=period).sum()

    rs = sum_up / sum_dw.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))

    # Edge cases: when sum_dw == 0 (all gains), RSI = 100. When sum_up == 0 (all losses), RSI = 0
    rsi = rsi.where(~(sum_dw == 0), 100.0)
    rsi = rsi.where(~(sum_up == 0), 0.0)
    return rsi


def compute_macd_signal(
    close: pd.Series, fast: int = 12, slow: int = 26, signal_period: int = 9
) -> pd.Series:
    """
    Signal (SIG) / MACD Signal Line.
    Formula:
        EMA(k)_t = EMA(k)_{t-1} * (1 - 2/(k+1)) + C_t * (2/(k+1))
        MACD_t = EMA(12)_t - EMA(26)_t
        Signal_t = MACD_t * (2/(n+1)) + Signal_{t-1} * (1 - 2/(n+1))
    """
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    sig = macd.ewm(span=signal_period, adjust=False).mean()
    return sig


def compute_lwr(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10
) -> pd.Series:
    """
    Larry William's %R (LWR).
    Formula: LWR_t = ((HH_{t-n+1} - C_t) / (HH_{t-n+1} - LL_{t-n+1})) * 100
    """
    ll = low.rolling(window=period, min_periods=period).min()
    hh = high.rolling(window=period, min_periods=period).max()
    diff = hh - ll
    diff = diff.replace(0, np.nan)
    lwr = ((hh - close) / diff) * 100.0
    return lwr.fillna(50.0)


def compute_ado(
    high: pd.Series, low: pd.Series, close: pd.Series
) -> pd.Series:
    """
    Accumulation/Distribution Oscillator (ADO).
    Formula: ADO_t = (H_t - C_t) / (H_t - L_t)
    """
    hl_diff = high - low
    hl_diff = hl_diff.replace(0, np.nan)
    ado = (high - close) / hl_diff
    return ado.fillna(0.5)


def compute_cci(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10
) -> pd.Series:
    """
    Commodity Channel Index (CCI).
    Formula:
        M_t = (H_t + L_t + C_t) / 3
        SM_t = sum_{i=0}^{n-1} M_{t-i} / n
        D_t = sum_{i=0}^{n-1} |M_{t-i} - SM_t| / n
        CCI_t = (M_t - SM_t) / (0.015 * D_t)
    """
    m = (high + low + close) / 3.0
    sm = m.rolling(window=period, min_periods=period).mean()

    def calc_mean_deviation(window: np.ndarray) -> float:
        mean_val = np.mean(window)
        return float(np.mean(np.abs(window - mean_val)))

    d = m.rolling(window=period, min_periods=period).apply(
        calc_mean_deviation, raw=True
    )
    denom = 0.015 * d
    denom = denom.replace(0, np.nan)
    cci = (m - sm) / denom
    return cci.fillna(0.0)


def compute_all_indicators(
    df: pd.DataFrame, config: Optional[IndicatorConfig] = None
) -> pd.DataFrame:
    """
    Compute all 10 technical indicators from OHLC dataframe.
    Requires columns: 'Open', 'High', 'Low', 'Close' (or lowercase).

    Returns a DataFrame containing the original columns plus the 10 indicator columns:
    ['SMA', 'WMA', 'MOM', 'STCK', 'STCD', 'RSI', 'SIG', 'LWR', 'ADO', 'CCI'].
    """
    cfg = config or IndicatorConfig()
    result = df.copy()

    col_map = {c.lower(): c for c in df.columns}
    open_col = col_map.get("open", "Open")
    high_col = col_map.get("high", "High")
    low_col = col_map.get("low", "Low")
    close_col = col_map.get("close", "Close")

    high = result[high_col]
    low = result[low_col]
    close = result[close_col]

    result["SMA"] = compute_sma(close, period=cfg.sma_period)
    result["WMA"] = compute_wma(close, period=cfg.wma_period)
    result["MOM"] = compute_mom(close, period=cfg.mom_period)
    result["STCK"] = compute_stck(high, low, close, period=cfg.stck_period)
    result["STCD"] = compute_stcd(result["STCK"], period=cfg.stcd_period)
    result["RSI"] = compute_rsi(close, period=cfg.rsi_period)
    result["SIG"] = compute_macd_signal(
        close, fast=cfg.macd_fast, slow=cfg.macd_slow, signal_period=cfg.macd_signal
    )
    result["LWR"] = compute_lwr(high, low, close, period=cfg.lwr_period)
    result["ADO"] = compute_ado(high, low, close)
    result["CCI"] = compute_cci(high, low, close, period=cfg.cci_period)

    return result
