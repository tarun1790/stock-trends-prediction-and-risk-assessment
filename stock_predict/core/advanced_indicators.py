"""
Advanced Feature Engineering & Quantitative Indicators.
Expands beyond the 10 basic IEEE indicators to include:
- ATR (Average True Range) & Volatility Bands (Bollinger %B & Bandwidth)
- ADX (Average Directional Index) with +DI / -DI for trend strength filtering
- CMF (Chaikin Money Flow) & VWAP (Volume-Weighted Average Price)
- Parkinson & Garman-Klass Volatility Estimators
- Fractional Differentiation for Memory Preservation
- Ternary Regime Encoding {-1 Strong Bear, 0 Neutral/Chop, +1 Strong Bull}
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from stock_predict.core.indicators import compute_all_indicators


def compute_atr(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
) -> pd.Series:
    """Average True Range (ATR)."""
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period, min_periods=period).mean()


def compute_bollinger_bands(
    close: pd.Series, period: int = 20, num_std: float = 2.0
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Bollinger Bands: Middle, Upper, Lower, %B, and Bandwidth.
    %B = (Close - Lower) / (Upper - Lower)
    Bandwidth = (Upper - Lower) / Middle
    """
    middle = close.rolling(window=period, min_periods=period).mean()
    std = close.rolling(window=period, min_periods=period).std()
    upper = middle + (std * num_std)
    lower = middle - (std * num_std)

    bandwidth = (upper - lower) / middle.replace(0, np.nan)
    percent_b = (close - lower) / (upper - lower).replace(0, np.nan)
    return middle, upper, lower, percent_b.fillna(0.5), bandwidth.fillna(0.0)


