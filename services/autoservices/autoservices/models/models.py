from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
import datetime
from autoservices.database.database import Base

# 1. ТАБЛИЦА: Клиенты / Пользователи приложения
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    
    # Отношение: один ко многим (у пользователя может быть несколько машин)
    cars = relationship("Car", back_populates="owner", cascade="all, delete-orphan")


# 2. ТАБЛИЦА: Автомобили клиентов
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)            # Марка (напр., Toyota)
    model = Column(String, nullable=False)            # Модель (напр., Camry)
    year = Column(Integer, nullable=False)             # Год выпуска
    vin = Column(String, unique=True, nullable=False)     # VIN-номер
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Обратные связи
    owner = relationship("User", back_populates="cars")
    orders = relationship("Order", back_populates="car", cascade="all, delete-orphan")


# 3. ТАБЛИЦА: Сотрудники автосервиса
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    position = Column(String, nullable=False)         # Должность (напр., Механик, Электрик)
    phone = Column(String, nullable=False)

    # Связь с заказами, которые принял или выполняет этот сотрудник
    orders = relationship("Order", back_populates="master")


# 4. ТАБЛИЦА: Справочник Услуг (Прайс-лист на работы)
class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) # Название (напр., "Замена колодок")
    price = Column(Float, nullable=False)              # Базовая стоимость работы

    order_links = relationship("OrderService", back_populates="service")


# 5. ТАБЛИЦА: Справочник Запчастей (Каталог деталей)
class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)             # Название (напр., "Фильтр масляный")
    sku = Column(String, unique=True, nullable=False)     # Артикул / Парт-номер
    price = Column(Float, nullable=False)              # Розничная цена детали
    stock = Column(Integer, default=0)                # Текущий остаток

    order_links = relationship("OrderPart", back_populates="part")


# 6. ТАБЛИЦА: Заказы (Заказ-наряды)
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False)
    status = Column(String, default="Новый")          # Статусы: Новый, В работе, Выполнен, Закрыт
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Прямые связи к сущностям
    car = relationship("Car", back_populates="orders")
    master = relationship("Employee", back_populates="orders")
    
    # Связи к соединительным таблицам (какие работы и запчасти внутри этого заказа)
    services = relationship("OrderService", back_populates="order", cascade="all, delete-orphan")
    parts = relationship("OrderPart", back_populates="order", cascade="all, delete-orphan")


# 7. ТАБЛИЦА: Работы, добавленные в конкретный заказ (Связующая M2M)
class OrderService(Base):
    __tablename__ = "order_services"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, default=1)             # Количество повторений операции

    order = relationship("Order", back_populates="services")
    service = relationship("Service", back_populates="order_links")


# 8. ТАБЛИЦА: Запчасти, потраченные на конкретный заказ (Связующая M2M)
class OrderPart(Base):
    __tablename__ = "order_parts"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    part_id = Column(Integer, ForeignKey("parts.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, default=1)             # Количество использованных штук

    order = relationship("Order", back_populates="parts")
    part = relationship("Part", back_populates="order_links")
