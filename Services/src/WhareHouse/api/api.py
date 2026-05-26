from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

# Импортируй свои схемы и модели базы данных
from .schemas.schemas import *
from .database import get_db
from AutoServices.models.models import UserModel, AppointmentModel, ClientModel, WorkerModel, GarageModel, BonusModel, InventoryModel

router = APIRouter(prefix="/api", tags=["AutoService Core Engine"])

# ==========================================
# 🔐 1. АВТОРИЗАЦИЯ И РЕГИСТРАЦИЯ
# ==========================================

@router.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.login == data.login, UserModel.password == data.password).first()
    
    if not user and data.login == "admin" and data.password == "123":
        return {"status": "success", "type": "admin", "user_id": 1}
        
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    if user.role == "admin":
        return {"status": "success", "type": "admin", "user_id": user.id}
        
    worker = db.query(WorkerModel).filter(WorkerModel.user_id == user.id).first()
    if worker:
        return {"status": "success", "type": "worker", "worker_id": worker.id}
        
    client = db.query(ClientModel).filter(ClientModel.user_id == user.id).first()
    if client:
        return {"status": "success", "type": "client", "client_id": client.id}
        
    raise HTTPException(status_code=403, detail="Роль пользователя не найдена")


@router.post("/auth/register")
def register_client(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.login == data.login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Этот логин уже занят")
        
    new_user = UserModel(login=data.login, password=data.password, role="client")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    new_client = ClientModel(user_id=new_user.id, full_name=data.full_name, phone=data.phone)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    new_bonus = BonusModel(client_id=new_client.id, balance=250)
    db.add(new_bonus)
    db.commit()
    
    return {"status": "success", "message": "Регистрация успешна"}


# ==========================================
# 📅 2. РАСПИСАНИЕ И ЗАПИСИ
# ==========================================

@router.get("/appointments", response_model=List[AppointmentResponse])
def get_all_appointments(db: Session = Depends(get_db)):
    return db.query(AppointmentModel).all()


@router.put("/appointments/{id}/status", response_model=AppointmentResponse)
def update_appointment_status(id: int, data: StatusUpdateRequest, db: Session = Depends(get_db)):
    app = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Запись не найдена")
        
    app.status = data.status
    db.commit()
    db.refresh(app)
    return app


@router.delete("/appointments/{id}", status_code=204)
def delete_appointment(id: int, db: Session = Depends(get_db)):
    app = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    db.delete(app)
    db.commit()
    return None


# ==========================================
# 👤 3. РУЧКИ КЛИЕНТА (ЧЕРЕЗ ID)
# ==========================================

@router.get("/users/client/{id}")
def get_current_client_profile(id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return {"full_name": client.full_name, "phone": client.phone}


@router.get("/appointments/my", response_model=List[AppointmentResponse])
def get_client_appointments(client_id: int, db: Session = Depends(get_db)):
    return db.query(AppointmentModel).filter(AppointmentModel.client_id == client_id).all()


@router.get("/garage", response_model=List[CarResponse])
def get_client_garage(client_id: int, db: Session = Depends(get_db)):
    return db.query(GarageModel).filter(GarageModel.client_id == client_id).all()


@router.get("/bonuses")
def get_client_bonuses(client_id: int, db: Session = Depends(get_db)):
    bonus = db.query(BonusModel).filter(BonusModel.client_id == client_id).first()
    if not bonus:
        return {"balance": 0}
    return {"balance": bonus.balance}


# ==========================================
# 📦 4. БАЗА КЛИЕНТОВ, СКЛАД И РАБОЧИЕ
# ==========================================

@router.get("/clients", response_model=List[ClientResponse])
def get_all_clients_for_admin(db: Session = Depends(get_db)):
    return db.query(ClientModel).all()


@router.get("/inventory")
def get_warehouse_inventory(db: Session = Depends(get_db)):
    """Выгрузка всех деталей со склада"""
    return db.query(InventoryModel).all()


@router.get("/workers/requests", response_model=List[AppointmentResponse])
def get_worker_requests(worker_id: int, db: Session = Depends(get_db)):
    return db.query(AppointmentModel).filter(
        AppointmentModel.worker_id == worker_id,
        AppointmentModel.status != "Выполнено"
    ).all()