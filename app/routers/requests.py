"""Роуты заявок: создание и получение."""

from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import OrderCreate

router = APIRouter(prefix="/api/requests", tags=["requests"])


@router.post("/")
def create_request(data: OrderCreate):
    conn = get_db()
    conn.execute(
        """INSERT INTO requests (client_id, client_name, client_email, client_phone,
           car_brand, car_model, car_year, description, service_id, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'new')""",
        (data.client_id, data.client_name, data.client_email, data.client_phone,
         data.car_brand, data.car_model, data.car_year, data.description,
         data.service_id))
    request_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return {"id": request_id, "status": "new"}


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
