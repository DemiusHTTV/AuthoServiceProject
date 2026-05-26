from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    login: str
    password: str


class ClientLoginResponse(BaseModel):
    client_id: int
    user_id: int
    full_name: str

class AdminLoginResponse(BaseModel):
    user_id: int
    is_manager: bool
    manager_id: Optional[int]
    full_name: str

class WorkerLoginResponse(BaseModel):
    worker_id: int
    user_id: int
    full_name: str


class UserCreate(BaseModel):
    login: str
    password: str

class UserResponse(BaseModel):
    id: int
    login: str
    class Config: from_attributes = True

class ClientCreate(BaseModel):
    user_id: int
    full_name: str
    phone: str
    car_brand: str

class ClientResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone: str
    car_brand: str
    class Config: from_attributes = True

class WorkerResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    class Config: from_attributes = True

# --- Заявки и Задачи ---
class RequestCreate(BaseModel):
    client_id: int

class RequestResponse(BaseModel):
    id: int
    client_id: int
    manager_id: Optional[int]
    status: str
    created_at: datetime
    class Config: from_attributes = True

class RequestServiceCreate(BaseModel):
    request_id: int
    service_name: str

class RequestServiceResponse(BaseModel):
    id: int
    request_id: int
    service_name: str
    status: str
    class Config: from_attributes = True

class AssignWorkerRequest(BaseModel):
    request_service_id: int
    worker_id: int

class TaskResponse(BaseModel):
    id: int
    request_service_id: int
    worker_id: int
    status: str
    class Config: from_attributes = True