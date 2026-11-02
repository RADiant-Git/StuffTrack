from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "stafftrack.db"
SCHEMA_FILE = BASE_DIR / "data" / "schema.sql"

def create_database():
    if not SCHEMA_FILE.exists():
        return

    sql_script = SCHEMA_FILE.read_text(encoding="utf-8")

    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(sql_script)
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()