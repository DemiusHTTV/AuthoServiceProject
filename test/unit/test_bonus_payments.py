import uuid

from fastapi.testclient import TestClient

from app.database import init_db, seed_db
from app.main import app
from autoservice_core import calculate_bonus


init_db()
seed_db()
client = TestClient(app)


def test_guest_cannot_spend_bonuses():
    response = client.post(
        "/api/requests/",
        json={
            "client_name": "Guest Bonus",
            "client_email": "guest_bonus@mail.ru",
            "client_phone": "+79001239999",
            "car_brand": "Ford",
            "car_model": "Focus",
            "car_year": 2018,
            "description": "Гость пытается списать бонусы",
            "service_id": 1,
            "bonus_to_spend": 100,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Бонусы доступны только авторизованному клиенту"


def test_cannot_spend_more_than_service_price():
    token = uuid.uuid4().hex[:8]
    register_response = client.post(
        "/api/clients/register",
        json={
            "name": f"Price User {token}",
            "email": f"price_{token}@mail.ru",
            "phone": "+79002220000",
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
            "car_brand": "Honda",
            "car_model": "Civic",
            "car_year": 2019,
            "description": "Списание выше цены услуги",
            "service_id": 1,
            "client_id": created_user["id"],
            "bonus_to_spend": 999,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Нельзя списать бонусов больше стоимости выбранной услуги"


def test_bonus_formula_returns_expected_value():
    assert calculate_bonus(5000, 1.0) == 250.0
    assert calculate_bonus(12000, 0.5) == 300.0
