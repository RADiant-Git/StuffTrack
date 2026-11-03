from typing import Optional
from exceptions import AppError, ErrorCode, FieldName


def require_not_empty(value: Optional[str], field_name: str) -> str:
    # Проверка на пустоту
    if value is None or not value.strip():
        raise AppError(ErrorCode.VALIDATION_EMPTY, field=field_name)
    return value.strip()


def require_email(value: Optional[str]) -> str:
    # Проверка email
    value = require_not_empty(value, FieldName.EMAIL)
    if "@" not in value or "." not in value.split("@")[-1]:
        raise AppError(ErrorCode.VALIDATION_INVALID_EMAIL)
    return value


def require_phone(value: Optional[str]) -> str:
    # Проверка телефона
    value = require_not_empty(value, FieldName.PHONE)
    digits = value.replace(" ", "").replace("-", "").replace("+", "")
    if not digits.isdigit() or len(digits) < 10:
        raise AppError(ErrorCode.VALIDATION_INVALID_PHONE)
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