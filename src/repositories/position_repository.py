from typing import Optional
from models import Position
from repositories.base import get_connection

class PositionRepository:
    
    @staticmethod
    def _map(row) -> Position:
        # Маппинг строки БД
        return Position(
            position_id=row[0],
            title=row[1],
            base_salary=row[2],
            requirements=row[3]
        )

    @staticmethod
    def create(title: str, base_salary: int, requirements: Optional[str] = None) -> int:
        # Создание должности
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Positions (title, base_salary, requirements)
            VALUES (?, ?, ?)
        """, (title, base_salary, requirements))
        conn.commit()
        last_id = cur.lastrowid
        return last_id

    @staticmethod
    def get_by_id(position_id: int) -> Optional[Position]:
        # Поиск по ID
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT position_id, title, base_salary, requirements
            FROM Positions
            WHERE position_id = ?
        """, (position_id,))
        row = cur.fetchone()
        return PositionRepository._map(row) if row else None

    @staticmethod
    def get_all() -> list[Position]:
        # Получение всех должностей
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT position_id, title, base_salary, requirements
            FROM Positions
            ORDER BY title ASC
        """)
        rows = cur.fetchall()
        return [PositionRepository._map(row) for row in rows]

    @staticmethod
    def update(
        position_id: int, 
        title: Optional[str] = None, 
        base_salary: Optional[int] = None, 
        requirements: Optional[str] = None
    ) -> bool:
        # Изменение данных должности
        fields_to_update = []
        params = []

        if title is not None:
            fields_to_update.append("title = ?")
            params.append(title)
        
        if base_salary is not None:
            fields_to_update.append("base_salary = ?")
            params.append(base_salary)
            
        if requirements is not None:
            fields_to_update.append("requirements = ?")
            params.append(requirements)

        if not fields_to_update:
            return False

        params.append(position_id)
        
        sql_query = f"""
            UPDATE Positions
            SET {", ".join(fields_to_update)}
            WHERE position_id = ?
        """

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql_query, tuple(params))
        conn.commit()
        changes = cur.rowcount
        
        return changes > 0

    @staticmethod
    def delete(position_id: int) -> bool:
        # Удаление должности
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                DELETE FROM Positions
                WHERE position_id = ?
            """, (position_id,))
            conn.commit()
            changes = cur.rowcount
            return changes > 0
        finally:
            pass