def compute_adx(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Average Directional Index (ADX) with +DI and -DI.
    Measures trend strength independently of direction.
    ADX > 25 indicates strong trending regime; ADX < 20 indicates choppy range.
    """
    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    tr = compute_atr(high, low, close, period=1)
    atr = tr.rolling(window=period, min_periods=period).mean()

    plus_di = 100.0 * (
        pd.Series(plus_dm, index=high.index).rolling(window=period).mean()
        / atr.replace(0, np.nan)
    )
    minus_di = 100.0 * (
        pd.Series(minus_dm, index=high.index).rolling(window=period).mean()
        / atr.replace(0, np.nan)
    )

    dx = 100.0 * ((plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan))
    adx = dx.rolling(window=period, min_periods=period).mean()

    return adx.fillna(20.0), plus_di.fillna(20.0), minus_di.fillna(20.0)


def compute_cmf(
    high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, period: int = 20
) -> pd.Series:
    """
    Chaikin Money Flow (CMF).
    Measures institutional accumulation vs distribution volume pressure.
    """
    hl_diff = high - low
    hl_diff = hl_diff.replace(0, np.nan)
    money_flow_multiplier = ((close - low) - (high - close)) / hl_diff
    money_flow_volume = money_flow_multiplier * volume

    cmf = (
        money_flow_volume.rolling(window=period, min_periods=period).sum()
        / volume.rolling(window=period, min_periods=period).sum().replace(0, np.nan)
    )
    return cmf.fillna(0.0)


def compute_vwap(
    high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, period: int = 20
) -> pd.Series:
    """Rolling Volume-Weighted Average Price (VWAP)."""
    typical_price = (high + low + close) / 3.0
    vp = typical_price * volume
    vwap = (
        vp.rolling(window=period, min_periods=period).sum()
        / volume.rolling(window=period, min_periods=period).sum().replace(0, np.nan)
    )
    return vwap.fillna(close)


def compute_parkinson_volatility(
    high: pd.Series, low: pd.Series, period: int = 20
) -> pd.Series:
    """
    Parkinson High-Low Volatility Estimator.
    5x more efficient than close-to-close historical standard deviation.
    """
    log_hl = np.log(high / low.replace(0, np.nan)) ** 2
    factor = 1.0 / (4.0 * np.log(2.0))
    rolling_var = factor * log_hl.rolling(window=period, min_periods=period).mean()
    annualized_vol = np.sqrt(rolling_var * 252.0)
    return annualized_vol.fillna(0.15)


def compute_fractional_differentiation(
    series: pd.Series, d: float = 0.4, threshold: float = 1e-4
) -> pd.Series:
    """
    Fractional Differentiation (Marcos Lopez de Prado method).
    Achieves mathematical stationarity while preserving maximum long-term memory.
    """
    weights = [1.0]
    k = 1
    while True:
        w = -weights[-1] / k * (d - k + 1)
        if abs(w) < threshold or k > 100:
            break
        weights.append(w)
        k += 1

    weights = np.array(weights[::-1])
    res = pd.Series(index=series.index, dtype=float)
    vals = series.values

    for i in range(len(weights) - 1, len(vals)):
        res.iloc[i] = np.dot(weights, vals[i - len(weights) + 1 : i + 1])

    return res.ffill().bfill()


def compute_ternary_regime_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert indicators into 3-State Ternary Regime Signals:
    +1: Strong Bullish
     0: Neutral / Sideways Chop / Consolidation
    -1: Strong Bearish
    Helps models avoid whipsaws during non-trending regimes.
    """
    close = df["Close"]
    res = pd.DataFrame(index=df.index)

    # 1. SMA Trend Regime (with 0.5% neutral zone)
    sma_diff = (close - df["SMA"]) / df["SMA"]
    res["REG_SMA"] = np.where(sma_diff > 0.005, 1, np.where(sma_diff < -0.005, -1, 0))

    # 2. RSI Regime (30-70 standard, 45-55 neutral zone)
    rsi = df["RSI"]
    res["REG_RSI"] = np.where(rsi > 55, 1, np.where(rsi < 45, -1, 0))

    # 3. ADX & Directional Regime
    if "ADX" in df.columns and "PLUS_DI" in df.columns and "MINUS_DI" in df.columns:
        trending = df["ADX"] > 20
        res["REG_ADX"] = np.where(
            trending & (df["PLUS_DI"] > df["MINUS_DI"]),
            1,
            np.where(trending & (df["MINUS_DI"] > df["PLUS_DI"]), -1, 0),
        )
    else:
        res["REG_ADX"] = 0

    # 4. Bollinger %B Regime
    if "BB_PCT_B" in df.columns:
        bb_pct = df["BB_PCT_B"]
        res["REG_BB"] = np.where(bb_pct > 0.7, 1, np.where(bb_pct < 0.3, -1, 0))
    else:
        res["REG_BB"] = 0

    # 5. CMF Volume Accumulation Regime
    if "CMF" in df.columns:
        cmf = df["CMF"]
        res["REG_CMF"] = np.where(cmf > 0.05, 1, np.where(cmf < -0.05, -1, 0))
    else:
        res["REG_CMF"] = 0

    return res


def compute_full_quant_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute comprehensive 25+ institutional feature matrix combining
    the 10 IEEE indicators with advanced volatility, momentum, and regime features.
    """
    # 1. Baseline 10 IEEE Indicators
    result = compute_all_indicators(df)

    high = result["High"]
    low = result["Low"]
    close = result["Close"]
    volume = (
        result["Volume"] if "Volume" in result.columns else pd.Series(1000.0, index=df.index)
    )

    # 2. Advanced Quant Indicators
    result["ATR"] = compute_atr(high, low, close, period=14)
    bb_mid, bb_up, bb_low, bb_pct, bb_width = compute_bollinger_bands(close, period=20)
    result["BB_MID"] = bb_mid
    result["BB_UP"] = bb_up
    result["BB_LOW"] = bb_low
    result["BB_PCT_B"] = bb_pct
    result["BB_WIDTH"] = bb_width

    adx, plus_di, minus_di = compute_adx(high, low, close, period=14)
    result["ADX"] = adx
    result["PLUS_DI"] = plus_di
    result["MINUS_DI"] = minus_di

    result["CMF"] = compute_cmf(high, low, close, volume, period=20)
    result["VWAP"] = compute_vwap(high, low, close, volume, period=20)
    result["PARK_VOL"] = compute_parkinson_volatility(high, low, period=20)
    result["FRAC_DIFF"] = compute_fractional_differentiation(close, d=0.4)

    # 3. Ternary Regime Signals
    regimes = compute_ternary_regime_signals(result)
    for col in regimes.columns:
        result[col] = regimes[col]

    return result
