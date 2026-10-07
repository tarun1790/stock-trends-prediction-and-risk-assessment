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


def test_api_universal_search():
    res = client.get("/api/stock/search?query=silver")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] > 0
    symbols = [r["symbol"] for r in data["results"]]
    assert "SI=F" in symbols or "SLV" in symbols

    res_gold = client.get("/api/stock/search?query=gold")
    assert res_gold.status_code == 200
    gold_data = res_gold.json()
    assert gold_data["count"] > 0


def test_api_commodity_resolution():
    from stock_predict.data.loader import DataLoader
    assert DataLoader.resolve_symbol("gold") == "GC=F"
    assert DataLoader.resolve_symbol("silver") == "SI=F"
    assert DataLoader.resolve_symbol("crude oil") == "CL=F"
    assert DataLoader.resolve_symbol("reliance") == "RELIANCE.NS"


def test_api_physical_credit_risk():
    res = client.get("/api/risk/credit/GC=F")
    assert res.status_code == 200
    data = res.json()
    assert data["synthetic_credit_rating"] == "AAA"
    assert "SAFE" in data["credit_risk_tier"]
    assert data["institutional_risk_synthesis"]["credit_passed"] is True

