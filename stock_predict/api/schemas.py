"""
Pydantic Request & Response Schemas for the FastAPI REST Service.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SystemStatusResponse(BaseModel):
    status: str
    version: str
    cuda_available: bool
    device: str
    gpu_name: Optional[str] = None
    available_models: List[str]
    available_sectors: List[str]


class DataFetchRequest(BaseModel):
    source: str = Field("sample", description="'sample' (TSE sector), 'ticker' (Yahoo Finance), or 'csv'")
    sector_key: Optional[str] = Field("diversified_financials", description="TSE sector key if source=='sample'")
    ticker: Optional[str] = Field(None, description="Ticker symbol (e.g. 'AAPL', 'NVDA', 'SPY') if source=='ticker'")
    start_date: Optional[str] = "2018-01-01"
    end_date: Optional[str] = None
    period: Optional[str] = "5y"


class IndicatorItem(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    sma: Optional[float] = None
    wma: Optional[float] = None
    mom: Optional[float] = None
    stck: Optional[float] = None
    stcd: Optional[float] = None
    rsi: Optional[float] = None
    sig: Optional[float] = None
    lwr: Optional[float] = None
    ado: Optional[float] = None
    cci: Optional[float] = None
    binary_signals: Optional[Dict[str, int]] = None


class IndicatorComputeResponse(BaseModel):
    total_records: int
    columns: List[str]
    records: List[Dict[str, Any]]


class ModelTrainRequest(BaseModel):
    model_name: str = Field("lstm", description="Model identifier (e.g. 'random_forest', 'xgboost', 'lstm', 'transformer', 'ensemble')")
    data_mode: str = Field("binary", description="'continuous' or 'binary'")
    sector_key: Optional[str] = "diversified_financials"
    ticker: Optional[str] = None
    sequence_length: int = 20
    test_size: float = 0.30
    epochs: int = 80
    hyperparameters: Optional[Dict[str, Any]] = None


class ModelTrainResponse(BaseModel):
    model_name: str
    data_mode: str
    metrics: Dict[str, Any]
    confusion_matrix: Dict[str, int]
    train_time_seconds: float


class BenchmarkRequest(BaseModel):
    sector_key: Optional[str] = "diversified_financials"
    ticker: Optional[str] = None
    models: Optional[List[str]] = None
    sequence_length: int = 20
    test_size: float = 0.30


class BenchmarkResponse(BaseModel):
    dataset_info: Dict[str, Any]
    continuous_results: List[Dict[str, Any]]
    binary_results: List[Dict[str, Any]]


class LivePredictRequest(BaseModel):
    ticker: str = Field("AAPL", description="Ticker symbol or 'sample'")
    model_name: str = Field("lstm", description="Model to use for inference")
    data_mode: str = Field("binary", description="'continuous' or 'binary'")


class LivePredictResponse(BaseModel):
    ticker: str
    model_name: str
    data_mode: str
    prediction_trend: str  # "UP" or "DOWN"
    prediction_signal: int  # 1 or 0
    confidence_up: float
    confidence_down: float
    last_price: float
    indicators: Dict[str, float]
    binary_signals: Dict[str, int]


class BacktestRequest(BaseModel):
    model_name: str = "lstm"
    data_mode: str = "binary"
    sector_key: Optional[str] = "diversified_financials"
    ticker: Optional[str] = None
    initial_capital: float = 100000.0
    allow_short: bool = False
    transaction_cost_pct: float = 0.001


class BacktestResponse(BaseModel):
    metrics: Dict[str, Any]
    equity_curve: Dict[str, Any]
