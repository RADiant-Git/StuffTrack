import re
from typing import Optional
from exceptions import AppError, ErrorCode, FieldName

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
NAME_REGEX = re.compile(r"^[A-Za-zА-Яа-яЁё\s\-]+$")


def require_not_empty(value: Optional[str], field_name: str) -> str:
    # Проверка на пустоту
    if value is None or not value.strip():
        raise AppError(ErrorCode.VALIDATION_EMPTY, field=field_name)
    return value.strip()


def require_email(value: Optional[str]) -> str:
    # Проверка почты
    value = require_not_empty(value, FieldName.EMAIL)
    if not EMAIL_REGEX.match(value):
        raise AppError(ErrorCode.VALIDATION_INVALID_EMAIL)
    return value


def require_phone(value: Optional[str]) -> str:
    # Проверка телефона
    value = require_not_empty(value, FieldName.PHONE)
    digits = re.sub(r"\D", "", value)
    if not (10 <= len(digits) <= 15):
        raise AppError(ErrorCode.VALIDATION_INVALID_PHONE)
    return digits


def require_name(value: Optional[str], field_name: str) -> str:
    # Проверка имени
    value = require_not_empty(value, field_name)
    if not NAME_REGEX.match(value):
        raise AppError(ErrorCode.VALIDATION_INVALID_NAME, field=field_name)
    return value


def require_positive_int(value: Optional[int], field_name: str) -> int:
    # Проверка положительного числа
    if value is None or value <= 0:
        raise AppError(ErrorCode.VALIDATION_POSITIVE_INT, field=field_name)
    return value


def require_min_length(value: Optional[str], min_len: int, field_name: str) -> str:
    # Проверка минимальной длины
    value = require_not_empty(value, field_name)
    if len(value) < min_len:
        raise AppError(ErrorCode.VALIDATION_TOO_SHORT, field=field_name, min_length=min_len)
    return value


def require_max_length(value: Optional[str], max_len: int, field_name: str) -> str:
    # Проверка максимальной длины
    if value is not None and len(value) > max_len:
        raise AppError(ErrorCode.VALIDATION_TOO_LONG, field=field_name, max_length=max_len)
    return value