from models import User
from dialogs import common, employee_dialog, output
from dialogs.errors import render_error
from exceptions import AppError
from services import employee_service, assignment_service, directory_service
from ui.helpers import pause


def _action_profile(user: User) -> None:
    # Мой профиль
    print(employee_dialog.PROFILE_HEADER)
    emp = employee_service.get_by_user(user.user_id)
    if emp is None:
        print(employee_dialog.NO_EMPLOYEE_CARD)
    else:
        print(output.format_profile(user, emp))
    pause()


def _action_positions() -> None:
    # Справочник должностей
    print(employee_dialog.POSITIONS_HEADER)
    print(output.format_positions(directory_service.list_positions()))
    pause()


def _action_departments() -> None:
    # Справочник отделов
    print(employee_dialog.DEPARTMENTS_HEADER)
    print(output.format_departments(directory_service.list_departments()))
    pause()


def _action_history(user: User) -> None:
    # История переводов
    print(employee_dialog.HISTORY_HEADER)
    emp = employee_service.get_by_user(user.user_id)
    if emp is None:
        print(employee_dialog.NO_EMPLOYEE_CARD)
        pause()
        return
    try:
        history = assignment_service.get_history(emp.employee_id)
        print(output.format_assignments(history))
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def employee_menu(user: User) -> None:
    # Меню сотрудника
    while True:
        print()
        print(employee_dialog.MENU_HEADER)
        print(employee_dialog.MENU_PROFILE)
        print(employee_dialog.MENU_POSITIONS)
        print(employee_dialog.MENU_DEPARTMENTS)
        print(employee_dialog.MENU_HISTORY)
        print(common.EXIT)
        choice = input(common.CHOOSE_ACTION).strip()

        if choice == "1":
            _action_profile(user)
        elif choice == "2":
            _action_positions()
        elif choice == "3":
            _action_departments()
        elif choice == "4":
            _action_history(user)
        elif choice == "0":
            break
        else:
            print(common.INVALID_CHOICE)
            pause()