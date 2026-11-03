class ErrorCode:
    # Auth
    AUTH_INVALID_CREDENTIALS  = "auth.invalid_credentials"
    AUTH_USER_BLOCKED         = "auth.user_blocked"
    AUTH_USERNAME_EXISTS      = "auth.username_exists"
    AUTH_ROLE_NOT_FOUND       = "auth.role_not_found"
    AUTH_PASSWORD_TOO_SHORT   = "auth.password_too_short"

    # Validation
    VALIDATION_EMPTY          = "validation.empty"
    VALIDATION_INVALID_EMAIL  = "validation.invalid_email"
    VALIDATION_INVALID_PHONE  = "validation.invalid_phone"
    VALIDATION_POSITIVE_INT   = "validation.positive_int"
    VALIDATION_TOO_SHORT      = "validation.too_short"
    VALIDATION_INVALID_STATUS = "validation.invalid_status"

    # Employee
    EMPLOYEE_NOT_FOUND        = "employee.not_found"
    EMPLOYEE_PHONE_EXISTS     = "employee.phone_exists"
    EMPLOYEE_FIRED            = "employee.fired"

    # Position
    POSITION_NOT_FOUND        = "position.not_found"
    POSITION_TITLE_EXISTS     = "position.title_exists"

    # Department
    DEPARTMENT_NOT_FOUND      = "department.not_found"
    DEPARTMENT_NAME_EXISTS    = "department.name_exists"

    # Assignment
    ASSIGNMENT_SAME_POSITION  = "assignment.same_position"

class FieldName:
    # Коды полей
    FULL_NAME       = "field.full_name"
    PHONE           = "field.phone"
    EMAIL           = "field.email"
    LOGIN           = "field.login"
    PASSWORD        = "field.password"
    STATUS          = "field.status"
    POSITION_TITLE  = "field.position_title"
    POSITION_SALARY = "field.position_salary"
    DEPARTMENT_NAME = "field.department_name"


class AppError(Exception):
    def __init__(self, code: str, **context):
        # Код + контекст для подстановки
        self.code = code
        self.context = context
        super().__init__(code)