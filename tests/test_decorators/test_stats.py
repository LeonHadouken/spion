# tests/test_decorators/test_stats.py
"""
Тесты для модуля stats.py.
"""

import pytest
import time
from spion.decorators.core.stats import CallStats


class TestCallStats:
    """Тесты для класса CallStats."""

    def test_initial_state(self):
        """Проверяем начальное состояние."""
        stats = CallStats()
        assert stats.call_count == 0
        assert stats.errors == 0
        assert stats.total_time == 0.0
        assert stats.last_call == 0.0
        assert stats.avg_time == 0.0

    def test_record_call(self):
        """Проверяем запись вызова."""
        stats = CallStats()
        now = time.time()

        stats.record_call(now)

        assert stats.call_count == 1
        assert stats.last_call == now

    def test_record_multiple_calls(self):
        """Проверяем запись нескольких вызовов."""
        stats = CallStats()

        for i in range(5):
            stats.record_call(time.time() + i)

        assert stats.call_count == 5

    def test_record_time(self):
        """Проверяем запись времени выполнения."""
        stats = CallStats()

        stats.record_time(0.1)
        stats.record_time(0.2)

        # Используем round для сравнения с плавающей точкой
        assert round(stats.total_time, 1) == 0.3

    def test_record_error(self):
        """Проверяем запись ошибок."""
        stats = CallStats()

        stats.record_error()
        stats.record_error()

        assert stats.errors == 2

    def test_avg_time_calculation(self):
        """Проверяем расчет среднего времени."""
        stats = CallStats()

        # Записываем вызовы
        stats.record_call(time.time())
        stats.record_call(time.time())

        # Записываем время
        stats.record_time(0.1)
        stats.record_time(0.3)

        assert stats.avg_time == 0.2  # (0.1 + 0.3) / 2

    def test_avg_time_no_calls(self):
        """Проверяем avg_time при нуле вызовов."""
        stats = CallStats()
        assert stats.avg_time == 0.0

    def test_reset(self):
        """Проверяем сброс статистики."""
        stats = CallStats()

        stats.record_call(time.time())
        stats.record_time(0.1)
        stats.record_error()

        stats.reset()

        assert stats.call_count == 0
        assert stats.errors == 0
        assert stats.total_time == 0.0
        assert stats.last_call == 0.0

    def test_to_dict(self):
        """Проверяем преобразование в словарь."""
        stats = CallStats()
        now = time.time()

        stats.record_call(now)
        stats.record_time(0.123)
        stats.record_error()

        data = stats.to_dict()

        assert data['call_count'] == 1
        assert data['errors'] == 1
        assert data['total_time'] == 0.123
        assert data['avg_time'] == 0.123
        assert data['last_call'] == now

    def test_complex_scenario(self):
        """Проверяем сложный сценарий."""
        stats = CallStats()

        # Симулируем 10 вызовов с разным временем
        for i in range(10):
            stats.record_call(time.time() + i)
            stats.record_time(i * 0.01)

            if i % 3 == 0:  # Каждый третий с ошибкой
                stats.record_error()

        assert stats.call_count == 10
        assert stats.errors == 4  # 0, 3, 6, 9
        assert round(stats.avg_time, 3) == 0.045  # (0 + 0.01 + ... + 0.09) / 10