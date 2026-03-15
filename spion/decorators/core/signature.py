# spion/decorators/core/signature.py

"""
Форматирование сигнатур функций.
"""

from typing import Callable, Any, Optional
import inspect


class SignatureFormatter:
    """
    Форматтер сигнатур функций.

    Отвечает за создание читаемых строковых представлений
    вызовов функций с аргументами.
    """

    def __init__(self, show_modules: bool = True, max_str_len: int = 50):
        """
        Инициализация форматтера.

        Args:
            show_modules: Показывать имена модулей
            max_str_len: Максимальная длина строковых значений
        """
        self.show_modules = show_modules
        self.max_str_len = max_str_len

    def format(self, func: Callable, args: tuple, kwargs: dict,
               show_types: bool = False) -> str:
        """
        Форматировать сигнатуру вызова.

        Args:
            func: Функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            show_types: Показывать типы аргументов

        Returns:
            str: Отформатированная сигнатура
        """
        parts = []

        # Имя функции
        if self.show_modules and hasattr(func, '__module__'):
            parts.append(func.__module__)
        parts.append(func.__qualname__ if hasattr(func, '__qualname__') else func.__name__)

        base_name = '.'.join(parts)

        # Добавляем информацию о типах если нужно
        if show_types:
            type_info = self._format_type_info(args, kwargs)
            if type_info:
                return f"{base_name}[{type_info}]"

        return base_name

    def format_with_args(self, func: Callable, args: tuple, kwargs: dict,
                         max_args: int = 5) -> str:
        """
        Форматировать сигнатуру с аргументами.

        Args:
            func: Функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            max_args: Максимальное количество аргументов для отображения

        Returns:
            str: Сигнатура с аргументами
        """
        base = self.format(func, args, kwargs, show_types=False)

        # Форматируем аргументы
        arg_strs = []

        # Позиционные аргументы (пропускаем self)
        start_idx = 1 if args and hasattr(args[0], '__class__') else 0
        for arg in args[start_idx:max_args + start_idx]:
            arg_strs.append(self._format_value(arg))

        if len(args) - start_idx > max_args:
            arg_strs.append('...')

        # Именованные аргументы
        for i, (k, v) in enumerate(kwargs.items()):
            if i >= max_args:
                arg_strs.append('...')
                break
            arg_strs.append(f"{k}={self._format_value(v)}")

        if arg_strs:
            return f"{base}({', '.join(arg_strs)})"
        return base

    def _format_type_info(self, args: tuple, kwargs: dict) -> str:
        """
        Форматировать информацию о типах.

        Args:
            args: Позиционные аргументы
            kwargs: Именованные аргументы

        Returns:
            str: Информация о типах
        """
        types = []

        # Типы позиционных аргументов
        for i, arg in enumerate(args):
            if i == 0 and hasattr(arg, '__class__'):
                continue  # Пропускаем self
            types.append(type(arg).__name__)

        # Типы именованных аргументов
        for k, v in kwargs.items():
            types.append(f"{k}:{type(v).__name__}")

        return ', '.join(types) if types else ''

    def _format_value(self, value: Any) -> str:
        """
        Форматировать значение для отображения.

        Args:
            value: Значение

        Returns:
            str: Отформатированное значение
        """
        # ИСПРАВЛЕНО: было from ...utils import format_value
        from .utils import format_value
        return format_value(value, max_len=self.max_str_len)
