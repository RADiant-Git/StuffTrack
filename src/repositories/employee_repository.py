from typing import Optional
from models import Employee
from enums import EmployeeStatus
from repositories.base import get_connection

class EmployeeRepository:
    
    @staticmethod
    def _map(row) -> Employee:
        # Маппинг строки БД
        return Employee(
            employee_id=row[0],
            full_name=row[1],
            phone=row[2],
            email=row[3],
            status=row[4],
            hire_date=row[5],
            department_id=row[6],
            current_position_id=row[7],
            user_id=row[8],
            department_name=row[9],
            position_title=row[10]
        )

    @staticmethod
    def create(
        full_name: str, 
        phone: str, 
        email: str, 
        department_id: int, 
        current_position_id: int, 
        user_id: Optional[int] = None
    ) -> int:
        # Регистрация нового сотрудника
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Employees (
                full_name, phone, email, status, hire_date, 
                department_id, current_position_id, user_id
            )
            VALUES (?, ?, ?, ?, datetime('now'), ?, ?, ?)
        """, (full_name, phone, email, EmployeeStatus.ACTIVE.value, department_id, current_position_id, user_id))
        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_by_id(employee_id: int) -> Optional[Employee]:
        # Поиск по ID
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                e.employee_id, e.full_name, e.phone, e.email, e.status, e.hire_date,
                e.department_id, e.current_position_id, e.user_id,
                d.name AS department_name, p.title AS position_title
            FROM Employees e
            LEFT JOIN Departments d ON e.department_id = d.department_id
            LEFT JOIN Positions p ON e.current_position_id = p.position_id
            WHERE e.employee_id = ?
        """, (employee_id,))
        row = cur.fetchone()
        conn.close()
        return EmployeeRepository._map(row) if row else None

    @staticmethod
    def get_by_phone(phone: str) -> Optional[Employee]:
        # Поиск по телефону
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.employee_id, e.full_name, e.phone, e.email, e.status, e.hire_date,
                e.department_id, e.current_position_id, e.user_id,
                d.name, p.title
            FROM Employees e
            LEFT JOIN Departments d ON e.department_id = d.department_id
            LEFT JOIN Positions p ON e.current_position_id = p.position_id
            WHERE e.phone = ?
        """, (phone,))
        row = cur.fetchone()
        conn.close()
        return EmployeeRepository._map(row) if row else None

    @staticmethod
    def search(
        full_name: Optional[str] = None, 
        position_id: Optional[int] = None, 
        status: Optional[str] = None
    ) -> list[Employee]:
        # Многокритериальный поиск сотрудников
        conn = get_connection()
        cur = conn.cursor()
        
        query = """
            SELECT 
                e.employee_id, e.full_name, e.phone, e.email, e.status, e.hire_date,
                e.department_id, e.current_position_id, e.user_id,
                d.name AS department_name, p.title AS position_title
            FROM Employees e
            LEFT JOIN Departments d ON e.department_id = d.department_id
            LEFT JOIN Positions p ON e.current_position_id = p.position_id
            WHERE 1=1
        """
        params = []

        if full_name:
            query += " AND e.full_name LIKE ?"
            params.append(f"%{full_name}%")
        if position_id:
            query += " AND e.current_position_id = ?"
            params.append(position_id)
        if status:
            query += " AND e.status = ?"
            params.append(status)

        query += " ORDER BY e.full_name ASC"
        
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        conn.close()
        return [EmployeeRepository._map(row) for row in rows]

    @staticmethod
    def update_personal_data(employee_id: int, full_name: str, phone: str, email: str) -> bool:
        # Изменение личных данных
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Employees
            SET full_name = ?, phone = ?, email = ?
            WHERE employee_id = ?
        """, (full_name, phone, email, employee_id))
        conn.commit()
        changes = cur.rowcount
        conn.close()
        return changes > 0

    @staticmethod
    def update_career_data(employee_id: int, status: str, current_position_id: int, department_id: int) -> bool:
        # Изменение кадровых реквизитов
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Employees
            SET status = ?, current_position_id = ?, department_id = ?
            WHERE employee_id = ?
        """, (status, current_position_id, department_id, employee_id))
        conn.commit()
        changes = cur.rowcount
        conn.close()
        return changes > 0

    @staticmethod
    def get_by_user_id(user_id: int) -> Optional[Employee]:
        # Поиск по пользователю
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                e.employee_id, e.full_name, e.phone, e.email, e.status, e.hire_date,
                e.department_id, e.current_position_id, e.user_id,
                d.name AS department_name, p.title AS position_title
            FROM Employees e
            LEFT JOIN Departments d ON e.department_id = d.department_id
            LEFT JOIN Positions p ON e.current_position_id = p.position_id
            WHERE e.user_id = ?
        """, (user_id,))
        row = cur.fetchone()
        conn.close()
        return EmployeeRepository._map(row) if row else None