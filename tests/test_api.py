import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_predictlife_basic(client):
    resp = client.post("/predictlife", json={"question": "What is my path?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "symbol" in data
    assert isinstance(data.get("symbol"), dict)
    assert "details" not in data


def test_predictlife_with_details(client):
    resp = client.post(
        "/predictlife",
        json={"question": "Show me the details", "include_details": True},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "symbol" in data
    assert isinstance(data.get("symbol"), dict)
    assert "details" in data
    details = data["details"]
    assert "bitstring" in details
    assert "entropy" in details
    assert "num_qubits" in details


def test_invalid_qubits(client):
    resp = client.post("/predictlife", json={"question": "Hi", "num_qubits": 1})
    assert resp.status_code == 422


def test_missing_question(client):
    resp = client.post("/predictlife", json={})
    assert resp.status_code == 422
    assert "detail" in resp.json()
