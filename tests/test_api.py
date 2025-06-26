import pytest

pytest.importorskip("httpx")
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_predictlife_basic():
    resp = client.post("/predictlife", json={"question": "Will I succeed?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data
    assert isinstance(data.get("symbol"), dict)
    assert "label" in data["symbol"]
    assert "details" not in data


def test_predictlife_with_details():
    resp = client.post("/predictlife", json={"question": "Tell me more", "include_details": True})
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data
    assert isinstance(data.get("symbol"), dict)
    assert "details" in data
    assert "bitstring" in data["details"]


def test_qrng_random_source():
    resp = client.post(
        "/predictlife",
        json={"question": "Hello", "random_source": "qrng", "mode": "direct"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data
    assert isinstance(data.get("symbol"), dict)


def test_invalid_qubits():
    resp = client.post("/predictlife", json={"question": "Hi", "num_qubits": 1})
    assert resp.status_code == 422