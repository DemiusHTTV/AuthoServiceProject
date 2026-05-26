from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from autoservices.database.database import get_db
import autoservices.models.models as models
import autoservices.schemas.schemas as schemas

router = APIRouter(prefix="/orders", tags=["Заказы"])

@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Проверяем машину
    car = db.query(models.Car).filter(models.Car.id == order.car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    
    # Создаем базовый заказ (пока без привязки сотрудника для упрощения)
    new_order = models.Order(
        car_id=order.car_id,
        employee_id=order.employee_id,
        status=order.status
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()
