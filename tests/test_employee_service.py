import pytest
from exceptions import AppError, ErrorCode
from services import employee_service
from repositories.employee_repository import EmployeeRepository
from enums import EmployeeStatus


def test_register_employee_success():
    # Регистрация нового сотрудника
    emp_id = employee_service.register_employee(
        full_name="Петров Петр Петрович",
        phone="+7 (999) 777-66-55",
        email="petrov@company.local",
        department_id=1,
        position_id=1,
    )
    assert emp_id > 0
    emp = EmployeeRepository.get_by_id(emp_id)
    assert emp.full_name == "Петров Петр Петрович"
    assert emp.status == EmployeeStatus.ACTIVE.value


def test_register_employee_duplicate_phone():
    # Регистрация занятого телефона
    employee_service.register_employee(
        full_name="Первый Сотрудник",
        phone="+7 (999) 000-11-22",
        email="first@company.local",
        department_id=1,
        position_id=1,
    )
    with pytest.raises(AppError) as exc:
        employee_service.register_employee(
            full_name="Второй Сотрудник",
            phone="+7 (999) 000-11-22",
            email="second@company.local",
            department_id=1,
            position_id=1,
        )
    assert exc.value.code == ErrorCode.EMPLOYEE_PHONE_EXISTS


def test_register_employee_duplicate_email():
    # Регистрация занятой почты
    with pytest.raises(AppError) as exc:
        employee_service.register_employee(
            full_name="Сидоров Сидор",
            phone="+7 (999) 000-00-01",
            email="smirnova@company.local",
            department_id=1,
            position_id=1,
        )
    assert exc.value.code == ErrorCode.EMPLOYEE_EMAIL_EXISTS


def test_register_employee_invalid_department():
    # Регистрация в несуществующий отдел
    with pytest.raises(AppError) as exc:
        employee_service.register_employee(
            full_name="Тестов Тест",
            phone="+7 (999) 111-00-11",
            email="test1@company.local",
            department_id=9999,
            position_id=1,
        )
    assert exc.value.code == ErrorCode.DEPARTMENT_NOT_FOUND


def test_update_personal_success():
    # Обновление профиля сотрудника
    employee_service.update_personal(
        employee_id=1,
        full_name="Смирнова Елена Васильевна",
        phone="+7 (910) 999-88-77",
        email="smirnova_new@company.local",
    )
    emp = EmployeeRepository.get_by_id(1)
    assert emp.full_name == "Смирнова Елена Васильевна"
    assert emp.email == "smirnova_new@company.local"


def test_update_personal_duplicate_email():
    # Обновление на занятую почту
    with pytest.raises(AppError) as exc:
        employee_service.update_personal(
            employee_id=1,
            full_name="Смирнова Елена Сергеевна",
            phone="+7 (910) 111-22-33",
            email="ivanov@company.local",
        )
    assert exc.value.code == ErrorCode.EMPLOYEE_EMAIL_EXISTS


def test_fire_employee_success():
    # Успешное увольнение сотрудника
    assert employee_service.fire_employee(1) is True
    emp = EmployeeRepository.get_by_id(1)
    assert emp.status == EmployeeStatus.FIRED.value


def test_fire_already_fired():
    # Повторное увольнение сотрудника
    employee_service.fire_employee(1)
    with pytest.raises(AppError) as exc:
        employee_service.fire_employee(1)
    assert exc.value.code == ErrorCode.EMPLOYEE_FIRED


def test_search_employees():
    # Поиск по фильтрам
    res_name = employee_service.search_employees(full_name="Иванов")
    assert len(res_name) == 1
    assert res_name[0].employee_id == 2

    res_status = employee_service.search_employees(status=EmployeeStatus.ACTIVE.value)
    assert len(res_status) >= 2


def test_search_invalid_status():
    # Поиск по неверному статусу
    with pytest.raises(AppError) as exc:
        employee_service.search_employees(status="неизвестный")
    assert exc.value.code == ErrorCode.VALIDATION_INVALID_STATUS