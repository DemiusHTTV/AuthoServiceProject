from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from autoservices.database.database import engine, Base

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
    return {"status": "ok", "message": "AutoServices на Poetry + SQLite3 запущен!"}
