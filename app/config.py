import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "autoservice.db")
WAREHOUSE_URL = os.getenv("WAREHOUSE_URL", "http://localhost:8001")
DEFAULT_BONUS = 3000
