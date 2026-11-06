from typing import Optional
from models import Assignment
from repositories.base import get_connection

class AssignmentRepository:
    
    @staticmethod
    def _map(row) -> Assignment:
        # Маппинг строки БД
        return Assignment(
            assignment_id=row[0],
            employee_id=row[1],
            position_id=row[2],
            start_date=row[3],
            end_date=row[4],
            notes=row[5],
            position_title=row[6],
        )

    @staticmethod
    def create_assignment(employee_id: int, position_id: int, notes: Optional[str] = None) -> int:
        # Создание записи назначения
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Assignments (employee_id, position_id, start_date, end_date, notes)
            VALUES (?, ?, datetime('now'), NULL, ?)
        """, (employee_id, position_id, notes))
        conn.commit()
        last_id = cur.lastrowid
        return last_id

    @staticmethod
    def close_current_assignment(employee_id: int, notes: Optional[str] = None) -> bool:
        # Закрытие активного назначения
        conn = get_connection()
        cur = conn.cursor()
        
        # Обновляем notes только если передан новый комментарий при закрытии/переводе
        if notes:
            query = """
                UPDATE Assignments
                SET end_date = datetime('now'), notes = ?
                WHERE employee_id = ? AND end_date IS NULL
            """
            cur.execute(query, (notes, employee_id))
        else:
            query = """
                UPDATE Assignments
                SET end_date = datetime('now')
                WHERE employee_id = ? AND end_date IS NULL
            """
            cur.execute(query, (employee_id,))
            
        conn.commit()
        changes = cur.rowcount
        return changes > 0

    @staticmethod
    def get_history_by_employee(employee_id: int) -> list[Assignment]:
        # Получение истории назначений
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.assignment_id, a.employee_id, a.position_id,
                   a.start_date, a.end_date, a.notes,
                   p.title AS position_title
            FROM Assignments a
            LEFT JOIN Positions p ON a.position_id = p.position_id
            WHERE a.employee_id = ?
            ORDER BY a.start_date DESC
        """, (employee_id,))
        rows = cur.fetchall()
        return [AssignmentRepository._map(row) for row in rows]