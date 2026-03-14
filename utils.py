# debug/utils.py
"""
Утилиты для логирования и отладки.
"""

from datetime import datetime
from typing import Callable, Any, Optional, Dict
import inspect
from functools import wraps

from .config import LogLevel, TrafficLight, BaseColors, should_log, get_config


def get_timestamp() -> str:
    """Получить временную метку."""
    fmt = get_config('timestamp_format', "%H:%M:%S.%f")
    return datetime.now().strftime(fmt)[:-3]  # Обрезаем микросекунды до миллисекунд


def get_light(level: str) -> dict:
    """
    Получить настройки светофора для уровня.

    Returns:
        Словарь с color, emoji, name
    """
    light = TrafficLight.get(level)
    if light and get_config('color_enabled', True):
        return {
            'color': light['color'],
            'emoji': light['emoji'],
            'name': light['name']
        }

    return {
        'color': BaseColors.RESET,
        'emoji': '⚪',
        'name': level
    }


def format_signature(func: Callable, args: tuple, include_module: bool = False) -> str:
    """
    Форматировать сигнатуру функции.

    Args:
        func: Функция
        args: Аргументы
        include_module: Включить имя модуля

    Returns:
        Отформатированная сигнатура
    """
    func_name = func.__name__

    # Проверка на метод класса
    if args and hasattr(args[0], '__class__'):
        class_name = args[0].__class__.__name__
        signature = f"{class_name}.{func_name}"
    else:
        signature = func_name

    # Добавление модуля если нужно
    if include_module and hasattr(func, '__module__'):
        module = func.__module__.split('.')[-1]
        signature = f"{module}.{signature}"

    return signature


def format_value(value: Any, max_len: int = 50) -> str:
    """
    Форматировать значение для вывода.

    Args:
        value: Значение
        max_len: Максимальная длина

    Returns:
        Отформатированное значение
    """
    if value is None:
        return "None"

    repr_val = repr(value)
    if len(repr_val) > max_len:
        repr_val = repr_val[:max_len] + "..."

    return repr_val


def log_message(level: str, message: str, timestamp: Optional[str] = None) -> None:
    """
    Вывести отформатированное сообщение.

    Args:
        level: Уровень логирования
        message: Сообщение
        timestamp: Временная метка (если None, создается новая)
    """
    if not should_log(level):
        return

    light = get_light(level)
    ts = timestamp or get_timestamp()

    if get_config('show_timestamp', True):
        print(f"{BaseColors.BLUE}[{ts}]{BaseColors.RESET} "
              f"{light['color']}{message}{BaseColors.RESET}")
    else:
        print(f"{light['color']}{message}{BaseColors.RESET}")


def safe_execute(func: Callable, *args, **kwargs) -> Any:
    """
    Безопасно выполнить функцию с обработкой ошибок.

    Args:
        func: Функция для выполнения
        args, kwargs: Аргументы функции

    Returns:
        Результат функции или None при ошибке
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_message(LogLevel.ERROR, f"Ошибка при выполнении {func.__name__}: {e}")
        return None


def get_class_hierarchy(obj: Any) -> list:
    """
    Получить иерархию классов объекта.

    Args:
        obj: Объект

    Returns:
        Список имен классов от потомка к предку
    """
    hierarchy = []
    cls = obj.__class__ if hasattr(obj, '__class__') else obj

    while cls:
        hierarchy.append(cls.__name__)
        cls = cls.__base__

    return hierarchy


def get_object_dependencies(obj: Any, dep_names: list = None) -> dict:
    """
    Получить зависимости объекта.

    Args:
        obj: Объект
        dep_names: Список имен атрибутов для проверки

    Returns:
        Словарь {имя_зависимости: тип}
    """
    if dep_names is None:
        dep_names = ['board', 'game_state', 'renderer', 'model', 'view', 'controller']

    deps = {}
    for dep in dep_names:
        if hasattr(obj, dep):
            attr = getattr(obj, dep)
            if attr is not None:
                deps[dep] = type(attr).__name__

    return deps