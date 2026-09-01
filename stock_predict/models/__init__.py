"""
Models Package: 11 Baseline Models from the IEEE Paper + Advanced DL/Ensembles.
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
    create_lstm_model,
    create_gru_model,
    create_bilstm_attention_model,
    create_transformer_model,
)
from stock_predict.models.ensemble import VotingEnsembleModel, StackingEnsembleModel

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
    "lstm": create_lstm_model,
    "gru": create_gru_model,
    "bilstm_attention": create_bilstm_attention_model,
    "transformer": create_transformer_model,
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
    "create_lstm_model",
    "create_gru_model",
    "create_bilstm_attention_model",
    "create_transformer_model",
    "VotingEnsembleModel",
    "StackingEnsembleModel",
    "MODEL_REGISTRY",
]
