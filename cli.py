"""
Command-Line Interface (CLI) for Stock Market Trend Prediction Platform.
Provides terminal commands for dataset generation, indicator computation,
comparative model benchmarking, live inference, and starting the FastAPI server.
"""

import argparse
import sys
import uvicorn
import pandas as pd
from stock_predict.config import DEVICE, PAPER_SECTORS
from stock_predict.data.loader import DataLoader
from stock_predict.core.indicators import compute_all_indicators
from stock_predict.evaluation.benchmark import BenchmarkRunner
from stock_predict.backtest.backtester import BacktestEngine
from stock_predict.core.preprocessing import prepare_dataset
from stock_predict.models import MODEL_REGISTRY, create_lstm_model


def run_benchmark_cli(args):
    print(f"================================================================")
    print(f" Stock Market Trend Prediction - IEEE Access Comparative Benchmark")
    print(f" Execution Device: {DEVICE}")
    print(f" Sector/Ticker: {args.target}")
    print(f"================================================================")

    loader = DataLoader()
    if args.target in PAPER_SECTORS:
        df = loader.load_sector_data(args.target)
    else:
        df = loader.fetch_live_data(args.target)

    runner = BenchmarkRunner(sequence_length=args.sequence_length)
    res = runner.run_full_benchmark(df=df, test_size=args.test_size)

    print("\n" + "=" * 80)
    print(f"{'MODEL':<20} | {'MODE':<12} | {'F1-SCORE':<10} | {'ACCURACY':<10} | {'ROC-AUC':<10} | {'TRAIN TIME':<10}")
    print("-" * 80)

    for row in res["continuous_results"]:
        print(
            f"{row['model_name']:<20} | {'Continuous':<12} | {row['f1_score']*100:>8.2f}% | {row['accuracy']*100:>8.2f}% | {row['roc_auc']:>9.3f} | {row['train_time_seconds']:>8.2f}s"
        )
    print("-" * 80)
    for row in res["binary_results"]:
        print(
            f"{row['model_name']:<20} | {'Binary':<12} | {row['f1_score']*100:>8.2f}% | {row['accuracy']*100:>8.2f}% | {row['roc_auc']:>9.3f} | {row['train_time_seconds']:>8.2f}s"
        )
    print("=" * 80 + "\n")


def run_backtest_cli(args):
    print(f"Running strategy backtest for {args.target} using {args.model} ({args.mode})...")
    loader = DataLoader()
    if args.target in PAPER_SECTORS:
        df = loader.load_sector_data(args.target)
    else:
        df = loader.fetch_live_data(args.target)

    data = prepare_dataset(df, mode=args.mode, sequence_length=20, test_size=0.40)
    model = create_lstm_model(epochs=60) if args.model == "lstm" else MODEL_REGISTRY[args.model]()

    if args.model in ["rnn", "lstm", "gru", "bilstm_attention", "transformer"]:
        model.fit(data["X_seq_train"], data["y_seq_train"])
        preds = model.predict(data["X_seq_test"])
    else:
        model.fit(data["X_train"], data["y_train"])
        preds = model.predict(data["X_test"])

    n_eval = len(preds)
    test_prices = data["raw_df"]["Close"].iloc[-n_eval:].values
    test_dates = data["raw_df"].index[-n_eval:]

    engine = BacktestEngine(initial_capital=args.capital)
    res = engine.run_backtest(prices=test_prices, signals=preds, dates=test_dates)
    m = res["metrics"]

    print("\n" + "=" * 50)
    print(f" Quantitative Trading Strategy Performance")
    print("=" * 50)
    print(f" Initial Capital:        ${m['initial_capital']:,.2f}")
    print(f" Final Portfolio Value:  ${m['final_portfolio_value']:,.2f}")
    strat_sign = "+" if m['strategy_total_return_pct'] >= 0 else ""
    bench_sign = "+" if m['benchmark_total_return_pct'] >= 0 else ""
    print(f" Strategy Total Return:  {strat_sign}{m['strategy_total_return_pct']}%")
    print(f" Benchmark Return:       {bench_sign}{m['benchmark_total_return_pct']}%")
    print(f" Sharpe Ratio:           {m['sharpe_ratio']}")
    print(f" Sortino Ratio:          {m['sortino_ratio']}")
    print(f" Max Drawdown:           {m['max_drawdown_pct']}%")
    print(f" Win Rate:               {m['win_rate_pct']}%")
    print(f" Total Trades:           {m['num_trades']}")
    print(f" Alpha:                  {m['alpha']}")
    print(f" Beta:                   {m['beta']}")
    print("=" * 50 + "\n")


def start_server_cli(args):
    print(f"Starting StockTrend AI Platform on http://{args.host}:{args.port}")
    uvicorn.run("stock_predict.api.main:app", host=args.host, port=args.port, reload=args.reload)


def main():
    parser = argparse.ArgumentParser(description="Stock Trend Prediction Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Serve command
    server_parser = subparsers.add_parser("serve", help="Launch FastAPI server and Web UI")
    server_parser.add_argument("--host", default="127.0.0.1", help="Host interface")
    server_parser.add_argument("--port", type=int, default=8000, help="Port number")
    server_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    # Benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Run comparative model benchmark")
    bench_parser.add_argument(
        "--target",
        default="diversified_financials",
        help="Sector key ('diversified_financials', 'petroleum', etc.) or ticker ('AAPL', 'NVDA')",
    )
    bench_parser.add_argument("--sequence-length", type=int, default=20, help="Sequence window")
    bench_parser.add_argument("--test-size", type=float, default=0.30, help="Test proportion")

    # Backtest command
    bt_parser = subparsers.add_parser("backtest", help="Simulate strategy backtest")
    bt_parser.add_argument("--target", default="diversified_financials", help="Sector or ticker")
    bt_parser.add_argument("--model", default="lstm", help="Model key")
    bt_parser.add_argument("--mode", default="binary", choices=["continuous", "binary"])
    bt_parser.add_argument("--capital", type=float, default=100000.0, help="Starting capital")

    args = parser.parse_args()

    if args.command == "serve":
        start_server_cli(args)
    elif args.command == "benchmark":
        run_benchmark_cli(args)
    elif args.command == "backtest":
        run_backtest_cli(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
