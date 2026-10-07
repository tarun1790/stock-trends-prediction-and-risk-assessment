"""
Market Data Loader & Ingestion Engine.
Supports Yahoo Finance live downloading, Binance 24/7 feeds, local CSV datasets,
and offline caching for reproducible pipelines.
"""

from pathlib import Path
from typing import Optional, Union
import numpy as np
import pandas as pd
from stock_predict.config import DATA_DIR, PAPER_SECTORS
from stock_predict.data.sample_data import generate_sector_historical_data


import time
from typing import Dict, List, Optional, Union

_MEM_CACHE: dict = {}

# Canonical Symbol Aliases covering commodities, crypto, indices, forex, and equities
SYMBOL_ALIASES: Dict[str, str] = {
    # Commodities
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "CRUDE": "CL=F",
    "CRUDE OIL": "CL=F",
    "OIL": "CL=F",
    "WTI": "CL=F",
    "BRENT": "BZ=F",
    "NATURAL GAS": "NG=F",
    "NATGAS": "NG=F",
    "GAS": "NG=F",
    "COPPER": "HG=F",
    "PLATINUM": "PL=F",
    "PALLADIUM": "PA=F",
    "GOLD ETF": "GLD",
    "SILVER ETF": "SLV",

    # Crypto
    "BITCOIN": "BTC-USD",
    "BTC": "BTC-USD",
    "ETHEREUM": "ETH-USD",
    "ETH": "ETH-USD",
    "SOLANA": "SOL-USD",
    "SOL": "SOL-USD",
    "DOGECOIN": "DOGE-USD",
    "DOGE": "DOGE-USD",
    "RIPPLE": "XRP-USD",
    "XRP": "XRP-USD",
    "CARDANO": "ADA-USD",
    "ADA": "ADA-USD",
    "BINANCE COIN": "BNB-USD",
    "BNB": "BNB-USD",

    # Major Indices
    "NIFTY": "^NSEI",
    "NIFTY 50": "^NSEI",
    "NIFTY50": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
    "BANK NIFTY": "^NSEBANK",
    "SENSEX": "^BSESN",
    "SP500": "SPY",
    "S&P 500": "SPY",
    "S&P": "SPY",
    "NASDAQ": "QQQ",
    "NASDAQ 100": "QQQ",
    "DOW": "DIA",
    "DOW JONES": "DIA",
    "RUSSELL 2000": "IWM",

    # Indian Equities (Colloquial to NSE Ticker)
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "INFOSYS": "INFY.NS",
    "INFY": "INFY.NS",
    "HDFC": "HDFCBANK.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "TATA MOTORS": "TMPV.NS",
    "TATAMOTORS": "TMPV.NS",
    "TATAMOTORS.NS": "TMPV.NS",
    "TMPV": "TMPV.NS",
    "TATA STEEL": "TATASTEEL.NS",
    "TATASTEEL": "TATASTEEL.NS",
    "SBI": "SBIN.NS",
    "SBIN": "SBIN.NS",
    "ITC": "ITC.NS",
    "BHARTI AIRTEL": "BHARTIARTL.NS",
    "AIRTEL": "BHARTIARTL.NS",
    "BHARTIARTL": "BHARTIARTL.NS",
    "ICICI": "ICICIBANK.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "WIPRO": "WIPRO.NS",
    "LT": "LT.NS",
    "L&T": "LT.NS",
    "MARUTI": "MARUTI.NS",
    "KOTAK": "KOTAKBANK.NS",
    "KOTAKBANK": "KOTAKBANK.NS",
    "ADANI ENTERPRISES": "ADANIENT.NS",
    "ADANIENT": "ADANIENT.NS",
    "ADANI PORTS": "ADANIPORTS.NS",
    "ADANIPORTS": "ADANIPORTS.NS",
    "BAJAJ FINANCE": "BAJFINANCE.NS",
    "BAJFINANCE": "BAJFINANCE.NS",
    "ASIAN PAINTS": "ASIANPAINT.NS",
    "ASIANPAINT": "ASIANPAINT.NS",
    "TITAN": "TITAN.NS",
    "SUN PHARMA": "SUNPHARMA.NS",
    "SUNPHARMA": "SUNPHARMA.NS",

    # US Mega-Caps & Popular Global Equities
    "APPLE": "AAPL",
    "MICROSOFT": "MSFT",
    "TESLA": "TSLA",
    "NVIDIA": "NVDA",
    "GOOGLE": "GOOGL",
    "ALPHABET": "GOOGL",
    "AMAZON": "AMZN",
    "META": "META",
    "FACEBOOK": "META",
    "NETFLIX": "NFLX",
    "AMD": "AMD",
    "INTEL": "INTC",
    "QUALCOMM": "QCOM",
    "BROADCOM": "AVGO",
    "TSMC": "TSM",
    "TAIWAN SEMICONDUCTOR": "TSM",
    "ASML": "ASML",
    "BERKSHIRE": "BRK-B",
    "JPMORGAN": "JPM",
    "JPM": "JPM",
    "VISA": "V",
    "MASTERCARD": "MA",
    "WALMART": "WMT",
    "DISNEY": "DIS",
    "BOEING": "BA",
    "COCA COLA": "KO",
    "COCA-COLA": "KO",
    "COKE": "KO",
    "PEPSI": "PEP",
    "PEPSICO": "PEP",
    "NIKE": "NKE",
    "FORD": "F",
    "GENERAL MOTORS": "GM",
    "GM": "GM",
    "UBER": "UBER",
    "AIRBNB": "ABNB",
    "PALANTIR": "PLTR",
    "COINBASE": "COIN",
    "SNOWFLAKE": "SNOW",
    "ALIBABA": "BABA",
    "BABA": "BABA",
    "SONY": "SONY",
    "TOYOTA": "TM",

    # Indian Growth & Tech Equities
    "SWIGGY": "SWIGGY.NS",
    "ZOMATO": "ZOMATO.NS",
    "PAYTM": "PAYTM.NS",
    "JIO": "JIOFIN.NS",
    "JIO FINANCIAL": "JIOFIN.NS",
    "OLA": "OLAELEC.NS",
    "OLA ELECTRIC": "OLAELEC.NS",
    "NYKAA": "NYKAA.NS",

    # Forex
    "USDINR": "USDINR=X",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "USDJPY=X",
    "EURINR": "EURINR=X",
    "GBPINR": "GBPINR=X",
}


