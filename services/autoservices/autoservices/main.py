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

