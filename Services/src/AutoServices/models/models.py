from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

class ClientModel(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    car_brand: Mapped[str] = mapped_column(String, nullable=False)

class ManagerModel(Base):
    __tablename__ = "managers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)

class WorkerModel(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)

class RequestModel(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("managers.id"), nullable=True)
    status: Mapped[str] = mapped_column(String, default="new") # new, in_progress, completed
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class RequestServiceModel(Base):
    __tablename__ = "request_services"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    service_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending") # pending, in_progress, done

class ExecutionModel(Base):
    __tablename__ = "executions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_service_id: Mapped[int] = mapped_column(ForeignKey("request_services.id", ondelete="CASCADE"), nullable=False)
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String, default="in_progress") # in_progress, completed