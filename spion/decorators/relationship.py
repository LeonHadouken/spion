# spion/decorators/relationship.py (исправленный)
"""
Декоратор для логирования связей между классами.
"""

from typing import Callable, Any
import inspect

from ..config import LogLevel
from .base.decorator import LoggerDecorator
from .core.utils import log_message, get_class_hierarchy, get_object_dependencies


class RelationshipDecorator(LoggerDecorator):
    """
    Логирование связей между классами, иерархии и зависимостей.
    """

    def __init__(self, level: str = LogLevel.DEBUG,
                 show_hierarchy: bool = True,
                 show_dependencies: bool = True,
                 show_types: bool = True,
                 analyze_return: bool = True):
        """
        Инициализация декоратора отношений.
        """
        super().__init__(level)
        self.show_hierarchy = show_hierarchy
        self.show_dependencies = show_dependencies
        self.show_types = show_types
        self.analyze_return = analyze_return

    def _get_call_type(self) -> str:
        """Получить тип вызова для фильтрации."""
        return "relationship"

    def _before(self, func: Callable, args: tuple, kwargs: dict,
                context, signature: str) -> None:
        """
        Логировать информацию о связях до вызова функции.
        """
        log_message(self.level, f"[🔗] {signature}", context.timestamp_str)

        # Логируем типы аргументов
        if self.show_types:
            self._log_arguments(func, args, kwargs, context)

        # Анализируем первый аргумент (обычно self или основной объект)
        if args and hasattr(args[0], '__class__'):
            if self.show_hierarchy:
                self._log_hierarchy(args[0], context)
            if self.show_dependencies:
                self._log_dependencies(args[0], context)

        # Анализируем остальные объекты в аргументах
        self._analyze_object_arguments(args, kwargs, context)

    def _after(self, result: Any, context, signature: str) -> None:
        """
        Логировать тип результата.
        """
        if not self.analyze_return or result is None:
            return

        self._log_return_type(result, context)

    def _log_arguments(self, func: Callable, args: tuple, kwargs: dict, context) -> None:
        """
        Логировать типы аргументов с подробным анализом.
        """
        try:
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for name, value in bound.arguments.items():
                if name == 'self':
                    continue

                analysis = self._analyze_value(name, value)
                log_message(self.level, analysis, context.timestamp_str)

        except Exception as e:
            log_message(
                LogLevel.DEBUG,
                f"  ⚠ Ошибка анализа аргументов: {e}",
                context.timestamp_str
            )

    def _analyze_value(self, name: str, value: Any) -> str:
        """
        Анализировать значение и вернуть строку с информацией.
        """
        value_type = type(value).__name__
        value_class = value.__class__.__name__ if hasattr(value, '__class__') else None

        # Базовая информация
        msg = f"  • {name}: {value_type}"

        # Информация о классе (если отличается от типа)
        if value_class and value_class != value_type:
            check = "✓" if value_type == value_class else "⚠"
            msg += f" (экземпляр {value_class}) {check}"

        # Для коллекций показываем длину
        if hasattr(value, '__len__') and not isinstance(value, (str, bytes)):
            try:
                length = len(value)
                msg += f" [{length}]"
            except:
                pass

        # Для объектов показываем ID (в DEBUG режиме)
        if self.level == LogLevel.DEBUG and hasattr(value, '__class__'):
            msg += f" (id={id(value)})"

        return msg

    def _log_hierarchy(self, instance: Any, context) -> None:
        """
        Логировать иерархию классов объекта.
        """
        hierarchy = get_class_hierarchy(instance)

        if len(hierarchy) > 1:
            hierarchy_str = " -> ".join(hierarchy)
            log_message(
                self.level,
                f"  📊 Иерархия: {hierarchy_str}",
                context.timestamp_str
            )

    def _log_dependencies(self, instance: Any, context) -> None:
        """
        Логировать зависимости объекта.
        """
        deps = get_object_dependencies(instance)

        if deps:
            deps_str = ", ".join([f"{name}: {type_}" for name, type_ in deps.items()])
            log_message(
                self.level,
                f"  🔗 Зависимости: {deps_str}",
                context.timestamp_str
            )

    def _analyze_object_arguments(self, args: tuple, kwargs: dict, context) -> None:
        """
        Анализировать объекты в аргументах на предмет зависимостей.
        """
        if not self.show_dependencies:
            return

        # Анализируем все аргументы-объекты
        for i, arg in enumerate(args[1:], 1):  # пропускаем self
            if hasattr(arg, '__class__') and not isinstance(arg, (str, int, float, bool)):
                deps = get_object_dependencies(arg)
                if deps:
                    deps_str = ", ".join([f"{name}: {type_}" for name, type_ in deps.items()])
                    log_message(
                        self.level,
                        f"  🔗 Аргумент[{i}] зависимости: {deps_str}",
                        context.timestamp_str
                    )

        for name, value in kwargs.items():
            if hasattr(value, '__class__') and not isinstance(value, (str, int, float, bool)):
                deps = get_object_dependencies(value)
                if deps:
                    deps_str = ", ".join([f"{name}: {type_}" for name, type_ in deps.items()])
                    log_message(
                        self.level,
                        f"  🔗 {name} зависимости: {deps_str}",
                        context.timestamp_str
                    )

    def _log_return_type(self, result: Any, context) -> None:
        """
        Логировать тип возвращаемого значения.
        """
        result_type = type(result).__name__
        result_class = result.__class__.__name__ if hasattr(result, '__class__') else None

        msg = f"  ↩️ Результат: {result_type}"
        if result_class and result_class != result_type:
            msg += f" (экземпляр {result_class})"

        # Для коллекций показываем длину
        if hasattr(result, '__len__') and not isinstance(result, (str, bytes)):
            try:
                length = len(result)
                msg += f" [{length}]"
            except:
                pass

        log_message(self.level, msg, context.timestamp_str)


def log_class_relationship(level: str = LogLevel.DEBUG,
                           show_hierarchy: bool = True,
                           show_dependencies: bool = True,
                           show_types: bool = True,
                           analyze_return: bool = True):
    """
    Декоратор для логирования связей между классами.
    """
    return RelationshipDecorator(
        level,
        show_hierarchy,
        show_dependencies,
        show_types,
        analyze_return
    )


def dig(level: str = LogLevel.DEBUG,
        show_hierarchy: bool = True,
        show_dependencies: bool = True,
        show_types: bool = True,
        analyze_return: bool = True):
    """
    🔍 Копнуть глубже — проанализировать иерархию и связи объекта.

    Пример:
        @dig()
        def analyze(obj):
            pass

        @dig(show_hierarchy=False, show_dependencies=True)
        def check_deps(obj):
            pass
    """
    return RelationshipDecorator(
        level,
        show_hierarchy,
        show_dependencies,
        show_types,
        analyze_return
    )

spy = log_class_relationship