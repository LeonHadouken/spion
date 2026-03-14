# debug/decorators/chain.py

"""
Декоратор для логирования цепочек вызовов.
Показывает вложенность вызовов с отступами, идеально для отслеживания рекурсии.
"""

from typing import Callable, Any, Dict
import threading

from debug.config import LogLevel
from debug.decorators.base import LoggerDecorator
from debug.utils import log_message, format_value


class ChainDecorator(LoggerDecorator):
    """
    Логирование цепочек вызовов с отступами.

    Показывает вложенность вызовов, что особенно полезно для:
    - Отслеживания рекурсивных функций
    - Понимания потока выполнения в сложных алгоритмах
    - Отладки древовидных структур

    Attributes:
        max_depth (int): Максимальная глубина для логирования
        call_id (int): Уникальный идентификатор цепочки
        _depth (int): Текущая глубина (общая для всех экземпляров)
        _local (threading.local): Потоково-локальное хранилище глубины

    Example:
        >>> @ChainDecorator(max_depth=3)
        ... def factorial(n):
        ...     if n <= 1:
        ...         return 1
        ...     return n * factorial(n-1)
    """

    # Потоково-локальное хранилище для глубины (поддержка многопоточности)
    _local = threading.local()
    _call_counter = 0
    _lock = threading.Lock()

    def __init__(self, level: str = LogLevel.DEBUG, max_depth: int = 5):
        """
        Инициализация декоратора цепочек.

        Args:
            level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_depth: Максимальная глубина для логирования
                      (вызовы глубже этой глубины не логируются)

        Example:
            >>> @ChainDecorator(max_depth=10)
            ... def deep_recursion(n):
            ...     if n <= 0:
            ...         return 0
            ...     return deep_recursion(n-1)
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

    def _should_log(self) -> bool:
        """
        Проверить, нужно ли логировать.

        Логируем только если:
        1. Не превышена максимальная глубина
        2. Базовый фильтр разрешает

        Returns:
            bool: True если нужно логировать
        """
        return self._get_depth() <= self.max_depth and super()._should_log()

    def _get_indent(self) -> str:
        """Получить отступ для текущей глубины."""
        return "  " * self._get_depth()

    def _before(self, func: Callable, args: tuple, kwargs: dict,
                context: Dict[str, Any]) -> None:
        """
        Логировать вход в функцию с отступом.

        Args:
            func: Декорируемая функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            context: Контекст вызова
        """
        depth = self._increase_depth()
        indent = self._get_indent()

        # Форматируем аргументы для отображения
        args_str = self._format_args_for_display(args, kwargs)

        log_message(
            self.level,
            f"{indent}[↘️] {self.signature}{args_str} (depth={depth})",
            self.timestamp
        )

    def _after(self, result: Any, context: Dict[str, Any]) -> None:
        """
        Логировать выход из функции с отступом.

        Args:
            result: Результат функции
            context: Контекст вызова
        """
        depth = self._get_depth()
        indent = self._get_indent()
        result_str = format_value(result, max_len=30)

        log_message(
            self.level,
            f"{indent}[↗️] {self.signature} -> {result_str} (depth={depth})",
            self.timestamp
        )

        self._decrease_depth()

    def _error(self, error: Exception, context: Dict[str, Any]) -> None:
        """
        Логировать ошибку с отступом.

        Args:
            error: Исключение
            context: Контекст вызова
        """
        depth = self._get_depth()
        indent = self._get_indent()

        log_message(
            LogLevel.ERROR,
            f"{indent}[❌] {self.signature}: {error} (depth={depth})",
            self.timestamp
        )

        # Для DEBUG уровня показываем стек
        if self.level == LogLevel.DEBUG:
            import traceback
            log_message(
                LogLevel.DEBUG,
                f"{indent}{traceback.format_exc().replace(chr(10), chr(10) + indent)}",
                self.timestamp
            )

        self._decrease_depth()

    def _format_args_for_display(self, args: tuple, kwargs: dict) -> str:
        """
        Форматировать аргументы для отображения в цепочке.

        Args:
            args: Позиционные аргументы
            kwargs: Именованные аргументы

        Returns:
            str: Отформатированная строка аргументов
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

    Показывает вложенность вызовов с отступами, что идеально подходит для:
    - Отслеживания рекурсивных функций
    - Понимания потока выполнения в сложных алгоритмах
    - Отладки обхода деревьев и графов

    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        max_depth: Максимальная глубина для логирования (вызовы глубже не логируются)

    Returns:
        Callable: Декорированная функция

    Example:
        >>> @log_method_chain(max_depth=3)
        ... def fibonacci(n):
        ...     if n <= 1:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
        ...
        >>> fibonacci(3)
        [14:30:25.123] 🔵 [↘️] fibonacci(3) (depth=1)
          [14:30:25.123] 🔵 [↘️] fibonacci(2) (depth=2)
            [14:30:25.123] 🔵 [↘️] fibonacci(1) (depth=3)
            [14:30:25.123] 🔵 [↗️] fibonacci(1) -> 1 (depth=3)
            [14:30:25.123] 🔵 [↘️] fibonacci(0) (depth=3)
            [14:30:25.123] 🔵 [↗️] fibonacci(0) -> 0 (depth=3)
          [14:30:25.123] 🔵 [↗️] fibonacci(2) -> 1 (depth=2)
          [14:30:25.123] 🔵 [↘️] fibonacci(1) (depth=2)
          [14:30:25.123] 🔵 [↗️] fibonacci(1) -> 1 (depth=2)
        [14:30:25.123] 🔵 [↗️] fibonacci(3) -> 2 (depth=1)

        >>> @log_method_chain(level=LogLevel.INFO, max_depth=2)
        ... def tree_traversal(node):
        ...     if node:
        ...         tree_traversal(node.left)
        ...         tree_traversal(node.right)
    """
    return ChainDecorator(level, max_depth)