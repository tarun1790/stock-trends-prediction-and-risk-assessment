"""
Automated Multi-Dataset Out-of-Sample Verification Script.
Tests 5 diverse market datasets across different asset classes:
1. MSFT (US Mega-Cap Software & AI)
2. RELIANCE.NS (Indian Blue-Chip Conglomerate)
3. SPY (S&P 500 Broad Market ETF)
4. BTC-USD (Cryptocurrency Digital Asset)
5. GC=F (Gold Futures Macro Commodity)

Evaluates Out-of-Sample (OOS) directional accuracy, F1-score, precision, recall,
and compares Continuous vs Binary feature representation on NVIDIA CUDA GPU.
"""

import time
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
    VotingEnsembleModel,
)
from stock_predict.evaluation.metrics import evaluate_predictions

loader = DataLoader()

DATASETS_TO_TEST = [
    {"name": "Microsoft Corp (MSFT)", "ticker": "MSFT", "asset_class": "US Mega-Cap Tech"},
    {"name": "Reliance Industries (RELIANCE.NS)", "ticker": "RELIANCE.NS", "asset_class": "Indian Blue-Chip Equity"},
    {"name": "S&P 500 Index ETF (SPY)", "ticker": "SPY", "asset_class": "US Market Benchmark ETF"},
    {"name": "Bitcoin USD (BTC-USD)", "ticker": "BTC-USD", "asset_class": "Crypto / Digital Asset"},
    {"name": "Gold Futures (GC=F)", "ticker": "GC=F", "asset_class": "Commodity / Safe Haven"},
]

def run_dataset_verification():
    print("=" * 80)
    print("OUT-OF-SAMPLE ACCURACY & PREDICTION VERIFICATION ACROSS 5 DATASETS")
    print(f"Hardware: {'NVIDIA CUDA GPU' if torch.cuda.is_available() else 'CPU'}")
    print("=" * 80)

    summary_rows = []

    for d in DATASETS_TO_TEST:
        ticker = d["ticker"]
        name = d["name"]
        asset_class = d["asset_class"]
        print(f"\n---> Fetching & Preparing Dataset: {name} ({ticker}) [{asset_class}]...")

        try:
            df = loader.fetch_live_data(ticker)
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            continue

        print(f"     Total Historical Records: {len(df)} days | Range: {str(df.index[0])[:10]} to {str(df.index[-1])[:10]}")

        # 1. Binary Preprocessing Dataset
        data_bin = prepare_dataset(df, mode="binary", sequence_length=20, test_size=0.30)
        # 2. Continuous Preprocessing Dataset
        data_cont = prepare_dataset(df, mode="continuous", sequence_length=20, test_size=0.30)

        # Models to evaluate
        models = [
            ("TFT (Temporal Fusion Transformer)", lambda: create_tft_model(epochs=35), True),
            ("TCN (Dilated ConvNet)", lambda: create_tcn_model(epochs=35), True),
            ("LSTM (Deep Recurrent)", lambda: create_lstm_model(epochs=35), True),
            ("Transformer Classifier", lambda: create_transformer_model(epochs=35), True),
            ("XGBoost Classifier", lambda: XGBoostModel(n_estimators=100), False),
            ("Random Forest", lambda: RandomForestModel(n_estimators=100), False),
        ]

        best_model_name = ""
        best_f1 = 0.0
        best_acc = 0.0
        best_mode = ""

        for m_name, factory, is_seq in models:
            # Test Binary Mode
            m_bin = factory()
            if is_seq:
                m_bin.fit(data_bin["X_seq_train"], data_bin["y_seq_train"])
                preds_bin = m_bin.predict(data_bin["X_seq_test"])
                probs_bin = m_bin.predict_proba(data_bin["X_seq_test"])
                y_true = data_bin["y_seq_test"]
            else:
                m_bin.fit(data_bin["X_train"], data_bin["y_train"])
                preds_bin = m_bin.predict(data_bin["X_test"])
                probs_bin = m_bin.predict_proba(data_bin["X_test"])
                y_true = data_bin["y_test"]

            res_bin = evaluate_predictions(y_true, preds_bin, probs_bin)

            # Test Continuous Mode
            m_cont = factory()
            if is_seq:
                m_cont.fit(data_cont["X_seq_train"], data_cont["y_seq_train"])
                preds_cont = m_cont.predict(data_cont["X_seq_test"])
                probs_cont = m_cont.predict_proba(data_cont["X_seq_test"])
                y_true_c = data_cont["y_seq_test"]
            else:
                m_cont.fit(data_cont["X_train"], data_cont["y_train"])
                preds_cont = m_cont.predict(data_cont["X_test"])
                probs_cont = m_cont.predict_proba(data_cont["X_test"])
                y_true_c = data_cont["y_test"]

            res_cont = evaluate_predictions(y_true_c, preds_cont, probs_cont)

            if res_bin["f1_score"] > best_f1:
                best_f1 = res_bin["f1_score"]
                best_acc = res_bin["accuracy"]
                best_model_name = m_name
                best_mode = "Binary (+1/-1)"

            if res_cont["f1_score"] > best_f1:
                best_f1 = res_cont["f1_score"]
                best_acc = res_cont["accuracy"]
                best_model_name = m_name
                best_mode = "Continuous [0,1]"

            print(f"     [{m_name}] -> Binary Acc: {res_bin['accuracy']*100:.1f}%, F1: {res_bin['f1_score']*100:.1f}% | Cont Acc: {res_cont['accuracy']*100:.1f}%, F1: {res_cont['f1_score']*100:.1f}%")

        # Live Next-Day Prediction Check
        latest_x = data_bin["X_seq_test"][-1:]
        live_model = create_tft_model(epochs=35)
        live_model.fit(data_bin["X_seq_train"], data_bin["y_seq_train"])
        live_prob = live_model.predict_proba(latest_x)[0]
        live_signal = "UP (+1)" if live_prob[1] >= 0.5 else "DOWN (-1)"
        live_conf = max(live_prob[1], live_prob[0]) * 100.0

        summary_rows.append({
            "Dataset": name,
            "Ticker": ticker,
            "Asset Class": asset_class,
            "Test Samples": len(data_bin["y_seq_test"]),
            "Top Architecture": best_model_name,
            "Best Mode": best_mode,
            "OOS Accuracy": f"{best_acc*100:.1f}%",
            "OOS F1-Score": f"{best_f1*100:.1f}%",
            "Live Trend Forecast": f"{live_signal} ({live_conf:.1f}%)",
        })

    print("\n" + "=" * 100)
    print("FINAL SUMMARY MATRIX: OUT-OF-SAMPLE PREDICTION VERIFICATION (5 DATASETS)")
    print("=" * 100)
    summary_df = pd.DataFrame(summary_rows)
    print(summary_df.to_string(index=False))

if __name__ == "__main__":
    run_dataset_verification()
