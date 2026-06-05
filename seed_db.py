from app.database.database import SessionLocal
from app.seed_from_csv import seed_autoservice_from_csv
db = SessionLocal()
seed_autoservice_from_csv(db)
print("Seeding complete")
