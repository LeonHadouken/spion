# simple.py

"""
Простые декораторы для логирования.
"""

from functools import wraps
from typing import Callable, Any, Optional
from time import time

from debug.config import LogLevel
from debug.decorators.base import LoggerDecorator
from debug.utils import log_message, format_signature, get_timestamp, format_value
from debug.filters import should_log


class LogDecorator(LoggerDecorator):
    """
    Простое логирование вызовов функций и методов.
    """

    def _before(self, func: Callable, args: tuple, kwargs: dict) -> None:
        """Логировать вызов функции."""
        msg = self.message or f"Вызов {self.signature}"

        # Добавляем аргументы для DEBUG уровня
        if self.level == LogLevel.DEBUG:
            args_repr = [format_value(a) for a in args[1:]]  # пропускаем self
            kwargs_repr = [f"{k}={format_value(v)}" for k, v in kwargs.items()]

            if args_repr or kwargs_repr:
                msg += f" с аргументами: {', '.join(args_repr + kwargs_repr)}"

        log_message(self.level, f"▶️ {msg}", self.timestamp)

    def _after(self, result: Any) -> None:
        """Логировать результат."""
        if self.level == LogLevel.DEBUG and result is not None:
            log_message(LogLevel.INFO, f"◀️ {self.signature} -> {format_value(result)}", self.timestamp)


def log(level: str = LogLevel.INFO, message: Optional[str] = None):
    """
    Декоратор для логирования вызовов.

    Args:
        level: Уровень логирования
        message: Пользовательское сообщение

    Example:
        @log(level=LogLevel.DEBUG)
        def my_function(x, y):
            return x + y
    """
    return LogDecorator(level, message)


def log_call_once(interval: float = 1.0):
    """
    Декоратор для логирования с интервалом (не чаще 1 раза в interval секунд).

    Args:
        interval: Минимальный интервал между логами в секундах

    Example:
        @log_call_once(interval=5.0)
        def frequently_called_function():
            pass
    """

    def decorator(func):
        last_logged = [0.0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            signature = format_signature(func, args)

            if now - last_logged[0] >= interval:
                last_logged[0] = now
                timestamp = get_timestamp()
                log_message('SYSTEM', f"[🔄] {signature}", timestamp)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_user_action():
    """
    Декоратор для логирования действий пользователя.
    Автоматически определяет координаты если они есть в аргументах.

    Example:
        @log_user_action()
        def make_move(self, position):
            pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signature = format_signature(func, args)
            timestamp = get_timestamp()

            # Поиск позиции в аргументах
            pos = next((a for a in args if hasattr(a, 'row') and hasattr(a, 'col')), None)

            if pos:
                coord = f"{chr(65 + pos.col)}{8 - pos.row}"  # A1, B2 и т.д.
                log_message(LogLevel.INFO, f"[👤] {signature} на {coord}", timestamp)
            else:
                log_message(LogLevel.INFO, f"[👤] {signature}", timestamp)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_state_change():
    """
    Декоратор для логирования изменений состояния.
    Автоматически определяет текущего игрока если он есть.

    Example:
        @log_state_change()
        def switch_player(self):
            pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            signature = format_signature(func, args)
            timestamp = get_timestamp()

            # Поиск текущего игрока
            if args and hasattr(args[0], 'current_player'):
                player = args[0].current_player
                log_message(LogLevel.WARNING, f"[🔄] {signature} | Ход: {player.value}", timestamp)
            else:
                log_message(LogLevel.WARNING, f"[🔄] {signature}", timestamp)

            return result

        return wrapper

    return decorator