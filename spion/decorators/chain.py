# spion/decorators/chain.py (исправленная версия)
"""
Декоратор для логирования цепочек вызовов.
"""

from typing import Callable, Any
import threading

from ..config import LogLevel
from .base.decorator import LoggerDecorator
from .core.utils import log_message, format_value


class ChainDecorator(LoggerDecorator):
    """
    Логирование цепочек вызовов с отступами.
    """

    # Потоково-локальное хранилище для глубины
    _local = threading.local()
    _call_counter = 0
    _lock = threading.Lock()

    def __init__(self, level: str = LogLevel.DEBUG, max_depth: int = 5):
        """
        Инициализация декоратора цепочек.
        """
        super().__init__(level)
        self.max_depth = max_depth

        # Уникальный ID для цепочки
        with ChainDecorator._lock:
            self.call_id = ChainDecorator._call_counter
            ChainDecorator._call_counter += 1

    def _get_depth(self) -> int:
        """Получить текущую глубину для текущего потока."""
        if not hasattr(ChainDecorator._local, 'depth'):
            ChainDecorator._local.depth = 0
        return ChainDecorator._local.depth

    def _set_depth(self, value: int) -> None:
        """Установить глубину для текущего потока."""
        ChainDecorator._local.depth = value

    def _increase_depth(self) -> int:
        """Увеличить глубину и вернуть новое значение."""
        depth = self._get_depth() + 1
        self._set_depth(depth)
        return depth

    def _decrease_depth(self) -> int:
        """Уменьшить глубину и вернуть новое значение."""
        depth = max(0, self._get_depth() - 1)
        self._set_depth(depth)
        return depth

    def _get_call_type(self) -> str:
        """Получить тип вызова для фильтрации."""
        return "chain"

    def _should_log(self, context, signature: str) -> bool:
        """
        Проверить, нужно ли логировать.
        Для цепочек всегда логируем, если не превышена глубина.
        """
        current_depth = self._get_depth()
        return current_depth <= self.max_depth

    def _get_indent(self) -> str:
        """Получить отступ для текущей глубины."""
        return "  " * self._get_depth()

    def _before(self, func: Callable, args: tuple, kwargs: dict,
                context, signature: str) -> None:
        """Логировать вход в функцию с отступом."""
        depth = self._increase_depth()

        # Проверяем глубину еще раз (на случай если увеличили сверх лимита)
        if depth <= self.max_depth:
            indent = self._get_indent()
            # Форматируем аргументы для отображения
            args_str = self._format_args_for_display(args, kwargs)

            log_message(
                self.level,
                f"{indent}[↘️] {signature}{args_str} (depth={depth})",
                context.timestamp_str
            )

    def _after(self, result: Any, context, signature: str) -> None:
        """Логировать выход из функции с отступом."""
        depth = self._get_depth()

        if depth <= self.max_depth:
            indent = self._get_indent()
            result_str = format_value(result, max_len=30)

            log_message(
                self.level,
                f"{indent}[↗️] {signature} -> {result_str} (depth={depth})",
                context.timestamp_str
            )

        self._decrease_depth()

    def _error(self, error: Exception, context, signature: str) -> None:
        """Логировать ошибку с отступом."""
        depth = self._get_depth()

        if depth <= self.max_depth:
            indent = self._get_indent()

            log_message(
                LogLevel.ERROR,
                f"{indent}[❌] {signature}: {error} (depth={depth})",
                context.timestamp_str
            )

            if self.level == LogLevel.DEBUG:
                from .core.utils import get_exception_traceback
                tb = get_exception_traceback()
                log_message(
                    LogLevel.DEBUG,
                    f"{indent}{tb.replace(chr(10), chr(10) + indent)}",
                    context.timestamp_str
                )

        self._decrease_depth()

    def _format_args_for_display(self, args: tuple, kwargs: dict) -> str:
        """
        Форматировать аргументы для отображения в цепочке.
        """
        if self.level != LogLevel.DEBUG:
            return ""

        parts = []

        # Позиционные аргументы (пропускаем self)
        start_idx = 1 if args and hasattr(args[0], '__class__') else 0
        for i, arg in enumerate(args[start_idx:], start_idx):
            parts.append(format_value(arg, max_len=20))

        # Именованные аргументы
        for k, v in kwargs.items():
            parts.append(f"{k}={format_value(v, max_len=20)}")

        if parts:
            return f"({', '.join(parts)})"
        return ""


def log_method_chain(level: str = LogLevel.DEBUG, max_depth: int = 5):
    """
    Декоратор для логирования цепочек вызовов.
    """
    return ChainDecorator(level, max_depth)


trace = log_method_chain