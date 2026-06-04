from wharehouse.app.main import app as warehouse_app
from fastapi.testclient import TestClient

def test_warehouse_health_endpoint():
    """Smoke-тест: проверяем, что микросервис склада отвечает на своём эндпоинте"""
    wh_client = TestClient(warehouse_app)
    response = wh_client.get("/api/warehouse/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"