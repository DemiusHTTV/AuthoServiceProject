from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AutoService API", version="1.0.0")

# CORS для фронтенда (чтобы Макс потом мог подключить статику)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Базовый проверочный эндпоинт (Healthcheck)
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "AutoService API запущен успешно!"}

# Тестовая заглушка для фронтенда, пока Дима не настроил Docker и статику
@app.get("/")
def serve_index():
    return {"message": "Тут будет главная страница фронтенда"}

# Пример использования переиспользуемого ядра (core)
from autoservice_core import Part
@app.get("/api/example-core")
def example_core_usage():
    part = Part(id=99, name="Тестовая деталь из ядра", count=1, price=100.0)
    return {"status": "ok", "core_part": part.model_dump()}