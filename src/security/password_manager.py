PREFIX_PLAIN = "plain:"


def hash_password(plain_password: str) -> str:
    # Хэширование пароля
    return f"{PREFIX_PLAIN}{plain_password}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    # Проверка пароля
    if not plain_password or not stored_hash:
        return False
    if stored_hash.startswith(PREFIX_PLAIN):
        return stored_hash[len(PREFIX_PLAIN):] == plain_password
    return False