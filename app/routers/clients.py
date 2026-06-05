"""Роуты клиентов: регистрация, логин, личный кабинет."""

from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import ClientRegister, ClientLogin
from app.config import DEFAULT_BONUS

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.post("/register")
def register(data: ClientRegister):
    conn = get_db()
    # Проверяем что email не занят
    existing = conn.execute("SELECT id FROM clients WHERE email = ?", (data.email,)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(400, "Email уже зарегистрирован")

    conn.execute(
        "INSERT INTO clients (name, email, phone, password, bonus_balance) VALUES (?, ?, ?, ?, ?)",
        (data.name, data.email, data.phone, data.password, DEFAULT_BONUS))
    client_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Начисляем приветственный бонус
    conn.execute(
        "INSERT INTO bonuses (client_id, amount, reason) VALUES (?, ?, ?)",
        (client_id, DEFAULT_BONUS, "Приветственный бонус"))
    conn.commit()
    conn.close()
    return {"id": client_id, "name": data.name, "email": data.email, "phone": data.phone,
            "bonus_balance": DEFAULT_BONUS}


@router.post("/login")
def login(data: ClientLogin):
    conn = get_db()
    client = conn.execute(
        "SELECT id, name, email, phone, bonus_balance FROM clients WHERE email = ? AND password = ?",
        (data.email, data.password)).fetchone()
    conn.close()
    if not client:
        raise HTTPException(401, "Неверный email или пароль")
    return dict(client)


@router.get("/{client_id}")
def get_profile(client_id: int):
    conn = get_db()
    client = conn.execute(
        "SELECT id, name, email, phone, bonus_balance FROM clients WHERE id = ?",
        (client_id,)).fetchone()
    if not client:
        conn.close()
        raise HTTPException(404, "Клиент не найден")

    # История заявок
    requests = conn.execute("""
        SELECT r.*, s.name as service_name, s.base_price
        FROM requests r
        LEFT JOIN services s ON r.service_id = s.id
        WHERE r.client_id = ?
        ORDER BY r.created_at DESC
    """, (client_id,)).fetchall()

    # Бонусы
    bonuses = conn.execute(
        "SELECT * FROM bonuses WHERE client_id = ? ORDER BY created_at DESC",
        (client_id,)).fetchall()
    conn.close()

    return {
        "client": dict(client),
        "requests": [dict(r) for r in requests],
        "bonuses": [dict(b) for b in bonuses]
    }
