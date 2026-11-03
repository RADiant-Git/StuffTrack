from typing import Optional
from dialogs import common, admin_dialog
from dialogs import output
from dialogs.errors import render_error
from services import employee_service, assignment_service, directory_service, auth_service
from ui.helpers import input_int, input_optional, pause, confirm
from exceptions import AppError


def _print_employees() -> None:
    # Список сотрудников
    print(output.format_employees(employee_service.search_employees()))


def _print_positions() -> None:
    # Список должностей
    print(output.format_positions(directory_service.list_positions()))


def _print_departments() -> None:
    # Список отделов
    print(output.format_departments(directory_service.list_departments()))


def _print_roles() -> None:
    # Список ролей
    for role in auth_service.list_roles():
        print(f"  {role.role_id}. {role.name}")


def _select_employee() -> Optional[int]:
    # Выбор сотрудника
    print(admin_dialog.AVAILABLE_EMPLOYEES)
    _print_employees()
    value = input_int(admin_dialog.PROMPT_EMPLOYEE_ID)
    return None if value in (None, 0) else value


def _select_position() -> Optional[int]:
    # Выбор должности
    print(admin_dialog.AVAILABLE_POSITIONS)
    _print_positions()
    value = input_int(admin_dialog.PROMPT_POSITION_ID)
    return None if value in (None, 0) else value


def _select_department() -> Optional[int]:
    # Выбор отдела
    print(admin_dialog.AVAILABLE_DEPARTMENTS)
    _print_departments()
    value = input_int(admin_dialog.PROMPT_DEPARTMENT_ID)
    return None if value in (None, 0) else value


def _action_list_employees() -> None:
    # Список сотрудников
    print(admin_dialog.EMPLOYEES_HEADER)
    _print_employees()
    pause()


def _action_add_employee() -> None:
    # Добавление сотрудника
    print(admin_dialog.ADD_HEADER)
    print(admin_dialog.INPUT_HINT)
    try:
        full_name = input(admin_dialog.PROMPT_FULL_NAME)
        phone = input(admin_dialog.PROMPT_PHONE)
        email = input(admin_dialog.PROMPT_EMAIL)
        dept_id = _select_department()
        pos_id = _select_position()
        if dept_id is None or pos_id is None:
            print(common.CANCELLED)
        else:
            new_id = employee_service.register_employee(
                full_name, phone, email, dept_id, pos_id
            )
            print(admin_dialog.EMPLOYEE_ADDED.format(id=new_id))
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _action_update_employee() -> None:
    # Изменение данных
    print(admin_dialog.UPDATE_HEADER)
    try:
        emp_id = _select_employee()
        if emp_id is None:
            print(common.CANCELLED)
        else:
            full_name = input(admin_dialog.PROMPT_FULL_NAME)
            phone = input(admin_dialog.PROMPT_PHONE)
            email = input(admin_dialog.PROMPT_EMAIL)
            employee_service.update_personal(emp_id, full_name, phone, email)
            print(admin_dialog.EMPLOYEE_UPDATED)
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _action_transfer_employee() -> None:
    # Перевод сотрудника
    print(admin_dialog.TRANSFER_HEADER)
    try:
        emp_id = _select_employee()
        pos_id = _select_position() if emp_id is not None else None
        if emp_id is None or pos_id is None:
            print(common.CANCELLED)
        else:
            notes = input_optional(admin_dialog.PROMPT_NOTES)
            new_id = assignment_service.transfer_employee(emp_id, pos_id, notes)
            print(admin_dialog.EMPLOYEE_TRANSFERRED.format(id=new_id))
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _action_fire_employee() -> None:
    # Увольнение сотрудника
    print(admin_dialog.FIRE_HEADER)
    try:
        emp_id = _select_employee()
        if emp_id is None:
            print(common.CANCELLED)
        else:
            emp = employee_service.get_employee(emp_id)
            if not confirm(admin_dialog.CONFIRM_FIRE.format(name=emp.full_name)):
                print(common.CANCELLED)
            else:
                employee_service.fire_employee(emp_id)
                print(admin_dialog.EMPLOYEE_FIRED)
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _action_employee_history() -> None:
    # История переводов
    print(admin_dialog.HISTORY_HEADER)
    try:
        emp_id = _select_employee()
        if emp_id is None:
            print(common.CANCELLED)
        else:
            history = assignment_service.get_history(emp_id)
            print(output.format_assignments(history))
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _action_add_position() -> None:
    # Добавление должности
    print(admin_dialog.POSITION_ADD_HEADER)
    try:
        title = input(admin_dialog.PROMPT_POSITION_TITLE)
        salary = input_int(admin_dialog.PROMPT_POSITION_SALARY) or 0
        requirements = input_optional(admin_dialog.PROMPT_POSITION_REQUIREMENTS)
        new_id = directory_service.create_position(title, salary, requirements)
        print(admin_dialog.POSITION_CREATED.format(id=new_id))
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _action_update_position() -> None:
    # Изменение должности
    print(admin_dialog.POSITION_UPDATE_HEADER)
    try:
        _print_positions()
        pos_id = input_int(admin_dialog.PROMPT_POSITION_ID)
        if pos_id in (None, 0):
            print(common.CANCELLED)
        else:
            title = input(admin_dialog.PROMPT_POSITION_TITLE)
            salary = input_int(admin_dialog.PROMPT_POSITION_SALARY)
            requirements = input_optional(admin_dialog.PROMPT_POSITION_REQUIREMENTS)
            directory_service.update_position(pos_id, title, salary, requirements)
            print(admin_dialog.POSITION_UPDATED)
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _positions_menu() -> None:
    # Подменю должностей
    while True:
        print()
        print(admin_dialog.POSITIONS_HEADER)
        print(admin_dialog.POSITION_MENU_LIST)
        print(admin_dialog.POSITION_MENU_ADD)
        print(admin_dialog.POSITION_MENU_UPDATE)
        print(common.BACK)
        choice = input(common.CHOOSE_ACTION).strip()

        if choice == "1":
            print(output.format_positions(directory_service.list_positions()))
            pause()
        elif choice == "2":
            _action_add_position()
        elif choice == "3":
            _action_update_position()
        elif choice == "0":
            break
        else:
            print(common.INVALID_CHOICE)
            pause()


