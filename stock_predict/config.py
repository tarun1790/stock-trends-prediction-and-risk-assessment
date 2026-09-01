"""
System configuration and global parameters.
Handles hardware acceleration (GPU/CUDA auto-detection), indicator defaults,
model hyperparameters from the IEEE Access paper, and sector definitions.
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
    Get the optimal execution device, defaulting to GPU/CUDA when available.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


DEVICE = get_device()


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


# Four stock market groups from the paper
PAPER_SECTORS = {
    "diversified_financials": "Diversified Financials",
    "petroleum": "Petroleum",
    "basic_metals": "Basic Metals",
    "non_metallic_minerals": "Non-metallic Minerals",
}
