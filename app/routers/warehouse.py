"""Прокси к микросервису склада."""

import httpx
from fastapi import APIRouter, HTTPException
from app.config import WAREHOUSE_URL

router = APIRouter(prefix="/api/warehouse", tags=["warehouse"])


@router.get("/parts")
async def get_parts():
    """Получить все детали со склада."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{WAREHOUSE_URL}/api/parts", timeout=5.0)
            return resp.json()
    except Exception as e:
        raise HTTPException(502, f"Склад недоступен: {str(e)}")


@router.get("/parts/{part_id}")
async def get_part(part_id: int):
    """Получить деталь по ID."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{WAREHOUSE_URL}/api/parts/{part_id}", timeout=5.0)
            if resp.status_code == 404:
                raise HTTPException(404, "Деталь не найдена")
            return resp.json()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"Склад недоступен: {str(e)}")


@router.get("/parts/search/{query}")
async def search_parts(query: str):
    """Поиск деталей по названию."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{WAREHOUSE_URL}/api/parts/search/{query}", timeout=5.0)
            return resp.json()
    except Exception as e:
        raise HTTPException(502, f"Склад недоступен: {str(e)}")
