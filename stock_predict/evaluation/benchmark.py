"""
Comprehensive Model Benchmarking Engine.
Executes systematic comparative analysis across continuous and binary data representations
reproducing Tables 4-9 and Figures 14-16 from the IEEE Access paper.
"""

from typing import Any, Dict, List, Optional
import time
import pandas as pd
import numpy as np
from stock_predict.core.preprocessing import prepare_dataset
from stock_predict.models import (
    MODEL_REGISTRY,
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
from stock_predict.evaluation.metrics import evaluate_predictions


class BenchmarkRunner:
    """
    Automated benchmark testbed for training, validating, and comparing
    ML/DL classifiers on financial time-series.
    """

    def __init__(self, sequence_length: int = 20):
        self.sequence_length = sequence_length

    def get_default_models(self) -> Dict[str, Any]:
        """Get instantiated instances of all 11 baseline models + advanced models."""
        return {
            "Decision Tree": DecisionTreeModel(max_depth=10),
            "Random Forest": RandomForestModel(n_estimators=100, max_depth=10),
            "AdaBoost": AdaBoostModel(n_estimators=250, learning_rate=0.1, max_depth=10),
            "XGBoost": XGBoostModel(n_estimators=100, max_depth=10, learning_rate=0.1),
            "LightGBM": LightGBMModel(n_estimators=100, max_depth=10, learning_rate=0.1),
            "SVC": SVCModel(kernel="rbf", C=1.0),
            "Naive Bayes": NaiveBayesModel(),
            "KNN": KNNModel(n_neighbors=15),
            "Logistic Regression": LogisticRegressionModel(C=1.0),
            "ANN": create_ann_model(hidden_dims=[200, 100], epochs=100),
            "RNN": create_rnn_model(hidden_dim=256, epochs=60),
            "LSTM": create_lstm_model(hidden_dim=256, epochs=60),
            "GRU": create_gru_model(hidden_dim=256, epochs=60),
            "BiLSTM-Attention": create_bilstm_attention_model(hidden_dim=256, epochs=60),
            "Transformer": create_transformer_model(d_model=64, epochs=60),
        }

    def run_single_model(
        self,
        model_name: str,
        model: Any,
        data_dict: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Train and evaluate a single model on prepared data."""
        is_sequence_model = model_name in [
            "RNN", "LSTM", "GRU", "BiLSTM-Attention", "Transformer"
        ]

        if is_sequence_model and "X_seq_train" in data_dict:
            X_tr = data_dict["X_seq_train"]
            y_tr = data_dict["y_seq_train"]
            X_te = data_dict["X_seq_test"]
            y_te = data_dict["y_seq_test"]
        else:
            X_tr = data_dict["X_train"]
            y_tr = data_dict["y_train"]
            X_te = data_dict["X_test"]
            y_te = data_dict["y_test"]

        start_time = time.perf_counter()
        model.fit(X_tr, y_tr, X_te, y_te)
        train_time = time.perf_counter() - start_time

        infer_start = time.perf_counter()
        y_pred = model.predict(X_te)
        y_prob = model.predict_proba(X_te)
        infer_time = time.perf_counter() - infer_start

        metrics = evaluate_predictions(
            y_true=y_te,
            y_pred=y_pred,
            y_prob=y_prob,
            latency_seconds=infer_time,
            num_samples=len(y_te),
        )
        metrics["model_name"] = model_name
        metrics["train_time_seconds"] = round(train_time, 4)
        metrics["inference_time_seconds"] = round(infer_time, 4)
        return metrics

    def run_full_benchmark(
        self,
        df: pd.DataFrame,
        models_to_run: Optional[List[str]] = None,
        test_size: float = 0.30,
    ) -> Dict[str, Any]:
        """
        Execute full comparative benchmark on both Continuous and Binary pipelines.
        """
        # Prepare datasets
        data_cont = prepare_dataset(
            df,
            mode="continuous",
            sequence_length=self.sequence_length,
            test_size=test_size,
        )
        data_bin = prepare_dataset(
            df,
            mode="binary",
            sequence_length=self.sequence_length,
            test_size=test_size,
        )

        all_models = self.get_default_models()
        target_names = models_to_run or list(all_models.keys())

        results_continuous: List[Dict[str, Any]] = []
        results_binary: List[Dict[str, Any]] = []

        print("--> Running Continuous Data Benchmark...")
        for name in target_names:
            if name in all_models:
                m = all_models[name]
                res = self.run_single_model(name, m, data_cont)
                res["mode"] = "continuous"
                results_continuous.append(res)

        print("--> Running Binary Data Benchmark...")
        all_models_bin = self.get_default_models()
        for name in target_names:
            if name in all_models_bin:
                m = all_models_bin[name]
                res = self.run_single_model(name, m, data_bin)
                res["mode"] = "binary"
                results_binary.append(res)

        return {
            "continuous_results": results_continuous,
            "binary_results": results_binary,
            "num_samples_total": len(df),
            "num_test_samples": len(data_cont["y_test"]),
        }
