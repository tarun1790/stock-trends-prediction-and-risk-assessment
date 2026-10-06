"""
Synthetic and Historical Benchmark Data Generator.
Calibrated for realistic market distributions across sectors:
- Technology
- Financials
- Energy
- Materials
"""

from typing import Dict, Tuple
import numpy as np
import pandas as pd

# Sector volatility and drift calibration parameters
SECTOR_CALIBRATION: Dict[str, Dict[str, float]] = {
    "technology": {
        "start_price": 150.0,
        "drift": 0.00055,
        "volatility": 0.022,
        "mean_sma": 180.0,
        "std_sma": 45.0,
    },
    "financials": {
        "start_price": 100.0,
        "drift": 0.00035,
        "volatility": 0.015,
        "mean_sma": 120.0,
        "std_sma": 30.0,
    },
    "energy": {
        "start_price": 80.0,
        "drift": 0.00045,
        "volatility": 0.018,
        "mean_sma": 95.0,
        "std_sma": 25.0,
    },
    "healthcare": {
        "start_price": 120.0,
        "drift": 0.00038,
        "volatility": 0.014,
        "mean_sma": 140.0,
        "std_sma": 28.0,
    },
    "diversified_financials": {
        "start_price": 1471.2,
        "drift": 0.00035,
        "volatility": 0.015,
        "mean_sma": 1471.201,
        "std_sma": 1196.926,
    },
    "petroleum": {
        "start_price": 24333.4,
        "drift": 0.00045,
        "volatility": 0.018,
        "mean_sma": 243334.2,
        "std_sma": 262509.8,
    },
    "basic_metals": {
        "start_price": 6928.4,
        "drift": 0.00040,
        "volatility": 0.016,
        "mean_sma": 69284.11,
        "std_sma": 60220.95,
    },
    "non_metallic_minerals": {
        "start_price": 1872.4,
        "drift": 0.00038,
        "volatility": 0.017,
        "mean_sma": 1872.483,
        "std_sma": 2410.316,
    },
}


def generate_sector_historical_data(
    sector_key: str = "diversified_financials",
    num_days: int = 2450,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate realistic 10-year historical OHLCV daily market series for a given sector
    calibrated to statistical market distributions.

    Args:
        sector_key: Sector identifier
        num_days: Number of trading days (~245 days/year * 10 years = 2450)
        seed: Random seed for reproducible benchmarking.

    Returns:
        DataFrame with ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'].
    """
    rng = np.random.default_rng(seed)
    params = SECTOR_CALIBRATION.get(
        sector_key, SECTOR_CALIBRATION["diversified_financials"]
    )

    p0 = params["start_price"]
    mu = params["drift"]
    sigma = params["volatility"]

    # Geometric Brownian Motion with cyclical market regimes
    t = np.linspace(0, 10, num_days)
    cyclical_component = 0.15 * np.sin(2 * np.pi * t / 3.0) + 0.08 * np.cos(2 * np.pi * t / 1.5)

    daily_returns = rng.normal(loc=mu, scale=sigma, size=num_days)
    log_returns = daily_returns + np.gradient(cyclical_component)

    price_path = p0 * np.exp(np.cumsum(log_returns))

    # Construct OHLC with daily intraday spread
    intraday_vol = rng.uniform(0.005, 0.020, size=num_days)
    open_prices = price_path * (1 + rng.normal(0, 0.003, size=num_days))
    high_prices = np.maximum(open_prices, price_path) * (1 + intraday_vol)
    low_prices = np.minimum(open_prices, price_path) * (1 - intraday_vol)
    close_prices = price_path
    volume = rng.lognormal(mean=14.5, sigma=0.6, size=num_days).astype(np.int64)

    dates = pd.date_range(start="2009-11-01", periods=num_days, freq="B")

    df = pd.DataFrame(
        {
            "Date": dates,
            "Open": np.round(open_prices, 2),
            "High": np.round(high_prices, 2),
            "Low": np.round(low_prices, 2),
            "Close": np.round(close_prices, 2),
            "Volume": volume,
        }
    )
    df.set_index("Date", inplace=True)
    return df
