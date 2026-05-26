from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# Импорты (подставь свои пути к файлам!)
from database.database import engine, Base, get_db
from models import User, Car, Employee, Order, Service, Part, OrderService, OrderPart
import schemas

# Создаем таблицы (если еще не созданы)
Base.metadata.create_all(bind=engine)


app = FastAPI(title="AutoServices API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешаем вообще всё для тестов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AutoServices на Poetry + SQLite3 запущен!"}

# РОУТ РЕГИСТРАЦИИ
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверка, нет ли уже такого пользователя
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    # Создаем объект модели
    new_user = User(
        fullname=user.fullname,
        phone=user.phone,
        email=user.email,
        password=user.password # В продакшене используй passlib для хеширования
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login_user(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # Ищем пользователя по email
    user = db.query(User).filter(User.email == user_data.email).first()
    
    # Простая проверка (в реальности используй хэширование!)
    if not user or user.password != user_data.password:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    return {"message": "Успешный вход", "user": {"name": user.fullname, "phone": user.phone}}

@app.get("/users/me/{email}")
def get_user_profile(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/orders")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(
        car_id=order.car_id,
        employee_id=order.employee_id,
        status="Новый"
    )
    db.add(new_order)
    db.commit()
    return {"message": "Order created successfully"}
@app.get("/users/cabinet/{email}")
def get_cabinet_data(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Собираем данные (включая связанные машины и заказы)
    return {
        "fullname": user.fullname,
        "cars": [{"brand": c.brand, "model": c.model, "vin": c.vin} for c in user.cars],
        "orders": [{"status": o.status, "created_at": o.created_at} for o in user.orders]
    }