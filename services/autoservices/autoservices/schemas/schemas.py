from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# 1. СХЕМЫ ДЛЯ USER (КЛИЕНТЫ)
# ==========================================
class UserBase(BaseModel):
    fullname: str = Field(..., examples=["Иванов Иван Иванович"])
    phone: str = Field(..., examples=["+79991112233"])
    email: Optional[str] = Field(None, examples=["ivan@example.com"])

class UserCreate(UserBase):
    pass  # То, что прилетает при создании клиента

class UserResponse(UserBase):
    id: int
    fullname: str
    phone: str
    email: str
    role: str

    class Config:
        from_attributes = True  # Позволяет Pydantic читать данные из ORM SQLAlchemy


# ==========================================
# 2. СХЕМЫ ДЛЯ CAR (АВТОМОБИЛИ)
# ==========================================
class CarBase(BaseModel):
    brand: str = Field(..., examples=["Toyota"])
    model: str = Field(..., examples=["Camry"])
    year: int = Field(..., examples=[2021])
    vin: str = Field(..., examples=["1A2B3C4D5E6F7G8H9"])

class CarCreate(CarBase):
    user_id: int  # ID владельца обязателен при привязке авто

class CarResponse(CarBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# ==========================================
# 3. СХЕМЫ ДЛЯ EMPLOYEE (СОТРУДНИКИ)
# ==========================================
class EmployeeBase(BaseModel):
    fullname: str
    position: str  # Механик, Мастер-приемщик и т.д.
    phone: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# 4. СХЕМЫ ДЛЯ SERVICE И PART (УСЛУГИ И ДЕТАЛИ)
# ==========================================
class ServiceBase(BaseModel):
    name: str
    price: float

class ServiceResponse(ServiceBase):
    id: int

    class Config:
        from_attributes = True

class PartBase(BaseModel):
    name: str
    sku: str
    price: float
    stock: int

class PartResponse(PartBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# 5. СХЕМЫ ДЛЯ ORDERS (ЗАКАЗЫ)
# ==========================================
class OrderBase(BaseModel):
    car_id: int
    employee_id: int
    status: Optional[str] = "Новый"

class OrderCreate(OrderBase):
        car_id: int
        employee_id: int

class OrderResponse(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6) # Обязательный пароль

class UserLogin(BaseModel):
        email: EmailStr
        password: str