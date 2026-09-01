"""
API Integration Tests for FastAPI Endpoints.
"""

from fastapi.testclient import TestClient
import pytest
from stock_predict.api.main import app

client = TestClient(app)


def test_api_status():
    res = client.get("/api/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "cuda_available" in data
    assert "available_models" in data


def test_api_indicators_compute():
    payload = {"source": "sample", "sector_key": "diversified_financials"}
    res = client.post("/api/indicators/compute", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_records"] > 0
    assert "records" in data
    first = data["records"][0]
    assert "close" in first
    assert "sma" in first
    assert "binary_signals" in first


def test_api_train_and_predict():
    train_payload = {
        "model_name": "decision_tree",
        "data_mode": "binary",
        "sector_key": "diversified_financials",
    }
    res = client.post("/api/train", json=train_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["model_name"] == "decision_tree"
    assert "metrics" in data
    assert "f1_score" in data["metrics"]


def test_api_backtest():
    payload = {
        "model_name": "random_forest",
        "data_mode": "binary",
        "sector_key": "diversified_financials",
        "initial_capital": 50000.0,
    }
    res = client.post("/api/backtest", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "metrics" in data
    assert "equity_curve" in data
    assert data["metrics"]["initial_capital"] == 50000.0
