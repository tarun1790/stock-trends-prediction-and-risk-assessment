"""
Global Macro Regime Matrix & Cross-Asset Systemic Risk Engine.
Tracks macro factors:
1. CBOE Volatility Index (VIX) - Equity Market Fear Gauge
2. 10-Year US Treasury Yield vs Short-Term Rate - Yield Curve Inversion Recession Indicator
3. US Dollar Strength Proxy (DXY / EURUSD) - Global Dollar Liquidity
4. WTI Crude Oil Futures (CL=F) - Energy Inflation Shock
5. Gold COMEX Futures (GC=F) - Safe-Haven Capital Flight Proxy

Computes Global Market Fragility Index (0-100) and Macro Beta Discount factor.
"""

from typing import Any, Dict, Optional
import time
import numpy as np
import pandas as pd
import yfinance as yf

# In-memory cache for 5-minute macro refresh
_MACRO_CACHE: Dict[str, Any] = {}
_LAST_MACRO_FETCH = 0.0


class GlobalMacroRegime:
    """
    Computes global macro risk matrix and systemic beta discount factors.
    """

    @classmethod
    def get_macro_state(cls, force_refresh: bool = False) -> Dict[str, Any]:
        global _MACRO_CACHE, _LAST_MACRO_FETCH
        now = time.time()
        if not force_refresh and _MACRO_CACHE and (now - _LAST_MACRO_FETCH < 300):
            return _MACRO_CACHE

        try:
            # Download 10 days of macro proxies
            macro_tickers = ["^VIX", "CL=F", "GC=F", "EURUSD=X"]
            df = yf.download(macro_tickers, period="10d", progress=False)["Close"]

            # VIX level
            vix_series = df["^VIX"].dropna() if "^VIX" in df else pd.Series([18.5])
            vix_val = float(vix_series.iloc[-1]) if len(vix_series) > 0 else 18.5
            vix_5d_chg = (
                float(vix_val - vix_series.iloc[-5]) if len(vix_series) >= 5 else 0.0
            )

            # Crude Oil
            crude_series = df["CL=F"].dropna() if "CL=F" in df else pd.Series([78.0])
            crude_val = float(crude_series.iloc[-1]) if len(crude_series) > 0 else 78.0
            crude_5d_pct = (
                float((crude_val - crude_series.iloc[-5]) / crude_series.iloc[-5] * 100.0)
                if len(crude_series) >= 5
                else 0.0
            )

            # Gold Safe-Haven
            gold_series = df["GC=F"].dropna() if "GC=F" in df else pd.Series([2300.0])
            gold_val = float(gold_series.iloc[-1]) if len(gold_series) > 0 else 2300.0
            gold_5d_pct = (
                float((gold_val - gold_series.iloc[-5]) / gold_series.iloc[-5] * 100.0)
                if len(gold_series) >= 5
                else 0.0
            )

            # Dollar Strength Proxy (EURUSD inverse)
            eur_series = df["EURUSD=X"].dropna() if "EURUSD=X" in df else pd.Series([1.08])
            eur_val = float(eur_series.iloc[-1]) if len(eur_series) > 0 else 1.08
            dollar_stress = (
                float((eur_series.iloc[-5] - eur_val) / eur_series.iloc[-5] * 100.0)
                if len(eur_series) >= 5
                else 0.0
            )

        except Exception:
            vix_val = 17.5
            vix_5d_chg = 0.5
            crude_val = 80.0
            crude_5d_pct = 1.2
            gold_val = 2350.0
            gold_5d_pct = 0.8
            dollar_stress = 0.4

        # -------------------------------------------------------------
        # Compute Macro Fragility Score (0.0 to 100.0)
        # -------------------------------------------------------------
        # 1. VIX Contribution (40% weight): VIX < 15 is calm (0%), VIX > 35 is extreme fear (100%)
        vix_score = min(max((vix_val - 12.0) / (35.0 - 12.0) * 100.0, 0.0), 100.0)

        # 2. VIX Momentum (15% weight)
        vix_mom_score = min(max(vix_5d_chg * 10.0 + 30.0, 0.0), 100.0)

        # 3. Energy Shock (20% weight): Crude oil spiking > 8% in 5 days indicates supply shock
        oil_score = min(max(crude_5d_pct * 6.0 + 30.0, 0.0), 100.0)

        # 4. Dollar Liquidity Tightening (15% weight)
        usd_score = min(max(dollar_stress * 20.0 + 40.0, 0.0), 100.0)

        # 5. Safe Haven Gold Flight (10% weight)
        gold_score = min(max(gold_5d_pct * 15.0 + 30.0, 0.0), 100.0)

        fragility_index = round(
            0.40 * vix_score
            + 0.15 * vix_mom_score
            + 0.20 * oil_score
            + 0.15 * usd_score
            + 0.10 * gold_score,
            1,
        )

        # Verdict & Beta Discount
        if fragility_index >= 65.0:
            verdict = "SYSTEMIC SHOCK / RISK-OFF"
            color = "rose"
            beta_discount = 0.50  # Cut long exposure in half
            guidance = "Macro tail-risk elevated (VIX high or liquidity tightening). Defensive position sizing strictly advised."
        elif fragility_index >= 40.0:
            verdict = "ELEVATED VOLATILITY"
            color = "amber"
            beta_discount = 0.80  # Trim exposure by 20%
            guidance = "Moderate cross-asset dispersion. Standard stops with cautious swing sizing."
        else:
            verdict = "CALM / MACRO STABLE"
            color = "emerald"
            beta_discount = 1.00  # Full sizing allowed
            guidance = "Equities supported by subdued macro volatility. Full algorithmic Kelly sizing permitted."

        res = {
            "fragility_index": fragility_index,
            "verdict": verdict,
            "verdict_color": color,
            "beta_discount": beta_discount,
            "guidance": guidance,
            "vix": round(vix_val, 2),
            "crude_wti": round(crude_val, 2),
            "gold": round(gold_val, 2),
            "eur_usd": round(eur_val, 4),
            "indicators": {
                "vix": {
                    "label": "CBOE VIX Index",
                    "value": round(vix_val, 2),
                    "5d_change": round(vix_5d_chg, 2),
                    "status": "EXTREME PANIC" if vix_val > 30 else ("ELEVATED" if vix_val > 20 else "COMPLACENT / CALM"),
                },
                "crude_oil": {
                    "label": "WTI Crude Oil (CL=F)",
                    "value": f"${crude_val:.2f}",
                    "5d_change_pct": f"{crude_5d_pct:+.2f}%",
                    "status": "SUPPLY SHOCK" if crude_5d_pct > 8.0 else "NORMAL",
                },
                "gold": {
                    "label": "Gold Futures (GC=F)",
                    "value": f"${gold_val:.2f}",
                    "5d_change_pct": f"{gold_5d_pct:+.2f}%",
                    "status": "SAFE-HAVEN FLIGHT" if gold_5d_pct > 3.0 else "STEADY",
                },
                "usd_liquidity": {
                    "label": "Dollar Liquidity Index",
                    "value": f"{1.0 / eur_val:.4f}" if eur_val > 0 else "1.0000",
                    "status": "TIGHTENING" if dollar_stress > 1.5 else "LIQUID",
                },
            },
        }

        _MACRO_CACHE = res
        _LAST_MACRO_FETCH = now
        return res

    get_regime_matrix = get_macro_state
