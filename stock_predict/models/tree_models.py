"""
Tree-Based Classifiers.
Implements the 4 tree models from Table 1 of the IEEE paper:
- Decision Tree
- Random Forest
- AdaBoost (with DecisionTree base estimator)
- XGBoost
Plus LightGBM as a modern state-of-the-art tree ensemble addition.
"""

from typing import Any, Dict, Optional
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import xgboost as xgb
import lightgbm as lgb
from stock_predict.models.base import BaseModelWrapper


class DecisionTreeModel(BaseModelWrapper):
    def __init__(self, max_depth: int = 10, random_state: int = 42, **kwargs):
        params = {"max_depth": max_depth, "random_state": random_state, **kwargs}
        super().__init__("DecisionTree", params)
        self.model = DecisionTreeClassifier(
            max_depth=max_depth, random_state=random_state, **kwargs
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "DecisionTreeModel":
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class RandomForestModel(BaseModelWrapper):
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 10,
        random_state: int = 42,
        n_jobs: int = -1,
        **kwargs,
    ):
        params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "random_state": random_state,
            **kwargs,
        }
        super().__init__("RandomForest", params)
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=n_jobs,
            **kwargs,
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "RandomForestModel":
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class AdaBoostModel(BaseModelWrapper):
    def __init__(
        self,
        n_estimators: int = 250,
        learning_rate: float = 0.1,
        max_depth: int = 10,
        random_state: int = 42,
        **kwargs,
    ):
        params = {
            "n_estimators": n_estimators,
            "learning_rate": learning_rate,
            "max_depth": max_depth,
            "random_state": random_state,
            **kwargs,
        }
        super().__init__("AdaBoost", params)
        base_tree = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
        self.model = AdaBoostClassifier(
            estimator=base_tree,
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=random_state,
            algorithm="SAMME",
            **kwargs,
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "AdaBoostModel":
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class XGBoostModel(BaseModelWrapper):
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 10,
        learning_rate: float = 0.1,
        random_state: int = 42,
        n_jobs: int = -1,
        **kwargs,
    ):
        params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "random_state": random_state,
            **kwargs,
        }
        super().__init__("XGBoost", params)
        self.model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=random_state,
            n_jobs=n_jobs,
            **kwargs,
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "XGBoostModel":
        eval_set = [(X_val, y_val)] if (X_val is not None and y_val is not None) else None
        self.model.fit(
            X_train,
            y_train,
            eval_set=eval_set,
            verbose=False,
        )
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class LightGBMModel(BaseModelWrapper):
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 10,
        learning_rate: float = 0.1,
        random_state: int = 42,
        n_jobs: int = -1,
        **kwargs,
    ):
        params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "random_state": random_state,
            **kwargs,
        }
        super().__init__("LightGBM", params)
        self.model = lgb.LGBMClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            n_jobs=n_jobs,
            verbose=-1,
            **kwargs,
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> "LightGBMModel":
        eval_set = [(X_val, y_val)] if (X_val is not None and y_val is not None) else None
        self.model.fit(
            X_train,
            y_train,
            eval_set=eval_set,
        )
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)
