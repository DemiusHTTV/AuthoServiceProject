import requests
from app.config import API_URL

def login(username: str, password: str):
    """
    Отправляет запрос на бэкенд для проверки логина мастера.
    Ожидает в ответ JSON вида: {"type": "worker", "worker_id": 5}
    """
    response = requests.post(
        f"{API_URL}/api/auth/login",  # Подгоняем под префикс /api
        json={
            "login": username,
            "password": password,
        },
    )
    response.raise_for_status()
    return response.json()


def get_worker_requests(worker_id: int):
    """
    Запрашивает список заявок конкретного мастера по его ID
    """
    response = requests.get(
        f"{API_URL}/api/workers/requests?worker_id={worker_id}"
    )
    response.raise_for_status()
    return response.json()


def update_request_status(request_id: int, status: str):
    """
    Обновляет статус заявки (например, 'В работе' или 'Выполнено')
    """
    response = requests.put(  # Меняем PATCH на PUT для единообразия с админкой
        f"{API_URL}/api/appointments/{request_id}/status",
        json={
            "status": status,
        },
    )
    response.raise_for_status()
    return response.json()