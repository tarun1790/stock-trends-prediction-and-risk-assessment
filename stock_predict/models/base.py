"""
Base Model Abstraction and Wrapper Interface.
Provides unified scikit-learn compatible fit, predict, predict_proba, save, and load.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union
import joblib
import numpy as np


class BaseModelWrapper(ABC):
    """
    Standard interface for all ML and PyTorch DL models.
    """

    def __init__(self, name: str, params: Optional[Dict[str, Any]] = None):
        self.name = name
        self.params = params or {}
        self.is_fitted = False

    @abstractmethod
    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "BaseModelWrapper":
        """Train the model on given data."""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict discrete class labels (0 or 1)."""
        pass

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities of shape (N, 2)."""
        pass

    def save(self, path: Union[str, Path]) -> None:
        """Persist model artifact."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Union[str, Path]) -> "BaseModelWrapper":
        """Load persisted model artifact."""
        return joblib.load(path)
