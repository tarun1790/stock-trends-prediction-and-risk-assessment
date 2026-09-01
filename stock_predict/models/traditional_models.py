"""
Traditional Supervised Learning Classifiers.
Implements the 4 traditional models from Table 2 of the IEEE paper:
- Support Vector Classifier (SVC: RBF, Poly, Sigmoid, Linear)
- Naïve Bayes (GaussianNB)
- K-Nearest Neighbors (KNN)
- Logistic Regression
"""

from typing import Any, Dict, Optional
import numpy as np
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from stock_predict.models.base import BaseModelWrapper


class SVCModel(BaseModelWrapper):
    def __init__(
        self,
        kernel: str = "rbf",
        C: float = 1.0,
        gamma: str = "scale",
        degree: int = 3,
        random_state: int = 42,
        **kwargs,
    ):
        params = {
            "kernel": kernel,
            "C": C,
            "gamma": gamma,
            "degree": degree,
            "random_state": random_state,
            **kwargs,
        }
        super().__init__("SVC", params)
        self.model = SVC(
            kernel=kernel,
            C=C,
            gamma=gamma,
            degree=degree,
            probability=True,
            random_state=random_state,
            **kwargs,
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "SVCModel":
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class NaiveBayesModel(BaseModelWrapper):
    def __init__(self, var_smoothing: float = 1e-9, **kwargs):
        params = {"var_smoothing": var_smoothing, **kwargs}
        super().__init__("NaiveBayes", params)
        self.model = GaussianNB(var_smoothing=var_smoothing, **kwargs)

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "NaiveBayesModel":
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class KNNModel(BaseModelWrapper):
    def __init__(
        self,
        n_neighbors: int = 15,
        weights: str = "uniform",
        algorithm: str = "auto",
        metric: str = "minkowski",
        p: int = 2,
        **kwargs,
    ):
        params = {
            "n_neighbors": n_neighbors,
            "weights": weights,
            "algorithm": algorithm,
            "metric": metric,
            "p": p,
            **kwargs,
        }
        super().__init__("KNN", params)
        self.model = KNeighborsClassifier(
            n_neighbors=n_neighbors,
            weights=weights,
            algorithm=algorithm,
            metric=metric,
            p=p,
            **kwargs,
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "KNNModel":
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class LogisticRegressionModel(BaseModelWrapper):
    def __init__(
        self,
        C: float = 1.0,
        penalty: str = "l2",
        tol: float = 1e-4,
        max_iter: int = 1000,
        random_state: int = 42,
        **kwargs,
    ):
        params = {
            "C": C,
            "penalty": penalty,
            "tol": tol,
            "max_iter": max_iter,
            "random_state": random_state,
            **kwargs,
        }
        super().__init__("LogisticRegression", params)
        self.model = LogisticRegression(
            C=C,
            penalty=penalty,
            tol=tol,
            max_iter=max_iter,
            random_state=random_state,
            **kwargs,
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "LogisticRegressionModel":
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)
