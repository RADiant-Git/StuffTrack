import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "data" / "stafftrack.db"

class DBManager:
    _conn = None

    @classmethod
    def get_connection(cls):
        if cls._conn is None:
            cls._conn = sqlite3.connect(DB_FILE)
            cls._conn.execute("PRAGMA foreign_keys = ON;")
        return cls._conn

    @classmethod
    def close_connection(cls):
        if cls._conn is not None:
            cls._conn.close()
            cls._conn = None

def get_connection():
    return DBManager.get_connection()