class DataLoader:
    """
    Unified Data Loader supporting live market downloads, Binance feeds,
    custom CSV files, and historical market sector data.
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
        and persists calibrated historical data.
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

    def fetch_binance_live_klines(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "1d",
        limit: int = 365,
    ) -> pd.DataFrame:
        """
        Fetch high-speed zero-auth live market klines directly from Binance public API.
        Zero credentials required, sub-second latency.
        """
        import urllib.request
        import json
        clean_sym = symbol.replace("-", "").replace("USD", "USDT").upper()
        if not clean_sym.endswith("USDT") and clean_sym in ["BTC", "ETH", "SOL", "BNB"]:
            clean_sym += "USDT"

        url = f"https://api.binance.com/api/v3/klines?symbol={clean_sym}&interval={interval}&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        cols = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_vol", "trades", "tb_base", "tb_quote", "ignore"]
        df_raw = pd.DataFrame(data, columns=cols)
        df = pd.DataFrame(index=pd.to_datetime(df_raw["open_time"], unit="ms"))
        df.index.name = "Date"
        df["Open"] = df_raw["open"].astype(float).values
        df["High"] = df_raw["high"].astype(float).values
        df["Low"] = df_raw["low"].astype(float).values
        df["Close"] = df_raw["close"].astype(float).values
        df["Volume"] = df_raw["volume"].astype(float).values
        return df

    @classmethod
    def resolve_symbol(cls, symbol: str) -> str:
        """
        Resolve colloquial names, commodity terms, company names, and un-suffixed tickers
        to canonical exchange-traded symbols.
        """
        if not symbol:
            return "AAPL"
        
        clean = symbol.strip().upper()

        # Direct alias check
        if clean in SYMBOL_ALIASES:
            return SYMBOL_ALIASES[clean]
        
        clean_norm = " ".join(clean.split())
        if clean_norm in SYMBOL_ALIASES:
            return SYMBOL_ALIASES[clean_norm]
        
        for k, v in SYMBOL_ALIASES.items():
            if clean == k or clean == v:
                return v

        # If not resolved from aliases, check if it's already an exact canonical ticker
        if (
            clean.endswith(".NS")
            or clean.endswith(".BO")
            or clean.endswith("=F")
            or clean.endswith("=X")
            or clean.startswith("^")
            or "-USD" in clean
        ):
            return clean

        # Resolve via global symbol search if query is colloquial or un-suffixed
        try:
            matches = cls.search_symbols(clean, limit=1)
            if matches and matches[0].get("symbol"):
                return matches[0]["symbol"]
        except Exception:
            pass

        return clean

    @classmethod
    def search_symbols(cls, query: str, limit: int = 8) -> List[Dict[str, str]]:
        """
        Universal symbol search across global markets with Yahoo Finance API
        and instant local matching for commodities, crypto, indices, and equities.
        """
        import urllib.request
        import urllib.parse
        import json

        if not query or not query.strip():
            return []

        clean_q = query.strip()
        clean_upper = clean_q.upper()
        results: List[Dict[str, str]] = []
        seen = set()

        # 1. Immediate local matching for commodities, crypto, indices, equities
        for name, sym in SYMBOL_ALIASES.items():
            is_match = False
            if clean_upper == name or clean_upper == sym:
                is_match = True
            elif clean_upper in name:
                is_match = True
            elif len(name) > 3 and name in clean_upper:
                is_match = True

            if is_match:
                if sym not in seen:
                    seen.add(sym)
                    asset_type = (
                        "COMMODITY" if "=F" in sym
                        else ("CRYPTO" if "-USD" in sym
                        else ("INDEX" if "^" in sym
                        else ("FOREX" if "=X" in sym else "EQUITY")))
                    )
                    results.append({
                        "symbol": sym,
                        "name": name.title(),
                        "exchange": "COMMODITY" if "=F" in sym else ("NSE" if ".NS" in sym else "GLOBAL"),
                        "type": asset_type,
                    })
                    if len(results) >= limit:
                        break

        # 2. Yahoo Finance public search
        try:
            url = f"https://query2.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(clean_q)}&quotesCount={limit}&newsCount=0"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            )
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            for item in data.get("quotes", []):
                sym = item.get("symbol")
                if not sym or sym in seen:
                    continue
                seen.add(sym)
                disp_name = item.get("shortname") or item.get("longname") or sym
                quote_type = item.get("quoteType", "EQUITY")
                exchange = item.get("exchange", "GLOBAL")

                results.append({
                    "symbol": sym,
                    "name": disp_name,
                    "exchange": exchange,
                    "type": quote_type,
                })
                if len(results) >= limit:
                    break
        except Exception:
            pass

        return results

    def fetch_live_data(
        self,
        ticker: str,
        start_date: Optional[str] = "2015-01-01",
        end_date: Optional[str] = None,
        period: Optional[str] = "5y",
        interval: str = "1d",
        force_refresh: bool = False,
        cache_ttl_seconds: Optional[float] = None,
    ) -> pd.DataFrame:
        """
        Fetch live or historical stock data from Yahoo Finance or Binance with in-memory TTL caching.

        Args:
            ticker: Stock symbol (e.g. 'AAPL', 'MSFT', 'NVDA', 'SPY', 'BTC-USD', 'GC=F', 'SI=F').
            start_date: Start date string (YYYY-MM-DD).
            end_date: End date string (YYYY-MM-DD).
            period: Lookback period string (e.g. '1y', '5y', '10y', 'max').
            interval: Bar size ('1d', '1wk', '1h').
            force_refresh: Bypass in-memory cache if True.
            cache_ttl_seconds: Custom TTL duration in seconds.

        Returns:
            Standardized DataFrame with ['Open', 'High', 'Low', 'Close', 'Volume'].
        """
        clean_ticker = self.resolve_symbol(ticker)
        safe_sym = clean_ticker.replace(":", "_").replace("/", "_").replace("\\", "_")
        cache_key = f"{clean_ticker}_{interval}_{start_date}_{period}"
        now_ts = time.time()

        # Determine optimal cache TTL based on asset type
        if cache_ttl_seconds is None:
            is_crypto = any(c in clean_ticker for c in ["BTC", "ETH", "SOL", "USDT"])
            cache_ttl = 4.0 if is_crypto else 10.0
        else:
            cache_ttl = cache_ttl_seconds

        # Fast In-Memory Cache Check (< 0.05ms)
        if not force_refresh and cache_key in _MEM_CACHE:
            last_time, cached_df = _MEM_CACHE[cache_key]
            if (now_ts - last_time) < cache_ttl:
                return cached_df.copy()

        # Direct zero-auth high-speed Binance feed for Crypto
        if clean_ticker in ["BTC-USD", "BTCUSDT", "ETH-USD", "ETHUSDT", "BTC", "ETH"]:
            try:
                df = self.fetch_binance_live_klines(symbol=clean_ticker, interval=interval, limit=365)
                cache_file = self.cache_dir / f"{safe_sym}_{interval}.csv"
                df.to_csv(cache_file)
                _MEM_CACHE[cache_key] = (now_ts, df)
                return df
            except Exception:
                pass  # Fallback to Yahoo Finance below

        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("yfinance package is required for live market data fetching.")

        cache_file = self.cache_dir / f"{safe_sym}_{interval}.csv"

        # Resilient network fetch with retry
        raw_df = pd.DataFrame()
        for attempt in range(2):
            try:
                t = yf.Ticker(clean_ticker)
                if start_date:
                    raw_df = t.history(start=start_date, end=end_date, interval=interval)
                else:
                    raw_df = t.history(period=period, interval=interval)
                if not raw_df.empty:
                    break
            except Exception:
                if attempt == 0:
                    time.sleep(0.4)

        if raw_df.empty:
            # Try searching symbol or appending .NS for Indian tickers
            alt_res = self.search_symbols(clean_ticker, limit=2)
            if alt_res and alt_res[0]["symbol"] != clean_ticker:
                try:
                    alt_sym = alt_res[0]["symbol"]
                    t_alt = yf.Ticker(alt_sym)
                    if start_date:
                        raw_df = t_alt.history(start=start_date, end=end_date, interval=interval)
                    else:
                        raw_df = t_alt.history(period=period, interval=interval)
                except Exception:
                    pass

        if not raw_df.empty:
            # Standardize columns
            df = pd.DataFrame(index=raw_df.index)
            df["Open"] = raw_df["Open"].values
            df["High"] = raw_df["High"].values
            df["Low"] = raw_df["Low"].values
            df["Close"] = raw_df["Close"].values
            df["Volume"] = (
                raw_df["Volume"].values if "Volume" in raw_df.columns else 0.0
            )

            # Persist memory & disk cache
            _MEM_CACHE[cache_key] = (now_ts, df)
            try:
                df.to_csv(cache_file)
            except Exception:
                pass
            return df

        # Fallback 1: In-memory cache
        if cache_key in _MEM_CACHE:
            return _MEM_CACHE[cache_key][1].copy()

        # Fallback 2: Disk cache
        if cache_file.exists():
            disk_df = pd.read_csv(cache_file, parse_dates=[0], index_col=0)
            _MEM_CACHE[cache_key] = (now_ts, disk_df)
            return disk_df

        raise ValueError(
            f"Unable to retrieve real-time market data for '{clean_ticker}'. "
            f"Please verify the asset symbol or exchange ticker format."
        )

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
