# debug/decorators/base.py

"""
Базовый класс для декораторов логирования.
"""

from functools import wraps
from typing import Callable, Any, Optional
import traceback

from ..config import LogLevel
from ..utils import get_timestamp, format_signature, log_message
from ..filters import should_log


class LoggerDecorator:
    """
    Базовый класс для декораторов логирования.
    Реализует шаблонный метод для логирования вызовов.
    """

    def __init__(self, level: str = LogLevel.INFO, message: Optional[str] = None):
        """
        Args:
            level: Уровень логирования
            message: Пользовательское сообщение
        """
        self.level = level
        self.message = message
        self.timestamp = None
        self.signature = None
        self.func = None

    def __call__(self, func: Callable):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.timestamp = get_timestamp()
            self.signature = format_signature(func, args)

            if self._should_log():
                self._before(func, args, kwargs)

            try:
                result = func(*args, **kwargs)
                if self._should_log():
                    self._after(result)
                return result
            except Exception as e:
                self._error(e)
                raise

        return wrapper

    def _should_log(self) -> bool:
        """Проверить, нужно ли логировать."""
        return should_log(self.signature, self._get_call_type())

    def _get_call_type(self) -> str:
        """Получить тип вызова (для фильтрации)."""
        return "call"

    def _before(self, func: Callable, args: tuple, kwargs: dict) -> None:
        """Действия до вызова функции."""
        pass

    def _after(self, result: Any) -> None:
        """Действия после вызова функции."""
        pass

    def _error(self, error: Exception) -> None:
        """Действия при ошибке."""
        log_message(LogLevel.ERROR, f"[❌] {self.signature}: {error}", self.timestamp)
        log_message(LogLevel.DEBUG, traceback.format_exc(), self.timestamp)