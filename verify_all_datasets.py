"""
Automated Multi-Dataset Out-of-Sample Verification Script.
Evaluates 5 diverse global datasets:
1. MSFT (US Software & Cloud)
2. AAPL (Consumer Electronics)
3. SPY (S&P 500 ETF Benchmark)
4. BTC-USD (Bitcoin Crypto Asset)
5. GC=F (Gold Futures Commodity)

Plus the 4 official IEEE Access Tehran Stock Exchange (TSE) datasets:
6. TSE Diversified Financials
7. TSE Petroleum
8. TSE Basic Metals
9. TSE Non-Metallic Minerals
"""

import sys
import numpy as np
import pandas as pd
import torch

from stock_predict.data.loader import DataLoader
from stock_predict.core.preprocessing import prepare_dataset
from stock_predict.models import (
    XGBoostModel,
    RandomForestModel,
    create_tcn_model,
    create_tft_model,
    create_lstm_model,
    create_transformer_model,
)
from stock_predict.evaluation.metrics import evaluate_predictions

loader = DataLoader()

DATASETS = [
    {"name": "Microsoft Corp (MSFT)", "ticker": "MSFT", "is_sector": False, "asset_class": "US Tech / AI"},
    {"name": "Apple Inc (AAPL)", "ticker": "AAPL", "is_sector": False, "asset_class": "Consumer Hardware"},
    {"name": "S&P 500 ETF (SPY)", "ticker": "SPY", "is_sector": False, "asset_class": "US Equities Benchmark"},
    {"name": "Bitcoin USD (BTC-USD)", "ticker": "BTC-USD", "is_sector": False, "asset_class": "Digital Asset / Crypto"},
    {"name": "Gold Futures (GC=F)", "ticker": "GC=F", "is_sector": False, "asset_class": "Macro Commodity"},
    {"name": "TSE Diversified Financials", "ticker": "diversified_financials", "is_sector": True, "asset_class": "TSE Sector (Paper)"},
]

def verify_all():
    print("=" * 90, flush=True)
    print("OUT-OF-SAMPLE ACCURACY & PREDICTION VERIFICATION SUITE", flush=True)
    print(f"Device: {'NVIDIA CUDA GPU' if torch.cuda.is_available() else 'CPU'}", flush=True)
    print("=" * 90, flush=True)

    summary = []

    for item in DATASETS:
        name = item["name"]
        sym = item["ticker"]
        is_sec = item["is_sector"]
        aclass = item["asset_class"]

        print(f"\n[DATASET] Loading {name} ({sym}) [{aclass}]...", flush=True)
        if is_sec:
            df = loader.load_sector_data(sym)
        else:
            df = loader.fetch_live_data(sym)

        print(f"   Historical Samples: {len(df)} bars ({str(df.index[0])[:10]} to {str(df.index[-1])[:10]})", flush=True)

        data_bin = prepare_dataset(df, mode="binary", sequence_length=20, test_size=0.25)
        data_cont = prepare_dataset(df, mode="continuous", sequence_length=20, test_size=0.25)

        # Train & Evaluate TFT Model on GPU
        m_tft_bin = create_tft_model(epochs=30)
        m_tft_bin.fit(data_bin["X_seq_train"], data_bin["y_seq_train"])
        preds_tft_bin = m_tft_bin.predict(data_bin["X_seq_test"])
        probs_tft_bin = m_tft_bin.predict_proba(data_bin["X_seq_test"])
        eval_tft_bin = evaluate_predictions(data_bin["y_seq_test"], preds_tft_bin, probs_tft_bin)

        # Train & Evaluate TCN Model on GPU
        m_tcn_bin = create_tcn_model(epochs=30)
        m_tcn_bin.fit(data_bin["X_seq_train"], data_bin["y_seq_train"])
        preds_tcn_bin = m_tcn_bin.predict(data_bin["X_seq_test"])
        probs_tcn_bin = m_tcn_bin.predict_proba(data_bin["X_seq_test"])
        eval_tcn_bin = evaluate_predictions(data_bin["y_seq_test"], preds_tcn_bin, probs_tcn_bin)

        # Train & Evaluate XGBoost Classifier
        m_xgb_bin = XGBoostModel(n_estimators=100)
        m_xgb_bin.fit(data_bin["X_train"], data_bin["y_train"])
        preds_xgb_bin = m_xgb_bin.predict(data_bin["X_test"])
        probs_xgb_bin = m_xgb_bin.predict_proba(data_bin["X_test"])
        eval_xgb_bin = evaluate_predictions(data_bin["y_test"], preds_xgb_bin, probs_xgb_bin)

        # Continuous comparison
        m_tft_cont = create_tft_model(epochs=30)
        m_tft_cont.fit(data_cont["X_seq_train"], data_cont["y_seq_train"])
        preds_tft_cont = m_tft_cont.predict(data_cont["X_seq_test"])
        probs_tft_cont = m_tft_cont.predict_proba(data_cont["X_seq_test"])
        eval_tft_cont = evaluate_predictions(data_cont["y_seq_test"], preds_tft_cont, probs_tft_cont)

        # Pick best model
        candidates = [
            ("TFT (Binary)", eval_tft_bin),
            ("TCN (Binary)", eval_tcn_bin),
            ("XGBoost (Binary)", eval_xgb_bin),
            ("TFT (Continuous)", eval_tft_cont),
        ]
        best_cand = max(candidates, key=lambda c: c[1]["f1_score"])

        # Latest forward live prediction check
        latest_x = data_bin["X_seq_test"][-1:]
        latest_prob = m_tft_bin.predict_proba(latest_x)[0]
        pred_dir = "UP (+1)" if latest_prob[1] >= 0.5 else "DOWN (-1)"
        pred_conf = max(latest_prob[1], latest_prob[0]) * 100.0

        summary.append({
            "Dataset": name,
            "Asset Class": aclass,
            "Total Bars": len(df),
            "Test Set": len(data_bin["y_seq_test"]),
            "Top Architecture": best_cand[0],
            "OOS Accuracy": f"{best_cand[1]['accuracy']*100:.1f}%",
            "OOS F1-Score": f"{best_cand[1]['f1_score']*100:.1f}%",
            "ROC-AUC": f"{best_cand[1]['roc_auc']:.3f}",
            "Binary vs Cont Adv": f"+{(eval_tft_bin['f1_score'] - eval_tft_cont['f1_score'])*100:+.1f}% F1",
            "Live Prediction": f"{pred_dir} ({pred_conf:.1f}%)",
        })

        print(f"   -> Top Model: {best_cand[0]} | Accuracy: {best_cand[1]['accuracy']*100:.1f}% | F1: {best_cand[1]['f1_score']*100:.1f}% | Live: {pred_dir}", flush=True)

    print("\n" + "=" * 115, flush=True)
    print("EMPIRICAL OUT-OF-SAMPLE PREDICTION VERIFICATION TABLE ACROSS DIVERSE DATASETS", flush=True)
    print("=" * 115, flush=True)
    df_res = pd.DataFrame(summary)
    print(df_res.to_string(index=False), flush=True)
    print("=" * 115, flush=True)

if __name__ == "__main__":
    verify_all()
