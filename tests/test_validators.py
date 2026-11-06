import pytest
from exceptions import AppError, ErrorCode, FieldName
from utils.validators import (
    require_not_empty,
    require_email,
    require_phone,
    require_name,
    require_positive_int,
    require_min_length,
    require_max_length,
)


def test_not_empty_success():
    # Проверка непустой строки
    assert require_not_empty("тест", FieldName.LOGIN) == "тест"
    assert require_not_empty("  пробелы  ", FieldName.LOGIN) == "пробелы"


def test_not_empty_failure():
    # Ошибка пустой строки
    with pytest.raises(AppError) as exc:
        require_not_empty("", FieldName.LOGIN)
    assert exc.value.code == ErrorCode.VALIDATION_EMPTY

    with pytest.raises(AppError) as exc:
        require_not_empty("   ", FieldName.LOGIN)
    assert exc.value.code == ErrorCode.VALIDATION_EMPTY

    with pytest.raises(AppError) as exc:
        require_not_empty(None, FieldName.LOGIN)
    assert exc.value.code == ErrorCode.VALIDATION_EMPTY


def test_email_success():
    # Валидный адрес почты
    assert require_email("user@example.com") == "user@example.com"
    assert require_email("admin.work+1@sub.domain.ru") == "admin.work+1@sub.domain.ru"


def test_email_failure():
    # Невалидный адрес почты
    invalid_emails = ["user@", "plainaddress", "@domain.com", "user@.com", "user@domain"]
    for email in invalid_emails:
        with pytest.raises(AppError) as exc:
            require_email(email)
        assert exc.value.code == ErrorCode.VALIDATION_INVALID_EMAIL


def test_phone_success():
    # Валидный номер телефона
    assert require_phone("+7 (999) 123-45-67") == "79991234567"
    assert require_phone("88005553535") == "88005553535"


def test_phone_failure():
    # Невалидный номер телефона
    invalid_phones = ["123", "phone_number", "+7(999)12", "1" * 16]
    for phone in invalid_phones:
        with pytest.raises(AppError) as exc:
            require_phone(phone)
        assert exc.value.code == ErrorCode.VALIDATION_INVALID_PHONE


def test_name_success():
    # Валидное имя сотрудника
    assert require_name("Иван Иванов", FieldName.FULL_NAME) == "Иван Иванов"
    assert require_name("Анна-Мария Смирнова", FieldName.FULL_NAME) == "Анна-Мария Смирнова"
    assert require_name("John Doe", FieldName.FULL_NAME) == "John Doe"


def test_name_failure():
    # Невалидное имя сотрудника
    invalid_names = ["Иван123", "Admin!", "user_name", "Смирнов@"]
    for name in invalid_names:
        with pytest.raises(AppError) as exc:
            require_name(name, FieldName.FULL_NAME)
        assert exc.value.code == ErrorCode.VALIDATION_INVALID_NAME


def test_positive_int_success():
    # Валидное положительное число
    assert require_positive_int(1, FieldName.POSITION_SALARY) == 1
    assert require_positive_int(50000, FieldName.POSITION_SALARY) == 50000


def test_positive_int_failure():
    # Ошибка неположительного числа
    for val in [0, -10, None]:
        with pytest.raises(AppError) as exc:
            require_positive_int(val, FieldName.POSITION_SALARY)
        assert exc.value.code == ErrorCode.VALIDATION_POSITIVE_INT


def test_min_length_success():
    # Проверка минимальной длины
    assert require_min_length("password", 6, FieldName.PASSWORD) == "password"


def test_min_length_failure():
    # Ошибка минимальной длины
    with pytest.raises(AppError) as exc:
        require_min_length("123", 6, FieldName.PASSWORD)
    assert exc.value.code == ErrorCode.VALIDATION_TOO_SHORT


def test_max_length_success():
    # Проверка максимальной длины
    assert require_max_length("text", 10, FieldName.FULL_NAME) == "text"
    assert require_max_length(None, 10, FieldName.FULL_NAME) is None


def test_max_length_failure():
    # Ошибка максимальной длины
    with pytest.raises(AppError) as exc:
        require_max_length("very_long_string", 5, FieldName.FULL_NAME)
    assert exc.value.code == ErrorCode.VALIDATION_TOO_LONG