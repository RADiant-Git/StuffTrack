from typing import Optional
from models import Assignment
from repositories.assignment_repository import AssignmentRepository
from repositories.employee_repository import EmployeeRepository
from repositories.position_repository import PositionRepository
from exceptions import AppError, ErrorCode
from enums import EmployeeStatus


def transfer_employee(employee_id: int, position_id: int, notes: Optional[str] = None) -> int:
    # Перевод сотрудника
    emp = EmployeeRepository.get_by_id(employee_id)
    if not emp:
        raise AppError(ErrorCode.EMPLOYEE_NOT_FOUND)
    if emp.status == EmployeeStatus.FIRED.value:
        raise AppError(ErrorCode.EMPLOYEE_FIRED)
    if not PositionRepository.get_by_id(position_id):
        raise AppError(ErrorCode.POSITION_NOT_FOUND)
    if emp.current_position_id == position_id:
        raise AppError(ErrorCode.ASSIGNMENT_SAME_POSITION)

    # Закрываем текущее назначение
    AssignmentRepository.close_current_assignment(employee_id)

    # Создаём новое
    new_id = AssignmentRepository.create_assignment(employee_id, position_id, notes)

    # Обновляем карточку сотрудника
    EmployeeRepository.update_career_data(
        employee_id=employee_id,
        status=emp.status,
        current_position_id=position_id,
        department_id=emp.department_id,
    )

    return new_id


def get_history(employee_id: int) -> list[Assignment]:
    # История переводов
    if not EmployeeRepository.get_by_id(employee_id):
        raise AppError(ErrorCode.EMPLOYEE_NOT_FOUND)
    return AssignmentRepository.get_history_by_employee(employee_id)