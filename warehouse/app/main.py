from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from autoservice_core import Part

app = FastAPI(title="Warehouse Microservice API", version="1.0.0")

# CORS для безопасности
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Перевели на использование доменной модели ядра (autoservice_core)
PARTS_DB = [
    Part(id=1, name="Фильтр масляный", count=12, price=850.0),
    Part(id=2, name="Колодки тормозные передние", count=4, price=3200.0),
    Part(id=3, name="Свеча зажигания", count=24, price=450.0),
]

@app.get("/api/warehouse/health")
def health_check():
    """Проверка живой ли склад"""
    return {"status": "ok", "service": "warehouse_service"}

@app.get("/api/parts")
def get_all_parts():
    """Эндпоинт, который будет дергать бэкенд Сани через httpx"""
    return [p.model_dump() for p in PARTS_DB]

@app.get("/api/parts/{part_id}")
def get_part_by_id(part_id: int):
    """Получить инфу по конкретной детали через ядро"""
    for part in PARTS_DB:
        if part.id == part_id:
            return part.model_dump()
    raise HTTPException(status_code=404, detail="Part not found")