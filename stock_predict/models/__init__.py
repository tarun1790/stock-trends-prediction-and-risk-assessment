"""
Models Package: Quantitative Forecasting Models (Tree Ensembles, Classical Learners, Advanced Deep Neural Networks, and Meta-Ensembles).
"""

from stock_predict.models.base import BaseModelWrapper
from stock_predict.models.tree_models import (
    DecisionTreeModel,
    RandomForestModel,
    AdaBoostModel,
    XGBoostModel,
    LightGBMModel,
)
from stock_predict.models.traditional_models import (
    SVCModel,
    NaiveBayesModel,
    KNNModel,
    LogisticRegressionModel,
)
from stock_predict.models.neural_models import (
    PyTorchModelWrapper,
    create_ann_model,
    create_rnn_model,
    create_gru_model,
    create_transformer_model,
)
from stock_predict.models.advanced_neural import (
    PyTorchTCN,
    PyTorchTFT,
    MultiHorizonForecaster,
)
from stock_predict.models.ensemble import VotingEnsembleModel, StackingEnsembleModel


def create_tcn_model(input_dim: int = 10, epochs: int = 60, **kwargs):
    return PyTorchModelWrapper(
        model_type="tcn",
        name="TCN",
        input_dim=input_dim,
        epochs=epochs,
        **kwargs,
    )


def create_tft_model(input_dim: int = 10, epochs: int = 60, **kwargs):
    return PyTorchModelWrapper(
        model_type="tft",
        name="TFT",
        input_dim=input_dim,
        epochs=epochs,
        **kwargs,
    )


# Map model keys to factory constructors
MODEL_REGISTRY = {
    "decision_tree": DecisionTreeModel,
    "random_forest": RandomForestModel,
    "adaboost": AdaBoostModel,
    "xgboost": XGBoostModel,
    "lightgbm": LightGBMModel,
    "svc": SVCModel,
    "naive_bayes": NaiveBayesModel,
    "knn": KNNModel,
    "logistic_regression": LogisticRegressionModel,
    "ann": create_ann_model,
    "rnn": create_rnn_model,
    "gru": create_gru_model,
    "transformer": create_transformer_model,
    "tcn": create_tcn_model,
    "tft": create_tft_model,
}

__all__ = [
    "BaseModelWrapper",
    "DecisionTreeModel",
    "RandomForestModel",
    "AdaBoostModel",
    "XGBoostModel",
    "LightGBMModel",
    "SVCModel",
    "NaiveBayesModel",
    "KNNModel",
    "LogisticRegressionModel",
    "PyTorchModelWrapper",
    "create_ann_model",
    "create_rnn_model",
    "create_gru_model",
    "create_transformer_model",
    "create_tcn_model",
    "create_tft_model",
    "VotingEnsembleModel",
    "StackingEnsembleModel",
    "MODEL_REGISTRY",
]
