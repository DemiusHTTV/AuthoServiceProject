from __future__ import annotations

import sqlite3

SCHEMA_STATEMENTS: list[str] = [
    # ---------------- ROLES ----------------
    """
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """,
    # ---------------- USERS ----------------
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role_id INTEGER NOT NULL,

        FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE
    )
    """,
    # ---------------- CLIENTS ----------------
    """
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        car_brand TEXT NOT NULL,

        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """,
    # ---------------- MANAGERS ----------------
    """
    CREATE TABLE IF NOT EXISTS managers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        full_name TEXT NOT NULL,

        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """,
    # ---------------- WORKERS ----------------
    """
    CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        full_name TEXT NOT NULL,

        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """,
    # ---------------- REQUESTS ----------------
    """
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        manager_id INTEGER,

        status TEXT NOT NULL DEFAULT 'new',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (client_id)
        REFERENCES clients(id),

        FOREIGN KEY (manager_id)
        REFERENCES managers(id)
    )
    """,
    # ---------------- SERVICES ----------------
    """
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL
    )
    """,
    # ---------------- REQUEST SERVICES ----------------
    """
    CREATE TABLE IF NOT EXISTS request_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',

        FOREIGN KEY (request_id)
        REFERENCES requests(id)
        ON DELETE CASCADE,

        FOREIGN KEY (service_id)
        REFERENCES services(id)
        ON DELETE CASCADE
    )
    """,
    # ---------------- EXECUTIONS ----------------
    """
    CREATE TABLE IF NOT EXISTS executions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_service_id INTEGER NOT NULL,
        worker_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'in_progress',

        FOREIGN KEY (request_service_id)
        REFERENCES request_services(id)
        ON DELETE CASCADE,

        FOREIGN KEY (worker_id)
        REFERENCES workers(id)
        ON DELETE CASCADE
    )
    """,
    # ---------------- SPARE PARTS ----------------
    """
    CREATE TABLE IF NOT EXISTS spare_parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """,
]


def init_schema(connection: sqlite3.Connection) -> None:
    for statement in SCHEMA_STATEMENTS:
        connection.execute(statement)

    # базовые роли (id генерится автоматически)
    connection.executemany(
        "INSERT OR IGNORE INTO roles(name) VALUES (?)",
        [("client",), ("manager",), ("worker",)],
    )
