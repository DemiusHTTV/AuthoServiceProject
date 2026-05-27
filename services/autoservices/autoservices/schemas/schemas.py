from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    fullname: str
    phone: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fullname: str
    phone: str
    email: str
    role: str

class CarCreate(BaseModel):
    brand: str
    model: str
    year: int = 2020
    vin: str
    user_id: int

class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    brand: str
    model: str
    year: int
    vin: str
    user_id: int

class EmployeeCreate(BaseModel):
    fullname: str
    position: str
    phone: str
    user_id: Optional[int] = None

class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fullname: str
    position: str
    phone: str
    user_id: Optional[int] = None

class ServiceCreate(BaseModel):
    name: str
    price: float

class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: float

class PublicOrderCreate(BaseModel):
    fullname: str
    phone: str
    brand: str
    model: str
    service_name: str
    description: Optional[str] = None

class OrderCreate(BaseModel):
    car_id: int
    employee_id: Optional[int] = None
    service_name: str
    description: Optional[str] = None
    status: str = "Новый"

class OrderStatusUpdate(BaseModel):
    status: str
    employee_id: Optional[int] = None

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    car_id: int
    employee_id: Optional[int]
    service_name: str
    description: Optional[str]
    status: str
    created_at: datetime
