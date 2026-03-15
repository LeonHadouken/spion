# spion/decorators/core/context.py

"""
Контекст вызова функции.
"""

from typing import Any, Dict, Optional, Callable
from datetime import datetime
import inspect


class CallContext:
    """
    Контекст вызова функции.

    Содержит всю информацию о конкретном вызове:
    - Аргументы
    - Временная метка
    - ID вызова
    - Информация о caller'е

    Attributes:
        call_id (int): ID вызова
        timestamp (datetime): Временная метка
        args (tuple): Позиционные аргументы
        kwargs (dict): Именованные аргументы
        caller_info (Optional[Dict]): Информация о caller'е
    """

    def __init__(self, call_id: int, timestamp: datetime,
                 args: tuple, kwargs: dict,
                 caller_info: Optional[Dict] = None):
        self.call_id = call_id
        self.timestamp = timestamp
        self.args = args
        self.kwargs = kwargs
        self.caller_info = caller_info

    @property
    def timestamp_str(self) -> str:
        """Временная метка в формате строки."""
        return self.timestamp.strftime('%H:%M:%S.%f')[:-3]

    @classmethod
    def create(cls, func: Callable, args: tuple, kwargs: dict,
               call_id: int, timestamp: datetime) -> 'CallContext':
        """
        Создать контекст вызова.

        Args:
            func: Вызываемая функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            call_id: ID вызова
            timestamp: Временная метка

        Returns:
            CallContext: Контекст вызова
        """
        caller_info = cls._get_caller_info()
        return cls(call_id, timestamp, args, kwargs, caller_info)

    @staticmethod
    def _get_caller_info() -> Optional[Dict[str, Any]]:
        """
        Получить информацию о caller'е.

        Returns:
            Optional[Dict]: Информация о caller'е или None
        """
        try:
            frame = inspect.currentframe()
            if frame and frame.f_back and frame.f_back.f_back:
                caller = frame.f_back.f_back
                return {
                    'function': caller.f_code.co_name,
                    'file': caller.f_code.co_filename,
                    'line': caller.f_lineno
                }
        except:
            pass
        return None

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать контекст в словарь.

        Returns:
            Dict[str, Any]: Словарь с данными контекста
        """
        return {
            'call_id': self.call_id,
            'timestamp': self.timestamp.isoformat(),
            'args_count': len(self.args),
            'kwargs_count': len(self.kwargs),
            'caller': self.caller_info
        }