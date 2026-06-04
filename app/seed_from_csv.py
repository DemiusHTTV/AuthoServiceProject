import csv
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import models

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def _seed_dir() -> Path:
    # .../autoservices/main.py -> .../ (service root) -> seed/
    return Path(__file__).resolve().parents[1] / "seed"


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows: list[dict[str, str]] = []
        for row in reader:
            if not row:
                continue
            if not any((v or "").strip() for v in row.values()):
                continue
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def _parse_dt(value: str) -> datetime:
    return datetime.strptime(value, DATETIME_FORMAT)


def _get_setting_int(db: Session, key: str, default: int) -> int:
    obj = db.get(models.Setting, key)
    if not obj:
        return default
    try:
        return int(obj.value)
    except ValueError:
        return default


def seed_autoservice_from_csv(db: Session) -> None:
    seed_dir = _seed_dir()

    # 1) settings
    for row in _read_csv(seed_dir / "settings.csv"):
        key = row.get("key", "")
        value = row.get("value", "")
        if not key or not value:
            continue
        obj = db.get(models.Setting, key)
        if not obj:
            db.add(models.Setting(key=key, value=value))
        else:
            obj.value = value
    db.commit()

    default_bonus = _get_setting_int(db, "default_bonus_balance", default=0)

    # 2) users
    for row in _read_csv(seed_dir / "users.csv"):
        email = row.get("email", "")
        phone = row.get("phone", "")
        if not email or not phone:
            continue
        user = db.query(models.User).filter(models.User.email == email).first()
        bonus_raw = row.get("bonus_balance", "")
        bonus_balance = (
            int(bonus_raw) if bonus_raw else default_bonus if row.get("role", "client") == "client" else 0
        )
        if not user:
            db.add(
                models.User(
                    fullname=row.get("fullname", "") or "Без имени",
                    phone=phone,
                    email=email,
                    password=row.get("password", "") or "client123",
                    role=row.get("role", "client") or "client",
                    bonus_balance=bonus_balance,
                )
            )
        else:
            user.fullname = row.get("fullname", user.fullname) or user.fullname
            user.phone = phone or user.phone
            user.password = row.get("password", user.password) or user.password
            user.role = row.get("role", user.role) or user.role
            user.bonus_balance = bonus_balance
    db.commit()

    # 3) employees
    for row in _read_csv(seed_dir / "employees.csv"):
        phone = row.get("phone", "")
        if not phone:
            continue
        employee = db.query(models.Employee).filter(models.Employee.phone == phone).first()
        user_id = None
        user_email = row.get("user_email", "")
        if user_email:
            u = db.query(models.User).filter(models.User.email == user_email).first()
            if u:
                user_id = u.id
        if not employee:
            db.add(
                models.Employee(
                    fullname=row.get("fullname", "") or "Без имени",
                    position=row.get("position", "") or "Сотрудник",
                    phone=phone,
                    user_id=user_id,
                )
            )
        else:
            employee.fullname = row.get("fullname", employee.fullname) or employee.fullname
            employee.position = row.get("position", employee.position) or employee.position
            employee.user_id = user_id
    db.commit()

    # 4) services
    for row in _read_csv(seed_dir / "services.csv"):
        name = row.get("name", "")
        if not name:
            continue
        obj = db.query(models.Service).filter(models.Service.name == name).first()
        price_raw = row.get("price", "0")
        try:
            price = float(price_raw)
        except ValueError:
            price = 0.0
        if not obj:
            db.add(models.Service(name=name, price=price))
        else:
            obj.price = price
    db.commit()

    # 5) cars
    for row in _read_csv(seed_dir / "cars.csv"):
        vin = row.get("vin", "")
        user_email = row.get("user_email", "")
        if not vin or not user_email:
            continue
        car = db.query(models.Car).filter(models.Car.vin == vin).first()
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            continue
        try:
            year = int(row.get("year", "2020") or "2020")
        except ValueError:
            year = 2020
        if not car:
            db.add(
                models.Car(
                    brand=row.get("brand", "") or "Unknown",
                    model=row.get("model", "") or "Unknown",
                    year=year,
                    vin=vin,
                    user_id=user.id,
                )
            )
        else:
            car.brand = row.get("brand", car.brand) or car.brand
            car.model = row.get("model", car.model) or car.model
            car.year = year
            car.user_id = user.id
    db.commit()

    # 6) orders (map (vin, created_at) -> order_id)
    order_key_to_id: dict[tuple[str, datetime], int] = {}
    for row in _read_csv(seed_dir / "orders.csv"):
        vin = row.get("car_vin", "")
        created_at_raw = row.get("created_at", "")
        if not vin or not created_at_raw:
            continue
        created_at = _parse_dt(created_at_raw)
        car = db.query(models.Car).filter(models.Car.vin == vin).first()
        if not car:
            continue
        q = (
            db.query(models.Order)
            .join(models.Car, models.Order.car_id == models.Car.id)
            .filter(models.Car.vin == vin, models.Order.created_at == created_at)
        )
        existing = q.first()
        employee_id = None
        employee_phone = row.get("employee_phone", "")
        if employee_phone:
            e = db.query(models.Employee).filter(models.Employee.phone == employee_phone).first()
            if e:
                employee_id = e.id
        if not existing:
            obj = models.Order(
                car_id=car.id,
                employee_id=employee_id,
                service_name=row.get("service_name", "") or "Услуга",
                description=row.get("description", "") or None,
                status=row.get("status", "") or "Новый",
                created_at=created_at,
            )
            db.add(obj)
            db.commit()
            db.refresh(obj)
            order_key_to_id[(vin, created_at)] = obj.id
        else:
            existing.employee_id = employee_id
            existing.service_name = row.get("service_name", existing.service_name) or existing.service_name
            existing.description = row.get("description", existing.description) or existing.description
            existing.status = row.get("status", existing.status) or existing.status
            db.commit()
            order_key_to_id[(vin, created_at)] = existing.id

    # 7) order_services
    for row in _read_csv(seed_dir / "order_services.csv"):
        vin = row.get("car_vin", "")
        created_at_raw = row.get("created_at", "")
        service_name = row.get("service_name", "")
        if not vin or not created_at_raw or not service_name:
            continue
        created_at = _parse_dt(created_at_raw)
        order_id = order_key_to_id.get((vin, created_at))
        if not order_id:
            continue
        service = db.query(models.Service).filter(models.Service.name == service_name).first()
        if not service:
            continue
        try:
            qty = int(row.get("quantity", "1") or "1")
        except ValueError:
            qty = 1
        link = (
            db.query(models.OrderService)
            .filter(models.OrderService.order_id == order_id, models.OrderService.service_id == service.id)
            .first()
        )
        if not link:
            db.add(models.OrderService(order_id=order_id, service_id=service.id, quantity=qty))
        else:
            link.quantity = qty
        db.commit()

    # 8) order_parts
    for row in _read_csv(seed_dir / "order_parts.csv"):
        vin = row.get("car_vin", "")
        created_at_raw = row.get("created_at", "")
        sku = row.get("part_sku", "")
        if not vin or not created_at_raw or not sku:
            continue
        created_at = _parse_dt(created_at_raw)
        order_id = order_key_to_id.get((vin, created_at))
        if not order_id:
            continue
        try:
            qty = int(row.get("quantity", "1") or "1")
        except ValueError:
            qty = 1
        try:
            price = float(row.get("part_price", "0") or "0")
        except ValueError:
            price = 0.0
        existing = (
            db.query(models.OrderPart)
            .filter(models.OrderPart.order_id == order_id, models.OrderPart.part_sku == sku)
            .first()
        )
        if not existing:
            db.add(
                models.OrderPart(
                    order_id=order_id,
                    part_sku=sku,
                    part_name=row.get("part_name", "") or sku,
                    part_price=price,
                    quantity=qty,
                )
            )
        else:
            existing.part_name = row.get("part_name", existing.part_name) or existing.part_name
            existing.part_price = price
            existing.quantity = qty
        db.commit()

