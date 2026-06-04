from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Smoke-тест: проверяем, что наш healthcheck эндпоинт доступен и отдает 'ok'"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "AutoService API запущен успешно!"}

def test_root_endpoint():
    """Smoke-тест: проверяем доступность корня"""
    response = client.get("/")
    assert response.status_code == 200