"""Pydantic-модели для валидации данных."""

from pydantic import BaseModel
from typing import Optional


class ClientRegister(BaseModel):
    name: str
    email: str
    phone: str
    password: str


class ClientLogin(BaseModel):
    email: str
    password: str


class WorkerLogin(BaseModel):
    login: str
    password: str


class AdminLogin(BaseModel):
    login: str
    password: str


class OrderCreate(BaseModel):
    client_name: str
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    car_brand: str
    car_model: str
    car_year: Optional[int] = None
    description: Optional[str] = None
    service_id: Optional[int] = None
    client_id: Optional[int] = None
    bonus_to_spend: float = 0


class AssignWorker(BaseModel):
    request_id: int
    worker_id: int


class StatusUpdate(BaseModel):
    status: str
