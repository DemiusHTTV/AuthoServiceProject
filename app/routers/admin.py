"""Роуты админ-панели: управление заявками, назначение работников."""

import csv
import os
from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import AdminLogin, AssignWorker, StatusUpdate
from app.config import DATA_DIR

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _get_admin_creds():
    """Прочитать логин/пароль админа из CSV."""
    path = os.path.join(DATA_DIR, "admin.csv")
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[0] if rows else None


@router.post("/login")
def admin_login(data: AdminLogin):
    creds = _get_admin_creds()
    if not creds:
        raise HTTPException(500, "Админ не настроен")
    if data.login != creds["login"] or data.password != creds["password_hash"]:
        raise HTTPException(401, "Неверный логин или пароль")
    return {"role": "admin", "name": creds["name"]}


@router.get("/requests")
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


@router.put("/requests/{request_id}/accept")
def accept_request(request_id: int):
    conn = get_db()
    conn.execute(
        "UPDATE requests SET status = 'accepted', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (request_id,))
    conn.commit()
    conn.close()
    return {"status": "accepted"}


@router.put("/requests/{request_id}/reject")
def reject_request(request_id: int):
    conn = get_db()
    conn.execute(
        "UPDATE requests SET status = 'rejected', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (request_id,))
    conn.commit()
    conn.close()
    return {"status": "rejected"}


@router.post("/assign")
def assign_worker(data: AssignWorker):
    conn = get_db()
    # Проверяем что заявка существует
    req = conn.execute("SELECT id, status FROM requests WHERE id = ?",
                       (data.request_id,)).fetchone()
    if not req:
        conn.close()
        raise HTTPException(404, "Заявка не найдена")

    # Проверяем работника
    worker = conn.execute("SELECT id FROM workers WHERE id = ?",
                          (data.worker_id,)).fetchone()
    if not worker:
        conn.close()
        raise HTTPException(404, "Работник не найден")

    conn.execute(
        "INSERT INTO request_assignments (request_id, worker_id, status) VALUES (?, ?, 'not_started')",
        (data.request_id, data.worker_id))

    # Обновляем статус заявки на in_progress
    conn.execute(
        "UPDATE requests SET status = 'in_progress', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (data.request_id,))
    conn.commit()
    conn.close()
    return {"message": "Работник назначен"}


@router.get("/workers")
def get_workers():
    conn = get_db()
    rows = conn.execute("""
        SELECT w.*, sp.name as specialization
        FROM workers w
        LEFT JOIN specializations sp ON w.specialization_id = sp.id
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.get("/services")
def get_services():
    conn = get_db()
    rows = conn.execute("SELECT * FROM services").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.get("/stats")
def get_stats():
    """Статистика для админ-панели."""
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as c FROM requests").fetchone()["c"]
    new = conn.execute("SELECT COUNT(*) as c FROM requests WHERE status = 'new'").fetchone()["c"]
    in_progress = conn.execute("SELECT COUNT(*) as c FROM requests WHERE status = 'in_progress'").fetchone()["c"]
    completed = conn.execute("SELECT COUNT(*) as c FROM requests WHERE status = 'completed'").fetchone()["c"]
    workers_count = conn.execute("SELECT COUNT(*) as c FROM workers").fetchone()["c"]
    conn.close()
    return {
        "total_requests": total,
        "new_requests": new,
        "in_progress": in_progress,
        "completed": completed,
        "workers_count": workers_count
    }
