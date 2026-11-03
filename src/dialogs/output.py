from models import Employee, Position, Department, Assignment, User
from dialogs import common

DASH = "—"

# Заголовки
EMPLOYEES_HEADER = "ID | ФИО | Телефон | Отдел | Должность | Статус"
POSITIONS_HEADER = "ID | Название | Оклад | Требования"
DEPARTMENTS_HEADER = "ID | Название | Описание"
ASSIGNMENTS_HEADER = "ID | Начало | Конец | Должность | Примечание"
PROFILE_HEADER = "=== Профиль ==="
HISTORY_HEADER = "=== История переводов ==="


def _value(v) -> str:
    # Значение или прочерк
    return str(v) if v not in (None, "") else DASH


def format_employee(emp: Employee) -> str:
    # Строка сотрудника
    return " | ".join([
        str(emp.employee_id),
        emp.full_name,
        emp.phone,
        _value(emp.department_name),
        _value(emp.position_title),
        emp.status,
    ])


def format_employees(items: list[Employee]) -> str:
    # Список сотрудников
    if not items:
        return common.EMPTY_LIST
    lines = [EMPLOYEES_HEADER]
    lines.extend(format_employee(e) for e in items)
    return "\n".join(lines)


def format_position(pos: Position) -> str:
    # Строка должности
    return " | ".join([
        str(pos.position_id),
        pos.title,
        str(pos.base_salary),
        _value(pos.requirements),
    ])


def format_positions(items: list[Position]) -> str:
    # Список должностей
    if not items:
        return common.EMPTY_LIST
    lines = [POSITIONS_HEADER]
    lines.extend(format_position(p) for p in items)
    return "\n".join(lines)


def format_department(dep: Department) -> str:
    # Строка отдела
    return " | ".join([
        str(dep.department_id),
        dep.name,
        _value(dep.description),
    ])


def format_departments(items: list[Department]) -> str:
    # Список отделов
    if not items:
        return common.EMPTY_LIST
    lines = [DEPARTMENTS_HEADER]
    lines.extend(format_department(d) for d in items)
    return "\n".join(lines)


def format_assignment(ass: Assignment) -> str:
    # Строка назначения
    return " | ".join([
        str(ass.assignment_id),
        ass.start_date,
        _value(ass.end_date),
        _value(ass.position_title),
        _value(ass.notes),
    ])


def format_assignments(items: list[Assignment]) -> str:
    # Список назначений
    if not items:
        return common.EMPTY_LIST
    lines = [HISTORY_HEADER, ASSIGNMENTS_HEADER]
    lines.extend(format_assignment(a) for a in items)
    return "\n".join(lines)


def format_profile(user: User, emp: Employee | None) -> str:
    # Профиль пользователя
    lines = [PROFILE_HEADER, f"Логин: {user.username}"]
    if emp is None:
        lines.append("Карточка сотрудника не привязана")
        return "\n".join(lines)
    lines.extend([
        f"ФИО: {emp.full_name}",
        f"Телефон: {emp.phone}",
        f"Email: {_value(emp.email)}",
        f"Отдел: {_value(emp.department_name)}",
        f"Должность: {_value(emp.position_title)}",
        f"Статус: {emp.status}",
        f"Дата приёма: {emp.hire_date}",
    ])
    return "\n".join(lines)