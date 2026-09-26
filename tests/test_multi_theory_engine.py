import pytest
import numpy as np
import pandas as pd
from stock_predict.core.multi_theory_engine import MultiTheoryPredictor
from stock_predict.data.loader import DataLoader


@pytest.fixture
def sample_df():
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=100, freq="B")
    prices = 100.0 * np.exp(np.cumsum(np.random.normal(0.0005, 0.015, 100)))
    df = pd.DataFrame(index=dates)
    df["Open"] = prices * 0.995
    df["High"] = prices * 1.015
    df["Low"] = prices * 0.985
    df["Close"] = prices
    df["Volume"] = np.random.randint(100000, 500000, 100)
    return df


def test_multi_theory_engine_basic(sample_df):
    predictor = MultiTheoryPredictor()
    res = predictor.analyze_theories("TEST_TICKER", sample_df)

    assert "theories" in res
    assert len(res["theories"]) == 8

    # Verify all 8 theories have positive, finite target prices
    for t in res["theories"]:
        assert t["target_price"] > 0
        assert np.isfinite(t["target_price"])
        assert "name" in t
        assert "expected_return_pct" in t

    # Verify synthesized target
    synth = res["synthesized_consensus"]
    assert synth["target_price"] > 0
    assert np.isfinite(synth["target_price"])
    assert synth["theories_count"] == 8

    # Verify multi-horizon forecasts
    horizons = res["multi_horizon_forecasts"]
    for h in [1, 3, 5, 10, 20]:
        key = f"horizon_{h}d"
        assert key in horizons
        assert horizons[key]["target_price"] > 0
        assert horizons[key]["bull_target_90th"] >= horizons[key]["target_price"]
        assert horizons[key]["bear_target_10th"] <= horizons[key]["target_price"]


def test_multi_theory_real_assets():
    loader = DataLoader()
    predictor = MultiTheoryPredictor()

    for ticker in ["NVDA", "RELIANCE.NS"]:
        df = loader.fetch_live_data(ticker)
        res = predictor.analyze_theories(ticker, df)

        assert res["ticker"] == ticker
        assert res["current_price"] > 0
        assert len(res["theories"]) == 8
        assert res["synthesized_consensus"]["target_price"] > 0

        # Check that Wall Street consensus theory exists
        t1 = res["theories"][0]
        assert t1["name"] == "Wall Street & Online Consensus Theory"
        assert t1["target_price"] > 0
