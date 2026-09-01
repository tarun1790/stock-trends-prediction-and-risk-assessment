"""
Evaluation Metrics Engine.
Computes F1-Score, Accuracy, ROC-AUC, Precision, Recall, Confusion Matrix,
and execution latency matching Section IV-A of the IEEE Access paper.
"""

from typing import Any, Dict, Optional, Tuple
import time
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    precision_score,
    recall_score,
    confusion_matrix,
    log_loss,
    brier_score_loss,
)


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
    latency_seconds: float = 0.0,
    num_samples: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Compute full suite of classification metrics.

    Equations from the paper:
        Precision = TP / (TP + FP)  [Eq 7]
        Recall = TP / (TP + FN)     [Eq 8]
        Accuracy = (TP + TN) / (TP + FP + TN + FN) [Eq 9]
        F1-Score = 2 * Precision * Recall / (Precision + Recall) [Eq 10]
        ROC-AUC: Area under the Receiver Operating Characteristic curve
    """
    acc = float(accuracy_score(y_true, y_pred))
    f1 = float(f1_score(y_true, y_pred, average="binary", zero_division=0))
    f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    precision = float(precision_score(y_true, y_pred, average="binary", zero_division=0))
    recall = float(recall_score(y_true, y_pred, average="binary", zero_division=0))

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = (0, 0, 0, 0)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()

    auc = 0.5
    ll = 0.0
    brier = 0.0
    if y_prob is not None:
        try:
            # Handle probability format (N, 2) or (N,)
            prob_pos = y_prob[:, 1] if y_prob.ndim == 2 else y_prob
            auc = float(roc_auc_score(y_true, prob_pos))
            ll = float(log_loss(y_true, y_prob, labels=[0, 1]))
            brier = float(brier_score_loss(y_true, prob_pos))
        except Exception:
            auc = 0.5

    n = num_samples or len(y_true)
    latency_per_sample_us = (
        (latency_seconds / max(n, 1)) * 1_000_000.0 if latency_seconds > 0 else 0.0
    )

    return {
        "accuracy": round(acc, 4),
        "f1_score": round(f1, 4),
        "f1_macro": round(f1_macro, 4),
        "roc_auc": round(auc, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "confusion_matrix": {
            "tp": int(tp),
            "fp": int(fp),
            "tn": int(tn),
            "fn": int(fn),
        },
        "log_loss": round(ll, 4),
        "brier_score": round(brier, 4),
        "latency_seconds": round(latency_seconds, 4),
        "latency_per_sample_us": round(latency_per_sample_us, 2),
    }
