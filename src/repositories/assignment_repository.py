from repositories.base import get_connection

class AssignmentRepository:
    @staticmethod
    def create(employee_id: int, position_id: int, start_date: str, notes: str | None = None) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Assignments (employee_id, position_id, start_date, notes)
            VALUES (?, ?, ?, ?)
        """, (employee_id, position_id, start_date, notes))
        conn.commit()
        conn.close()

    @staticmethod
    def close_current_assignment(employee_id: int, end_date: str) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Assignments 
            SET end_date = ? 
            WHERE employee_id = ? AND end_date IS NULL
        """, (end_date, employee_id))
        conn.commit()
        conn.close()