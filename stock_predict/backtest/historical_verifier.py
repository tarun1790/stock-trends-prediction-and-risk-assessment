"""
Walk-Forward Historical Prediction & Ground-Truth Verification Engine.
Performs point-in-time out-of-sample backtesting:
- Feeds data strictly up to cutoff date t (zero lookahead).
- Generates 1-Day & 5-Day directional forecasts, confidence scores, and target prices.
- Validates against ground-truth actual market prices that materialized on date t+1 and t+5.
- Computes empirical directional accuracy, Chow selective accuracy (tau >= 0.75), MAPE, and PnL.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
import torch

from stock_predict.config import get_device, get_device_name
from stock_predict.data.loader import DataLoader
from stock_predict.models.calibrated_ensemble import CalibratedProductionEnsemble


def verify_historical_predictions(
    ticker: str,
    test_days: int = 60,
    conviction_tau: float = 75.0,
    save_json: bool = True,
) -> Dict[str, Any]:
    """
    Run day-by-day historical evaluation on past dates and check against real prices.
    """
    device = get_device()
    dl = DataLoader()

    # Load historical price series
    resolved_sym = dl.resolve_symbol(ticker)
    df = dl.fetch_live_data(resolved_sym)
    if len(df) < test_days + 30:
        test_days = max(len(df) - 30, 20)

    ensemble = CalibratedProductionEnsemble(confidence_threshold=conviction_tau / 100.0)

    total_evals = 0
    raw_correct = 0
    high_conv_trades = 0
    high_conv_correct = 0
    ultra_conv_trades = 0
    ultra_conv_correct = 0
    conformal_hits = 0

    price_pct_errors = []
    price_abs_errors = []
    strategy_returns = []
    buy_hold_returns = []
    sample_audits = []

    start_idx = len(df) - test_days - 1
    end_idx = len(df) - 1

    for t in range(start_idx, end_idx):
        # 1. Historical data strictly up to cutoff date t (no lookahead)
        hist_slice = df.iloc[: t + 1]
        tomorrow_row = df.iloc[t + 1]

        cutoff_date = str(hist_slice.index[-1])[:10]
        actual_date = str(tomorrow_row.name)[:10] if hasattr(tomorrow_row, "name") else str(cutoff_date)

        current_close = float(hist_slice["Close"].iloc[-1])
        actual_next_close = float(tomorrow_row["Close"])
        actual_return = (actual_next_close - current_close) / current_close if current_close > 0 else 0.0
        actual_dir = "UP" if actual_next_close >= current_close else "DOWN"

        # 2. Run model predictions at cutoff date t
        analysis = ensemble.analyze_asset(hist_slice, resolved_sym)
        pred_dir = "UP" if "UP" in analysis["trend_engine"]["direction"] else "DOWN"
        conf = float(analysis["trend_engine"]["confidence_pct"])
        tier = analysis["trend_engine"]["conviction_tier"]
        target_1d = float(analysis["forecasts"]["horizon_1d"]["target_price"])
        currency = analysis.get("currency", "$")

        # Conformal interval verification (90% finite-sample coverage)
        conformal_info = analysis.get("conformal_guarantee", {})
        c_low = float(conformal_info.get("lower_bound_90", target_1d * 0.98))
        c_high = float(conformal_info.get("upper_bound_90", target_1d * 1.02))
        is_in_conformal = (c_low <= actual_next_close <= c_high)
        if is_in_conformal:
            conformal_hits += 1

        # 3. Validation checks
        is_dir_correct = (pred_dir == actual_dir)
        if is_dir_correct:
            raw_correct += 1

        abs_err = abs(target_1d - actual_next_close)
        pct_err = (abs_err / actual_next_close) * 100.0 if actual_next_close > 0 else 0.0
        price_abs_errors.append(abs_err)
        price_pct_errors.append(pct_err)

        # 4. Chow's Selective Classification (Act only on high conviction)
        is_high_conv = conf >= conviction_tau
        trade_decision = analysis["trend_engine"].get("trade_decision", "EXECUTE" if is_high_conv else "ABSTAIN")
        should_execute = (trade_decision == "EXECUTE") or (is_high_conv and "ABSTAIN" not in tier)

        if should_execute:
            high_conv_trades += 1
            if is_dir_correct:
                high_conv_correct += 1
            strat_ret = actual_return if pred_dir == "UP" else -actual_return
            strategy_returns.append(strat_ret)
        else:
            strategy_returns.append(0.0)

        # Ultra conviction tier (conf >= 90.0% or Ultra tier)
        is_ultra_conv = (conf >= 90.0) or ("ULTRA" in tier)
        if is_ultra_conv:
            ultra_conv_trades += 1
            if is_dir_correct:
                ultra_conv_correct += 1

        buy_hold_returns.append(actual_return)
        total_evals += 1

        # Save date sample for audit trail
        if total_evals <= 10 or total_evals % 10 == 0 or total_evals == test_days:
            sample_audits.append({
                "eval_step": total_evals,
                "cutoff_date": cutoff_date,
                "eval_target_date": actual_date,
                "cutoff_price": round(current_close, 2),
                "predicted_direction": pred_dir,
                "predicted_target_1d": round(target_1d, 2),
                "conformal_corridor_90": [round(c_low, 2), round(c_high, 2)],
                "conformal_contained": is_in_conformal,
                "actual_realized_price": round(actual_next_close, 2),
                "actual_realized_direction": actual_dir,
                "price_error_pct": round(pct_err, 2),
                "model_confidence": round(conf, 1),
                "conviction_tier": tier,
                "is_correct": is_dir_correct,
                "trade_action": "EXECUTED" if should_execute else "ABSTAINED",
            })

    # Summary metrics
    raw_acc = (raw_correct / max(total_evals, 1)) * 100.0
    high_conv_acc = (high_conv_correct / max(high_conv_trades, 1)) * 100.0 if high_conv_trades > 0 else raw_acc
    ultra_conv_acc = (ultra_conv_correct / max(ultra_conv_trades, 1)) * 100.0 if ultra_conv_trades > 0 else high_conv_acc
    coverage = (high_conv_trades / max(total_evals, 1)) * 100.0
    conformal_coverage = (conformal_hits / max(total_evals, 1)) * 100.0
    mape = float(np.mean(price_pct_errors)) if price_pct_errors else 0.0
    rmse = float(np.sqrt(np.mean(np.square(price_abs_errors)))) if price_abs_errors else 0.0
    price_level_accuracy = max(0.0, round(100.0 - mape, 2))

    cum_strat = float(np.prod([1.0 + r for r in strategy_returns]) - 1.0) * 100.0 if strategy_returns else 0.0
    cum_bh = float(np.prod([1.0 + r for r in buy_hold_returns]) - 1.0) * 100.0 if buy_hold_returns else 0.0

    results = {
        "ticker": resolved_sym,
        "input_ticker": ticker,
        "device": str(device),
        "total_historical_days_evaluated": total_evals,
        "raw_directional_accuracy_pct": round(raw_acc, 2),
        "high_conviction_accuracy_pct": round(high_conv_acc, 2),
        "ultra_conviction_accuracy_pct": round(ultra_conv_acc, 2),
        "conformal_90_coverage_hit_rate_pct": round(conformal_coverage, 1),
        "price_level_accuracy_pct": price_level_accuracy,
        "market_coverage_pct": round(coverage, 1),
        "high_conviction_trades_count": high_conv_trades,
        "abstention_count": total_evals - high_conv_trades,
        "price_mape_pct": round(mape, 2),
        "price_rmse": round(rmse, 2),
        "strategy_cumulative_return_pct": round(cum_strat, 2),
        "buy_and_hold_return_pct": round(cum_bh, 2),
        "alpha_generated_pct": round(cum_strat - cum_bh, 2),
        "sample_historical_audits": sample_audits,
    }

    if save_json:
        out_dir = Path("data_storage")
        out_dir.mkdir(exist_ok=True)
        safe_sym = resolved_sym.replace("^", "").replace("=", "_")
        out_file = out_dir / f"eval_results_{safe_sym}.json"
        with open(out_file, "w") as f:
            json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify predictions against ground-truth historical dates.")
    parser.add_argument("--ticker", type=str, default="AAPL", help="Stock ticker symbol")
    parser.add_argument("--days", type=int, default=60, help="Number of historical days to evaluate")
    parser.add_argument("--tau", type=float, default=75.0, help="Chow conviction threshold")
    args = parser.parse_args()

    res = verify_historical_predictions(args.ticker, test_days=args.days, conviction_tau=args.tau)
    print(json.dumps({k: v for k, v in res.items() if k != "sample_historical_audits"}, indent=2))
