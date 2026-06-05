from fastapi.testclient import TestClient

from warehouse_service.main import app as warehouse_app


wh_client = TestClient(warehouse_app)


def test_warehouse_parts_endpoint_returns_data():
    response = wh_client.get("/api/parts")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) > 0
    assert {"id", "name", "article", "price", "quantity"}.issubset(payload[0].keys())


def test_warehouse_calculate_endpoint_returns_total():
    response = wh_client.post(
        "/api/calculate",
        json={"items": [{"part_id": 1, "qty": 2}]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["total_price"] > 0
