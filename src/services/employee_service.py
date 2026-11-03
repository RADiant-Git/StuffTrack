from typing import Optional
from models import Employee
from repositories.employee_repository import EmployeeRepository
from repositories.department_repository import DepartmentRepository
from repositories.position_repository import PositionRepository
from repositories.assignment_repository import AssignmentRepository
from exceptions import AppError, ErrorCode, FieldName
from enums import EmployeeStatus
from utils.validators import require_not_empty, require_email, require_phone

VALID_STATUSES = frozenset(s.value for s in EmployeeStatus)


def register_employee(
    full_name: str,
    phone: str,
    email: str,
    department_id: int,
    position_id: int,
    user_id: Optional[int] = None,
) -> int:
    # Регистрация сотрудника
    full_name = require_not_empty(full_name, FieldName.FULL_NAME)
    phone = require_phone(phone)
    email = require_email(email)

    if not DepartmentRepository.get_by_id(department_id):
        raise AppError(ErrorCode.DEPARTMENT_NOT_FOUND)
    if not PositionRepository.get_by_id(position_id):
        raise AppError(ErrorCode.POSITION_NOT_FOUND)

    # Дубликат по телефону
    if EmployeeRepository.get_by_phone(phone):
        raise AppError(ErrorCode.EMPLOYEE_PHONE_EXISTS)

    return EmployeeRepository.create(
        full_name=full_name,
        phone=phone,
        email=email,
        department_id=department_id,
        current_position_id=position_id,
        user_id=user_id,
    )


def update_personal(employee_id: int, full_name: str, phone: str, email: str) -> bool:
    # Обновление личных данных
    if not EmployeeRepository.get_by_id(employee_id):
        raise AppError(ErrorCode.EMPLOYEE_NOT_FOUND)

    full_name = require_not_empty(full_name, FieldName.FULL_NAME)
    phone = require_phone(phone)
    email = require_email(email)

    return EmployeeRepository.update_personal_data(employee_id, full_name, phone, email)


def fire_employee(employee_id: int) -> bool:
    # Увольнение сотрудника
    emp = EmployeeRepository.get_by_id(employee_id)
    if not emp:
        raise AppError(ErrorCode.EMPLOYEE_NOT_FOUND)
    if emp.status == EmployeeStatus.FIRED.value:
        raise AppError(ErrorCode.EMPLOYEE_FIRED)

    # Закрываем текущее назначение
    AssignmentRepository.close_current_assignment(employee_id)

    return EmployeeRepository.update_career_data(
        employee_id=employee_id,
        status=EmployeeStatus.FIRED.value,
        current_position_id=emp.current_position_id,
        department_id=emp.department_id,
    )


def search_employees(
    full_name: Optional[str] = None,
    position_id: Optional[int] = None,
    status: Optional[str] = None,
) -> list[Employee]:
    # Поиск сотрудников
    if status is not None and status not in VALID_STATUSES:
        raise AppError(ErrorCode.VALIDATION_INVALID_STATUS)
    return EmployeeRepository.search(
        full_name=full_name,
        position_id=position_id,
        status=status,
    )


def get_employee(employee_id: int) -> Employee:
    # Получение сотрудника
    emp = EmployeeRepository.get_by_id(employee_id)
    if not emp:
        raise AppError(ErrorCode.EMPLOYEE_NOT_FOUND)
    return emp


def get_by_user(user_id: int) -> Optional[Employee]:
    # Профиль по пользователю
    return EmployeeRepository.get_by_user_id(user_id)