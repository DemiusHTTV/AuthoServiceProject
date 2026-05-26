from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .schemas.schemas import *
from .database import get_db
from AutoServices.models.models import UserModel, ClientModel, ManagerModel, WorkerModel, RequestModel

router = APIRouter(prefix="/api/v1", tags=["AutoService Core"])

# ==========================================
# 🚗 ВХОД ДЛЯ КЛИЕНТОВ (Веб-сайт клиентов)
# ==========================================
@router.post("/auth/client/login")
def client_login(data: LoginRequest, db: Session = Depends(get_db)):
    """Проверяет логин/пароль и проверяет, что этот юзер зарегистрирован как КЛИЕНТ"""
    user = db.query(UserModel).filter(UserModel.login == data.login, UserModel.password == data.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    client = db.query(ClientModel).filter(ClientModel.user_id == user.id).first()
    if not client:
        raise HTTPException(status_code=403, detail="Доступ запрещен. Вы не являетесь клиентом.")
        
    return {"client_id": client.id, "user_id": user.id, "full_name": client.full_name}


# ==========================================
# 👑 ВХОД ДЛЯ АДМИНОВ / МЕНЕДЖЕРОВ (Админ-панель)
# ==========================================
@router.post("/auth/admin/login")
def admin_login(data: LoginRequest, db: Session = Depends(get_db)):
    """Вход для бэк-офиса (Админы и Менеджеры)"""
    user = db.query(UserModel).filter(UserModel.login == data.login, UserModel.password == data.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    # Проверяем, менеджер ли это
    manager = db.query(ManagerModel).filter(ManagerModel.user_id == user.id).first()
    
    # Если не менеджер, проверяем, может это чистый Админ (нет в клиентах/воркерах/менеджерах)
    is_client = db.query(ClientModel).filter(ClientModel.user_id == user.id).first()
    is_worker = db.query(WorkerModel).filter(WorkerModel.user_id == user.id).first()
    
    if not manager and (is_client or is_worker):
        raise HTTPException(status_code=403, detail="У вас нет прав администратора")
        
    return {
        "user_id": user.id,
        "is_manager": manager is not None,
        "manager_id": manager.id if manager else None,
        "full_name": manager.full_name if manager else "Главный Администратор"
    }


# ==========================================
# 💻 ВХОД ДЛЯ РАБОТНИКОВ (Десктопное приложение)
# ==========================================
@router.post("/auth/worker/login")
def worker_login(data: LoginRequest, db: Session = Depends(get_db)):
    """Точка входа для десктопного приложения автомехаников"""
    user = db.query(UserModel).filter(UserModel.login == data.login, UserModel.password == data.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    worker = db.query(WorkerModel).filter(WorkerModel.user_id == user.id).first()
    if not worker:
        raise HTTPException(status_code=403, detail="Этот аккаунт не зарегистрирован как работник")
        
    return {"worker_id": worker.id, "user_id": user.id, "full_name": worker.full_name}


# ==========================================
# 📊 ТАБЛИЦЫ ДЛЯ РАЗНЫХ ИНТЕРФЕЙСОВ
# ==========================================

# Для Админки (список работников и управление)
@router.get("/admin/workers", response_model=List[WorkerResponse])
def get_all_workers(db: Session = Depends(get_db)):
    return db.query(WorkerModel).all()

# Для Админки/Менеджеров (список всех заявок)
@router.get("/manager/requests", response_model=List[RequestResponse])
def get_all_requests(db: Session = Depends(get_db)):
    return db.query(RequestModel).all()

# Для десктопа Воркера (только его задачи)
@router.get("/worker/{worker_id}/tasks")
def get_worker_tasks(worker_id: int, db: Session = Depends(get_db)):
    # Здесь логика запроса задач для конкретного id воркера
    pass