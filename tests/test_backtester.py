"""
Unit Tests for Strategy Backtester Engine.
"""

import numpy as np
import pytest
from stock_predict.backtest.backtester import BacktestEngine


def test_backtest_engine_metrics():
    engine = BacktestEngine(initial_capital=100000.0, transaction_cost_pct=0.001)

    prices = np.array([100.0, 105.0, 110.0, 108.0, 112.0, 115.0, 120.0])
    signals = np.array([1, 1, 1, 0, 1, 1, 1])

    res = engine.run_backtest(prices, signals)
    assert "metrics" in res
    assert "equity_curve" in res

    m = res["metrics"]
    assert m["initial_capital"] == 100000.0
    assert m["final_portfolio_value"] > 0
    assert "sharpe_ratio" in m
    assert "sortino_ratio" in m
    assert "max_drawdown_pct" in m
    assert "win_rate_pct" in m
    assert "alpha" in m
    assert "beta" in m

    eq = res["equity_curve"]
    assert len(eq["strategy_wealth"]) == len(prices)
    assert len(eq["benchmark_wealth"]) == len(prices)


def test_backtest_mismatch_error():
    engine = BacktestEngine()
    with pytest.raises(ValueError):
        engine.run_backtest(np.array([100.0, 105.0]), np.array([1]))
