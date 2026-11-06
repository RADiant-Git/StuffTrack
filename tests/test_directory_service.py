import pytest
from exceptions import AppError, ErrorCode
from services import directory_service
from repositories.position_repository import PositionRepository
from repositories.department_repository import DepartmentRepository


def test_create_position_success():
    # Создание новой должности
    pos_id = directory_service.create_position("Системный аналитик", 95000, "SQL, UML")
    assert pos_id > 0
    pos = PositionRepository.get_by_id(pos_id)
    assert pos.title == "Системный аналитик"


def test_create_position_duplicate_title():
    # Создание дубликата должности
    with pytest.raises(AppError) as exc:
        directory_service.create_position("Младший разработчик", 50000)
    assert exc.value.code == ErrorCode.POSITION_TITLE_EXISTS


def test_update_position_success():
    # Обновление параметров должности
    directory_service.update_position(1, title="Junior Dev", base_salary=70000)
    pos = PositionRepository.get_by_id(1)
    assert pos.title == "Junior Dev"
    assert pos.base_salary == 70000


def test_update_position_duplicate_title():
    # Изменение названия должности
    with pytest.raises(AppError) as exc:
        directory_service.update_position(1, title="Ведущий разработчик")
    assert exc.value.code == ErrorCode.POSITION_TITLE_EXISTS


def test_update_position_not_found():
    # Обновление несуществующей должности
    with pytest.raises(AppError) as exc:
        directory_service.update_position(9999, title="Новая")
    assert exc.value.code == ErrorCode.POSITION_NOT_FOUND


def test_create_department_success():
    # Создание нового отдела
    dep_id = directory_service.create_department("Бухгалтерия", "Финансовый учет")
    assert dep_id > 0
    dep = DepartmentRepository.get_by_id(dep_id)
    assert dep.name == "Бухгалтерия"


def test_create_department_duplicate_name():
    # Создание дубликата отдела
    with pytest.raises(AppError) as exc:
        directory_service.create_department("Отдел разработки")
    assert exc.value.code == ErrorCode.DEPARTMENT_NAME_EXISTS


def test_update_department_duplicate_name():
    # Изменение названия отдела
    with pytest.raises(AppError) as exc:
        directory_service.update_department(2, name="Отдел разработки")
    assert exc.value.code == ErrorCode.DEPARTMENT_NAME_EXISTS