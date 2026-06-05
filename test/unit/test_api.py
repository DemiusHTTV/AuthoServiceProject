from fastapi.testclient import TestClient
import uuid

from app.database import init_db, seed_db
from app.main import app

init_db()
seed_db()
client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_create_request_with_bonus_spend_updates_balance():
    token = uuid.uuid4().hex[:8]
    register_response = client.post(
        "/api/clients/register",
        json={
            "name": f"Test User {token}",
            "email": f"test_{token}@mail.ru",
            "phone": "+79000000000",
            "password": "secret123",
        },
    )
    assert register_response.status_code == 200
    created_user = register_response.json()

    response = client.post(
        "/api/requests/",
        json={
            "client_name": created_user["name"],
            "client_email": created_user["email"],
            "client_phone": created_user["phone"],
            "car_brand": "Toyota",
            "car_model": "Corolla",
            "car_year": 2020,
            "description": "Тестовая заявка со списанием бонусов",
            "service_id": 1,
            "client_id": created_user["id"],
            "bonus_to_spend": 300,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "new"
    assert payload["estimated_price"] == 500.0
    assert payload["bonus_spent"] == 300.0
    assert payload["final_price"] == 200.0
    assert payload["bonus_balance"] == 2700.0

    profile_response = client.get(f"/api/clients/{created_user['id']}")
    assert profile_response.status_code == 200
    profile = profile_response.json()
    assert profile["client"]["bonus_balance"] == 2700.0
    assert any(bonus["amount"] == -300.0 for bonus in profile["bonuses"])


def test_create_request_rejects_bonus_spend_above_balance():
    token = uuid.uuid4().hex[:8]
    register_response = client.post(
        "/api/clients/register",
        json={
            "name": f"Test User {token}",
            "email": f"test_{token}@mail.ru",
            "phone": "+79000000001",
            "password": "secret123",
        },
    )
    assert register_response.status_code == 200
    created_user = register_response.json()

    response = client.post(
        "/api/requests/",
        json={
            "client_name": created_user["name"],
            "client_email": created_user["email"],
            "client_phone": created_user["phone"],
            "car_brand": "Kia",
            "car_model": "Rio",
            "car_year": 2021,
            "description": "Тестовая заявка с неверным списанием",
            "service_id": 2,
            "client_id": created_user["id"],
            "bonus_to_spend": 5000,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Недостаточно бонусов на счёте"
