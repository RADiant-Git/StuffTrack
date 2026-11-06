import pytest
from exceptions import AppError, ErrorCode
from services import assignment_service, employee_service
from repositories.employee_repository import EmployeeRepository


def test_transfer_employee_success():
    # Успешный перевод сотрудника
    new_assignment_id = assignment_service.transfer_employee(
        employee_id=1,
        position_id=1,
        notes="Перевод на младшего разработчика",
    )
    assert new_assignment_id > 0

    emp = EmployeeRepository.get_by_id(1)
    assert emp.current_position_id == 1

    history = assignment_service.get_history(1)
    assert history[0].position_id == 1
    assert history[0].end_date is None


def test_transfer_to_same_position():
    # Перевод на текущую должность
    with pytest.raises(AppError) as exc:
        assignment_service.transfer_employee(employee_id=1, position_id=3)
    assert exc.value.code == ErrorCode.ASSIGNMENT_SAME_POSITION


def test_transfer_fired_employee():
    # Перевод уволенного сотрудника
    employee_service.fire_employee(1)
    with pytest.raises(AppError) as exc:
        assignment_service.transfer_employee(employee_id=1, position_id=1)
    assert exc.value.code == ErrorCode.EMPLOYEE_FIRED


def test_transfer_non_existent_position():
    # Перевод на несуществующую должность
    with pytest.raises(AppError) as exc:
        assignment_service.transfer_employee(employee_id=1, position_id=9999)
    assert exc.value.code == ErrorCode.POSITION_NOT_FOUND


def test_get_history_not_found():
    # История несуществующего сотрудника
    with pytest.raises(AppError) as exc:
        assignment_service.get_history(9999)
    assert exc.value.code == ErrorCode.EMPLOYEE_NOT_FOUND