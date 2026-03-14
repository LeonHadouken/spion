# debug/decorators/chain.py

"""
Декоратор для логирования цепочек вызовов.
"""

from typing import Callable, Any

from debug.config import LogLevel
from debug.decorators.base import LoggerDecorator
from debug.utils import log_message, format_value


class ChainDecorator(LoggerDecorator):
    """
    Логирование цепочек вызовов с отступами.
    Показывает вложенность вызовов.
    """

    _depth = 0
    _call_id = 0

    def __init__(self, level: str = LogLevel.DEBUG, max_depth: int = 5):
        """
        Args:
            level: Уровень логирования
            max_depth: Максимальная глубина для логирования
        """
        super().__init__(level)
        self.max_depth = max_depth
        self.call_id = ChainDecorator._call_id
        ChainDecorator._call_id += 1

    def _get_call_type(self) -> str:
        return "chain"

    def _should_log(self) -> bool:
        """Логируем только до определенной глубины."""
        return ChainDecorator._depth <= self.max_depth and super()._should_log()

    def _before(self, func: Callable, args: tuple, kwargs: dict) -> None:
        """Логировать вход в функцию с отступом."""
        indent = "  " * ChainDecorator._depth
        log_message(self.level, f"{indent}[↘️] {self.signature}", self.timestamp)
        ChainDecorator._depth += 1

    def _after(self, result: Any) -> None:
        """Логировать выход из функции с отступом."""
        ChainDecorator._depth -= 1
        indent = "  " * ChainDecorator._depth
        result_str = format_value(result)
        log_message(self.level, f"{indent}[↗️] {self.signature} -> {result_str}", self.timestamp)


def log_method_chain(level: str = LogLevel.DEBUG, max_depth: int = 5):
    """
    Декоратор для логирования цепочек вызовов.
    Показывает вложенность вызовов с отступами.

    Args:
        level: Уровень логирования
        max_depth: Максимальная глубина для логирования

    Example:
        @log_method_chain(max_depth=3)
        def recursive_function(n):
            if n <= 0:
                return 0
            return n + recursive_function(n-1)
    """
    return ChainDecorator(level, max_depth)