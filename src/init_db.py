import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "stafftrack.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")

def create_database():
    print(f"📦 Создание базы данных: {DB_FILE}")
    
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Подключаемся и накатываем скрипт
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.executescript(sql_script)
        conn.commit()
        print("✅ Все таблицы успешно созданы и наполнены тестовыми данными!")
    except Exception as e:
        print(f"❌ Ошибка при инициализации базы данных: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()