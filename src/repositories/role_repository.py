from typing import Optional
from models import Role
from repositories.base import get_connection

class RoleRepository:

    @staticmethod
    def _map(row) -> Role:
        # Маппинг строки
        return Role(
            role_id=row[0],
            name=row[1],
            description=row[2]
        )

    @staticmethod
    def get_all() -> list[Role]:
        # Все роли
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT role_id, name, description FROM Roles ORDER BY name ASC")
        rows = cur.fetchall()
        return [RoleRepository._map(row) for row in rows]

    @staticmethod
    def get_by_id(role_id: int) -> Optional[Role]:
        # Поиск по ID
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT role_id, name, description FROM Roles WHERE role_id = ?", (role_id,))
        row = cur.fetchone()
        return RoleRepository._map(row) if row else None