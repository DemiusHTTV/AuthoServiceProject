from __future__ import annotations

import sqlite3

SCHEMA_STATEMENTS: list[str] = [
    # базовые таблицы (на них есть FK)
    """
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS spare_parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """,
    # ---------------- WAREHOUSE ----------------
    """
    CREATE TABLE IF NOT EXISTS warehouse (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id INTEGER NOT NULL UNIQUE,
        quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),

        FOREIGN KEY (part_id)
        REFERENCES spare_parts(id)
        ON DELETE CASCADE
    )
    """,
    # ---------------- SERVICE PARTS ----------------
    """
    CREATE TABLE IF NOT EXISTS service_parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_id INTEGER NOT NULL,
        part_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),

        FOREIGN KEY (service_id)
        REFERENCES services(id),

        FOREIGN KEY (part_id)
        REFERENCES spare_parts(id),

        UNIQUE(service_id, part_id)
    )
    """,
]


def init_schema(connection: sqlite3.Connection) -> None:
    for statement in SCHEMA_STATEMENTS:
        connection.execute(statement)
