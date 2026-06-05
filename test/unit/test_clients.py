import uuid

from fastapi.testclient import TestClient

from app.database import init_db, seed_db
from app.main import app


init_db()
seed_db()
client = TestClient(app)


def test_register_client_returns_welcome_bonus():
    token = uuid.uuid4().hex[:8]
    response = client.post(
        "/api/clients/register",
        json={
            "name": f"Client {token}",
            "email": f"client_{token}@mail.ru",
            "phone": "+79001230000",
            "password": "client123",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == f"Client {token}"
    assert payload["bonus_balance"] == 3000


def test_register_client_rejects_duplicate_email():
    token = uuid.uuid4().hex[:8]
    email = f"dup_{token}@mail.ru"

    first = client.post(
        "/api/clients/register",
        json={
            "name": "Dup User",
            "email": email,
            "phone": "+79001230001",
            "password": "client123",
        },
    )
    assert first.status_code == 200

    second = client.post(
        "/api/clients/register",
        json={
            "name": "Dup User Again",
            "email": email,
            "phone": "+79001230002",
            "password": "client123",
        },
    )

    assert second.status_code == 400
    assert second.json()["detail"] == "Email уже зарегистрирован"


def test_login_existing_client_returns_profile_payload():
    response = client.post(
        "/api/clients/login",
        json={
            "email": "ivanov@mail.ru",
            "password": "client123",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == "ivanov@mail.ru"
    assert "bonus_balance" in payload


def test_get_client_profile_contains_requests_and_bonuses():
    response = client.get("/api/clients/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["client"]["id"] == 1
    assert isinstance(payload["requests"], list)
    assert isinstance(payload["bonuses"], list)
