"""
Unit Tests for Advanced Features: TCN, TFT, Multi-Horizon, and Risk Backtester.
"""

import numpy as np
import pandas as pd
import pytest
import torch
from stock_predict.core.advanced_indicators import (
    compute_atr,
    compute_bollinger_bands,
    compute_adx,
    compute_cmf,
    compute_vwap,
    compute_parkinson_volatility,
    compute_fractional_differentiation,
    compute_full_quant_features,
)
from stock_predict.models.advanced_neural import (
    PyTorchTCN,
    PyTorchTFT,
    MultiHorizonForecaster,
)
from stock_predict.evaluation.explainability import compute_feature_saliency
from stock_predict.backtest.advanced_backtester import AdvancedRiskBacktester
from stock_predict.models.neural_models import create_lstm_model


@pytest.fixture
def ohlcv_df():
    dates = pd.date_range("2021-01-01", periods=100, freq="B")
    close = np.linspace(100, 150, 100) + np.sin(np.linspace(0, 10, 100)) * 5
    high = close + 2.0
    low = close - 2.0
    open_p = close - 0.5
    vol = np.random.randint(1000, 5000, size=100)
    return pd.DataFrame(
        {"Open": open_p, "High": high, "Low": low, "Close": close, "Volume": vol},
        index=dates,
    )


def test_advanced_indicators(ohlcv_df):
    quant_df = compute_full_quant_features(ohlcv_df)
    expected = ["ATR", "BB_MID", "BB_PCT_B", "ADX", "CMF", "VWAP", "PARK_VOL", "FRAC_DIFF"]
    for col in expected:
        assert col in quant_df.columns
    assert not quant_df["ATR"].dropna().empty


def test_tcn_and_tft_forward():
    x = torch.randn(8, 20, 10)
    tcn = PyTorchTCN(input_dim=10, num_channels=[32, 32])
    out_tcn = tcn(x)
    assert out_tcn.shape == (8, 2)

    tft = PyTorchTFT(input_dim=10, hidden_dim=32)
    out_tft, var_w, attn_w = tft(x)
    assert out_tft.shape == (8, 2)
    assert var_w.shape[0] == 8


def test_multi_horizon_forecaster():
    X_seq = np.random.randn(80, 15, 10).astype(np.float32)
    prices = np.linspace(100, 150, 80)
    forecaster = MultiHorizonForecaster(input_dim=10, epochs=2, batch_size=16)
    forecaster.fit(X_seq, prices)
    fcasts = forecaster.predict_multi_horizon(X_seq[-1:])
    assert "horizon_1d" in fcasts
    assert "horizon_5d" in fcasts
    assert "horizon_20d" in fcasts


def test_explainability(ohlcv_df):
    model = create_lstm_model(hidden_dim=32, epochs=2)
    X = np.random.randn(20, 10, 10).astype(np.float32)
    y = np.random.randint(0, 2, size=20)
    model.fit(X, y)

    res = compute_feature_saliency(
        model_wrapper=model,
        input_sample=X[-1:],
        feature_names=["SMA", "WMA", "MOM", "STCK", "STCD", "RSI", "SIG", "LWR", "ADO", "CCI"],
    )
    assert "feature_importance" in res
    assert "temporal_weights" in res
    assert len(res["feature_importance"]) == 10


def test_advanced_risk_backtest():
    prices = np.linspace(100, 130, 50)
    signals = np.random.randint(0, 2, size=50)
    engine = AdvancedRiskBacktester(initial_capital=100000.0)
    res = engine.run_risk_managed_backtest(prices, signals)
    assert "metrics" in res
    assert "monte_carlo" in res
    assert res["metrics"]["var_95_pct"] is not None
