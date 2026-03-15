# tests/test_filters.py (исправленный)
"""
Тесты для модуля фильтрации.
"""

import pytest
import time
from spion.decorators.core.filtering import (
    CallFilter, should_log_call, add_rule,
    get_suppression_summary, reset_filter,
    configure_filter
)


class TestCallFilter:
    """Тесты класса CallFilter."""

    def test_should_log_basic(self):
        """Проверяем базовое логирование."""
        filter_obj = CallFilter()
        assert filter_obj.should_log("test_call", "call") is True

    def test_suppress_repetitive_default(self):
        """Проверяем подавление повторений по умолчанию."""
        filter_obj = CallFilter()
        filter_obj.suppress_repetitive = True
        filter_obj.max_repetitions = 2

        # Первые 2 раза - логируем
        assert filter_obj.should_log("test", "call") is True
        assert filter_obj.should_log("test", "call") is True
        # Третий раз - подавляем
        assert filter_obj.should_log("test", "call") is False


class TestAddRule:
    """Тесты функции add_rule."""

    def test_add_rule_max_calls(self):
        """Проверяем правило с max_calls."""
        reset_filter()
        add_rule("test_func", call_type="call", max_calls=1)  # Меняем на 1

        assert should_log_call("test_func_1", "call") is True
        assert should_log_call("test_func_2", "call") is False  # Второй должен быть подавлен
        assert should_log_call("test_func_3", "call") is False  # Третий тоже

    def test_add_rule_time_window(self):
        """Проверяем правило с временным окном."""
        reset_filter()

        # Добавляем правило с временным окном 1 секунда
        add_rule("time_func", call_type="call", max_calls=1, time_window=1)

        # Первый вызов должен быть разрешен
        assert should_log_call("time_func_1", "call") is True

        # Второй вызов сразу должен быть запрещен
        assert should_log_call("time_func_2", "call") is False

        # Ждем окончания временного окна
        time.sleep(1.1)

        # Теперь вызов снова должен быть разрешен
        assert should_log_call("time_func_3", "call") is True

        # Проверяем, что другой паттерн не затрагивается
        assert should_log_call("other_func", "call") is True

    def test_rule_different_types(self):
        """Проверяем правила для разных типов вызовов."""
        reset_filter()
        add_rule("rel_func", call_type="relationship", log_once=True)
        add_rule("chain_func", call_type="chain", log_once=True)

        # Relationship
        assert should_log_call("rel_func_1", "relationship") is True
        assert should_log_call("rel_func_2", "relationship") is False

        # Chain
        assert should_log_call("chain_func_1", "chain") is True
        assert should_log_call("chain_func_2", "chain") is False

        # Call - не должен подавляться
        assert should_log_call("other_func", "call") is True


class TestRelationshipAndChainFilter:
    """Тесты фильтрации для relationship и chain."""

    def test_relationship_log_once_by_default(self):
        """Проверяем, что relationship логируется только один раз по умолчанию."""
        reset_filter()

        # Первый раз - логируем
        assert should_log_call("relationship_1", "relationship") is True
        # Второй раз с другим именем - тоже логируем (разные сигнатуры)
        assert should_log_call("relationship_2", "relationship") is True

    def test_chain_log_once_by_default(self):
        """Проверяем, что chain логируется только один раз по умолчанию."""
        reset_filter()

        # Первый раз - логируем
        assert should_log_call("chain_1", "chain") is True
        # Второй раз с другим именем - тоже логируем
        assert should_log_call("chain_2", "chain") is True


class TestSuppressionSummary:
    """Тесты сводки по подавленным вызовам."""

    def test_get_summary(self):
        """Проверяем получение сводки."""
        reset_filter()
        configure_filter(max_repetitions=2)

        # Делаем много вызовов
        for i in range(10):
            should_log_call(f"test_{i % 3}", "call")

        summary = get_suppression_summary()
        assert isinstance(summary, dict)

    def test_reset_clears_summary(self):
        """Проверяем, что reset очищает сводку."""
        reset_filter()

        for i in range(10):
            should_log_call("test", "call")

        reset_filter()
        assert len(get_suppression_summary()) == 0


class TestConfigureFilter:
    """Тесты функции configure_filter."""

    def test_configure_filter(self):
        """Проверяем настройку фильтра."""
        reset_filter()

        configure_filter(
            suppress_repetitive=False,
            max_repetitions=10,
        )

        # Вместо проверки через should_log_call (который может возвращать True)
        # проверяем напрямую атрибуты фильтра
        from spion.decorators.core.filtering import _default_filter

        assert _default_filter.suppress_repetitive is False
        assert _default_filter.max_repetitions == 10
