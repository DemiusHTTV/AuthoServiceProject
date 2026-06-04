from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(tags=["auth/users"])

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    if db.query(models.User).filter(models.User.phone == user.phone).first():
        raise HTTPException(status_code=400, detail="Телефон уже зарегистрирован")
    default_bonus = 0
    setting = db.get(models.Setting, "default_bonus_balance")
    if setting:
        try:
            default_bonus = int(setting.value)
        except ValueError:
            default_bonus = 0
    new_user = models.User(**user.model_dump(), role="client", bonus_balance=default_bonus)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or user.password != user_data.password:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    return {"message": "Успешный вход", "user": schemas.UserResponse.model_validate(user)}

@router.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).order_by(models.User.id.desc()).all()

@router.get("/users/cabinet/{email}")
def get_cabinet_data(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orders = []
    for car in user.cars:
        for order in car.orders:
            orders.append({
                "id": order.id,
                "car": f"{car.brand} {car.model}",
                "service_name": order.service_name,
                "status": order.status,
                "created_at": order.created_at,
            })
    return {
        "id": user.id,
        "fullname": user.fullname,
        "email": user.email,
        "role": user.role,
        "bonus_balance": user.bonus_balance,
        "cars": [{"id": c.id, "brand": c.brand, "model": c.model, "year": c.year, "vin": c.vin} for c in user.cars],
        "orders": orders,
    }
