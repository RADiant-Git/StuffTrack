import os
from typing import Optional
from dialogs import common


def pause() -> None:
    # Пауза
    input(common.PRESS_ENTER)


def clear() -> None:
    # Очистка экрана
    os.system("cls" if os.name == "nt" else "clear")


def input_int(prompt: str) -> Optional[int]:
    # Ввод целого числа
    try:
        raw = input(prompt).strip()
        return int(raw) if raw else None
    except ValueError:
        return None


def input_optional(prompt: str) -> Optional[str]:
    # Необязательное поле
    raw = input(prompt).strip()
    return raw if raw else None


def confirm(prompt: Optional[str] = None) -> bool:
    # Подтверждение действия
    msg = prompt if prompt is not None else common.CONFIRM_PROMPT
    answer = input(msg).strip().lower()
    return answer in ("y", "yes", "д", "да", "1")