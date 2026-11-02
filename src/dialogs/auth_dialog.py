from services import AuthService

def show_auth_menu():
    print("=== АВТОРИЗАЦИЯ В СИСТЕМЕ STAFFTRACK ===")
    username = input("Введите логин: ")
    password = input("Введите пароль: ")
    
    try:
        user = AuthService.authenticate(username, password)
        print("Авторизация успешна.")
        return user
    except Exception as e:
        print(f"Ошибка аутентификации: {e}")
        return None