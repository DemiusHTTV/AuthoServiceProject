from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/cars", tags=["cars"])

@router.post("/", response_model=schemas.CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    if not db.query(models.User).filter(models.User.id == car.user_id).first():
        raise HTTPException(status_code=404, detail="Владелец не найден")
    if db.query(models.Car).filter(models.Car.vin == car.vin).first():
        raise HTTPException(status_code=400, detail="Автомобиль с таким VIN уже существует")
    new_car = models.Car(**car.model_dump())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

@router.get("/", response_model=list[schemas.CarResponse])
def get_cars(db: Session = Depends(get_db)):
    return db.query(models.Car).order_by(models.Car.id.desc()).all()
