from typing import Optional
from models import User
from enums import RoleID
from exceptions import AppError
from dialogs import common, auth_dialog
from dialogs.errors import render_error
from services import auth_service
from ui.helpers import pause


def start_menu() -> str:
    # Стартовое меню
    print(common.APP_TITLE)
    print(auth_dialog.MENU_HEADER)
    print(auth_dialog.MENU_LOGIN)
    print(auth_dialog.MENU_REGISTER)
    print(auth_dialog.MENU_EXIT)
    return input(common.CHOOSE_ACTION).strip()


def login_flow() -> Optional[User]:
    # Вход в систему
    print(auth_dialog.LOGIN_HEADER)
    username = input(auth_dialog.LOGIN_PROMPT)
    password = input(auth_dialog.PASSWORD_PROMPT)

    try:
        user = auth_service.login(username, password)
    except AppError as e:
        print(render_error(e.code, e.context))
        pause()
        return None

    print(auth_dialog.LOGIN_SUCCESS.format(username=user.username))
    print(auth_dialog.LOGIN_ROLE_INFO.format(role=auth_service.get_role_name(user)))
    pause()
    return user


def register_flow() -> bool:
    # Регистрация
    print(auth_dialog.REGISTER_HEADER)
    username = input(auth_dialog.REGISTER_USERNAME_PROMPT)
    password = input(
        auth_dialog.REGISTER_PASSWORD_PROMPT.format(
            min_length=auth_service.MIN_PASSWORD_LENGTH
        )
    )
    password_confirm = input(auth_dialog.REGISTER_PASSWORD_CONFIRM_PROMPT)

    if password != password_confirm:
        print(auth_dialog.PASSWORDS_DO_NOT_MATCH)
        pause()
        return False

    try:
        auth_service.register(username, password, RoleID.EMPLOYEE)
    except AppError as e:
        print(render_error(e.code, e.context))
        pause()
        return False

    print(auth_dialog.REGISTER_SUCCESS)
    pause()
    return True