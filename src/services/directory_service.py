from typing import Optional
from models import Position, Department
from repositories.position_repository import PositionRepository
from repositories.department_repository import DepartmentRepository
from exceptions import AppError, ErrorCode, FieldName
from utils.validators import require_not_empty, require_positive_int


def create_position(title: str, base_salary: int, requirements: Optional[str] = None) -> int:
    # Создание должности
    title = require_not_empty(title, FieldName.POSITION_TITLE)
    base_salary = require_positive_int(base_salary, FieldName.POSITION_SALARY)

    for p in PositionRepository.get_all():
        if p.title.lower() == title.lower():
            raise AppError(ErrorCode.POSITION_TITLE_EXISTS)

    return PositionRepository.create(title, base_salary, requirements)


def update_position(
    position_id: int,
    title: Optional[str] = None,
    base_salary: Optional[int] = None,
    requirements: Optional[str] = None,
) -> bool:
    # Обновление должности
    if not PositionRepository.get_by_id(position_id):
        raise AppError(ErrorCode.POSITION_NOT_FOUND)

    if title is not None:
        title = require_not_empty(title, FieldName.POSITION_TITLE)
    if base_salary is not None:
        base_salary = require_positive_int(base_salary, FieldName.POSITION_SALARY)

    return PositionRepository.update(position_id, title, base_salary, requirements)


def create_department(name: str, description: Optional[str] = None) -> int:
    # Создание отдела
    name = require_not_empty(name, FieldName.DEPARTMENT_NAME)

    for d in DepartmentRepository.get_all():
        if d.name.lower() == name.lower():
            raise AppError(ErrorCode.DEPARTMENT_NAME_EXISTS)

    return DepartmentRepository.create(name, description)


def update_department(department_id: int, name: str, description: Optional[str] = None) -> bool:
    # Обновление отдела
    if not DepartmentRepository.get_by_id(department_id):
        raise AppError(ErrorCode.DEPARTMENT_NOT_FOUND)

    name = require_not_empty(name, FieldName.DEPARTMENT_NAME)
    return DepartmentRepository.update(department_id, name, description)


def list_positions() -> list[Position]:
    # Список должностей
    return PositionRepository.get_all()


def list_departments() -> list[Department]:
    # Список отделов
    return DepartmentRepository.get_all()