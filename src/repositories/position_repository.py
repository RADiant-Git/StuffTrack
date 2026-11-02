from models import Position
from repositories.base import get_connection

class PositionRepository:
    @staticmethod
    def get_by_id(position_id: int) -> Position | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT position_id, title, base_salary, requirements 
            FROM Positions 
            WHERE position_id = ?
        """, (position_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Position(
                position_id=row[0],
                title=row[1],
                base_salary=row[2],
                requirements=row[3]
            )
        return None