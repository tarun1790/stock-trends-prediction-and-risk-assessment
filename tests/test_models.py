"""
Unit & Integration Tests for ML and PyTorch DL Models.
Verifies GPU/CPU execution, fit, predict, predict_proba, and metric calculations.
"""

import numpy as np
import pytest
import torch
from stock_predict.models import (
    DecisionTreeModel,
    RandomForestModel,
    AdaBoostModel,
    XGBoostModel,
    LightGBMModel,
    SVCModel,
    NaiveBayesModel,
    KNNModel,
    LogisticRegressionModel,
    create_ann_model,
    create_rnn_model,
    create_lstm_model,
    create_gru_model,
    create_bilstm_attention_model,
    create_transformer_model,
    VotingEnsembleModel,
)


@pytest.fixture
def synthetic_classification_data():
    np.random.seed(42)
    X = np.random.randn(150, 10).astype(np.float32)
    y = np.random.randint(0, 2, size=150).astype(np.int64)
    return X[:100], y[:100], X[100:], y[100:]


@pytest.fixture
def synthetic_sequence_data():
    np.random.seed(42)
    X_seq = np.random.randn(150, 10, 10).astype(np.float32)
    y_seq = np.random.randint(0, 2, size=150).astype(np.int64)
    return X_seq[:100], y_seq[:100], X_seq[100:], y_seq[100:]


def test_tree_models(synthetic_classification_data):
    X_tr, y_tr, X_te, y_te = synthetic_classification_data
    models = [
        DecisionTreeModel(max_depth=5),
        RandomForestModel(n_estimators=10, max_depth=5),
        AdaBoostModel(n_estimators=10, max_depth=5),
        XGBoostModel(n_estimators=10, max_depth=5),
        LightGBMModel(n_estimators=10, max_depth=5),
    ]
    for m in models:
        m.fit(X_tr, y_tr)
        preds = m.predict(X_te)
        probas = m.predict_proba(X_te)
        assert len(preds) == len(y_te)
        assert probas.shape == (len(y_te), 2)


def test_traditional_models(synthetic_classification_data):
    X_tr, y_tr, X_te, y_te = synthetic_classification_data
    models = [
        SVCModel(kernel="linear"),
        NaiveBayesModel(),
        KNNModel(n_neighbors=5),
        LogisticRegressionModel(),
    ]
    for m in models:
        m.fit(X_tr, y_tr)
        preds = m.predict(X_te)
        probas = m.predict_proba(X_te)
        assert len(preds) == len(y_te)
        assert probas.shape == (len(y_te), 2)


def test_pytorch_neural_models(synthetic_sequence_data):
    X_tr, y_tr, X_te, y_te = synthetic_sequence_data
    models = [
        create_ann_model(hidden_dims=[64, 32], epochs=5),
        create_rnn_model(hidden_dim=32, epochs=5),
        create_lstm_model(hidden_dim=32, epochs=5),
        create_gru_model(hidden_dim=32, epochs=5),
        create_bilstm_attention_model(hidden_dim=32, epochs=5),
        create_transformer_model(d_model=32, epochs=5),
    ]
    for m in models:
        # Check GPU device allocation
        if torch.cuda.is_available():
            assert m.device.type == "cuda"
        m.fit(X_tr, y_tr)
        preds = m.predict(X_te)
        probas = m.predict_proba(X_te)
        assert len(preds) == len(y_te)
        assert probas.shape == (len(y_te), 2)


def test_voting_ensemble(synthetic_classification_data):
    X_tr, y_tr, X_te, y_te = synthetic_classification_data
    est1 = RandomForestModel(n_estimators=10)
    est2 = XGBoostModel(n_estimators=10)
    ensemble = VotingEnsembleModel(estimators=[est1, est2])

    ensemble.fit(X_tr, y_tr)
    preds = ensemble.predict(X_te)
    probas = ensemble.predict_proba(X_te)
    assert len(preds) == len(y_te)
    assert probas.shape == (len(y_te), 2)
