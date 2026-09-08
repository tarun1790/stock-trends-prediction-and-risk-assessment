"""
Comprehensive 19-Dataset Quantitative Benchmark.
Evaluates ProductionAlphaEngine across 19 global asset classes over 250 walk-forward trading days:
- US Mega-Caps & Tech Leaders (NVDA, AAPL, MSFT, AMZN, GOOGL, META, TSLA, PLTR)
- Major Indices & ETFs (SPY, QQQ, GLD, GC=F)
- Cryptocurrencies (BTC-USD)
- Indian Blue-Chip Equities (RELIANCE.NS, HDFCBANK.NS)
- IEEE Research Paper 10-Year Datasets (Diversified Financials, Petroleum, Basic Metals, Non-metallic Minerals)
"""

from typing import Any, Dict
import numpy as np
import pandas as pd
import torch
from stock_predict.data.loader import DataLoader
from stock_predict.models.production_alpha_engine import ProductionAlphaEngine

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Executing 19-Dataset Benchmark on Compute Device: {device}")


def evaluate_asset(ticker: str, test_days: int = 200) -> Dict[str, Any]:
    dl = DataLoader()
    if ticker.lower() in [
        "diversified_financials",
        "petroleum",
        "basic_metals",
        "non_metallic_minerals",
    ]:
        df = dl.load_sector_data(ticker.lower())
    else:
        df = dl.fetch_live_data(ticker)

    if len(df) < test_days + 60:
        test_days = max(len(df) - 60, 40)

    engine = ProductionAlphaEngine(confidence_cutoff=70.0)

    total_bars = 0
    acted_trades = 0
    acted_correct = 0
    mean_rev_trades = 0
    mean_rev_correct = 0
    trend_trades = 0
    trend_correct = 0
    abstained_bars = 0

    price_errors_pct = []
    conformal_hits = 0

    strategy_returns = []
    buy_hold_returns = []

    start_idx = len(df) - test_days - 1
    end_idx = len(df) - 1

    for t in range(start_idx, end_idx):
        hist_slice = df.iloc[: t + 1]
        actual_tomorrow = df.iloc[t + 1]

        curr_close = float(hist_slice["Close"].iloc[-1])
        next_close = float(actual_tomorrow["Close"])
        actual_ret = (next_close - curr_close) / curr_close
        actual_dir = 1 if next_close >= curr_close else 0

        pred = engine.predict_asset(hist_slice, ticker)

        total_bars += 1
        exp_price = pred["expected_next_price"]
        pct_err = abs(exp_price - next_close) / next_close
        price_errors_pct.append(pct_err)

        # Check Conformal 90% Bound
        c_low = pred["conformal_bounds"]["conformal_lower_90"]
        c_high = pred["conformal_bounds"]["conformal_upper_90"]
        if c_low <= next_close <= c_high:
            conformal_hits += 1

        # Check Trading Decision
        pred_dir = 1 if pred["direction"] == "UP (+1)" else 0

        if pred["acted"]:
            acted_trades += 1
            is_correct = pred_dir == actual_dir
            if is_correct:
                acted_correct += 1

            if "MEAN_REVERSION" in pred["regime"]:
                mean_rev_trades += 1
                if is_correct:
                    mean_rev_correct += 1
            elif "TREND" in pred["regime"]:
                trend_trades += 1
                if is_correct:
                    trend_correct += 1

            # Strategy return: long if UP, short if DOWN
            strat_r = actual_ret if pred_dir == 1 else -actual_ret
            strategy_returns.append(strat_r)
        else:
            abstained_bars += 1
            strategy_returns.append(0.0)  # Cash preservation

        buy_hold_returns.append(actual_ret)

    win_rate = (acted_correct / max(acted_trades, 1)) * 100.0
    conformal_coverage = (conformal_hits / total_bars) * 100.0
    mape = float(np.mean(price_errors_pct)) * 100.0
    strat_cum = float(np.prod([1.0 + r for r in strategy_returns]) - 1.0) * 100.0
    bh_cum = float(np.prod([1.0 + r for r in buy_hold_returns]) - 1.0) * 100.0

    return {
        "ticker": ticker,
        "total_bars": total_bars,
        "acted_trades": acted_trades,
        "coverage_pct": round((acted_trades / total_bars) * 100.0, 1),
        "abstained": abstained_bars,
        "selective_win_rate": round(win_rate, 2),
        "trend_trades": trend_trades,
        "trend_win_rate": round((trend_correct / max(trend_trades, 1)) * 100.0, 1),
        "mean_rev_trades": mean_rev_trades,
        "mean_rev_win_rate": round((mean_rev_correct / max(mean_rev_trades, 1)) * 100.0, 1),
        "expected_price_mape": round(mape, 2),
        "conformal_90_hit_rate": round(conformal_coverage, 1),
        "strategy_return": round(strat_cum, 2),
        "buy_hold_return": round(bh_cum, 2),
        "alpha": round(strat_cum - bh_cum, 2),
    }


if __name__ == "__main__":
    assets = [
        "SPY", "QQQ", "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "PLTR",
        "GLD", "GC=F", "BTC-USD", "RELIANCE.NS", "HDFCBANK.NS",
        "diversified_financials", "petroleum", "basic_metals", "non_metallic_minerals"
    ]

    print(f"\n==========================================================================================================")
    print(f"                         MULTI-DATASET EMPIRICAL BENCHMARK (19 ASSETS | 100 TRADING DAYS)                 ")
    print(f"==========================================================================================================")
    print(f"{'Ticker':<16} | {'Coverage':<8} | {'Win Rate':<8} | {'Trend Acc':<9} | {'MeanRev':<8} | {'Price Err':<9} | {'Conformal':<9} | {'Strategy Ret':<12} | {'Alpha':<10}")
    print(f"----------------------------------------------------------------------------------------------------------")

    results = []
    for sym in assets:
        res = evaluate_asset(sym, test_days=100)
        results.append(res)
        strat_str = f"{res['strategy_return']:+.2f}%"
        alpha_str = f"{res['alpha']:+.2f}%"
        print(f"{res['ticker']:<16} | {res['coverage_pct']:<7}% | {res['selective_win_rate']:<7}% | {res['trend_win_rate']:<8}% | {res['mean_rev_win_rate']:<7}% | {res['expected_price_mape']:<8}% | {res['conformal_90_hit_rate']:<8}% | {strat_str:<12} | {alpha_str:<10}")

    df_res = pd.DataFrame(results)
    avg_win = df_res["selective_win_rate"].mean()
    avg_mape = df_res["expected_price_mape"].mean()
    avg_conf = df_res["conformal_90_hit_rate"].mean()
    avg_strat = df_res["strategy_return"].mean()
    avg_alpha = df_res["alpha"].mean()

    print(f"==========================================================================================================")
    print(f"BENCHMARK SUMMARY ACROSS ALL 19 DATASETS:")
    print(f"  Average High-Conviction Selective Win Rate:   {avg_win:.2f}%")
    print(f"  Average Expected Price Error (MAPE):          {avg_mape:.2f}% (Price Accuracy: {100-avg_mape:.2f}%)")
    print(f"  Average 90% Conformal Coverage Hit Rate:      {avg_conf:.2f}%")
    print(f"  Average Strategy Cumulative Return:           {avg_strat:+.2f}%")
    print(f"  Average Alpha Generated over Buy & Hold:      {avg_alpha:+.2f}%")
    print(f"==========================================================================================================\n")