def _action_add_department() -> None:
    # Добавление отдела
    print(admin_dialog.DEPARTMENT_ADD_HEADER)
    try:
        name = input(admin_dialog.PROMPT_DEPARTMENT_NAME)
        description = input_optional(admin_dialog.PROMPT_DEPARTMENT_DESCRIPTION)
        new_id = directory_service.create_department(name, description)
        print(admin_dialog.DEPARTMENT_CREATED.format(id=new_id))
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _action_update_department() -> None:
    # Изменение отдела
    print(admin_dialog.DEPARTMENT_UPDATE_HEADER)
    try:
        _print_departments()
        dep_id = input_int(admin_dialog.PROMPT_DEPARTMENT_ID)
        if dep_id in (None, 0):
            print(common.CANCELLED)
        else:
            name = input(admin_dialog.PROMPT_DEPARTMENT_NAME)
            description = input_optional(admin_dialog.PROMPT_DEPARTMENT_DESCRIPTION)
            directory_service.update_department(dep_id, name, description)
            print(admin_dialog.DEPARTMENT_UPDATED)
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def _departments_menu() -> None:
    # Подменю отделов
    while True:
        print()
        print(admin_dialog.DEPARTMENTS_HEADER)
        print(admin_dialog.DEPARTMENT_MENU_LIST)
        print(admin_dialog.DEPARTMENT_MENU_ADD)
        print(admin_dialog.DEPARTMENT_MENU_UPDATE)
        print(common.BACK)
        choice = input(common.CHOOSE_ACTION).strip()

        if choice == "1":
            print(output.format_departments(directory_service.list_departments()))
            pause()
        elif choice == "2":
            _action_add_department()
        elif choice == "3":
            _action_update_department()
        elif choice == "0":
            break
        else:
            print(common.INVALID_CHOICE)
            pause()


def _action_create_user() -> None:
    # Создание пользователя
    print(admin_dialog.USER_CREATE_HEADER)
    print(admin_dialog.AVAILABLE_ROLES)
    _print_roles()
    try:
        username = input(admin_dialog.PROMPT_LOGIN)
        password = input(admin_dialog.PROMPT_PASSWORD)
        role_id = input_int(admin_dialog.PROMPT_ROLE_ID)
        if role_id in (None, 0):
            print(common.CANCELLED)
        else:
            new_id = auth_service.register(username, password, role_id)
            print(admin_dialog.USER_CREATED.format(id=new_id))
    except AppError as e:
        print(render_error(e.code, e.context))
    pause()


def admin_menu(user) -> None:
    # Меню администратора
    while True:
        print()
        print(admin_dialog.MENU_HEADER)
        print(admin_dialog.MENU_EMPLOYEES)
        print(admin_dialog.MENU_EMPLOYEE_ADD)
        print(admin_dialog.MENU_EMPLOYEE_UPDATE)
        print(admin_dialog.MENU_EMPLOYEE_TRANSFER)
        print(admin_dialog.MENU_EMPLOYEE_FIRE)
        print(admin_dialog.MENU_EMPLOYEE_HISTORY)
        print(admin_dialog.MENU_POSITIONS)
        print(admin_dialog.MENU_DEPARTMENTS)
        print(admin_dialog.MENU_USER_CREATE)
        print(common.EXIT)
        choice = input(common.CHOOSE_ACTION).strip()

        if choice == "1":
            _action_list_employees()
        elif choice == "2":
            _action_add_employee()
        elif choice == "3":
            _action_update_employee()
        elif choice == "4":
            _action_transfer_employee()
        elif choice == "5":
            _action_fire_employee()
        elif choice == "6":
            _action_employee_history()
        elif choice == "7":
            _positions_menu()
        elif choice == "8":
            _departments_menu()
        elif choice == "9":
            _action_create_user()
        elif choice == "0":
            break
        else:
            print(common.INVALID_CHOICE)
            pause()