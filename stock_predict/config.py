"""
System configuration and global parameters.
Handles hardware acceleration (dynamic GPU/CUDA, MPS, CPU detection),
technical indicator parameters, and model hyperparameters.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import torch

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data_storage"
SAVED_MODELS_DIR = BASE_DIR / "saved_models"

DATA_DIR.mkdir(parents=True, exist_ok=True)
SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)


def get_device() -> torch.device:
    """
    Get the optimal execution device, defaulting to GPU/CUDA when available,
    Apple Silicon MPS if on macOS, or high-performance CPU multi-threading.
    Ensures seamless execution on any laptop hardware.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def get_device_name() -> str:
    """
    Get the human-readable name of the active compute device dynamically.
    """
    if torch.cuda.is_available():
        return f"{torch.cuda.get_device_name(0)} (CUDA)"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "Apple Silicon GPU (MPS)"
    return "Universal CPU Multi-Thread"


DEVICE = get_device()
DEVICE_NAME = get_device_name()


@dataclass
class IndicatorConfig:
    """Configuration parameters for the 10 technical indicators."""
    sma_period: int = 10
    wma_period: int = 10
    mom_period: int = 10
    stck_period: int = 10
    stcd_period: int = 10
    rsi_period: int = 10
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    lwr_period: int = 10
    ado_period: int = 10
    cci_period: int = 10


@dataclass
class PreprocessingConfig:
    """Data preprocessing and sequence configuration."""
    test_size: float = 0.30
    random_state: int = 42
    sequence_length: int = 20  # Days of lookback for recurrent models (1 to 30)
    normalize_continuous: bool = True
    feature_columns: List[str] = field(
        default_factory=lambda: [
            "SMA", "WMA", "MOM", "STCK", "STCD", "RSI", "SIG", "LWR", "ADO", "CCI"
        ]
    )


# Market sector presets
PAPER_SECTORS = {
    "technology": "Technology",
    "financials": "Financials",
    "energy": "Energy",
    "healthcare": "Healthcare",
    "diversified_financials": "Financials",
    "petroleum": "Energy",
    "basic_metals": "Materials",
    "non_metallic_minerals": "Industrials",
}
