# warehouse_service/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Warehouse Microservice API", version="1.0.0")

# CORS для безопасности
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Временная хардкод-база деталей для старта (пока Дима не настроил общую БД)
FAKE_PARTS_STORAGE = [
    {"id": 1, "name": "Фильтр масляный", "count": 12, "price": 850.0},
    {"id": 2, "name": "Колодки тормозные передние", "count": 4, "price": 3200.0},
    {"id": 3, "name": "Свеча зажигания", "count": 24, "price": 450.0},
]

@app.get("/api/warehouse/health")
def health_check():
    """Проверка живой ли склад"""
    return {"status": "ok", "service": "warehouse_service"}

@app.get("/api/parts")
def get_all_parts():
    """Эндпоинт, который будет дергать бэкенд Сани через httpx"""
    return FAKE_PARTS_STORAGE

@app.get("/api/parts/{part_id}")
def get_part_by_id(part_id: int):
    """Получить инфу по конкретной детали"""
    for part in FAKE_PARTS_STORAGE:
        if part["id"] == part_id:
            return part
    return {"error": "Part not found"}, 404