from typing import Optional
from models import Department
from repositories.base import get_connection

class DepartmentRepository:

    @staticmethod
    def _map(row) -> Department:
        # Маппинг строки
        return Department(
            department_id=row[0],
            name=row[1],
            description=row[2]
        )

    @staticmethod
    def create(name: str, description: Optional[str] = None) -> int:
        # Создание отдела
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Departments (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        last_id = cur.lastrowid
        return last_id

    @staticmethod
    def get_all() -> list[Department]:
        # Все отделы
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT department_id, name, description FROM Departments ORDER BY name ASC")
        rows = cur.fetchall()
        return [DepartmentRepository._map(row) for row in rows]

    @staticmethod
    def get_by_id(department_id: int) -> Optional[Department]:
        # Поиск по ID
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT department_id, name, description FROM Departments WHERE department_id = ?", (department_id,))
        row = cur.fetchone()
        return DepartmentRepository._map(row) if row else None

    @staticmethod
    def update(department_id: int, name: str, description: Optional[str] = None) -> bool:
        # Обновление отдела
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Departments
            SET name = ?, description = ?
            WHERE department_id = ?
        """, (name, description, department_id))
        conn.commit()
        changes = cur.rowcount
        return changes > 0

    @staticmethod
    def delete(department_id: int) -> bool:
        # Удаление отдела
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Departments WHERE department_id = ?", (department_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            pass