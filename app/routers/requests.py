"""Роуты заявок: создание и получение."""

from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import OrderCreate

router = APIRouter(prefix="/api/requests", tags=["requests"])


@router.post("/")
def create_request(data: OrderCreate):
    conn = get_db()
    estimated_price = 0.0
    bonus_spent = round(float(data.bonus_to_spend or 0), 2)
    final_price = 0.0

    if bonus_spent < 0:
        conn.close()
        raise HTTPException(400, "Количество списываемых бонусов не может быть отрицательным")

    client = None
    if data.client_id is not None:
        client = conn.execute(
            "SELECT id, bonus_balance FROM clients WHERE id = ?",
            (data.client_id,)
        ).fetchone()
        if not client:
            conn.close()
            raise HTTPException(404, "Клиент не найден")

    if data.service_id is not None:
        service = conn.execute(
            "SELECT id, base_price FROM services WHERE id = ?",
            (data.service_id,)
        ).fetchone()
        if not service:
            conn.close()
            raise HTTPException(404, "Услуга не найдена")
        estimated_price = float(service["base_price"] or 0)

    if bonus_spent > 0:
        if not client:
            conn.close()
            raise HTTPException(400, "Бонусы доступны только авторизованному клиенту")
        if data.service_id is None:
            conn.close()
            raise HTTPException(400, "Для списания бонусов нужно выбрать услугу")
        if bonus_spent > float(client["bonus_balance"]):
            conn.close()
            raise HTTPException(400, "Недостаточно бонусов на счёте")
        if bonus_spent > estimated_price:
            conn.close()
            raise HTTPException(400, "Нельзя списать бонусов больше стоимости выбранной услуги")

    final_price = max(estimated_price - bonus_spent, 0)

    conn.execute(
        """INSERT INTO requests (client_id, client_name, client_email, client_phone,
           car_brand, car_model, car_year, description, service_id, status,
           estimated_price, bonus_spent, final_price)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'new', ?, ?, ?)""",
        (data.client_id, data.client_name, data.client_email, data.client_phone,
         data.car_brand, data.car_model, data.car_year, data.description,
         data.service_id, estimated_price, bonus_spent, final_price))
    request_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    updated_bonus_balance = None
    if client and bonus_spent > 0:
        conn.execute(
            "UPDATE clients SET bonus_balance = bonus_balance - ? WHERE id = ?",
            (bonus_spent, data.client_id)
        )
        conn.execute(
            """INSERT INTO bonuses (client_id, amount, reason)
               VALUES (?, ?, ?)""",
            (data.client_id, -bonus_spent, f"Списание бонусов по заявке #{request_id}")
        )
        updated_bonus_balance = round(float(client["bonus_balance"]) - bonus_spent, 2)
    elif client:
        updated_bonus_balance = float(client["bonus_balance"])

    conn.commit()
    conn.close()
    return {
        "id": request_id,
        "status": "new",
        "estimated_price": estimated_price,
        "bonus_spent": bonus_spent,
        "final_price": final_price,
        "bonus_balance": updated_bonus_balance,
    }


@router.get("/")
def get_all_requests():
    conn = get_db()
    rows = conn.execute("""
        SELECT r.*, s.name as service_name, s.base_price
        FROM requests r
        LEFT JOIN services s ON r.service_id = s.id
        ORDER BY r.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.get("/{request_id}")
def get_request(request_id: int):
    conn = get_db()
    row = conn.execute("""
        SELECT r.*, s.name as service_name, s.base_price
        FROM requests r
        LEFT JOIN services s ON r.service_id = s.id
        WHERE r.id = ?
    """, (request_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(404, "Заявка не найдена")

    # Назначенные работники
    assignments = conn.execute("""
        SELECT ra.*, w.name as worker_name, sp.name as specialization
        FROM request_assignments ra
        JOIN workers w ON ra.worker_id = w.id
        LEFT JOIN specializations sp ON w.specialization_id = sp.id
        WHERE ra.request_id = ?
    """, (request_id,)).fetchall()
    conn.close()

    return {**dict(row), "assignments": [dict(a) for a in assignments]}
