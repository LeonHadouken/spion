# spion/decorators/core/stats.py

"""
Статистика вызовов функций.
"""

from typing import Dict, Any
import time


class CallStats:
    """
    Статистика вызовов функции.

    Attributes:
        call_count (int): Количество вызовов
        errors (int): Количество ошибок
        total_time (float): Общее время выполнения
        last_call (float): Время последнего вызова
    """

    def __init__(self):
        self.call_count = 0
        self.errors = 0
        self.total_time = 0.0
        self.last_call = 0.0

    def record_call(self, call_time: float) -> None:
        """
        Записать вызов.

        Args:
            call_time: Время вызова
        """
        self.call_count += 1
        self.last_call = call_time

    def record_time(self, elapsed: float) -> None:
        """
        Записать время выполнения.

        Args:
            elapsed: Затраченное время
        """
        self.total_time += elapsed

    def record_error(self) -> None:
        """Записать ошибку."""
        self.errors += 1

    def reset(self) -> None:
        """Сбросить статистику."""
        self.call_count = 0
        self.errors = 0
        self.total_time = 0.0
        self.last_call = 0.0

    @property
    def avg_time(self) -> float:
        """Среднее время выполнения."""
        if self.call_count > 0:
            return self.total_time / self.call_count
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """
        Получить статистику в виде словаря.

        Returns:
            Dict[str, Any]: Статистика
        """
        return {
            'call_count': self.call_count,
            'errors': self.errors,
            'total_time': self.total_time,
            'avg_time': self.avg_time,
            'last_call': self.last_call,
        }