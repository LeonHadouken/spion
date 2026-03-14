# debug/decorators/relationship.py

"""
Декоратор для логирования связей между классами.
Анализирует иерархию классов, зависимости и типы аргументов.
"""

from typing import Callable, Any, Dict, Optional, List
import inspect

from debug.config import LogLevel
from debug.decorators.base import LoggerDecorator
from debug.utils import log_message, get_class_hierarchy, get_object_dependencies


class RelationshipDecorator(LoggerDecorator):
    """
    Логирование связей между классами, иерархии и зависимостей.

    Анализирует:
    - Типы аргументов и их соответствие ожидаемым типам
    - Иерархию наследования классов
    - Зависимости объектов (композиция/агрегация)

    Attributes:
        show_hierarchy (bool): Показывать иерархию классов
        show_dependencies (bool): Показывать зависимости
        show_types (bool): Показывать типы аргументов
        analyze_return (bool): Анализировать тип возвращаемого значения

    Example:
        >>> @RelationshipDecorator(show_hierarchy=True, show_dependencies=True)
        ... def process_user(user, db):
        ...     return user.save(db)
    """

    def __init__(self, level: str = LogLevel.DEBUG,
                 show_hierarchy: bool = True,
                 show_dependencies: bool = True,
                 show_types: bool = True,
                 analyze_return: bool = True):
        """
        Инициализация декоратора отношений.

        Args:
            level: Уровень логирования
            show_hierarchy: Показывать иерархию классов
            show_dependencies: Показывать зависимости объектов
            show_types: Показывать типы аргументов
            analyze_return: Анализировать тип возвращаемого значения

        Example:
            >>> @RelationshipDecorator(show_hierarchy=True, show_dependencies=False)
            ... def analyze(obj):
            ...     return obj.value
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
                context: Dict[str, Any]) -> None:
        """
        Логировать информацию о связях до вызова функции.

        Args:
            func: Декорируемая функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            context: Контекст вызова
        """
        log_message(self.level, f"[🔗] {self.signature}", self.timestamp)

        # Логируем типы аргументов
        if self.show_types:
            self._log_arguments(func, args, kwargs)

        # Анализируем первый аргумент (обычно self или основной объект)
        if args and hasattr(args[0], '__class__'):
            if self.show_hierarchy:
                self._log_hierarchy(args[0])
            if self.show_dependencies:
                self._log_dependencies(args[0])

        # Анализируем остальные объекты в аргументах
        self._analyze_object_arguments(func, args, kwargs)

    def _after(self, result: Any, context: Dict[str, Any]) -> None:
        """
        Логировать тип результата.

        Args:
            result: Результат функции
            context: Контекст вызова
        """
        if not self.analyze_return or result is None:
            return

        self._log_return_type(result)

    def _log_arguments(self, func: Callable, args: tuple, kwargs: dict) -> None:
        """
        Логировать типы аргументов с подробным анализом.

        Args:
            func: Функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
        """
        try:
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for name, value in bound.arguments.items():
                if name == 'self':
                    continue

                analysis = self._analyze_value(name, value)
                log_message(self.level, analysis, self.timestamp)

        except Exception as e:
            log_message(
                LogLevel.DEBUG,
                f"  ⚠ Ошибка анализа аргументов: {e}",
                self.timestamp
            )

    def _analyze_value(self, name: str, value: Any) -> str:
        """
        Анализировать значение и вернуть строку с информацией.

        Args:
            name: Имя аргумента
            value: Значение

        Returns:
            str: Отформатированная информация
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

    def _log_hierarchy(self, instance: Any) -> None:
        """
        Логировать иерархию классов объекта.

        Args:
            instance: Объект для анализа
        """
        hierarchy = get_class_hierarchy(instance)

        if len(hierarchy) > 1:
            hierarchy_str = " -> ".join(hierarchy)
            log_message(
                self.level,
                f"  📊 Иерархия: {hierarchy_str}",
                self.timestamp
            )

    def _log_dependencies(self, instance: Any) -> None:
        """
        Логировать зависимости объекта.

        Args:
            instance: Объект для анализа
        """
        deps = get_object_dependencies(instance)

        if deps:
            deps_str = ", ".join([f"{name}: {type_}" for name, type_ in deps.items()])
            log_message(
                self.level,
                f"  🔗 Зависимости: {deps_str}",
                self.timestamp
            )

    def _analyze_object_arguments(self, func: Callable, args: tuple,
                                  kwargs: dict) -> None:
        """
        Анализировать объекты в аргументах на предмет зависимостей.

        Args:
            func: Функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
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
                        self.timestamp
                    )

        for name, value in kwargs.items():
            if hasattr(value, '__class__') and not isinstance(value, (str, int, float, bool)):
                deps = get_object_dependencies(value)
                if deps:
                    deps_str = ", ".join([f"{name}: {type_}" for name, type_ in deps.items()])
                    log_message(
                        self.level,
                        f"  🔗 {name} зависимости: {deps_str}",
                        self.timestamp
                    )

    def _log_return_type(self, result: Any) -> None:
        """
        Логировать тип возвращаемого значения.

        Args:
            result: Результат функции
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

        log_message(self.level, msg, self.timestamp)


def log_class_relationship(level: str = LogLevel.DEBUG,
                           show_hierarchy: bool = True,
                           show_dependencies: bool = True,
                           show_types: bool = True,
                           analyze_return: bool = True):
    """
    Декоратор для логирования связей между классами.

    Анализирует иерархию классов, зависимости и типы аргументов.
    Помогает понять структуру кода и отношения между объектами.

    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        show_hierarchy: Показывать иерархию классов
        show_dependencies: Показывать зависимости объектов
        show_types: Показывать типы аргументов
        analyze_return: Анализировать тип возвращаемого значения

    Returns:
        Callable: Декорированная функция

    Example:
        >>> class User:
        ...     def __init__(self):
        ...         self.db = Database()
        ...         self.cache = Cache()
        ...
        >>> @log_class_relationship(show_hierarchy=True, show_dependencies=True)
        ... def save_user(user, validate=True):
        ...     user.db.save(user)
        ...     return True
        ...
        >>> save_user(User())
        [14:30:25.123] 🔵 [🔗] save_user
          • user: User (экземпляр User) ✓
          • validate: bool
          📊 Иерархия: User -> object
          🔗 Зависимости: db: Database, cache: Cache
          ↩️ Результат: bool

        >>> @log_class_relationship(show_hierarchy=False, show_types=False)
        ... def simple_func(x):
        ...     return x * 2
    """
    return RelationshipDecorator(
        level,
        show_hierarchy,
        show_dependencies,
        show_types,
        analyze_return
    )