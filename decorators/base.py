# debug/decorators/base.py

"""
Базовый класс для декораторов логирования.
Реализует шаблонный метод для логирования вызовов с сохранением всех метаданных.
"""

from functools import wraps, update_wrapper
from typing import Callable, Any, Optional, Dict, Union
import traceback
import inspect
from datetime import datetime
import time

from ..config import LogLevel, get_config
from ..utils import get_timestamp, format_signature, log_message, format_value
from ..filters import should_log


class LoggerDecorator:
    """
    Базовый класс для декораторов логирования.

    Реализует шаблонный метод для логирования вызовов с возможностью
    расширения в дочерних классах. Сохраняет все метаданные оригинальной функции.

    Attributes:
        level (str): Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        message (Optional[str]): Пользовательское сообщение
        timestamp (Optional[str]): Временная метка вызова
        signature (Optional[str]): Сигнатура функции
        func (Optional[Callable]): Декорируемая функция
        call_count (int): Счётчик вызовов для этой функции
        total_time (float): Общее время выполнения
        last_call (float): Время последнего вызова

    Example:
        >>> class MyDecorator(LoggerDecorator):
        ...     def _before(self, func, args, kwargs):
        ...         log_message(self.level, f"Starting {func.__name__}")
        ...
        ...     def _after(self, result):
        ...         log_message(self.level, f"Finished with result: {result}")
    """

    def __init__(self, level: str = LogLevel.INFO, message: Optional[str] = None):
        """
        Инициализация базового декоратора.

        Args:
            level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Пользовательское сообщение для логирования

        Example:
            >>> @LoggerDecorator(level=LogLevel.DEBUG, message="Custom message")
            ... def test():
            ...     pass
        """
        self.level = level
        self.message = message
        self.timestamp = None
        self.signature = None
        self.func = None

        # Статистика вызовов
        self.call_count = 0
        self.total_time = 0.0
        self.last_call = 0.0
        self.errors = 0

        # Метаданные декоратора
        self.__name__ = self.__class__.__name__
        self.__doc__ = self.__class__.__doc__

    def __call__(self, func: Callable) -> Callable:
        """
        Декорирование функции с сохранением всех метаданных.

        Args:
            func: Декорируемая функция

        Returns:
            Callable: Обёрнутая функция с сохранёнными метаданными

        Note:
            Сохраняет:
            - __name__
            - __doc__
            - __annotations__
            - __module__
            - __qualname__
            - __dict__
            - __wrapped__ (ссылку на оригинальную функцию)
        """
        self.func = func
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__
        self.__annotations__ = getattr(func, '__annotations__', {})
        self.__dict__.update(getattr(func, '__dict__', {}))

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Сохраняем метаданные вызова
            call_time = time.time()
            self.last_call = call_time
            self.call_count += 1
            self.timestamp = get_timestamp()

            # Формируем сигнатуру с контекстом
            self.signature = self._get_signature(func, args, kwargs)

            # Дополнительный контекст для логирования
            call_context = self._get_call_context(args, kwargs)

            # Проверяем, нужно ли логировать
            if self._should_log():
                self._before(func, args, kwargs, call_context)

            try:
                # Замеряем время выполнения
                start_time = time.time() if self._should_measure_time() else 0

                # Выполняем функцию
                result = func(*args, **kwargs)

                # Считаем время
                if self._should_measure_time():
                    elapsed = time.time() - start_time
                    self.total_time += elapsed

                # Логируем результат
                if self._should_log():
                    self._after(result, call_context)

                return result

            except Exception as e:
                self.errors += 1
                self._error(e, call_context)
                raise

        # Дополнительно сохраняем метаданные (на всякий случай)
        wrapper.__logger_decorator__ = self
        wrapper.__wrapped__ = func
        wrapper.__original_func__ = func

        # Сохраняем информацию о декораторе
        wrapper.__decorator_name__ = self.__class__.__name__
        wrapper.__decorator_level__ = self.level

        return wrapper

    def _get_signature(self, func: Callable, args: tuple, kwargs: dict) -> str:
        """
        Получить расширенную сигнатуру функции.

        Args:
            func: Функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы

        Returns:
            str: Расширенная сигнатура с типами и значениями
        """
        base_sig = format_signature(func, args, include_module=True)

        # Добавляем информацию о типах для DEBUG режима
        if self.level == LogLevel.DEBUG and get_config('show_types', False):
            type_info = []

            # Типы позиционных аргументов
            for i, arg in enumerate(args):
                if i == 0 and hasattr(arg, '__class__'):
                    continue  # Пропускаем self
                type_info.append(f"{type(arg).__name__}")

            # Типы именованных аргументов
            for k, v in kwargs.items():
                type_info.append(f"{k}:{type(v).__name__}")

            if type_info:
                base_sig += f"[{', '.join(type_info)}]"

        return base_sig

    def _get_call_context(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """
        Получить контекст вызова (дополнительная информация).

        Args:
            args: Позиционные аргументы
            kwargs: Именованные аргументы

        Returns:
            Dict[str, Any]: Словарь с контекстом вызова
        """
        context = {
            'call_id': self.call_count,
            'timestamp': self.timestamp,
            'args_count': len(args),
            'kwargs_count': len(kwargs),
        }

        # Добавляем информацию о caller'е если доступно
        try:
            frame = inspect.currentframe()
            if frame and frame.f_back and frame.f_back.f_back:
                caller = frame.f_back.f_back
                context['caller'] = {
                    'function': caller.f_code.co_name,
                    'file': caller.f_code.co_filename,
                    'line': caller.f_lineno
                }
        except:
            pass

        return context

    def _should_log(self) -> bool:
        """
        Проверить, нужно ли логировать.

        Returns:
            bool: True если нужно логировать
        """
        # Проверяем через фильтр
        if not should_log(self.signature, self._get_call_type()):
            return False

        # Проверяем уровень логирования
        return True

    def _should_measure_time(self) -> bool:
        """
        Проверить, нужно ли замерять время выполнения.

        Returns:
            bool: True если нужно замерять время
        """
        return self.level in (LogLevel.DEBUG, LogLevel.INFO)

    def _get_call_type(self) -> str:
        """
        Получить тип вызова (для фильтрации).

        Returns:
            str: Тип вызова ("call", "relationship", "chain" и т.д.)
        """
        return "call"

    def _before(self, func: Callable, args: tuple, kwargs: dict,
                context: Dict[str, Any]) -> None:
        """
        Действия до вызова функции.

        Args:
            func: Декорируемая функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            context: Контекст вызова (call_id, timestamp и т.д.)

        Note:
            Переопределяется в дочерних классах
        """
        pass

    def _after(self, result: Any, context: Dict[str, Any]) -> None:
        """
        Действия после вызова функции.

        Args:
            result: Результат функции
            context: Контекст вызова

        Note:
            Переопределяется в дочерних классах
        """
        pass

    def _error(self, error: Exception, context: Dict[str, Any]) -> None:
        """
        Действия при ошибке.

        Args:
            error: Исключение
            context: Контекст вызова

        Note:
            По умолчанию логирует ошибку и стектрейс
        """
        log_message(
            LogLevel.ERROR,
            f"[❌] {self.signature}: {error} (call #{context['call_id']})",
            self.timestamp
        )

        if self.level == LogLevel.DEBUG:
            log_message(
                LogLevel.DEBUG,
                traceback.format_exc(),
                self.timestamp
            )

    # Дескрипторные методы для работы с классами
    def __get__(self, obj, objtype=None):
        """
        Поддержка дескрипторного протокола для методов классов.

        Позволяет правильно работать с методами классов,
        сохраняя связь с экземпляром.

        Args:
            obj: Экземпляр класса
            objtype: Тип класса

        Returns:
            Callable: Связанный метод или сам декоратор
        """
        if obj is None:
            return self

        # Создаём связанный метод
        from types import MethodType
        return MethodType(self.__call__, obj)

    def get_stats(self) -> Dict[str, Any]:
        """
        Получить статистику вызовов.

        Returns:
            Dict[str, Any]: Статистика:
                - call_count: количество вызовов
                - errors: количество ошибок
                - total_time: общее время выполнения
                - avg_time: среднее время выполнения
                - last_call: время последнего вызова
        """
        stats = {
            'call_count': self.call_count,
            'errors': self.errors,
            'total_time': self.total_time,
            'last_call': self.last_call,
        }

        if self.call_count > 0:
            stats['avg_time'] = self.total_time / self.call_count
        else:
            stats['avg_time'] = 0

        return stats

    def reset_stats(self) -> None:
        """Сбросить статистику вызовов."""
        self.call_count = 0
        self.total_time = 0.0
        self.last_call = 0.0
        self.errors = 0

    def __repr__(self) -> str:
        """Представление декоратора."""
        return (f"<{self.__class__.__name__}(level='{self.level}', "
                f"func={self.func.__name__ if self.func else 'None'})>")

    def __str__(self) -> str:
        """Строковое представление."""
        return f"{self.__class__.__name__}[{self.level}]"


# Вспомогательный класс для композиции декораторов
class DecoratorComposer:
    """
    Композитор декораторов для применения нескольких декораторов одновременно.

    Example:
        >>> combo = DecoratorComposer(log(), log_method_chain())
        >>> @combo
        ... def test():
        ...     pass
    """

    def __init__(self, *decorators):
        """
        Инициализация композитора.

        Args:
            *decorators: Декораторы для применения
        """
        self.decorators = decorators

    def __call__(self, func):
        """Применить все декораторы к функции."""
        for decorator in reversed(self.decorators):
            func = decorator(func)
        return func

    def __repr__(self):
        return f"DecoratorComposer({self.decorators})"


# Декоратор для добавления метаданных
def with_metadata(func: Callable) -> Callable:
    """
    Декоратор для добавления метаданных к функции.

    Args:
        func: Функция для декорирования

    Returns:
        Callable: Функция с дополнительными метаданными

    Example:
        >>> @with_metadata
        ... def test():
        ...     '''Docstring'''
        ...     pass
        >>> test.__metadata__['decorated_at']
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Добавляем метаданные
    wrapper.__metadata__ = {
        'decorated_at': datetime.now().isoformat(),
        'original_name': func.__name__,
        'original_module': func.__module__,
        'original_doc': func.__doc__,
    }

    return wrapper


# Контекстный менеджер для временного отключения логирования
class disable_logging:
    """
    Контекстный менеджер для временного отключения логирования.

    Example:
        >>> with disable_logging():
        ...     noisy_function()  # Не будет логироваться
    """

    def __enter__(self):
        self.old_config = get_config('enabled')
        from ..config import configure
        configure(enabled=False)
        return self

    def __exit__(self, *args):
        from ..config import configure
        configure(enabled=self.old_config)