from enum import Enum, IntEnum


class RoleID(IntEnum):
    # Роли системы
    ADMIN = 1
    EMPLOYEE = 2


class EmployeeStatus(str, Enum):
    # Статусы сотрудников
    ACTIVE = "активен"
    ON_LEAVE = "в отпуске"
    FIRED = "уволен"