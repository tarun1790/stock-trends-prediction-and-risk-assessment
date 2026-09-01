"""
Unit Tests for the 10 Technical Indicators (Table 10 of IEEE Access Paper).
"""

import numpy as np
import pandas as pd
import pytest
from stock_predict.core.indicators import (
    compute_sma,
    compute_wma,
    compute_mom,
    compute_stck,
    compute_stcd,
    compute_rsi,
    compute_macd_signal,
    compute_lwr,
    compute_ado,
    compute_cci,
    compute_all_indicators,
)


@pytest.fixture
def sample_ohlcv_data():
    """Generate 50 days of synthetic price data for indicator testing."""
    dates = pd.date_range("2020-01-01", periods=50, freq="B")
    close = np.linspace(100, 150, 50) + np.sin(np.linspace(0, 10, 50)) * 5
    high = close + 2.0
    low = close - 2.0
    open_p = close - 0.5
    volume = np.random.randint(1000, 5000, size=50)

    df = pd.DataFrame(
        {
            "Open": open_p,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": volume,
        },
        index=dates,
    )
    return df


def test_compute_sma(sample_ohlcv_data):
    close = sample_ohlcv_data["Close"]
    sma = compute_sma(close, period=10)
    assert len(sma) == len(close)
    assert np.isnan(sma.iloc[0])
    assert not np.isnan(sma.iloc[9])
    # Expected mean of first 10 close prices
    expected_10 = close.iloc[:10].mean()
    assert np.isclose(sma.iloc[9], expected_10, atol=1e-5)


def test_compute_wma(sample_ohlcv_data):
    close = sample_ohlcv_data["Close"]
    wma = compute_wma(close, period=10)
    assert len(wma) == len(close)
    assert np.isnan(wma.iloc[0])
    assert not np.isnan(wma.iloc[9])


def test_compute_mom(sample_ohlcv_data):
    close = sample_ohlcv_data["Close"]
    mom = compute_mom(close, period=10)
    assert len(mom) == len(close)
    expected_9 = close.iloc[9] - close.iloc[0]
    assert np.isclose(mom.iloc[9], expected_9, atol=1e-5)


def test_compute_stck_and_stcd(sample_ohlcv_data):
    high = sample_ohlcv_data["High"]
    low = sample_ohlcv_data["Low"]
    close = sample_ohlcv_data["Close"]

    stck = compute_stck(high, low, close, period=10)
    stcd = compute_stcd(stck, period=10)

    assert len(stck) == len(close)
    assert len(stcd) == len(close)
    assert (stck.dropna() >= 0).all() and (stck.dropna() <= 100).all()


def test_compute_rsi(sample_ohlcv_data):
    close = sample_ohlcv_data["Close"]
    rsi = compute_rsi(close, period=10)
    assert len(rsi) == len(close)
    valid_rsi = rsi.dropna()
    assert (valid_rsi >= 0).all() and (valid_rsi <= 100).all()


def test_compute_macd_signal(sample_ohlcv_data):
    close = sample_ohlcv_data["Close"]
    sig = compute_macd_signal(close, fast=12, slow=26, signal_period=9)
    assert len(sig) == len(close)
    assert not sig.dropna().empty


def test_compute_lwr(sample_ohlcv_data):
    high = sample_ohlcv_data["High"]
    low = sample_ohlcv_data["Low"]
    close = sample_ohlcv_data["Close"]
    lwr = compute_lwr(high, low, close, period=10)
    assert len(lwr) == len(close)
    assert (lwr.dropna() >= 0).all() and (lwr.dropna() <= 100).all()


def test_compute_ado(sample_ohlcv_data):
    high = sample_ohlcv_data["High"]
    low = sample_ohlcv_data["Low"]
    close = sample_ohlcv_data["Close"]
    ado = compute_ado(high, low, close)
    assert len(ado) == len(close)
    assert (ado >= 0).all() and (ado <= 1.0).all()


def test_compute_cci(sample_ohlcv_data):
    high = sample_ohlcv_data["High"]
    low = sample_ohlcv_data["Low"]
    close = sample_ohlcv_data["Close"]
    cci = compute_cci(high, low, close, period=10)
    assert len(cci) == len(close)
    assert not cci.dropna().empty


def test_compute_all_indicators(sample_ohlcv_data):
    res = compute_all_indicators(sample_ohlcv_data)
    expected_cols = [
        "SMA", "WMA", "MOM", "STCK", "STCD", "RSI", "SIG", "LWR", "ADO", "CCI"
    ]
    for col in expected_cols:
        assert col in res.columns
