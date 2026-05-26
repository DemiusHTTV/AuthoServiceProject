from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from autoservices.database.database import engine, Base
import autoservices.models.models as models

# Инициализируем структуру таблиц в SQLite3
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoServices API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "База данных SQLite3 успешно синхронизирована. 8 таблиц готовы!"}
