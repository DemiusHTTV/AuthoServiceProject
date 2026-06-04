from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from autoservices.database.database import get_db
from autoservices.models import models
from autoservices.schemas import schemas

import httpx
from typing import List
from autoservice_core import OrderItem, calculate_total_price, Part

router = APIRouter(prefix="/orders", tags=["orders"])

WAREHOUSE_URL = "http://localhost:8001"

@router.post("/calculate")
async def calculate_order(items: List[OrderItem]):
    """
    Расчет заказа: идем в микросервис склада за деталями,
    используем наше ядро (autoservice_core) для расчета стоимости.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{WAREHOUSE_URL}/api/parts")
            response.raise_for_status()
            parts_db = [Part(**p) for p in response.json()]
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Склад временно недоступен")
            
    try:
        total = calculate_total_price(items, parts_db)
        return {"status": "success", "total_price": total, "items_count": len(items)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/public", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def public_order(order: schemas.PublicOrderCreate, db: Session = Depends(get_db)):
    email = f"client_{order.phone.replace('+','').replace(' ','').replace('-','').replace('(','').replace(')','')}@phone.local"
    user = db.query(models.User).filter(models.User.phone == order.phone).first()
    if not user:
        default_bonus = 0
        setting = db.get(models.Setting, "default_bonus_balance")
        if setting:
            try:
                default_bonus = int(setting.value)
            except ValueError:
                default_bonus = 0
        user = models.User(
            fullname=order.fullname,
            phone=order.phone,
            email=email,
            password="client123",
            role="client",
            bonus_balance=default_bonus,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    car = models.Car(brand=order.brand, model=order.model, year=2020, vin=f"TEMP-{user.id}-{int(__import__('time').time())}", user_id=user.id)
    db.add(car)
    db.commit()
    db.refresh(car)
    new_order = models.Order(car_id=car.id, service_name=order.service_name, description=order.description, status="Новый")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not db.query(models.Car).filter(models.Car.id == order.car_id).first():
        raise HTTPException(status_code=404, detail="Машина не найдена")
    new_order = models.Order(**order.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).options(joinedload(models.Order.car).joinedload(models.Car.owner), joinedload(models.Order.master)).order_by(models.Order.id.desc()).all()
    return [{
        "id": o.id,
        "service_name": o.service_name,
        "description": o.description,
        "status": o.status,
        "created_at": o.created_at,
        "car": {"id": o.car.id, "brand": o.car.brand, "model": o.car.model, "vin": o.car.vin},
        "client": {"id": o.car.owner.id, "fullname": o.car.owner.fullname, "phone": o.car.owner.phone, "email": o.car.owner.email},
        "employee": {"id": o.master.id, "fullname": o.master.fullname} if o.master else None,
    } for o in orders]

@router.patch("/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, payload: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    order.status = payload.status
    if payload.employee_id is not None:
        order.employee_id = payload.employee_id
    db.commit()
    db.refresh(order)
    return order
