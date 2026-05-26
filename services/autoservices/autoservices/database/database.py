from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Ссылка на БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./autoservice.db"

# 2. Движок (engine)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Базовый класс для моделей
Base = declarative_base()

# 5. Функция-зависимость для получения сессии в роутах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()