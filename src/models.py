from dataclasses import dataclass

@dataclass
class Role:
    role_id: int
    name: str
    description: str | None = None

@dataclass
class User:
    user_id: int
    username: str
    password_hash: str
    is_active: int
    role_id: int

@dataclass
class Department:
    department_id: int
    name: str
    description: str | None = None

@dataclass
class Position:
    position_id: int
    title: str
    base_salary: int
    requirements: str | None = None

@dataclass
class Employee:
    employee_id: int
    full_name: str
    phone: str
    email: str
    status: str
    hire_date: str
    department_id: int
    current_position_id: int
    user_id: int | None = None

    department_name: str | None = None
    position_title: str | None = None

@dataclass
class Assignment:
    assignment_id: int
    employee_id: int
    position_id: int
    start_date: str
    end_date: str | None = None
    notes: str | None = None

    position_title: str | None = None