from exceptions import ErrorCode, FieldName

ERROR_MESSAGES = {
    ErrorCode.AUTH_INVALID_CREDENTIALS:     "Неверный логин или пароль",
    ErrorCode.AUTH_USER_BLOCKED:            "Учётная запись заблокирована",
    ErrorCode.AUTH_USERNAME_EXISTS:         "Пользователь с таким логином уже существует",
    ErrorCode.AUTH_ROLE_NOT_FOUND:          "Роль не найдена",
    ErrorCode.AUTH_PASSWORD_TOO_SHORT:      "Пароль должен быть не короче {min_length} символов",

    ErrorCode.VALIDATION_EMPTY:             "{field} не может быть пустым",
    ErrorCode.VALIDATION_INVALID_EMAIL:     "Некорректный email",
    ErrorCode.VALIDATION_INVALID_PHONE:     "Некорректный номер телефона",
    ErrorCode.VALIDATION_POSITIVE_INT:      "{field} должен быть положительным числом",
    ErrorCode.VALIDATION_TOO_SHORT:         "{field} должен быть не короче {min_length} символов",
    ErrorCode.VALIDATION_INVALID_STATUS:              "Недопустимый статус",

    ErrorCode.EMPLOYEE_NOT_FOUND:           "Сотрудник не найден",
    ErrorCode.EMPLOYEE_PHONE_EXISTS:        "Сотрудник с таким телефоном уже существует",
    ErrorCode.EMPLOYEE_FIRED:               "Сотрудник уволен, операция невозможна",

    ErrorCode.POSITION_NOT_FOUND:           "Должность не найдена",
    ErrorCode.POSITION_TITLE_EXISTS:        "Должность с таким названием уже существует",

    ErrorCode.DEPARTMENT_NOT_FOUND:         "Отдел не найден",
    ErrorCode.DEPARTMENT_NAME_EXISTS:       "Отдел с таким названием уже существует",

    ErrorCode.ASSIGNMENT_SAME_POSITION:     "Сотрудник уже занимает эту должность",
}


FIELD_NAMES = {
    FieldName.FULL_NAME:       "ФИО",
    FieldName.PHONE:           "Телефон",
    FieldName.EMAIL:           "Email",
    FieldName.LOGIN:           "Логин",
    FieldName.PASSWORD:        "Пароль",
    FieldName.STATUS:          "Статус",
    FieldName.POSITION_TITLE:  "Название должности",
    FieldName.POSITION_SALARY: "Оклад",
    FieldName.DEPARTMENT_NAME: "Название отдела",
}


def render_error(code: str, context: dict) -> str:
    # Код → текст
    template = ERROR_MESSAGES.get(code, code)
    if not context:
        return template
    resolved = {
        k: FIELD_NAMES.get(v, v) if isinstance(v, str) else v
        for k, v in context.items()
    }
    return template.format(**resolved)