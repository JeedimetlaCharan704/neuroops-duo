"""
Unit and integration tests for OmniPay Gateway.
"""
import pytest
from fastapi.testclient import TestClient
from target_service.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "region" in data
    assert data["carbon_intensity_gco2_kwh"] > 0

def test_prometheus_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "omnipay_requests_total" in response.text
    assert "omnipay_carbon_intensity" in response.text

def test_process_valid_payment():
    payload = {
        "user_id": "usr_9981",
        "amount": 250.75,
        "currency": "USD",
        "payment_method": "credit_card"
    }
    response = client.post("/api/v1/payments", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "CONFIRMED"
    assert data["amount"] == 250.75
    assert "transaction_id" in data
    assert data["carbon_cost_gco2"] > 0

def test_process_negative_payment_rejection():
    payload = {
        "user_id": "usr_hacker",
        "amount": -50.00,
        "currency": "USD",
        "payment_method": "credit_card"
    }
    response = client.post("/api/v1/payments", json=payload)
    # Pydantic validates amount > 0 and returns 422 Unprocessable Entity
    assert response.status_code == 422

def test_list_transactions():
    response = client.get("/api/v1/transactions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_carbon_status():
    response = client.get("/api/v1/carbon-status")
    assert response.status_code == 200
    data = response.json()
    assert "is_carbon_optimal" in data
