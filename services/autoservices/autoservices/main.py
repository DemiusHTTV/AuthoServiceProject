from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from autoservices.api import cars, employees, orders, services, users
from autoservices.database.database import Base, SessionLocal, engine
from autoservices.models import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoServices API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(cars.router)
app.include_router(orders.router)
app.include_router(employees.router)
app.include_router(services.router)

@app.on_event("startup")
def seed_data():
    db: Session = SessionLocal()
    try:
        if not db.query(models.User).filter(models.User.email == "admin@autoservice.local").first():
            admin = models.User(fullname="Главный администратор", phone="+70000000001", email="admin@autoservice.local", password="admin123", role="admin")
            db.add(admin)
        if not db.query(models.User).filter(models.User.email == "worker@autoservice.local").first():
            worker_user = models.User(fullname="Иван Механик", phone="+70000000002", email="worker@autoservice.local", password="worker123", role="worker")
            db.add(worker_user)
            db.commit()
            db.refresh(worker_user)
            db.add(models.Employee(fullname="Иван Механик", position="Автомеханик", phone="+70000000002", user_id=worker_user.id))
        base_services = [("Диагностика подвески", 500), ("Ремонт двигателя", 5000), ("Техническое обслуживание", 1200), ("Ремонт тормозной системы", 800)]
        for name, price in base_services:
            if not db.query(models.Service).filter(models.Service.name == name).first():
                db.add(models.Service(name=name, price=price))
        db.commit()
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AutoServices API запущен"}
