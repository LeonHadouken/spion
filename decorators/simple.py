# debug/decorators/simple.py

"""
Простые декораторы для логирования.
Базовые декораторы для повседневного использования.
"""

from functools import wraps
from typing import Callable, Any, Optional, Dict
from time import time
import threading

from debug.config import LogLevel
from debug.decorators.base import LoggerDecorator
from debug.utils import log_message, format_signature, get_timestamp, format_value


class LogDecorator(LoggerDecorator):
    """
    Простое логирование вызовов функций и методов.

    Логирует:
    - Вход в функцию (▶️)
    - Выход с результатом для DEBUG уровня (◀️)
    - Ошибки с трейсом (❌)

    Example:
        >>> @LogDecorator(level=LogLevel.INFO)
        ... def hello(name):
        ...     return f"Hello, {name}!"
    """

    def _before(self, func: Callable, args: tuple, kwargs: dict,
                context: Dict[str, Any]) -> None:
        """
        Логировать вызов функции.

        Args:
            func: Декорируемая функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            context: Контекст вызова
        """
        msg = self.message or f"Вызов {self.signature}"

        # Добавляем аргументы для DEBUG уровня
        if self.level == LogLevel.DEBUG:
            args_str = self._format_arguments(args, kwargs)
            if args_str:
                msg += f" {args_str}"

        # Добавляем номер вызова
        msg += f" (вызов #{context['call_id']})"

        log_message(self.level, f"▶️ {msg}", self.timestamp)

    def _after(self, result: Any, context: Dict[str, Any]) -> None:
        """
        Логировать результат.

        Args:
            result: Результат функции
            context: Контекст вызова
        """
        if self.level == LogLevel.DEBUG and result is not None:
            log_message(
                LogLevel.INFO,
                f"◀️ {self.signature} -> {format_value(result)} (вызов #{context['call_id']})",
                self.timestamp
            )

    def _format_arguments(self, args: tuple, kwargs: dict) -> str:
        """
        Форматировать аргументы для отображения.

        Args:
            args: Позиционные аргументы
            kwargs: Именованные аргументы

        Returns:
            str: Отформатированная строка аргументов
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


def log(level: str = LogLevel.INFO, message: Optional[str] = None):
    """
    Декоратор для базового логирования вызовов.

    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        message: Пользовательское сообщение (опционально)

    Returns:
        Callable: Декорированная функция

    Example:
        >>> @log(level=LogLevel.DEBUG)
        ... def add(a, b):
        ...     return a + b
        ...
        >>> add(5, 3)
        [14:30:25.123] 🔵 ▶️ Вызов add с аргументами: 5, 3 (вызов #1)
        [14:30:25.123] 🟢 ◀️ add -> 8 (вызов #1)

        >>> @log(level=LogLevel.WARNING, message="Редкая операция")
        ... def dangerous_operation():
        ...     return "done"
        ...
        >>> dangerous_operation()
        [14:30:25.123] 🟡 ▶️ Редкая операция (вызов #1)

        >>> @log(level=LogLevel.ERROR)
        ... def might_fail():
        ...     raise ValueError("Ошибка")
        ...
        >>> might_fail()
        [14:30:25.123] 🔴 [❌] might_fail: Ошибка (вызов #1)
    """
    return LogDecorator(level, message)


# Потокобезопасное хранилище для log_call_once
_call_once_storage = threading.local()


def log_call_once(interval: float = 1.0):
    """
    Декоратор для логирования с интервалом (не чаще 1 раза в interval секунд).

    Полезно для:
    - Шумных функций, вызываемых очень часто
    - Мониторинга состояния
    - Прогресс-баров

    Args:
        interval: Минимальный интервал между логами в секундах

    Returns:
        Callable: Декорированная функция

    Example:
        >>> @log_call_once(interval=5.0)
        ... def check_status():
        ...     return "OK"
        ...
        >>> for _ in range(20):
        ...     check_status()  # Логируется только раз в 5 секунд
        ...     time.sleep(0.5)

        >>> @log_call_once(interval=60.0)
        ... def report_metrics():
        ...     # Тяжёлая операция сбора метрик
        ...     return {"cpu": 10, "memory": 50}
    """

    def decorator(func):
        # Используем словарь в потоково-локальном хранилище
        if not hasattr(_call_once_storage, 'last_logged'):
            _call_once_storage.last_logged = {}

        func_key = f"{func.__module__}.{func.__name__}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            signature = format_signature(func, args, include_module=True)

            # Проверяем, когда логировали в последний раз
            last = _call_once_storage.last_logged.get(func_key, 0)

            if now - last >= interval:
                _call_once_storage.last_logged[func_key] = now
                timestamp = get_timestamp()

                # Добавляем информацию об интервале
                log_message(
                    'SYSTEM',
                    f"[🔄] {signature} (интервал={interval}с)",
                    timestamp
                )

                # Для DEBUG режима показываем количество пропущенных вызовов
                if last > 0:
                    skipped = int((now - last) / interval) - 1
                    if skipped > 0:
                        log_message(
                            LogLevel.DEBUG,
                            f"   ⏱️ Пропущено {skipped} вызовов",
                            timestamp
                        )

            return func(*args, **kwargs)

        # Сохраняем метаданные
        wrapper.__original_func__ = func
        wrapper.__interval__ = interval
        return wrapper

    return decorator


def log_user_action():
    """
    Декоратор для логирования действий пользователя.

    Автоматически определяет координаты если они есть в аргументах.
    Ищет объекты с атрибутами row и col и конвертирует в шахматную нотацию.
    Полезно для GUI приложений, игр, веб-интерфейсов.

    Returns:
        Callable: Декорированная функция

    Example:
        >>> class Position:
        ...     def __init__(self, row, col):
        ...         self.row = row
        ...         self.col = col
        ...
        >>> class Game:
        ...     @log_user_action()
        ...     def click(self, position):
        ...         print(f"Клик на {position.row}, {position.col}")
        ...
        >>> game = Game()
        >>> game.click(Position(3, 4))  # row=3 -> 5, col=4 -> E
        [14:30:25.123] [👤] Game.click на E5

        >>> @log_user_action()
        ... def login(username, password):
        ...     authenticate(username, password)
        ...
        >>> login("user", "pass")
        [14:30:25.123] [👤] login
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signature = format_signature(func, args, include_module=True)
            timestamp = get_timestamp()

            # Поиск позиции в аргументах
            pos = next(
                (a for a in args if hasattr(a, 'row') and hasattr(a, 'col')),
                None
            )

            if pos:
                # Конвертация в шахматную нотацию (A1, B2 и т.д.)
                try:
                    col_letter = chr(65 + pos.col) if 0 <= pos.col <= 25 else '?'
                    row_num = 8 - pos.row if 0 <= pos.row <= 7 else pos.row + 1
                    coord = f"{col_letter}{row_num}"

                    # Добавляем информацию о координатах
                    log_message(
                        LogLevel.INFO,
                        f"[👤] {signature} на {coord} (row={pos.row}, col={pos.col})",
                        timestamp
                    )
                except (ValueError, TypeError):
                    # Если координаты некорректные, логируем упрощённо
                    log_message(
                        LogLevel.INFO,
                        f"[👤] {signature} (координаты: {pos})",
                        timestamp
                    )
            else:
                log_message(LogLevel.INFO, f"[👤] {signature}", timestamp)

            return func(*args, **kwargs)

        # Сохраняем метаданные
        wrapper.__is_user_action__ = True
        return wrapper

    return decorator


def log_state_change():
    """
    Декоратор для логирования изменений состояния.

    Автоматически определяет текущего игрока если он есть
    (ищет атрибут current_player у self).
    Полезно для игр, конечных автоматов, систем с состоянием.

    Returns:
        Callable: Декорированная функция

    Example:
        >>> from enum import Enum
        >>> class Player(Enum):
        ...     WHITE = "белые"
        ...     BLACK = "черные"
        ...
        >>> class Game:
        ...     def __init__(self):
        ...         self.current_player = Player.WHITE
        ...         self.move_count = 0
        ...
        ...     @log_state_change()
        ...     def switch_player(self):
        ...         self.current_player = (
        ...             Player.BLACK if self.current_player == Player.WHITE
        ...             else Player.WHITE
        ...         )
        ...         self.move_count += 1
        ...
        >>> game = Game()
        >>> game.switch_player()
        [14:30:25.123] [🔄] Game.switch_player | Ход: белые (ход #1)
        >>> game.switch_player()
        [14:30:25.123] [🔄] Game.switch_player | Ход: черные (ход #2)

        >>> class TrafficLight:
        ...     def __init__(self):
        ...         self.current_player = "cars"  # Для декоратора
        ...         self.color = "red"
        ...
        ...     @log_state_change()
        ...     def change(self):
        ...         self.color = "green"
        ...
        >>> light = TrafficLight()
        >>> light.change()
        [14:30:25.123] [🔄] TrafficLight.change | Ход: cars
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Сохраняем состояние ДО изменения
            state_before = {}
            if args and hasattr(args[0], '__dict__'):
                # Копируем текущее состояние для сравнения
                state_before = args[0].__dict__.copy()

            signature = format_signature(func, args, include_module=True)
            timestamp = get_timestamp()

            # Выполняем функцию (состояние изменится)
            result = func(*args, **kwargs)

            # Анализируем изменения
            changes = []
            if args and hasattr(args[0], '__dict__'):
                state_after = args[0].__dict__
                for key, value in state_after.items():
                    if key in state_before and state_before[key] != value:
                        changes.append(f"{key}: {state_before[key]} -> {value}")
                    elif key not in state_before:
                        changes.append(f"{key}: (new) {value}")

            # Формируем сообщение
            player_info = ""
            if args and hasattr(args[0], 'current_player'):
                player = args[0].current_player
                # Если это Enum, берём value, иначе строку
                player_value = getattr(player, 'value', player)
                player_info = f" | Ход: {player_value}"

            # Добавляем информацию об изменениях для DEBUG режима
            if changes and LogLevel.DEBUG:
                changes_str = ", ".join(changes[:3])  # Ограничиваем до 3 изменений
                if len(changes) > 3:
                    changes_str += f" и ещё {len(changes) - 3}"
                player_info += f" | Изменения: {changes_str}"

            # Добавляем счётчик вызовов
            call_count = getattr(args[0], '_state_change_count', 0) + 1 if args else 0
            if args:
                args[0]._state_change_count = call_count
                player_info += f" (ход #{call_count})"

            log_message(
                LogLevel.WARNING,
                f"[🔄] {signature}{player_info}",
                timestamp
            )

            return result

        # Сохраняем метаданные
        wrapper.__is_state_change__ = True
        return wrapper

    return decorator


# Удобные алиасы для быстрого доступа
watch = log  # алиас для @log
trace = log_method_chain  # алиас для @log_method_chain
spy = log_class_relationship  # алиас для @log_class_relationship
user = log_user_action  # алиас для @log_user_action
state = log_state_change  # алиас для @log_state_change
throttle = log_call_once  # алиас для @log_call_once