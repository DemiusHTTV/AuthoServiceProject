from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from autoservices.database.database import engine, Base
from autoservices.api.users import router as users_router
from autoservices.api.cars import router as cars_router
from autoservices.api.orders import router as orders_router

# Создание таблиц при запуске
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Чистый Автосервис API",
    description="Бэкенд-сервис для управления заказами автосервиса",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем наши модули ручек
app.include_router(users_router, prefix="/api")
app.include_router(cars_router, prefix="/api")
app.include_router(orders_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API Автосервиса полностью готово к работе!"}
