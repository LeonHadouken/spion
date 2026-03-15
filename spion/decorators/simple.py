# spion/decorators/simple.py (исправляем импорт trace)
"""
Простые декораторы для логирования.
"""

from functools import wraps
from typing import Callable, Any, Optional
from time import time
import threading

from ..config import LogLevel
from .base.decorator import LoggerDecorator
from .core.utils import log_message, format_signature, get_timestamp, format_value
from .chain import trace  # Правильный импорт trace из chain.py


class LogDecorator(LoggerDecorator):
    """
    Простое логирование вызовов функций и методов.
    """

    def _before(self, func: Callable, args: tuple, kwargs: dict,
                context, signature: str) -> None:
        """
        Логировать вызов функции.
        """
        msg = self.message or f"Вызов {signature}"

        # Добавляем аргументы для DEBUG уровня
        if self.level == LogLevel.DEBUG:
            args_str = self._format_arguments(args, kwargs)
            if args_str:
                msg += f" {args_str}"

        # Добавляем номер вызова
        msg += f" (вызов #{context.call_id})"

        log_message(self.level, f"▶️ {msg}", context.timestamp_str)

    def _after(self, result: Any, context, signature: str) -> None:
        """
        Логировать результат.
        """
        if self.level == LogLevel.DEBUG and result is not None:
            log_message(
                LogLevel.INFO,
                f"◀️ {signature} -> {format_value(result)} (вызов #{context.call_id})",
                context.timestamp_str
            )

    def _format_arguments(self, args: tuple, kwargs: dict) -> str:
        """
        Форматировать аргументы для отображения.
        """
        parts = []

        # Позиционные аргументы (пропускаем self для методов)
        start_idx = 1 if args and hasattr(args[0], '__class__') else 0
        for arg in args[start_idx:]:
            parts.append(format_value(arg))

        # Именованные аргументы
        for k, v in kwargs.items():
            parts.append(f"{k}={format_value(v)}")

        if parts:
            return f"с аргументами: {', '.join(parts)}"
        return ""


# Основные декораторы
def log(level: str = LogLevel.INFO, message: Optional[str] = None):
    """Декоратор для базового логирования вызовов."""
    return LogDecorator(level, message)


# СИНТАКСИЧЕСКИЙ САХАР ✨
def watch(level: str = LogLevel.INFO, message: Optional[str] = None):
    """
    Следить за функцией (алиас для @log)
    """
    return LogDecorator(level, message)


def light(level: str = LogLevel.INFO):
    """
    Лёгкое логирование (только вход)
    """
    return LogDecorator(level)


def silent(level: str = LogLevel.ERROR):
    """
    Тихий режим — только ошибки
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                from spion.decorators.base.decorator import LoggerDecorator
                from spion.decorators.core.context import CallContext
                from datetime import datetime

                temp_decorator = LoggerDecorator(level=level)
                context = CallContext.create(
                    func=func,
                    args=args,
                    kwargs=kwargs,
                    call_id=1,
                    timestamp=datetime.now()
                )
                signature = format_signature(func, args, include_module=True)
                temp_decorator._error(e, context, signature)
                raise

        return wrapper

    return decorator


# Потокобезопасное хранилище для log_call_once
_call_once_storage = threading.local()


def log_call_once(interval: float = 1.0):
    """
    Декоратор для логирования с интервалом.
    """

    def decorator(func):
        if not hasattr(_call_once_storage, 'last_logged'):
            _call_once_storage.last_logged = {}

        func_key = f"{func.__module__}.{func.__name__}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            signature = format_signature(func, args, include_module=True)

            last = _call_once_storage.last_logged.get(func_key, 0)

            if now - last >= interval:
                _call_once_storage.last_logged[func_key] = now
                timestamp = get_timestamp()

                log_message(
                    'SYSTEM',
                    f"[🔄] {signature} (интервал={interval}с)",
                    timestamp
                )

                if last > 0:
                    skipped = int((now - last) / interval) - 1
                    if skipped > 0:
                        log_message(
                            LogLevel.DEBUG,
                            f"   ⏱️ Пропущено {skipped} вызовов",
                            timestamp
                        )

            return func(*args, **kwargs)

        wrapper.__original_func__ = func
        wrapper.__interval__ = interval
        return wrapper

    return decorator


def throttle(interval: float = 1.0):
    """Ограничить частоту логирования (алиас для @log_call_once)"""
    return log_call_once(interval)


def log_user_action():
    """Декоратор для логирования действий пользователя."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signature = format_signature(func, args, include_module=True)
            timestamp = get_timestamp()

            pos = next(
                (a for a in args if hasattr(a, 'row') and hasattr(a, 'col')),
                None
            )

            if pos:
                try:
                    col_letter = chr(65 + pos.col) if 0 <= pos.col <= 25 else '?'
                    row_num = 8 - pos.row if 0 <= pos.row <= 7 else pos.row + 1
                    coord = f"{col_letter}{row_num}"

                    log_message(
                        LogLevel.INFO,
                        f"[👤] {signature} на {coord} (row={pos.row}, col={pos.col})",
                        timestamp
                    )
                except (ValueError, TypeError):
                    log_message(
                        LogLevel.INFO,
                        f"[👤] {signature} (координаты: {pos})",
                        timestamp
                    )
            else:
                log_message(LogLevel.INFO, f"[👤] {signature}", timestamp)

            return func(*args, **kwargs)

        wrapper.__is_user_action__ = True
        return wrapper

    return decorator


def user():
    """Логировать действия пользователя (алиас для @log_user_action)"""
    return log_user_action()


def log_state_change():
    """Декоратор для логирования изменений состояния."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            state_before = {}
            if args and hasattr(args[0], '__dict__'):
                state_before = args[0].__dict__.copy()

            signature = format_signature(func, args, include_module=True)
            timestamp = get_timestamp()

            result = func(*args, **kwargs)

            changes = []
            if args and hasattr(args[0], '__dict__'):
                state_after = args[0].__dict__
                for key, value in state_after.items():
                    if key in state_before and state_before[key] != value:
                        changes.append(f"{key}: {state_before[key]} -> {value}")
                    elif key not in state_before:
                        changes.append(f"{key}: (new) {value}")

            player_info = ""
            if args and hasattr(args[0], 'current_player'):
                player = args[0].current_player
                player_value = getattr(player, 'value', player)
                player_info = f" | Ход: {player_value}"

            if changes:
                changes_str = ", ".join(changes[:3])
                if len(changes) > 3:
                    changes_str += f" и ещё {len(changes) - 3}"
                player_info += f" | Изменения: {changes_str}"

            log_message(
                LogLevel.WARNING,
                f"[🔄] {signature}{player_info}",
                timestamp
            )

            return result

        wrapper.__is_state_change__ = True
        return wrapper

    return decorator


def state():
    """Логировать изменения состояния (алиас для @log_state_change)"""
    return log_state_change()


def spy(*decorators):
    """Шпион — комбинация нескольких декораторов"""
    from .base.composer import DecoratorComposer
    return DecoratorComposer(*decorators)


# Экспортируем всё нужное
__all__ = [
    'LogDecorator',
    'log',
    'log_call_once',
    'log_user_action',
    'log_state_change',
    'watch',
    'light',
    'silent',
    'trace',  # теперь trace импортирован из chain.py
    'user',
    'state',
    'throttle',
    'spy',
]