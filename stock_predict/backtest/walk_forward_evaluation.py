"""
Walk-Forward Out-of-Sample Accuracy Evaluation.
Simulates day-by-day out-of-sample next-day prediction across past 250 trading days:
Predicts Day t+1 from data strictly up to Day t, then validates against actual outcome.
"""

import numpy as np
import pandas as pd
import torch
from stock_predict.data.loader import DataLoader
from stock_predict.models.calibrated_ensemble import CalibratedProductionEnsemble

# Configure PyTorch GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def run_day_by_day_walk_forward(ticker_symbol: str, test_days: int = 250, conviction_threshold: float = 75.0):
    dl = DataLoader()
    if ticker_symbol.lower() in [
        "diversified_financials",
        "petroleum",
        "basic_metals",
        "non_metallic_minerals",
    ]:
        df = dl.load_sector_data(ticker_symbol.lower())
    else:
        df = dl.fetch_live_data(ticker_symbol)

    if len(df) < test_days + 60:
        test_days = max(len(df) - 60, 50)

    ensemble = CalibratedProductionEnsemble(confidence_threshold=0.75)

    total_tested = 0
    raw_correct = 0
    selective_correct = 0
    selective_trades = 0
    selective_abstained = 0

    price_absolute_errors = []
    price_pct_errors = []

    trade_returns = []
    buy_hold_returns = []
    daily_logs = []

    # Start index for out-of-sample backtest window
    start_idx = len(df) - test_days - 1
    end_idx = len(df) - 1

    for t in range(start_idx, end_idx):
        # Window strictly up to day t (NO lookahead bias)
        hist_slice = df.iloc[: t + 1]
        actual_tomorrow = df.iloc[t + 1]

        current_close = float(hist_slice["Close"].iloc[-1])
        actual_next_close = float(actual_tomorrow["Close"])
        actual_return = (actual_next_close - current_close) / current_close
        actual_direction = 1 if actual_next_close >= current_close else 0

        # Model forecast for Day t+1
        analysis = ensemble.analyze_asset(hist_slice, ticker_symbol)
        
        pred_direction = 1 if analysis["trend_engine"]["direction"] == "UP (+1)" else 0
        conf_pct = analysis["trend_engine"]["confidence_pct"]
        adx_val = analysis["adx_regime"]["adx_value"]
        exp_next_price = analysis["forecasts"]["horizon_1d"]["target_price"]

        # 1. Raw unconstrained next-day direction test
        is_raw_correct = (pred_direction == actual_direction)
        if is_raw_correct:
            raw_correct += 1

        # 2. Selective classification (High-Conviction Filter)
        # Act when confidence >= threshold OR ADX trend is confirmed
        acted = (conf_pct >= conviction_threshold) or (adx_val >= 25.0)
        is_sel_correct = False

        if acted:
            selective_trades += 1
            is_sel_correct = (pred_direction == actual_direction)
            if is_sel_correct:
                selective_correct += 1

            strat_ret = actual_return if pred_direction == 1 else -actual_return
            trade_returns.append(strat_ret)
        else:
            selective_abstained += 1
            trade_returns.append(0.0)

        buy_hold_returns.append(actual_return)

        # Expected price accuracy
        abs_err = abs(exp_next_price - actual_next_close)
        pct_err = abs_err / actual_next_close

        price_absolute_errors.append(abs_err)
        price_pct_errors.append(pct_err)

        total_tested += 1

        # Collect sample records
        if total_tested % 50 == 0 or total_tested == test_days:
            date_str = str(actual_tomorrow.name)[:10] if hasattr(actual_tomorrow, "name") else f"Day {total_tested}"
            daily_logs.append({
                "day": total_tested,
                "date": date_str,
                "price_today": round(current_close, 2),
                "actual_tomorrow": round(actual_next_close, 2),
                "expected_tomorrow": round(exp_next_price, 2),
                "abs_error": round(abs_err, 2),
                "pct_error": round(pct_err * 100, 2),
                "predicted_dir": "UP (+1)" if pred_direction == 1 else "DOWN (-1)",
                "actual_dir": "UP (+1)" if actual_direction == 1 else "DOWN (-1)",
                "confidence": conf_pct,
                "acted": acted,
                "correct": is_sel_correct if acted else "ABSTAIN",
            })

    raw_acc = (raw_correct / total_tested) * 100.0
    sel_acc = (selective_correct / max(selective_trades, 1)) * 100.0
    coverage = (selective_trades / total_tested) * 100.0
    mape = float(np.mean(price_pct_errors)) * 100.0
    rmse = float(np.sqrt(np.mean(np.square(price_absolute_errors))))

    strat_cum = float(np.prod([1.0 + r for r in trade_returns]) - 1.0) * 100.0
    bh_cum = float(np.prod([1.0 + r for r in buy_hold_returns]) - 1.0) * 100.0

    print(f"\n=======================================================")
    print(f"  WALK-FORWARD NEXT-DAY BACKTEST RESULTS: {ticker_symbol.upper()}")
    print(f"  Evaluation Window: Past {total_tested} Consecutive Trading Days (1 Year)")
    print(f"=======================================================")
    print(f"Total Days Tested:                {total_tested}")
    print(f"Raw 1-Day Direction Accuracy:     {raw_acc:.2f}% (Forced guessing on every bar)")
    print(f"High-Conviction Selective Acc:    {sel_acc:.2f}% (Chow's Rule tau >= 0.75 / ADX >= 25)")
    print(f"Days Acted / Traded:              {selective_trades} ({coverage:.1f}% market coverage)")
    print(f"Days Abstained (Cash Mode):       {selective_abstained} ({100-coverage:.1f}% capital preservation)")
    print(f"Expected Price Mean Error (MAPE): {mape:.2f}%")
    print(f"Expected Price RMSE:              ${rmse:.2f}")
    print(f"Strategy Cumulative Return:       +{strat_cum:.2f}%")
    print(f"Buy & Hold Benchmark Return:      +{bh_cum:.2f}%")
    print(f"Alpha Generated:                  +{strat_cum - bh_cum:.2f}%")
    print(f"=======================================================")

    return {
        "ticker": ticker_symbol,
        "total_days": total_tested,
        "raw_accuracy": round(raw_acc, 2),
        "selective_accuracy": round(sel_acc, 2),
        "coverage": round(coverage, 1),
        "mape": round(mape, 2),
        "rmse": round(rmse, 2),
        "strategy_return": round(strat_cum, 2),
        "buy_hold_return": round(bh_cum, 2),
        "sample_logs": daily_logs,
    }


if __name__ == "__main__":
    assets = ["SPY", "NVDA", "AAPL", "MSFT", "diversified_financials"]
    for a in assets:
        run_day_by_day_walk_forward(a, test_days=250)

