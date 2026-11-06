from dialogs import common
from init_db import create_database, DB_FILE
from repositories.base import DBManager
from services import auth_service
from ui import auth_ui
from ui.admin_menu import admin_menu
from ui.employee_menu import employee_menu
from ui.helpers import pause


def main() -> None:
    # Точка входа
    if not DB_FILE.exists():
        create_database()

    try:
        while True:
            choice = auth_ui.start_menu()
            if choice == "1":
                user = auth_ui.login_flow()
                if user is None:
                    continue
                if auth_service.is_admin(user):
                    admin_menu(user)
                else:
                    employee_menu(user)
                break
            elif choice == "2":
                auth_ui.register_flow()
            elif choice == "0":
                break
            else:
                print(common.INVALID_CHOICE)
                pause()
    finally:
        DBManager.close_connection()
        print(common.GOODBYE)


if __name__ == "__main__":
    main()