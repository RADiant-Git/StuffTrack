from typing import Optional
from models import User
from repositories.base import get_connection

class UserRepository:

    @staticmethod
    def _map(row) -> User:
        # Маппинг строки
        return User(
            user_id=row[0],
            username=row[1],
            password_hash=row[2],
            is_active=row[3],
            role_id=row[4]
        )

    @staticmethod
    def create(username: str, password_hash: str, role_id: int) -> int:
        # Создание пользователя
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Users (username, password_hash, is_active, role_id)
            VALUES (?, ?, 1, ?)
        """, (username, password_hash, role_id))
        conn.commit()
        last_id = cur.lastrowid
        return last_id

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        # Поиск по логину
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, password_hash, is_active, role_id FROM Users WHERE username = ?", (username,))
        row = cur.fetchone()
        return UserRepository._map(row) if row else None

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        # Поиск по ID
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, password_hash, is_active, role_id FROM Users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return UserRepository._map(row) if row else None

    @staticmethod
    def update_status(user_id: int, is_active: int) -> bool:
        # Смена статуса
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Users SET is_active = ? WHERE user_id = ?", (is_active, user_id))
        conn.commit()
        changes = cur.rowcount
        return changes > 0

    @staticmethod
    def update_password(user_id: int, new_password_hash: str) -> bool:
        # Смена пароля
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Users SET password_hash = ? WHERE user_id = ?", (new_password_hash, user_id))
        conn.commit()
        changes = cur.rowcount
        return changes > 0