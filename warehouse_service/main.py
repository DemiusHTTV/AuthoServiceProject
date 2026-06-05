"""Микросервис склада — отдельный FastAPI сервис для управления запчастями."""

import csv
import sqlite3
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from autoservice_core import calculate_total_price, Part, OrderItem
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "warehouse.db")

app = FastAPI(title="Warehouse Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS warehouse_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            article TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER DEFAULT 0,
            category TEXT
        )
    """)
    conn.commit()

    # Загрузка из CSV если пусто
    if conn.execute("SELECT COUNT(*) FROM warehouse_parts").fetchone()[0] == 0:
        csv_path = os.path.join(DATA_DIR, "warehouse_parts.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    conn.execute(
                        "INSERT INTO warehouse_parts (id, name, article, price, quantity, category) VALUES (?, ?, ?, ?, ?, ?)",
                        (row["id"], row["name"], row["article"], row["price"],
                         row["quantity"], row["category"]))
            conn.commit()
    conn.close()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/api/parts")
def get_all_parts():
    conn = get_db()
    rows = conn.execute("SELECT * FROM warehouse_parts ORDER BY category, name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/parts/search/{query}")
def search_parts(query: str):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM warehouse_parts WHERE name LIKE ? OR article LIKE ?",
        (f"%{query}%", f"%{query}%")).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/parts/{part_id}")
def get_part(part_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM warehouse_parts WHERE id = ?", (part_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Деталь не найдена")
    return dict(row)


@app.get("/api/parts/low-stock/{threshold}")
def low_stock(threshold: int = 10):
    """Детали с количеством меньше порога — параметризованный запрос."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM warehouse_parts WHERE quantity < ? ORDER BY quantity",
        (threshold,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

class CalculatePayload(BaseModel):
    items: list[OrderItem]

@app.post("/api/calculate")
def calculate_order_total(payload: CalculatePayload):
    conn = get_db()
    rows = conn.execute("SELECT * FROM warehouse_parts").fetchall()
    conn.close()
    
    parts_db = []
    for r in rows:
        parts_db.append(Part(
            id=r["id"],
            name=r["name"],
            article=r["article"],
            price=r["price"],
            quantity=r["quantity"],
            category=r["category"]
        ))
        
    try:
        total = calculate_total_price(payload.items, parts_db)
        return {"total_price": total, "status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
