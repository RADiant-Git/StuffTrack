import sys
import sqlite3
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from repositories.base import DBManager

SCHEMA_FILE = BASE_DIR / "data" / "schema.sql"


@pytest.fixture(autouse=True)
def setup_test_db():
    # Настройка тестовой БД
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    if SCHEMA_FILE.exists():
        conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
    DBManager._conn = conn
    yield conn
    DBManager.close_connection()