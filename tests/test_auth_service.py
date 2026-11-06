import pytest
from exceptions import AppError, ErrorCode
from services import auth_service
from repositories.user_repository import UserRepository
from enums import RoleID


def test_login_success():
    # Успешная авторизация пользователя
    user = auth_service.login("admin_varya", "admin123")
    assert user.username == "admin_varya"
    assert auth_service.is_admin(user) is True


def test_login_invalid_password():
    # Ошибка неверного пароля
    with pytest.raises(AppError) as exc:
        auth_service.login("admin_varya", "wrong_pass")
    assert exc.value.code == ErrorCode.AUTH_INVALID_CREDENTIALS


def test_login_non_existent_user():
    # Авторизация несуществующего пользователя
    with pytest.raises(AppError) as exc:
        auth_service.login("non_existent", "admin123")
    assert exc.value.code == ErrorCode.AUTH_INVALID_CREDENTIALS


def test_login_blocked_user():
    # Авторизация заблокированного пользователя
    user = UserRepository.get_by_username("dev_anatolii")
    UserRepository.update_status(user.user_id, 0)

    with pytest.raises(AppError) as exc:
        auth_service.login("dev_anatolii", "dev123")
    assert exc.value.code == ErrorCode.AUTH_USER_BLOCKED


def test_register_success():
    # Успешная регистрация пользователя
    new_id = auth_service.register("new_user", "password123", RoleID.EMPLOYEE)
    assert new_id > 0
    created = UserRepository.get_by_id(new_id)
    assert created.username == "new_user"


def test_register_duplicate_username():
    # Регистрация существующего логина
    with pytest.raises(AppError) as exc:
        auth_service.register("admin_varya", "password123", RoleID.EMPLOYEE)
    assert exc.value.code == ErrorCode.AUTH_USERNAME_EXISTS


def test_register_short_password():
    # Регистрация короткого пароля
    with pytest.raises(AppError) as exc:
        auth_service.register("valid_login", "123", RoleID.EMPLOYEE)
    assert exc.value.code == ErrorCode.AUTH_PASSWORD_TOO_SHORT


def test_register_role_not_found():
    # Регистрация несуществующей роли
    with pytest.raises(AppError) as exc:
        auth_service.register("valid_login", "password123", 9999)
    assert exc.value.code == ErrorCode.AUTH_ROLE_NOT_FOUND


def test_list_roles():
    # Получение списка ролей
    roles = auth_service.list_roles()
    assert len(roles) >= 2