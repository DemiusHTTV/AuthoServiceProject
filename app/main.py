"""FastAPI — точка входа основного сервиса автосервиса."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database import init_db, seed_db
from app.routers import clients, requests, admin, workers, warehouse
from app.config import BASE_DIR

app = FastAPI(title="AutoService API", version="1.0.0")

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(clients.router)
app.include_router(requests.router)
app.include_router(admin.router)
app.include_router(workers.router)
app.include_router(warehouse.router)

# API для получения списка услуг (публичный)
from app.database import get_db

@app.get("/api/services")
def get_services():
    conn = get_db()
    rows = conn.execute("SELECT * FROM services").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Раздача фронтенда
frontend_dir = os.path.join(BASE_DIR, "frontend")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/admin")
def serve_admin():
    return FileResponse(os.path.join(frontend_dir, "admin.html"))

@app.get("/worker")
def serve_worker():
    return FileResponse(os.path.join(frontend_dir, "worker.html"))

# Статические файлы (css, js)
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")


@app.on_event("startup")
def startup():
    init_db()
    seed_db()
