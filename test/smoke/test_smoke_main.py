from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_services_endpoint_returns_seeded_data():
    response = client.get("/api/services")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) > 0
    assert {"id", "name", "base_price"}.issubset(payload[0].keys())
