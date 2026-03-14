# debug/decorators/relationship.py

"""
Декоратор для логирования связей между классами.
"""

from typing import Callable, Any
import inspect

from debug.config import LogLevel
from debug.decorators.base import LoggerDecorator
from debug.utils import log_message, get_class_hierarchy, get_object_dependencies


class RelationshipDecorator(LoggerDecorator):
    """
    Логирование связей между классами, иерархии и зависимостей.
    """

    def __init__(self, level: str = LogLevel.DEBUG, show_hierarchy: bool = True,
                 show_dependencies: bool = True):
        """
        Args:
            level: Уровень логирования
            show_hierarchy: Показывать иерархию классов
            show_dependencies: Показывать зависимости
        """
        super().__init__(level)
        self.show_hierarchy = show_hierarchy
        self.show_dependencies = show_dependencies

    def _get_call_type(self) -> str:
        return "relationship"

    def _before(self, func: Callable, args: tuple, kwargs: dict) -> None:
        """Логировать информацию о связях."""
        log_message(self.level, f"[🔗] {self.signature}", self.timestamp)

        self._log_arguments(func, args, kwargs)

        if args and hasattr(args[0], '__class__'):
            if self.show_hierarchy:
                self._log_hierarchy(args[0])
            if self.show_dependencies:
                self._log_dependencies(args[0])

    def _log_arguments(self, func: Callable, args: tuple, kwargs: dict) -> None:
        """Логировать типы аргументов."""
        try:
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for name, value in bound.arguments.items():
                if name == 'self':
                    continue

                value_type = type(value).__name__
                value_class = value.__class__.__name__ if hasattr(value, '__class__') else None

                msg = f"  • {name}: {value_type}"
                if value_class and value_class != value_type:
                    check = "✓" if value_type == value_class else "⚠"
                    msg += f" (экземпляр {value_class}) {check}"

                log_message(self.level, msg, self.timestamp)
        except Exception:
            pass  # Игнорируем ошибки при анализе сигнатуры

    def _log_hierarchy(self, instance: Any) -> None:
        """Логировать иерархию классов."""
        hierarchy = get_class_hierarchy(instance)

        if len(hierarchy) > 1:
            hierarchy_str = " -> ".join(hierarchy)
            log_message(self.level, f"  📊 Иерархия: {hierarchy_str}", self.timestamp)

    def _log_dependencies(self, instance: Any) -> None:
        """Логировать зависимости объекта."""
        deps = get_object_dependencies(instance)

        if deps:
            deps_str = ", ".join([f"{name}: {type_}" for name, type_ in deps.items()])
            log_message(self.level, f"  🔗 Зависимости: {deps_str}", self.timestamp)

    def _after(self, result: Any) -> None:
        """Логировать тип результата."""
        if result is None:
            return

        result_type = type(result).__name__
        result_class = result.__class__.__name__ if hasattr(result, '__class__') else None

        msg = f"  ↩️ Результат: {result_type}"
        if result_class and result_class != result_type:
            msg += f" (экземпляр {result_class})"

        log_message(self.level, msg, self.timestamp)


def log_class_relationship(level: str = LogLevel.DEBUG, show_hierarchy: bool = True,
                           show_dependencies: bool = True):
    """
    Декоратор для логирования связей между классами.

    Args:
        level: Уровень логирования
        show_hierarchy: Показывать иерархию классов
        show_dependencies: Показывать зависимости

    Example:
        @log_class_relationship(show_hierarchy=True)
        def process_move(self, board, position):
            pass
    """
    return RelationshipDecorator(level, show_hierarchy, show_dependencies)