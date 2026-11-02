from models import User
from repositories.base import get_connection

class UserRepository:
    @staticmethod
    def get_by_username(username: str) -> User | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, username, password_hash, is_active, role_id 
            FROM Users 
            WHERE username = ?
        """, (username,))
        row = cur.fetchone()
        conn.close()
        if row:
            return User(
                user_id=row[0], 
                username=row[1], 
                password_hash=row[2], 
                is_active=row[3], 
                role_id=row[4]
            )
        return None