from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from autoservices.database.database import get_db
import autoservices.models.models as models
import autoservices.schemas.schemas as schemas

router = APIRouter(prefix="/cars", tags=["Автомобили"])

@router.post("/", response_model=schemas.CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    # Проверяем существующего владельца
    owner = db.query(models.User).filter(models.User.id == car.user_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Указанный владелец (User) не найден")

    # Проверяем уникальность VIN
    db_car = db.query(models.Car).filter(models.Car.vin == car.vin).first()
    if db_car:
        raise HTTPException(status_code=400, detail="Автомобиль с таким VIN уже существует")

    new_car = models.Car(
        brand=car.brand, 
        model=car.model, 
        year=car.year, 
        vin=car.vin, 
        user_id=car.user_id
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

@router.get("/", response_model=List[schemas.CarResponse])
def get_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Car).offset(skip).limit(limit).all()
