"""SQLite database: создание таблиц и загрузка начальных данных из CSV."""

import csv
import sqlite3
import os
from app.config import DB_PATH, DATA_DIR


def get_db():
    """Получить соединение с БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Создать таблицы если не существуют."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS specializations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            base_price REAL NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            bonus_balance REAL DEFAULT 3000,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            specialization_id INTEGER,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY (specialization_id) REFERENCES specializations(id)
        );

        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            client_name TEXT NOT NULL,
            client_email TEXT,
            client_phone TEXT,
            car_brand TEXT NOT NULL,
            car_model TEXT NOT NULL,
            car_year INTEGER,
            description TEXT,
            service_id INTEGER,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (service_id) REFERENCES services(id)
        );

        CREATE TABLE IF NOT EXISTS request_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            worker_id INTEGER NOT NULL,
            status TEXT DEFAULT 'not_started',
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES requests(id),
            FOREIGN KEY (worker_id) REFERENCES workers(id)
        );

        CREATE TABLE IF NOT EXISTS bonuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );

        CREATE TABLE IF NOT EXISTS parts_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            part_id INTEGER NOT NULL,
            quantity_used INTEGER DEFAULT 1,
            FOREIGN KEY (request_id) REFERENCES requests(id)
        );
    """)
    conn.commit()
    conn.close()


def _read_csv(filename):
    """Прочитать CSV файл и вернуть список словарей."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def seed_db():
    """Загрузить начальные данные из CSV если таблицы пустые."""
    conn = get_db()
    cur = conn.cursor()

    # Специализации
    if cur.execute("SELECT COUNT(*) FROM specializations").fetchone()[0] == 0:
        for row in _read_csv("specializations.csv"):
            cur.execute("INSERT INTO specializations (id, name) VALUES (?, ?)",
                        (row["id"], row["name"]))

    # Услуги
    if cur.execute("SELECT COUNT(*) FROM services").fetchone()[0] == 0:
        for row in _read_csv("services.csv"):
            cur.execute(
                "INSERT INTO services (id, name, base_price, description) VALUES (?, ?, ?, ?)",
                (row["id"], row["name"], row["base_price"], row["description"]))

    # Клиенты
    if cur.execute("SELECT COUNT(*) FROM clients").fetchone()[0] == 0:
        for row in _read_csv("clients.csv"):
            cur.execute(
                "INSERT INTO clients (id, name, email, phone, password, bonus_balance) VALUES (?, ?, ?, ?, ?, ?)",
                (row["id"], row["name"], row["email"], row["phone"],
                 row["password_hash"], row["bonus_balance"]))

    # Работники
    if cur.execute("SELECT COUNT(*) FROM workers").fetchone()[0] == 0:
        for row in _read_csv("workers.csv"):
            cur.execute(
                "INSERT INTO workers (id, name, phone, specialization_id, login, password) VALUES (?, ?, ?, ?, ?, ?)",
                (row["id"], row["name"], row["phone"], row["specialization_id"],
                 row["login"], row["password_hash"]))

    # Заявки
    if cur.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 0:
        for row in _read_csv("requests.csv"):
            client_id = row["client_id"] if row["client_id"] else None
            cur.execute(
                """INSERT INTO requests (id, client_id, client_name, client_email,
                   client_phone, car_brand, car_model, car_year, description,
                   service_id, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (row["id"], client_id, row["client_name"], row["client_email"],
                 row["client_phone"], row["car_brand"], row["car_model"],
                 row.get("car_year"), row["description"], row["service_id"],
                 row["status"], row["created_at"]))

    # Назначения
    if cur.execute("SELECT COUNT(*) FROM request_assignments").fetchone()[0] == 0:
        for row in _read_csv("request_assignments.csv"):
            completed = row["completed_at"] if row["completed_at"] else None
            cur.execute(
                """INSERT INTO request_assignments (id, request_id, worker_id, status,
                   assigned_at, completed_at) VALUES (?, ?, ?, ?, ?, ?)""",
                (row["id"], row["request_id"], row["worker_id"], row["status"],
                 row["assigned_at"], completed))

    # Бонусы
    if cur.execute("SELECT COUNT(*) FROM bonuses").fetchone()[0] == 0:
        for row in _read_csv("bonuses.csv"):
            cur.execute(
                "INSERT INTO bonuses (id, client_id, amount, reason, created_at) VALUES (?, ?, ?, ?, ?)",
                (row["id"], row["client_id"], row["amount"], row["reason"],
                 row["created_at"]))

    # Использование деталей
    if cur.execute("SELECT COUNT(*) FROM parts_usage").fetchone()[0] == 0:
        for row in _read_csv("parts_usage.csv"):
            cur.execute(
                "INSERT INTO parts_usage (id, request_id, part_id, quantity_used) VALUES (?, ?, ?, ?)",
                (row["id"], row["request_id"], row["part_id"], row["quantity_used"]))

    conn.commit()
    conn.close()
