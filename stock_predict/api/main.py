"""
FastAPI Production Web API & Application Server.
Exposes endpoints for data ingestion, indicator extraction, model training,
comparative benchmarking, live predictions, and quantitative backtesting.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import time
import torch
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from stock_predict.config import DEVICE, PAPER_SECTORS
from stock_predict.data.loader import DataLoader
from stock_predict.core.indicators import compute_all_indicators
from stock_predict.core.preprocessing import (
    prepare_dataset,
    binary_preprocessing,
    continuous_preprocessing,
    create_sequences,
    INDICATOR_COLUMNS,
)
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
from stock_predict.evaluation.benchmark import BenchmarkRunner
from stock_predict.evaluation.explainability import compute_feature_saliency
from stock_predict.backtest.backtester import BacktestEngine
from stock_predict.backtest.advanced_backtester import AdvancedRiskBacktester
from stock_predict.models.advanced_neural import MultiHorizonForecaster, PyTorchTCN, PyTorchTFT
from stock_predict.core.advanced_indicators import compute_full_quant_features
from stock_predict.api.schemas import (
    SystemStatusResponse,
    DataFetchRequest,
    IndicatorComputeResponse,
    ModelTrainRequest,
    ModelTrainResponse,
    BenchmarkRequest,
    BenchmarkResponse,
    LivePredictRequest,
    LivePredictResponse,
    BacktestRequest,
    BacktestResponse,
)

app = FastAPI(
    title="Stock Market Trend Prediction Platform",
    description="Quantitative ML/DL Platform via Continuous and Binary Data Analysis (IEEE Access)",
    version="1.0.0",
)

# CORS middleware for cross-origin access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_loader = DataLoader()
UI_DIR = Path(__file__).resolve().parent.parent / "ui" / "static"


def _load_requested_data(req_data: Any) -> pd.DataFrame:
    """Helper to load data based on request parameters."""
    if hasattr(req_data, "ticker") and req_data.ticker:
        return data_loader.fetch_live_data(req_data.ticker)
    elif hasattr(req_data, "sector_key") and req_data.sector_key:
        return data_loader.load_sector_data(req_data.sector_key)
    return data_loader.load_sector_data("diversified_financials")


def _instantiate_model(model_name: str, **kwargs) -> Any:
    """Instantiate a model wrapper by name."""
    name_clean = model_name.lower().replace(" ", "_").replace("-", "_")
    if name_clean in MODEL_REGISTRY:
        factory = MODEL_REGISTRY[name_clean]
        if name_clean in ["ann", "rnn", "lstm", "gru", "bilstm_attention", "transformer"]:
            epochs = kwargs.get("epochs", 80)
            return factory(epochs=epochs)
        # Non-neural models: remove DL specific kwargs
        clean_kwargs = {k: v for k, v in kwargs.items() if k not in ["epochs", "sequence_length"]}
        return factory(**clean_kwargs) if clean_kwargs else factory()
    elif name_clean == "ensemble":
        estimators = [
            RandomForestModel(n_estimators=100),
            XGBoostModel(n_estimators=100),
            create_lstm_model(epochs=60),
            create_transformer_model(epochs=60),
        ]
        return VotingEnsembleModel(estimators=estimators)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown model name '{model_name}'. Available: {list(MODEL_REGISTRY.keys()) + ['ensemble']}",
        )


@app.get("/api/status", response_model=SystemStatusResponse)
def get_system_status():
    """Retrieve system diagnostics, hardware acceleration details, and available models."""
    cuda_avail = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_avail else None

    return SystemStatusResponse(
        status="healthy",
        version="1.0.0",
        cuda_available=cuda_avail,
        device=str(DEVICE),
        gpu_name=gpu_name,
        available_models=list(MODEL_REGISTRY.keys()) + ["ensemble"],
        available_sectors=list(PAPER_SECTORS.keys()),
    )


@app.post("/api/data/fetch")
def fetch_market_data(req: DataFetchRequest):
    """Ingest stock market data from Yahoo Finance or IEEE TSE sectors."""
    try:
        if req.source == "ticker" and req.ticker:
            df = data_loader.fetch_live_data(
                ticker=req.ticker,
                start_date=req.start_date,
                end_date=req.end_date,
                period=req.period,
            )
        else:
            sector = req.sector_key or "diversified_financials"
            df = data_loader.load_sector_data(sector)

        preview = []
        for dt, row in df.tail(100).iterrows():
            preview.append({
                "date": str(dt)[:10],
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": float(row.get("Volume", 0)),
            })

        return {
            "total_records": len(df),
            "start_date": str(df.index[0])[:10],
            "end_date": str(df.index[-1])[:10],
            "summary_stats": {
                "close_mean": round(float(df["Close"].mean()), 2),
                "close_min": round(float(df["Close"].min()), 2),
                "close_max": round(float(df["Close"].max()), 2),
                "close_std": round(float(df["Close"].std()), 2),
            },
            "records": preview,
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/indicators/compute")
def compute_indicators_api(req: DataFetchRequest):
    """Compute the 10 IEEE technical indicators & binary signals."""
    try:
        df = _load_requested_data(req)
        ind_df = compute_all_indicators(df)
        bin_signals = binary_preprocessing(ind_df, zero_one_mode=False)

        records = []
        tail_df = ind_df.tail(150)
        bin_tail = bin_signals[-150:]

        for i, (dt, row) in enumerate(tail_df.iterrows()):
            item = {
                "date": str(dt)[:10],
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": float(row.get("Volume", 0)),
                "sma": round(float(row["SMA"]), 2) if not pd.isna(row["SMA"]) else None,
                "wma": round(float(row["WMA"]), 2) if not pd.isna(row["WMA"]) else None,
                "mom": round(float(row["MOM"]), 2) if not pd.isna(row["MOM"]) else None,
                "stck": round(float(row["STCK"]), 2) if not pd.isna(row["STCK"]) else None,
                "stcd": round(float(row["STCD"]), 2) if not pd.isna(row["STCD"]) else None,
                "rsi": round(float(row["RSI"]), 2) if not pd.isna(row["RSI"]) else None,
                "sig": round(float(row["SIG"]), 2) if not pd.isna(row["SIG"]) else None,
                "lwr": round(float(row["LWR"]), 2) if not pd.isna(row["LWR"]) else None,
                "ado": round(float(row["ADO"]), 4) if not pd.isna(row["ADO"]) else None,
                "cci": round(float(row["CCI"]), 2) if not pd.isna(row["CCI"]) else None,
                "binary_signals": {
                    col: int(bin_tail[i, c_idx])
                    for c_idx, col in enumerate(INDICATOR_COLUMNS)
                },
            }
            records.append(item)

        return {
            "total_records": len(ind_df),
            "columns": list(ind_df.columns),
            "records": records,
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/train", response_model=ModelTrainResponse)
def train_model_api(req: ModelTrainRequest):
    """Train a machine learning or PyTorch deep learning model."""
    try:
        df = _load_requested_data(req)
        data = prepare_dataset(
            df,
            mode=req.data_mode,
            sequence_length=req.sequence_length,
            test_size=req.test_size,
        )

        model = _instantiate_model(req.model_name, epochs=req.epochs)
        is_seq = req.model_name.lower() in [
            "rnn", "lstm", "gru", "bilstm_attention", "transformer"
        ]

        if is_seq and "X_seq_train" in data:
            X_tr, y_tr = data["X_seq_train"], data["y_seq_train"]
            X_te, y_te = data["X_seq_test"], data["y_seq_test"]
        else:
            X_tr, y_tr = data["X_train"], data["y_train"]
            X_te, y_te = data["X_test"], data["y_test"]

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

        return ModelTrainResponse(
            model_name=req.model_name,
            data_mode=req.data_mode,
            metrics=metrics,
            confusion_matrix=metrics["confusion_matrix"],
            train_time_seconds=round(train_time, 4),
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/benchmark", response_model=BenchmarkResponse)
def run_benchmark_api(req: BenchmarkRequest):
    """Execute complete comparative benchmark suite across Continuous and Binary data representations."""
    try:
        df = _load_requested_data(req)
        runner = BenchmarkRunner(sequence_length=req.sequence_length)
        res = runner.run_full_benchmark(
            df=df,
            models_to_run=req.models,
            test_size=req.test_size,
        )

        return BenchmarkResponse(
            dataset_info={
                "total_samples": res["num_samples_total"],
                "test_samples": res["num_test_samples"],
                "sequence_length": req.sequence_length,
                "hardware": "GPU / CUDA" if torch.cuda.is_available() else "CPU",
            },
            continuous_results=res["continuous_results"],
            binary_results=res["binary_results"],
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/predict", response_model=LivePredictResponse)
def predict_live_trend(req: LivePredictRequest):
    """Generate real-time stock trend prediction (UP vs DOWN) with indicator signals."""
    try:
        df = data_loader.fetch_live_data(req.ticker) if req.ticker != "sample" else data_loader.load_sector_data("diversified_financials")
        data = prepare_dataset(df, mode=req.data_mode, sequence_length=20)

        model = _instantiate_model(req.model_name, epochs=60)
        is_seq = req.model_name.lower() in [
            "rnn", "lstm", "gru", "bilstm_attention", "transformer"
        ]

        if is_seq and "X_seq_train" in data:
            model.fit(data["X_seq_train"], data["y_seq_train"])
            latest_x = data["X_seq_test"][-1:]
        else:
            model.fit(data["X_train"], data["y_train"])
            latest_x = data["X_test"][-1:]

        probs = model.predict_proba(latest_x)[0]
        prob_up = float(probs[1]) if len(probs) > 1 else float(probs[0])
        prob_down = 1.0 - prob_up
        signal = 1 if prob_up >= 0.5 else 0

        # Latest indicators
        ind_df = compute_all_indicators(df).dropna()
        last_row = ind_df.iloc[-1]
        bin_signals = binary_preprocessing(ind_df, zero_one_mode=False)[-1]

        indicators = {
            col: round(float(last_row[col]), 2) for col in INDICATOR_COLUMNS
        }
        bin_dict = {
            col: int(bin_signals[i]) for i, col in enumerate(INDICATOR_COLUMNS)
        }

        return LivePredictResponse(
            ticker=req.ticker,
            model_name=req.model_name,
            data_mode=req.data_mode,
            prediction_trend="UP" if signal == 1 else "DOWN",
            prediction_signal=signal,
            confidence_up=round(prob_up * 100.0, 2),
            confidence_down=round(prob_down * 100.0, 2),
            last_price=round(float(last_row["Close"]), 2),
            indicators=indicators,
            binary_signals=bin_dict,
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/backtest", response_model=BacktestResponse)
def run_backtest_api(req: BacktestRequest):
    """Simulate strategy trading execution with risk & return analytics."""
    try:
        df = _load_requested_data(req)
        data = prepare_dataset(df, mode=req.data_mode, sequence_length=20, test_size=0.40)

        model = _instantiate_model(req.model_name, epochs=60)
        is_seq = req.model_name.lower() in [
            "rnn", "lstm", "gru", "bilstm_attention", "transformer"
        ]

        if is_seq and "X_seq_train" in data:
            model.fit(data["X_seq_train"], data["y_seq_train"])
            X_eval = data["X_seq_test"]
            y_eval = data["y_seq_test"]
        else:
            model.fit(data["X_train"], data["y_train"])
            X_eval = data["X_test"]
            y_eval = data["y_test"]

        preds = model.predict(X_eval)

        # Get test slice price series
        clean_df = data["raw_df"]
        n_eval = len(preds)
        test_prices = clean_df["Close"].iloc[-n_eval:].values
        test_dates = clean_df.index[-n_eval:]

        engine = BacktestEngine(
            initial_capital=req.initial_capital,
            transaction_cost_pct=req.transaction_cost_pct,
        )
        result = engine.run_backtest(
            prices=test_prices,
            signals=preds,
            dates=test_dates,
            allow_short=req.allow_short,
        )

        return BacktestResponse(
            metrics=result["metrics"],
            equity_curve=result["equity_curve"],
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/predict/multi-horizon")
def predict_multi_horizon_api(req: LivePredictRequest):
    """
    Multi-Horizon Forecasting Engine.
    Simultaneously forecasts 1D, 3D, 5D, 10D, and 20D forward price trends and magnitude.
    """
    try:
        df = data_loader.fetch_live_data(req.ticker) if req.ticker != "sample" else data_loader.load_sector_data("diversified_financials")
        data = prepare_dataset(df, mode=req.data_mode, sequence_length=20)

        forecaster = MultiHorizonForecaster(input_dim=10, epochs=40)
        forecaster.fit(data["X_seq_train"], data["raw_df"]["Close"].values)

        latest_x = data["X_seq_test"][-1:] if "X_seq_test" in data else data["X_seq_train"][-1:]
        forecasts = forecaster.predict_multi_horizon(latest_x)

        return {
            "ticker": req.ticker,
            "data_mode": req.data_mode,
            "last_price": round(float(df["Close"].iloc[-1]), 2),
            "forecasts": forecasts,
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/explain")
def explain_prediction_api(req: LivePredictRequest):
    """
    Explainable AI (XAI) Engine.
    Returns Temporal Attention Heatmaps and Indicator Importance Attribution.
    """
    try:
        df = data_loader.fetch_live_data(req.ticker) if req.ticker != "sample" else data_loader.load_sector_data("diversified_financials")
        data = prepare_dataset(df, mode=req.data_mode, sequence_length=20)

        model = _instantiate_model(req.model_name, epochs=40)
        is_seq = req.model_name.lower() in [
            "rnn", "lstm", "gru", "bilstm_attention", "transformer", "tcn", "tft"
        ]

        if is_seq and "X_seq_train" in data:
            model.fit(data["X_seq_train"], data["y_seq_train"])
            sample_x = data["X_seq_test"][-1:]
        else:
            model.fit(data["X_train"], data["y_train"])
            sample_x = data["X_test"][-1:]

        from stock_predict.evaluation.explainability import compute_feature_saliency
        explanation = compute_feature_saliency(
            model_wrapper=model,
            input_sample=sample_x,
            feature_names=INDICATOR_COLUMNS,
        )

        return {
            "ticker": req.ticker,
            "model_name": req.model_name,
            "data_mode": req.data_mode,
            "explanation": explanation,
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/backtest/monte-carlo")
def monte_carlo_backtest_api(req: BacktestRequest):
    """
    Institutional Risk Backtester with 1,000-Path Monte Carlo Simulation (VaR / CVaR 95%).
    """
    try:
        df = _load_requested_data(req)
        data = prepare_dataset(df, mode=req.data_mode, sequence_length=20, test_size=0.40)

        model = _instantiate_model(req.model_name, epochs=50)
        is_seq = req.model_name.lower() in [
            "rnn", "lstm", "gru", "bilstm_attention", "transformer", "tcn", "tft"
        ]

        if is_seq and "X_seq_train" in data:
            model.fit(data["X_seq_train"], data["y_seq_train"])
            X_eval = data["X_seq_test"]
        else:
            model.fit(data["X_train"], data["y_train"])
            X_eval = data["X_test"]

        preds = model.predict(X_eval)
        probas = model.predict_proba(X_eval)[:, 1]

        clean_df = data["raw_df"]
        n_eval = len(preds)
        test_prices = clean_df["Close"].iloc[-n_eval:].values
        test_dates = clean_df.index[-n_eval:]

        from stock_predict.backtest.advanced_backtester import AdvancedRiskBacktester
        adv_engine = AdvancedRiskBacktester(
            initial_capital=req.initial_capital,
            transaction_cost_pct=req.transaction_cost_pct,
            target_annual_vol=0.15,
            trailing_stop_pct=0.03,
        )
        res = adv_engine.run_risk_managed_backtest(
            prices=test_prices,
            signals=preds,
            confidence_probs=probas,
            dates=test_dates,
        )

        return res
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/indicators/advanced")
def advanced_indicators_api(req: DataFetchRequest):
    """
    25+ Institutional Quantitative Features with Volatility & Ternary Regime Filters.
    """
    try:
        df = _load_requested_data(req)
        from stock_predict.core.advanced_indicators import compute_full_quant_features
        quant_df = compute_full_quant_features(df)

        preview = []
        for dt, row in quant_df.tail(50).iterrows():
            preview.append({
                "date": str(dt)[:10],
                "close": round(float(row["Close"]), 2),
                "atr": round(float(row["ATR"]), 2) if not pd.isna(row["ATR"]) else None,
                "adx": round(float(row["ADX"]), 2) if not pd.isna(row["ADX"]) else None,
                "cmf": round(float(row["CMF"]), 4) if not pd.isna(row["CMF"]) else None,
                "bb_pct_b": round(float(row["BB_PCT_B"]), 2) if not pd.isna(row["BB_PCT_B"]) else None,
                "park_vol": round(float(row["PARK_VOL"]), 3) if not pd.isna(row["PARK_VOL"]) else None,
                "reg_sma": int(row.get("REG_SMA", 0)),
                "reg_rsi": int(row.get("REG_RSI", 0)),
                "reg_adx": int(row.get("REG_ADX", 0)),
            })

        return {
            "total_records": len(quant_df),
            "records": preview,
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


# Static frontend serving
if UI_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(UI_DIR)), name="static")

    @app.get("/")
    def serve_dashboard():
        return FileResponse(str(UI_DIR / "index.html"))

