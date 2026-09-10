"""
TradingView 26-Indicator Composite Technical Matrix & AI Alpha Engine.
Computes standard institutional technical ratings:
- 15 Moving Averages (SMA 10/20/50/100/200, EMA 10/20/50/100/200, Hull MA, VWMA, SuperTrend, Ichimoku, Golden Cross)
- 11 Oscillators (RSI 14, Stochastic 14-3-3, CCI 20, ADX 14, Awesome Osc, MOM 10, MACD 12-26-9, StochRSI, Williams %R, BullBear Power, Ultimate Osc)
- Danelfin/Kavout-style AI Alpha Score (1.0 to 10.0)
- ADX Trend-Regime Strength Classifier
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


def _fast_wma(vals: np.ndarray, period: int) -> np.ndarray:
    """Vectorized Weighted Moving Average via 1D Convolution."""
    if len(vals) < period:
        return np.full_like(vals, np.nan)
    weights = np.arange(1, period + 1, dtype=float)
    weights /= np.sum(weights)
    conv = np.convolve(vals, weights[::-1], mode="full")[: len(vals)]
    conv[: period - 1] = np.nan
    return conv


def compute_supertrend(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10, multiplier: float = 3.0
) -> Tuple[pd.Series, pd.Series]:
    """SuperTrend Indicator (Trend + Dynamic Trailing Stop) - Vectorized array indexing."""
    prev_close = close.shift(1)
    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    atr = tr.rolling(window=period, min_periods=period).mean()

    hl2 = (high + low) / 2.0
    upperband = (hl2 + (multiplier * atr)).values
    lowerband = (hl2 - (multiplier * atr)).values
    close_vals = close.values

    n = len(close_vals)
    st_vals = np.empty(n, dtype=float)
    st_vals[:] = np.nan
    dir_vals = np.ones(n, dtype=int)

    in_uptrend = True
    for i in range(period, n):
        curr_c = close_vals[i]
        curr_upper = upperband[i]
        curr_lower = lowerband[i]

        if in_uptrend:
            if curr_c < curr_lower:
                in_uptrend = False
                st_vals[i] = curr_upper
                dir_vals[i] = -1
            else:
                prev_st = st_vals[i - 1] if i > period and not np.isnan(st_vals[i - 1]) else curr_lower
                st_vals[i] = max(curr_lower, prev_st)
                dir_vals[i] = 1
        else:
            if curr_c > curr_upper:
                in_uptrend = True
                st_vals[i] = curr_lower
                dir_vals[i] = 1
            else:
                prev_st = st_vals[i - 1] if i > period and not np.isnan(st_vals[i - 1]) else curr_upper
                st_vals[i] = min(curr_upper, prev_st)
                dir_vals[i] = -1

    st_series = pd.Series(st_vals, index=close.index).ffill().bfill()
    dir_series = pd.Series(dir_vals, index=close.index).fillna(1)
    return st_series, dir_series


def compute_hull_ma(close: pd.Series, period: int = 9) -> pd.Series:
    """Hull Moving Average (HMA) - Ultra low lag, vectorized via 1D convolutions."""
    vals = close.values.astype(float)
    half_length = max(int(period / 2), 1)
    sqrt_length = max(int(np.sqrt(period)), 1)

    wma_half = _fast_wma(vals, half_length)
    wma_full = _fast_wma(vals, period)
    raw_hma = 2.0 * wma_half - wma_full
    hma_vals = _fast_wma(raw_hma, sqrt_length)

    hma_s = pd.Series(hma_vals, index=close.index)
    return hma_s.ffill().bfill()


def compute_vwma(close: pd.Series, volume: pd.Series, period: int = 20) -> pd.Series:
    """Volume-Weighted Moving Average (VWMA)."""
    pv = close * volume
    vwma = pv.rolling(window=period, min_periods=period).sum() / volume.rolling(
        window=period, min_periods=period
    ).sum().replace(0, np.nan)
    return vwma.fillna(close)


def compute_awesome_oscillator(high: pd.Series, low: pd.Series) -> pd.Series:
    """Awesome Oscillator (AO = SMA5(HL2) - SMA34(HL2))."""
    hl2 = (high + low) / 2.0
    ao = hl2.rolling(window=5).mean() - hl2.rolling(window=34).mean()
    return ao.fillna(0.0)


def compute_stochastic_rsi(
    rsi: pd.Series, period: int = 14, smooth_k: int = 3, smooth_d: int = 3
) -> Tuple[pd.Series, pd.Series]:
    """Stochastic RSI (%K and %D)."""
    min_rsi = rsi.rolling(window=period).min()
    max_rsi = rsi.rolling(window=period).max()
    denom = (max_rsi - min_rsi).replace(0, np.nan)
    stoch_rsi = (rsi - min_rsi) / denom * 100.0
    stoch_k = stoch_rsi.rolling(window=smooth_k).mean()
    stoch_d = stoch_k.rolling(window=smooth_d).mean()
    return stoch_k.fillna(50.0), stoch_d.fillna(50.0)


def compute_bull_bear_power(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 13) -> Tuple[pd.Series, pd.Series]:
    """Elder-Ray Bull and Bear Power."""
    ema = close.ewm(span=period, adjust=False).mean()
    bull_power = high - ema
    bear_power = low - ema
    return bull_power.fillna(0.0), bear_power.fillna(0.0)


def compute_ultimate_oscillator(
    high: pd.Series, low: pd.Series, close: pd.Series, p1: int = 7, p2: int = 14, p3: int = 28
) -> pd.Series:
    """Ultimate Oscillator (Larry Williams)."""
    prev_close = close.shift(1)
    true_low = pd.concat([low, prev_close], axis=1).min(axis=1)
    true_high = pd.concat([high, prev_close], axis=1).max(axis=1)
    bp = close - true_low
    tr = true_high - true_low

    avg7 = bp.rolling(p1).sum() / tr.rolling(p1).sum().replace(0, np.nan)
    avg14 = bp.rolling(p2).sum() / tr.rolling(p2).sum().replace(0, np.nan)
    avg28 = bp.rolling(p3).sum() / tr.rolling(p3).sum().replace(0, np.nan)

    ult = 100.0 * (4.0 * avg7 + 2.0 * avg14 + avg28) / 7.0
    return ult.fillna(50.0)


def compute_26_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes TradingView's official 26 technical indicators:
    15 Moving Averages and 11 Oscillators, with buy/neutral/sell ratings and scores.
    """
    if len(df) > 350:
        df = df.iloc[-350:]

    close = df["Close"].copy()
    high = df["High"].copy()
    low = df["Low"].copy()
    volume = df["Volume"].copy() if "Volume" in df.columns else pd.Series(1.0, index=df.index)

    curr_p = float(close.iloc[-1])
    prev_p = float(close.iloc[-2]) if len(close) > 1 else curr_p

    # -------------------------------------------------------------------------
    # 1. 15 MOVING AVERAGES
    # -------------------------------------------------------------------------
    ma_signals: Dict[str, Dict[str, Any]] = {}

    ma_configs = [
        ("SMA 10", close.rolling(10).mean(), "sma_10"),
        ("SMA 20", close.rolling(20).mean(), "sma_20"),
        ("SMA 50", close.rolling(50).mean(), "sma_50"),
        ("SMA 100", close.rolling(100).mean(), "sma_100"),
        ("SMA 200", close.rolling(200).mean(), "sma_200"),
        ("EMA 10", close.ewm(span=10, adjust=False).mean(), "ema_10"),
        ("EMA 20", close.ewm(span=20, adjust=False).mean(), "ema_20"),
        ("EMA 50", close.ewm(span=50, adjust=False).mean(), "ema_50"),
        ("EMA 100", close.ewm(span=100, adjust=False).mean(), "ema_100"),
        ("EMA 200", close.ewm(span=200, adjust=False).mean(), "ema_200"),
    ]

    for name, series, key in ma_configs:
        val = float(series.iloc[-1]) if not pd.isna(series.iloc[-1]) else curr_p
        threshold = val * 0.002
        if curr_p > (val + threshold):
            sig, score = "BUY", 1
        elif curr_p < (val - threshold):
            sig, score = "SELL", -1
        else:
            sig, score = "NEUTRAL", 0
        ma_signals[key] = {
            "name": name,
            "value": round(val, 2),
            "action": sig,
            "score": score,
        }

    # Hull MA
    hma_series = compute_hull_ma(close, period=9)
    hma_val = float(hma_series.iloc[-1]) if not pd.isna(hma_series.iloc[-1]) else curr_p
    hma_sig = "BUY" if curr_p > hma_val else ("SELL" if curr_p < hma_val else "NEUTRAL")
    ma_signals["hull_ma"] = {
        "name": "Hull MA (9)",
        "value": round(hma_val, 2),
        "action": hma_sig,
        "score": 1 if hma_sig == "BUY" else (-1 if hma_sig == "SELL" else 0),
    }

    # VWMA
    vwma_series = compute_vwma(close, volume, period=20)
    vwma_val = float(vwma_series.iloc[-1]) if not pd.isna(vwma_series.iloc[-1]) else curr_p
    vwma_sig = "BUY" if curr_p > vwma_val else ("SELL" if curr_p < vwma_val else "NEUTRAL")
    ma_signals["vwma"] = {
        "name": "VWMA (20)",
        "value": round(vwma_val, 2),
        "action": vwma_sig,
        "score": 1 if vwma_sig == "BUY" else (-1 if vwma_sig == "SELL" else 0),
    }

    # SuperTrend (10, 3)
    st_val_series, st_dir = compute_supertrend(high, low, close, period=10, multiplier=3.0)
    st_val = float(st_val_series.iloc[-1]) if not pd.isna(st_val_series.iloc[-1]) else curr_p
    st_is_up = int(st_dir.iloc[-1]) == 1
    ma_signals["supertrend"] = {
        "name": "SuperTrend (10, 3)",
        "value": round(st_val, 2),
        "action": "BUY" if st_is_up else "SELL",
        "score": 1 if st_is_up else -1,
    }

    # Ichimoku Base Line (Kijun-sen 26)
    high_26 = high.rolling(26).max()
    low_26 = low.rolling(26).min()
    kijun = (high_26 + low_26) / 2.0
    kijun_val = float(kijun.iloc[-1]) if not pd.isna(kijun.iloc[-1]) else curr_p
    kijun_sig = "BUY" if curr_p > kijun_val else ("SELL" if curr_p < kijun_val else "NEUTRAL")
    ma_signals["ichimoku_baseline"] = {
        "name": "Ichimoku Base Line (26)",
        "value": round(kijun_val, 2),
        "action": kijun_sig,
        "score": 1 if kijun_sig == "BUY" else (-1 if kijun_sig == "SELL" else 0),
    }

    # Golden Cross (EMA 50 vs EMA 200)
    ema_50 = ma_signals["ema_50"]["value"]
    ema_200 = ma_signals["ema_200"]["value"]
    is_golden = ema_50 >= ema_200
    ma_signals["golden_cross"] = {
        "name": "Golden/Death Cross (50/200)",
        "value": round(ema_50 - ema_200, 2),
        "action": "BUY" if is_golden else "SELL",
        "score": 1 if is_golden else -1,
    }

    # -------------------------------------------------------------------------
    # 2. 11 OSCILLATORS
    # -------------------------------------------------------------------------
    osc_signals: Dict[str, Dict[str, Any]] = {}

    # 1. RSI (14)
    delta = close.diff()
    gain = delta.clip(lower=0.0).rolling(window=14).mean()
    loss = (-delta.clip(upper=0.0)).rolling(window=14).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi_series = 100.0 - (100.0 / (1.0 + rs))
    rsi_val = float(rsi_series.iloc[-1]) if not pd.isna(rsi_series.iloc[-1]) else 50.0
    if rsi_val > 70:
        rsi_sig, rsi_score = "SELL", -1  # Overbought
    elif rsi_val < 30:
        rsi_sig, rsi_score = "BUY", 1    # Oversold
    elif rsi_val >= 50:
        rsi_sig, rsi_score = "BUY", 1    # Bullish momentum
    else:
        rsi_sig, rsi_score = "SELL", -1
    osc_signals["rsi_14"] = {"name": "RSI (14)", "value": round(rsi_val, 1), "action": rsi_sig, "score": rsi_score}

    # 2. Stochastic Oscillator %K & %D (14, 3, 3)
    low_14 = low.rolling(14).min()
    high_14 = high.rolling(14).max()
    stoch_k = 100.0 * ((close - low_14) / (high_14 - low_14).replace(0, np.nan)).rolling(3).mean()
    stoch_d = stoch_k.rolling(3).mean()
    stoch_k_val = float(stoch_k.iloc[-1]) if not pd.isna(stoch_k.iloc[-1]) else 50.0
    stoch_d_val = float(stoch_d.iloc[-1]) if not pd.isna(stoch_d.iloc[-1]) else 50.0
    if stoch_k_val > 80:
        stoch_sig = "SELL"
    elif stoch_k_val < 20:
        stoch_sig = "BUY"
    else:
        stoch_sig = "BUY" if stoch_k_val >= stoch_d_val else "SELL"
    osc_signals["stochastic"] = {
        "name": "Stochastic %K(14,3,3)",
        "value": round(stoch_k_val, 1),
        "action": stoch_sig,
        "score": 1 if stoch_sig == "BUY" else -1,
    }

    # 3. CCI (20)
    tp = (high + low + close) / 3.0
    tp_sma = tp.rolling(20).mean()
    mad = tp.rolling(20).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    cci = (tp - tp_sma) / (0.015 * mad.replace(0, np.nan))
    cci_val = float(cci.iloc[-1]) if not pd.isna(cci.iloc[-1]) else 0.0
    if cci_val > 100:
        cci_sig, cci_score = "BUY", 1     # Strong momentum breakout
    elif cci_val < -100:
        cci_sig, cci_score = "SELL", -1   # Downward breakout
    elif cci_val >= 0:
        cci_sig, cci_score = "BUY", 1
    else:
        cci_sig, cci_score = "SELL", -1
    osc_signals["cci_20"] = {"name": "CCI (20)", "value": round(cci_val, 1), "action": cci_sig, "score": cci_score}

    # 4. ADX (14) with +DI / -DI
    from stock_predict.core.advanced_indicators import compute_adx
    adx_series, plus_di, minus_di = compute_adx(high, low, close, period=14)
    adx_val = float(adx_series.iloc[-1]) if not pd.isna(adx_series.iloc[-1]) else 20.0
    p_di_val = float(plus_di.iloc[-1]) if not pd.isna(plus_di.iloc[-1]) else 20.0
    m_di_val = float(minus_di.iloc[-1]) if not pd.isna(minus_di.iloc[-1]) else 20.0
    if adx_val >= 25:
        adx_sig = "BUY" if p_di_val >= m_di_val else "SELL"
    else:
        adx_sig = "NEUTRAL"
    osc_signals["adx_14"] = {
        "name": "ADX (14)",
        "value": round(adx_val, 1),
        "action": adx_sig,
        "score": 1 if adx_sig == "BUY" else (-1 if adx_sig == "SELL" else 0),
    }

    # 5. Awesome Oscillator (AO)
    ao_series = compute_awesome_oscillator(high, low)
    ao_val = float(ao_series.iloc[-1]) if not pd.isna(ao_series.iloc[-1]) else 0.0
    ao_prev = float(ao_series.iloc[-2]) if len(ao_series) > 1 else ao_val
    ao_sig = "BUY" if ao_val > ao_prev else "SELL"
    osc_signals["awesome_osc"] = {
        "name": "Awesome Oscillator",
        "value": round(ao_val, 2),
        "action": ao_sig,
        "score": 1 if ao_sig == "BUY" else -1,
    }

    # 6. Momentum (MOM 10)
    mom = close - close.shift(10)
    mom_val = float(mom.iloc[-1]) if not pd.isna(mom.iloc[-1]) else 0.0
    mom_sig = "BUY" if mom_val >= 0 else "SELL"
    osc_signals["momentum_10"] = {
        "name": "Momentum (10)",
        "value": round(mom_val, 2),
        "action": mom_sig,
        "score": 1 if mom_sig == "BUY" else -1,
    }

    # 7. MACD (12, 26, 9)
    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist = macd_line - signal_line
    hist_val = float(macd_hist.iloc[-1]) if not pd.isna(macd_hist.iloc[-1]) else 0.0
    macd_sig = "BUY" if hist_val >= 0 else "SELL"
    osc_signals["macd_hist"] = {
        "name": "MACD Level (12,26,9)",
        "value": round(hist_val, 2),
        "action": macd_sig,
        "score": 1 if macd_sig == "BUY" else -1,
    }

    # 8. Stochastic RSI (14, 14, 3, 3)
    stoch_rsi_k, stoch_rsi_d = compute_stochastic_rsi(rsi_series, period=14)
    sr_k_val = float(stoch_rsi_k.iloc[-1])
    sr_d_val = float(stoch_rsi_d.iloc[-1])
    sr_sig = "BUY" if sr_k_val >= sr_d_val else "SELL"
    osc_signals["stoch_rsi"] = {
        "name": "Stoch RSI (14,14,3,3)",
        "value": round(sr_k_val, 1),
        "action": sr_sig,
        "score": 1 if sr_sig == "BUY" else -1,
    }

    # 9. Williams %R (14)
    w_r = -100.0 * ((high_14 - close) / (high_14 - low_14).replace(0, np.nan))
    wr_val = float(w_r.iloc[-1]) if not pd.isna(w_r.iloc[-1]) else -50.0
    if wr_val > -20:
        wr_sig = "SELL"
    elif wr_val < -80:
        wr_sig = "BUY"
    else:
        wr_sig = "BUY" if wr_val >= -50.0 else "SELL"
    osc_signals["williams_r"] = {
        "name": "Williams %R (14)",
        "value": round(wr_val, 1),
        "action": wr_sig,
        "score": 1 if wr_sig == "BUY" else -1,
    }

    # 10. Bull Bear Power (13)
    bull_p, bear_p = compute_bull_bear_power(high, low, close, period=13)
    bbp_val = float(bull_p.iloc[-1] + bear_p.iloc[-1])
    bbp_sig = "BUY" if bbp_val >= 0 else "SELL"
    osc_signals["bull_bear_power"] = {
        "name": "Bull Bear Power (13)",
        "value": round(bbp_val, 2),
        "action": bbp_sig,
        "score": 1 if bbp_sig == "BUY" else -1,
    }

    # 11. Ultimate Oscillator (7, 14, 28)
    ult_osc = compute_ultimate_oscillator(high, low, close)
    ult_val = float(ult_osc.iloc[-1]) if not pd.isna(ult_osc.iloc[-1]) else 50.0
    if ult_val > 70:
        ult_sig = "SELL"
    elif ult_val < 30:
        ult_sig = "BUY"
    else:
        ult_sig = "BUY" if ult_val >= 50 else "SELL"
    osc_signals["ultimate_osc"] = {
        "name": "Ultimate Oscillator",
        "value": round(ult_val, 1),
        "action": ult_sig,
        "score": 1 if ult_sig == "BUY" else -1,
    }

    # -------------------------------------------------------------------------
    # 3. CONSENSUS RATINGS SUMMARY
    # -------------------------------------------------------------------------
    ma_bull = sum(1 for item in ma_signals.values() if item["action"] == "BUY")
    ma_bear = sum(1 for item in ma_signals.values() if item["action"] == "SELL")
    ma_neut = sum(1 for item in ma_signals.values() if item["action"] == "NEUTRAL")
    ma_total = len(ma_signals)
    ma_score = round((ma_bull - ma_bear) / ma_total, 2)  # -1.0 to +1.0

    if ma_score > 0.45:
        ma_verdict = "STRONG BUY"
    elif ma_score > 0.10:
        ma_verdict = "BUY"
    elif ma_score < -0.45:
        ma_verdict = "STRONG SELL"
    elif ma_score < -0.10:
        ma_verdict = "SELL"
    else:
        ma_verdict = "NEUTRAL"

    osc_bull = sum(1 for item in osc_signals.values() if item["action"] == "BUY")
    osc_bear = sum(1 for item in osc_signals.values() if item["action"] == "SELL")
    osc_neut = sum(1 for item in osc_signals.values() if item["action"] == "NEUTRAL")
    osc_total = len(osc_signals)
    osc_score = round((osc_bull - osc_bear) / osc_total, 2)

    if osc_score > 0.45:
        osc_verdict = "STRONG BUY"
    elif osc_score > 0.10:
        osc_verdict = "BUY"
    elif osc_score < -0.45:
        osc_verdict = "STRONG SELL"
    elif osc_score < -0.10:
        osc_verdict = "SELL"
    else:
        osc_verdict = "NEUTRAL"

    # Overall Combined (26 Indicators)
    tot_bull = ma_bull + osc_bull
    tot_bear = ma_bear + osc_bear
    tot_neut = ma_neut + osc_neut
    tot_signals = ma_total + osc_total
    overall_score = round((tot_bull - tot_bear) / tot_signals, 2)

    if overall_score > 0.40:
        overall_verdict = "STRONG BUY"
        action_badge = "bg-emerald-500 text-black font-extrabold"
    elif overall_score > 0.10:
        overall_verdict = "BUY"
        action_badge = "border border-emerald-500 text-emerald-400 font-bold"
    elif overall_score < -0.40:
        overall_verdict = "STRONG SELL"
        action_badge = "bg-rose-500 text-black font-extrabold"
    elif overall_score < -0.10:
        overall_verdict = "SELL"
        action_badge = "border border-rose-500 text-rose-400 font-bold"
    else:
        overall_verdict = "NEUTRAL"
        action_badge = "border border-zinc-700 text-zinc-300 font-bold"

    # -------------------------------------------------------------------------
    # 4. DANELFIN-STYLE AI ALPHA SCORE (1.0 TO 10.0)
    # -------------------------------------------------------------------------
    # Maps overall confluence and trend strength to a unified 1.0 - 10.0 scale:
    # 5.0 is baseline market neutral; 10.0 is perfect institutional buy confluence.
    raw_alpha = 5.0 + (overall_score * 4.5)
    # Trend regime amplification: if ADX > 25, trend conviction is boosted
    if adx_val >= 25:
        raw_alpha += (0.5 if overall_score >= 0 else -0.5)
    ai_alpha_score = round(max(min(raw_alpha, 10.0), 1.0), 1)

    # -------------------------------------------------------------------------
    # 5. ADX TREND REGIME
    # -------------------------------------------------------------------------
    if adx_val >= 30:
        trend_strength = "STRONG TREND"
        trend_desc = "Market exhibits powerful directional momentum. Trend-following models hold maximum statistical validity."
    elif adx_val >= 20:
        trend_strength = "MODERATE TREND"
        trend_desc = "Consistent directional bias with intermittent counter-trend retracements."
    else:
        trend_strength = "RANGEBOUND CHOP"
        trend_desc = "Low trend strength / sideways consolidation. Favor mean-reversion and bounded volatility strategies."

    return {
        "current_price": curr_p,
        "ai_alpha_score": ai_alpha_score,
        "ai_alpha_badge": action_badge,
        "ai_alpha_verdict": overall_verdict,
        "adx_regime": {
            "adx_value": round(adx_val, 1),
            "strength": trend_strength,
            "description": trend_desc,
            "plus_di": round(p_di_val, 1),
            "minus_di": round(m_di_val, 1),
        },
        "moving_averages": {
            "bullish": ma_bull,
            "neutral": ma_neut,
            "bearish": ma_bear,
            "score": ma_score,
            "verdict": ma_verdict,
            "signals": ma_signals,
        },
        "oscillators": {
            "bullish": osc_bull,
            "neutral": osc_neut,
            "bearish": osc_bear,
            "score": osc_score,
            "verdict": osc_verdict,
            "signals": osc_signals,
        },
        "overall": {
            "bullish": tot_bull,
            "neutral": tot_neut,
            "bearish": tot_bear,
            "total_indicators": tot_signals,
            "score": overall_score,
            "verdict": overall_verdict,
            "action_badge": action_badge,
            "win_probability_pct": round(min(max(50.0 + (overall_score * 42.0), 20.0), 94.0), 1),
        },
    }
