from models import Employee
from repositories.base import get_connection

class EmployeeRepository:
    @staticmethod
    def create(full_name: str, phone: str, email: str, status: str, hire_date: str, department_id: int, current_position_id: int, user_id: int | None = None) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Employees (full_name, phone, email, status, hire_date, department_id, current_position_id, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (full_name, phone, email, status, hire_date, department_id, current_position_id, user_id))
        generated_id = cur.lastrowid
        conn.commit()
        conn.close()
        return generated_id

    @staticmethod
    def get_all() -> list[Employee]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                e.employee_id, e.full_name, e.phone, e.email, e.status, e.hire_date, 
                e.department_id, e.current_position_id, e.user_id,
                d.name AS department_name,
                p.title AS position_title
            FROM Employees e
            LEFT JOIN Departments d ON e.department_id = d.department_id
            LEFT JOIN Positions p ON e.current_position_id = p.position_id
        """)
        rows = cur.fetchall()
        conn.close()
        employees = []
        for r in rows:
            emp = Employee(
                employee_id=r[0], 
                full_name=r[1], 
                phone=r[2], 
                email=r[3], 
                status=r[4], 
                hire_date=r[5], 
                department_id=r[6], 
                current_position_id=r[7], 
                user_id=r[8]
            )
            emp.department_name = r[9]
            emp.position_title = r[10]
            employees.append(emp)
        return employees

    @staticmethod
    def update_position(employee_id: int, position_id: int) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Employees 
            SET current_position_id = ? 
            WHERE employee_id = ?
        """, (position_id, employee_id))
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        return updated