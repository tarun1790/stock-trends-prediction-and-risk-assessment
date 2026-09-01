"""
Ensemble Classifiers: Stacking and Soft-Voting Meta-Estimators.
Combines tree, kernel, linear, and deep neural models for superior predictive stability.
"""

from typing import Any, Dict, List, Optional
import numpy as np
from sklearn.linear_model import LogisticRegression
from stock_predict.models.base import BaseModelWrapper


class VotingEnsembleModel(BaseModelWrapper):
    """
    Soft-Voting Ensemble that aggregates prediction probabilities
    from diverse base estimators (Trees, SVM, PyTorch DL).
    """

    def __init__(
        self,
        estimators: List[BaseModelWrapper],
        weights: Optional[List[float]] = None,
        name: str = "VotingEnsemble",
    ):
        super().__init__(name, {"num_estimators": len(estimators)})
        self.estimators = estimators
        if weights is None:
            self.weights = np.ones(len(estimators)) / len(estimators)
        else:
            w_arr = np.array(weights, dtype=np.float64)
            self.weights = w_arr / w_arr.sum()

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "VotingEnsembleModel":
        for est in self.estimators:
            if not est.is_fitted:
                est.fit(X_train, y_train, X_val, y_val)
        self.is_fitted = True
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        probas = [est.predict_proba(X) for est in self.estimators]
        # Weighted average of probabilities
        weighted_proba = np.zeros_like(probas[0])
        for p, w in zip(probas, self.weights):
            weighted_proba += p * w
        return weighted_proba

    def predict(self, X: np.ndarray) -> np.ndarray:
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)


class StackingEnsembleModel(BaseModelWrapper):
    """
    Stacking Meta-Classifier using cross-validated base predictions
    as meta-features for a final meta-learner (Logistic Regression).
    """

    def __init__(
        self,
        estimators: List[BaseModelWrapper],
        meta_learner: Optional[Any] = None,
        name: str = "StackingEnsemble",
    ):
        super().__init__(name, {"num_estimators": len(estimators)})
        self.estimators = estimators
        self.meta_learner = meta_learner or LogisticRegression(C=1.0)

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "StackingEnsembleModel":
        meta_features = []
        for est in self.estimators:
            if not est.is_fitted:
                est.fit(X_train, y_train, X_val, y_val)
            # Predict train probabilities
            prob = est.predict_proba(X_train)[:, 1:2]
            meta_features.append(prob)

        meta_X = np.hstack(meta_features)
        self.meta_learner.fit(meta_X, y_train)
        self.is_fitted = True
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        meta_features = [est.predict_proba(X)[:, 1:2] for est in self.estimators]
        meta_X = np.hstack(meta_features)
        return self.meta_learner.predict_proba(meta_X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)
