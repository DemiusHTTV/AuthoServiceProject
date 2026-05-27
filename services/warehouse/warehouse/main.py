from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from warehouse.api import parts
from warehouse.database.database import Base, SessionLocal, engine
from warehouse.models import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Warehouse API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(parts.router)

@app.on_event("startup")
def seed_parts():
    db: Session = SessionLocal()
    try:
        data = [("Масляный фильтр", "OIL-001", 650, 20), ("Тормозные колодки", "BRK-010", 2400, 12), ("Свеча зажигания", "SPK-100", 450, 40)]
        for name, sku, price, stock in data:
            if not db.query(models.Part).filter(models.Part.sku == sku).first():
                db.add(models.Part(name=name, sku=sku, price=price, stock=stock))
        db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "ok", "message": "Warehouse API запущен"}
