from models import User
from repositories.user_repository import UserRepository
from repositories.role_repository import RoleRepository
from security.password_manager import hash_password, verify_password
from enums import RoleID
from exceptions import AppError, ErrorCode, FieldName
from utils.validators import require_not_empty

MIN_PASSWORD_LENGTH = 6


def login(username: str, password: str) -> User:
    # Авторизация
    username = require_not_empty(username, FieldName.LOGIN)
    if not password:
        raise AppError(ErrorCode.VALIDATION_EMPTY, field=FieldName.PASSWORD)

    user = UserRepository.get_by_username(username)
    if not user or not verify_password(password, user.password_hash):
        raise AppError(ErrorCode.AUTH_INVALID_CREDENTIALS)

    if not user.is_active:
        raise AppError(ErrorCode.AUTH_USER_BLOCKED)

    return user


def register(username: str, password: str, role_id: int) -> int:
    # Регистрация
    username = require_not_empty(username, FieldName.LOGIN)
    if not password or len(password) < MIN_PASSWORD_LENGTH:
        raise AppError(ErrorCode.AUTH_PASSWORD_TOO_SHORT, min_length=MIN_PASSWORD_LENGTH)

    if UserRepository.get_by_username(username):
        raise AppError(ErrorCode.AUTH_USERNAME_EXISTS)

    if not RoleRepository.get_by_id(role_id):
        raise AppError(ErrorCode.AUTH_ROLE_NOT_FOUND)

    return UserRepository.create(username, hash_password(password), role_id)


def get_role_name(user: User) -> str:
    # Название роли
    role = RoleRepository.get_by_id(user.role_id)
    return role.name if role else "?"

from models import User, Role


def list_roles() -> list[Role]:
    # Список ролей
    return RoleRepository.get_all()


def is_admin(user: User) -> bool:
    # Проверка админа
    return user.role_id == RoleID.ADMIN