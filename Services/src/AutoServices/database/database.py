from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Generator

DEFAULT_DB_PATH = os.environ.get("DB_PATH", "autoservice.db")


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    if path.parent and str(path.parent) not in ("", "."):
        path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path, check_same_thread=False)
    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON;")
    connection.execute("PRAGMA journal_mode = WAL;")
    connection.execute("PRAGMA synchronous = NORMAL;")
    connection.execute("PRAGMA busy_timeout = 5000;")

    return connection


def get_db() -> Generator[sqlite3.Connection, None, None]:
    connection = get_connection()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
