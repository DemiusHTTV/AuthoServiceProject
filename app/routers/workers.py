"""Роуты панели работника: просмотр задач, смена статуса."""

from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import WorkerLogin, StatusUpdate

router = APIRouter(prefix="/api/workers", tags=["workers"])


@router.post("/login")
def worker_login(data: WorkerLogin):
    conn = get_db()
    worker = conn.execute(
        """SELECT w.id, w.name, w.phone, w.login, sp.name as specialization
           FROM workers w
           LEFT JOIN specializations sp ON w.specialization_id = sp.id
           WHERE w.login = ? AND w.password = ?""",
        (data.login, data.password)).fetchone()
    conn.close()
    if not worker:
        raise HTTPException(401, "Неверный логин или пароль")
    return dict(worker)


@router.get("/{worker_id}/tasks")
def get_tasks(worker_id: int):
    conn = get_db()
    tasks = conn.execute("""
        SELECT ra.id as assignment_id, ra.status as task_status,
               ra.assigned_at, ra.completed_at,
               r.id as request_id, r.client_name, r.car_brand, r.car_model,
               r.car_year, r.description, r.status as request_status,
               s.name as service_name
        FROM request_assignments ra
        JOIN requests r ON ra.request_id = r.id
        LEFT JOIN services s ON r.service_id = s.id
        WHERE ra.worker_id = ?
        ORDER BY ra.assigned_at DESC
    """, (worker_id,)).fetchall()
    conn.close()
    return [dict(t) for t in tasks]


@router.put("/tasks/{assignment_id}/status")
def update_task_status(assignment_id: int, data: StatusUpdate):
    conn = get_db()
    assignment = conn.execute(
        "SELECT * FROM request_assignments WHERE id = ?",
        (assignment_id,)).fetchone()
    if not assignment:
        conn.close()
        raise HTTPException(404, "Назначение не найдено")

    if data.status == "done":
        conn.execute(
            "UPDATE request_assignments SET status = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?",
            (data.status, assignment_id))
        # Проверяем все ли задания по заявке выполнены
        request_id = assignment["request_id"]
        pending = conn.execute(
            "SELECT COUNT(*) as c FROM request_assignments WHERE request_id = ? AND status != 'done'",
            (request_id,)).fetchone()["c"]
        # Не считаем текущее (уже обновлённое)
        if pending <= 1:
            conn.execute(
                "UPDATE requests SET status = 'completed', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (request_id,))
    else:
        conn.execute(
            "UPDATE request_assignments SET status = ? WHERE id = ?",
            (data.status, assignment_id))
        # Если начали работу — обновим статус заявки
        if data.status == "in_progress":
            conn.execute(
                "UPDATE requests SET status = 'in_progress', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (assignment["request_id"],))

    conn.commit()
    conn.close()
    return {"status": data.status}
