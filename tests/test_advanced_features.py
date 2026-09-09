"""
Tests for Advanced Quantitative Modules:
1. Fractional Differentiation (Marcos López de Prado)
2. Global Macro Regime & Systemic Risk Matrix
3. Virtual Paper-Trading Execution Engine & PnL Ledger
4. Financial NLP News Sentiment Analysis
"""

import pytest
import numpy as np
import pandas as pd
import tempfile
import os

from stock_predict.core.fractional_diff import FractionalDifferentiator
from stock_predict.core.macro_regime import GlobalMacroRegime
from stock_predict.core.paper_trading import PaperTradingEngine
from stock_predict.core.news_sentiment import FinancialNewsSentimentEngine


def test_fractional_differentiation_weights():
    """Verify fractional weights decay properly and sum towards zero."""
    weights = FractionalDifferentiator.fractional_weights(d=0.4, size=10, threshold=1e-3)
    assert len(weights) > 0
    # Convolution weights are arranged in chronological order: latest price t is at [-1]
    assert weights[-1] == 1.0       # w_0 = 1.0
    assert weights[-2] == -0.4      # w_1 = -d = -0.4
    # Weights decay backwards in time
    assert abs(weights[-2]) > abs(weights[0])


def test_fractional_differentiation_transform():
    """Verify fractional differentiation preserves index and transforms series."""
    np.random.seed(42)
    prices = pd.Series(100.0 + np.cumsum(np.random.randn(150)), index=pd.date_range("2024-01-01", periods=150))
    
    diff_series = FractionalDifferentiator.differentiate(prices, d=0.45)
    assert len(diff_series) >= 100
    assert not diff_series.isna().all()
    # Memory preservation: correlation with original series should be substantial (> 0.4)
    aligned_prices = prices.loc[diff_series.index]
    corr = np.corrcoef(aligned_prices.values, diff_series.values)[0, 1]
    assert corr > 0.40


def test_fractional_diff_optimal_d():
    """Verify optimal d discovery finds a valid d between 0 and 1."""
    np.random.seed(42)
    prices = pd.Series(200.0 + np.cumsum(np.random.randn(200)), index=pd.date_range("2023-01-01", periods=200))
    
    res = FractionalDifferentiator.find_optimal_d(prices, d_range=np.linspace(0.1, 0.9, 5))
    assert "optimal_d" in res
    assert 0.0 < res["optimal_d"] <= 1.0
    assert "adf_pvalue" in res
    assert "memory_correlation" in res


def test_global_macro_regime_matrix():
    """Verify Global Macro Regime matrix computes fragility index and beta factor."""
    res = GlobalMacroRegime.get_regime_matrix()
    assert "fragility_index" in res
    assert 0.0 <= res["fragility_index"] <= 100.0
    assert any(term in res["verdict"] for term in ["CALM", "ELEVATED", "SYSTEMIC SHOCK"])
    assert 0.50 <= res["beta_discount"] <= 1.00
    assert "vix" in res
    assert "crude_wti" in res
    assert "gold" in res
    assert "eur_usd" in res


def test_paper_trading_engine():
    """Verify paper trading order execution, position updates, and PnL ledger."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger_path = os.path.join(tmpdir, "test_portfolio.json")
        engine = PaperTradingEngine(portfolio_file=ledger_path)
        
        # Test Buy Order
        order_res = engine.execute_order(
            ticker="NVDA",
            action="BUY",
            quantity=10,
            current_price=120.0,
            stop_loss=115.0,
            take_profit=130.0,
        )
        assert order_res["status"] == "FILLED"
        assert "NVDA" in engine.positions
        assert engine.positions["NVDA"]["quantity"] == 10
        assert engine.positions["NVDA"]["entry_price"] > 120.0  # Slippage added
        
        # Test Mark-to-Market
        engine.mark_to_market({"NVDA": 125.0})
        assert engine.positions["NVDA"]["unrealized_pnl"] > 0
        
        # Test Close Position
        close_res = engine.close_position("NVDA", current_price=126.0)
        assert close_res["status"] == "CLOSED"
        assert "NVDA" not in engine.positions
        assert len(engine.trade_history) == 1
        assert engine.trade_history[0]["net_pnl"] > 0


def test_financial_news_sentiment():
    """Verify headline sentiment polarity scoring."""
    sample_text = "NVIDIA reports record quarterly revenue and soaring AI chip demand, beating market expectations."
    score, polarity = FinancialNewsSentimentEngine.score_headline(sample_text)
    assert polarity == "BULLISH"
    assert score > 0
    
    bearish_text = "Global markets tumble sharply as inflation fears escalate and corporate profits plunge."
    b_score, b_polarity = FinancialNewsSentimentEngine.score_headline(bearish_text)
    assert b_polarity == "BEARISH"
    assert b_score < 0
