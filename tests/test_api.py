from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to SecurePay Cloud"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_payment():
    response = client.post(
        "/payments",
        json={"amount": 250, "currency": "EGP"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 250
    assert data["currency"] == "EGP"
    assert data["status"] == "simulated"
    assert "payment_id" in data


def test_reject_zero_amount():
    response = client.post(
        "/payments",
        json={"amount": 0, "currency": "EGP"},
    )
    assert response.status_code == 422


def test_reject_negative_amount():
    response = client.post(
        "/payments",
        json={"amount": -10, "currency": "EGP"},
    )
    assert response.status_code == 422
