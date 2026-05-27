import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from autoservices.database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="client", nullable=False)  # client/admin/worker
    cars = relationship("Car", back_populates="owner", cascade="all, delete-orphan")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    position = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    orders = relationship("Order", back_populates="master")

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    vin = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="cars")
    orders = relationship("Order", back_populates="car", cascade="all, delete-orphan")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    order_links = relationship("OrderService", back_populates="service")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    service_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="Новый", nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    car = relationship("Car", back_populates="orders")
    master = relationship("Employee", back_populates="orders")
    services = relationship("OrderService", back_populates="order", cascade="all, delete-orphan")
    parts = relationship("OrderPart", back_populates="order", cascade="all, delete-orphan")

class OrderService(Base):
    __tablename__ = "order_services"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, default=1)
    order = relationship("Order", back_populates="services")
    service = relationship("Service", back_populates="order_links")

class OrderPart(Base):
    __tablename__ = "order_parts"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    part_sku = Column(String, nullable=False)
    part_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    order = relationship("Order", back_populates="parts")
