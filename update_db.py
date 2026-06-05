from app.database.database import SessionLocal
from app.models.models import Order
db = SessionLocal()
status_map = {
    "Новый": "new",
    "Принят": "accepted",
    "В работе": "in_progress",
    "Закрыт": "completed",
    "Отклонен": "rejected"
}
orders = db.query(Order).all()
for o in orders:
    if o.status in status_map:
        o.status = status_map[o.status]
db.commit()
print("Updated statuses")
