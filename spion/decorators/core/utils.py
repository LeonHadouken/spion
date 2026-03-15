# spion/decorators/core/utils.py (исправленный)
"""
Утилиты для логирования и отладки.
"""

from datetime import datetime
from typing import Callable, Any, Optional
import traceback

from ...config import LogLevel, TrafficLight, BaseColors, should_log, get_config


def get_timestamp() -> str:
    """Получить временную метку."""
    fmt = get_config('timestamp_format', "%H:%M:%S.%f")
    return datetime.now().strftime(fmt)[:-3]


def get_light(level: str) -> dict:
    """
    Получить настройки светофора для уровня.
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


def format_signature(func, args: tuple, include_module: bool = False) -> str:
    """
    Форматировать сигнатуру функции.
    """
    if hasattr(func, '__self__') or (args and hasattr(args[0], '__class__')):
        # Это метод класса
        if args and hasattr(args[0], '__class__'):
            class_name = args[0].__class__.__name__
            func_name = func.__name__
            signature = f"{class_name}.{func_name}"
        else:
            signature = func.__name__
    else:
        signature = func.__name__

    if include_module and hasattr(func, '__module__'):
        module = func.__module__.split('.')[-1]
        signature = f"{module}.{signature}"

    return signature


def format_value(value: Any, max_len: int = 50) -> str:
    """
    Форматировать значение для вывода.
    """
    if value is None:
        return "None"

    try:
        repr_val = repr(value)
        if len(repr_val) > max_len:
            repr_val = repr_val[:max_len] + "..."
        return repr_val
    except:
        return f"<{type(value).__name__} object>"


def log_message(level: str, message: str, timestamp: Optional[str] = None) -> None:
    """
    Вывести отформатированное сообщение.
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


def safe_execute(func, *args, **kwargs) -> Any:
    """
    Безопасно выполнить функцию с обработкой ошибок.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_message(LogLevel.ERROR, f"Ошибка при выполнении {getattr(func, '__name__', 'unknown')}: {e}")
        return None


def get_class_hierarchy(obj: Any) -> list:
    """
    Получить иерархию классов объекта.
    """
    hierarchy = []
    cls = obj.__class__ if hasattr(obj, '__class__') else type(obj)

    while cls:
        hierarchy.append(cls.__name__)
        cls = cls.__base__

    return hierarchy


def get_object_dependencies(obj: Any, dep_names: list = None) -> dict:
    """
    Получить зависимости объекта.
    """
    if dep_names is None:
        dep_names = ['board', 'game_state', 'renderer', 'model', 'view', 'controller',
                     'db', 'database', 'cache', 'logger', 'config']

    deps = {}
    for dep in dep_names:
        if hasattr(obj, dep):
            attr = getattr(obj, dep)
            if attr is not None:
                deps[dep] = type(attr).__name__

    return deps


def get_exception_traceback() -> str:
    """Получить текущий traceback как строку."""
    return traceback.format_exc()