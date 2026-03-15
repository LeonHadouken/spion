# spion/decorators/base/decorator.py (ИСПРАВЛЕННАЯ - без дубликатов)
"""
Базовый класс для декораторов логирования.
"""

from functools import wraps
from typing import Callable, Any, Optional, Dict
from datetime import datetime
import time

from ...config import LogLevel
from ..core.stats import CallStats
from ..core.signature import SignatureFormatter
from ..core.context import CallContext
from ..core.filtering import should_log_call
from ..core.utils import log_message, get_exception_traceback


class LoggerDecorator:
    """
    Базовый класс для декораторов логирования.
    """

    def __init__(self, level: str = LogLevel.INFO, message: Optional[str] = None):
        """
        Инициализация базового декоратора.
        """
        self.level = level
        self.message = message
        self.func = None

        # Компоненты
        self.stats = CallStats()
        self.signature_formatter = SignatureFormatter()
        self.current_context = None

        # Метаданные
        self.__name__ = self.__class__.__name__
        self.__doc__ = self.__class__.__doc__

    def __call__(self, func: Callable) -> Callable:
        """
        Декорирование функции с сохранением всех метаданных.
        """
        self.func = func
        self._copy_function_metadata(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Обновляем статистику
            call_time = time.time()
            self.stats.record_call(call_time)

            # Создаём контекст вызова
            context = CallContext.create(
                func=func,
                args=args,
                kwargs=kwargs,
                call_id=self.stats.call_count,
                timestamp=datetime.now()
            )
            self.current_context = context

            # Форматируем сигнатуру
            signature = self.signature_formatter.format(
                func, args, kwargs,
                show_types=(self.level == LogLevel.DEBUG)
            )

            # Проверяем, нужно ли логировать
            if self._should_log(context, signature):
                self._before(func, args, kwargs, context, signature)

            try:
                # Замеряем время выполнения
                start_time = time.time() if self._should_measure_time() else 0

                # Выполняем функцию
                result = func(*args, **kwargs)

                # Обновляем статистику времени
                if self._should_measure_time():
                    elapsed = time.time() - start_time
                    self.stats.record_time(elapsed)

                # Логируем результат
                if self._should_log(context, signature):
                    self._after(result, context, signature)

                return result

            except Exception as e:
                self.stats.record_error()
                self._error(e, context, signature)
                raise

            finally:
                self.current_context = None

        # Сохраняем дополнительные метаданные
        wrapper.__logger_decorator__ = self
        wrapper.__wrapped__ = func
        wrapper.__decorator_name__ = self.__class__.__name__
        wrapper.__decorator_level__ = self.level

        return wrapper

    def _copy_function_metadata(self, func: Callable) -> None:
        """Копирует метаданные функции в декоратор."""
        self.__name__ = getattr(func, '__name__', self.__name__)
        self.__module__ = getattr(func, '__module__', self.__module__)
        self.__doc__ = getattr(func, '__doc__', self.__doc__)
        self.__annotations__ = getattr(func, '__annotations__', {})
        if hasattr(func, '__dict__'):
            self.__dict__.update(func.__dict__)

    def _should_log(self, context: CallContext, signature: str) -> bool:
        """
        Проверить, нужно ли логировать.
        """
        from ..core.filtering import should_log_call
        return should_log_call(signature, self._get_call_type())

    def _should_measure_time(self) -> bool:
        """Проверить, нужно ли замерять время выполнения."""
        return self.level in (LogLevel.DEBUG, LogLevel.INFO)

    def _get_call_type(self) -> str:
        """Получить тип вызова для фильтрации."""
        return "call"

    def _before(self, func: Callable, args: tuple, kwargs: dict,
                context: CallContext, signature: str) -> None:
        """
        Действия до вызова функции.
        Переопределяется в дочерних классах.
        """
        pass

    def _after(self, result: Any, context: CallContext, signature: str) -> None:
        """
        Действия после вызова функции.
        Переопределяется в дочерних классах.
        """
        pass

    def _error(self, error: Exception, context: CallContext, signature: str) -> None:
        """
        Действия при ошибке.
        """
        log_message(
            LogLevel.ERROR,
            f"[❌] {signature}: {error} (call #{context.call_id})",
            context.timestamp_str
        )

        if self.level == LogLevel.DEBUG:
            log_message(
                LogLevel.DEBUG,
                get_exception_traceback(),
                context.timestamp_str
            )

    # Дескрипторные методы
    def __get__(self, obj, objtype=None):
        """Поддержка дескрипторного протокола для методов классов."""
        if obj is None:
            return self
        from types import MethodType
        return MethodType(self.__call__, obj)

    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику вызовов."""
        return self.stats.to_dict()

    def reset_stats(self) -> None:
        """Сбросить статистику вызовов."""
        self.stats.reset()

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__}(level='{self.level}', "
                f"func={getattr(self.func, '__name__', 'None')})>")

