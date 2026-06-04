import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from autoservice_core import OrderItem, calculate_total_price, Part

app = FastAPI(title="AutoService Main API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WAREHOUSE_URL = "http://localhost:8001"  # Порт, на котором будет висеть склад в докере

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "AutoService API запущен успешно!"}

@app.post("/api/orders/calculate")
async def calculate_order(items: List[OrderItem]):
    """
    Создание заказа: идем в микросервис склада за актуальными деталями,
    затем используем наше ядро (autoservice_core) для расчета стоимости.
    """
    # 1. Запрашиваем актуальный каталог деталей со склада
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{WAREHOUSE_URL}/api/parts")
            response.raise_for_status()
            parts_data = response.json()
            # Конвертируем JSON в доменные модели
            parts_db = [Part(**p) for p in parts_data]
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Склад временно недоступен")
            
    # 2. Вычисляем итоговую стоимость через переиспользуемое ядро
    try:
        total = calculate_total_price(items, parts_db)
        return {"status": "success", "total_price": total, "items_count": len(items)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
