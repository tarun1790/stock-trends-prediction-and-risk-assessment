"""
Market Data Loader & Ingestion Engine.
Supports Yahoo Finance live downloading, local CSV datasets, TSE sector presets,
and offline caching for reproducible pipelines.
"""

from pathlib import Path
from typing import Optional, Union
import numpy as np
import pandas as pd
from stock_predict.config import DATA_DIR, PAPER_SECTORS
from stock_predict.data.sample_data import generate_sector_historical_data


class DataLoader:
    """
    Unified Data Loader supporting live market downloads, custom CSV files,
    and historical sector datasets from the IEEE research paper.
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or DATA_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load_sector_data(
        self,
        sector_key: str = "diversified_financials",
        force_refresh: bool = False,
    ) -> pd.DataFrame:
        """
        Load historical sector dataset. Uses cached CSV if present, otherwise generates
        and persists the Table 11 calibrated 10-year dataset.
        """
        if sector_key not in PAPER_SECTORS:
            raise ValueError(
                f"Unknown sector '{sector_key}'. Available: {list(PAPER_SECTORS.keys())}"
            )

        cache_file = self.cache_dir / f"{sector_key}_10yr.csv"
        if cache_file.exists() and not force_refresh:
            df = pd.read_csv(cache_file, parse_dates=["Date"], index_col="Date")
            return df

        df = generate_sector_historical_data(sector_key=sector_key, num_days=2450)
        df.to_csv(cache_file)
        return df

    def fetch_live_data(
        self,
        ticker: str,
        start_date: Optional[str] = "2015-01-01",
        end_date: Optional[str] = None,
        period: Optional[str] = "5y",
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Fetch live or historical stock data from Yahoo Finance.

        Args:
            ticker: Stock symbol (e.g. 'AAPL', 'MSFT', 'NVDA', 'SPY', 'BTC-USD').
            start_date: Start date string (YYYY-MM-DD).
            end_date: End date string (YYYY-MM-DD).
            period: Lookback period string (e.g. '1y', '5y', '10y', 'max').
            interval: Bar size ('1d', '1wk', '1h').

        Returns:
            Standardized DataFrame with ['Open', 'High', 'Low', 'Close', 'Volume'].
        """
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("yfinance package is required for live market data fetching.")

        clean_ticker = ticker.strip().upper()
        cache_file = self.cache_dir / f"{clean_ticker}_{interval}.csv"

        try:
            t = yf.Ticker(clean_ticker)
            if start_date:
                raw_df = t.history(start=start_date, end=end_date, interval=interval)
            else:
                raw_df = t.history(period=period, interval=interval)

            if raw_df.empty:
                raise ValueError(f"No market data returned for ticker '{ticker}'")

            # Standardize columns
            df = pd.DataFrame(index=raw_df.index)
            df["Open"] = raw_df["Open"].values
            df["High"] = raw_df["High"].values
            df["Low"] = raw_df["Low"].values
            df["Close"] = raw_df["Close"].values
            df["Volume"] = (
                raw_df["Volume"].values if "Volume" in raw_df.columns else 0
            )

            # Persist cache
            df.to_csv(cache_file)
            return df

        except Exception as ex:
            if cache_file.exists():
                return pd.read_csv(cache_file, parse_dates=[0], index_col=0)
            raise RuntimeError(f"Failed to fetch market data for '{ticker}': {ex}")

    def load_custom_csv(
        self,
        file_path: Union[str, Path],
        date_col: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Load and normalize arbitrary custom CSV files.
        Maps standard column names: Open, High, Low, Close, Volume.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        raw_df = pd.read_csv(path)

        # Standardize column names
        col_map = {col.lower().strip(): col for col in raw_df.columns}

        # Date column
        if date_col and date_col in raw_df.columns:
            raw_df[date_col] = pd.to_datetime(raw_df[date_col])
            raw_df.set_index(date_col, inplace=True)
        elif "date" in col_map:
            raw_df[col_map["date"]] = pd.to_datetime(raw_df[col_map["date"]])
            raw_df.set_index(col_map["date"], inplace=True)
        elif "time" in col_map:
            raw_df[col_map["time"]] = pd.to_datetime(raw_df[col_map["time"]])
            raw_df.set_index(col_map["time"], inplace=True)

        req_cols = ["open", "high", "low", "close"]
        for col in req_cols:
            if col not in col_map:
                raise ValueError(
                    f"Required column '{col}' missing in CSV. Found: {list(raw_df.columns)}"
                )

        standard_df = pd.DataFrame(index=raw_df.index)
        standard_df["Open"] = raw_df[col_map["open"]].astype(float)
        standard_df["High"] = raw_df[col_map["high"]].astype(float)
        standard_df["Low"] = raw_df[col_map["low"]].astype(float)
        standard_df["Close"] = raw_df[col_map["close"]].astype(float)
        if "volume" in col_map:
            standard_df["Volume"] = raw_df[col_map["volume"]].astype(float)
        else:
            standard_df["Volume"] = 0.0

        standard_df.dropna(inplace=True)
        return standard_df
