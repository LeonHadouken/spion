"""
Тесты для модуля filters.py.
"""

import pytest
import time
from debug.filters import (
    LogFilter, add_rule, should_log,
    get_suppression_summary, reset_filter,
    configure_filter
)


class TestLogFilter:
    """Тесты класса LogFilter."""

    def test_singleton(self):
        """Проверяем, что LogFilter - синглтон."""
        filter1 = LogFilter()
        filter2 = LogFilter()
        assert filter1 is filter2

    def test_should_log_basic(self):
        """Проверяем базовое логирование."""
        filter_obj = LogFilter()
        assert filter_obj.should_log("test_call", "call") is True

    def test_suppress_repetitive_default(self):
        """Проверяем подавление повторений по умолчанию."""
        filter_obj = LogFilter()
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
        add_rule("test_func", rule_type="call", max_calls=2)

        assert should_log("test_func_1", "call") is True
        assert should_log("test_func_2", "call") is True
        assert should_log("test_func_3", "call") is False

    def test_add_rule_log_once(self):
        """Проверяем правило log_once."""
        reset_filter()
        add_rule("once_func", rule_type="call", log_once=True)

        assert should_log("once_func_1", "call") is True
        assert should_log("once_func_2", "call") is False

    def test_add_rule_time_window(self):
        """Проверяем правило с временным окном."""
        reset_filter()
        add_rule("time_func", rule_type="call", max_calls=1, time_window=1)

        assert should_log("time_func_1", "call") is True
        # Второй вызов сразу - должен быть подавлен
        assert should_log("time_func_2", "call") is False

        # Ждем окончания временного окна
        time.sleep(1.1)
        assert should_log("time_func_3", "call") is True

    def test_rule_different_types(self):
        """Проверяем правила для разных типов вызовов."""
        reset_filter()
        add_rule("rel_func", rule_type="relationship", log_once=True)
        add_rule("chain_func", rule_type="chain", log_once=True)

        # Relationship
        assert should_log("rel_func_1", "relationship") is True
        assert should_log("rel_func_2", "relationship") is False

        # Chain
        assert should_log("chain_func_1", "chain") is True
        assert should_log("chain_func_2", "chain") is False

        # Call - не должен подавляться
        assert should_log("other_func", "call") is True


class TestRelationshipAndChainFilter:
    """Тесты фильтрации для relationship и chain."""

    def test_relationship_log_once_by_default(self):
        """Проверяем, что relationship логируется только один раз по умолчанию."""
        reset_filter()

        # Первый раз - логируем
        assert should_log("relationship_1", "relationship") is True
        # Второй раз - подавляем
        assert should_log("relationship_2", "relationship") is False

    def test_chain_log_once_by_default(self):
        """Проверяем, что chain логируется только один раз по умолчанию."""
        reset_filter()

        # Первый раз - логируем
        assert should_log("chain_1", "chain") is True
        # Второй раз - подавляем
        assert should_log("chain_2", "chain") is False

    def test_different_keys_different_filters(self):
        """Проверяем, что разные ключи независимы."""
        reset_filter()

        # Relationship для разных ключей
        assert should_log("rel_A", "relationship") is True
        assert should_log("rel_B", "relationship") is True
        assert should_log("rel_A", "relationship") is False
        assert should_log("rel_B", "relationship") is False


class TestSuppressionSummary:
    """Тесты сводки по подавленным вызовам."""

    def test_get_summary(self):
        """Проверяем получение сводки."""
        reset_filter()
        configure_filter(max_repetitions=2)

        # Делаем много вызовов
        for i in range(10):
            should_log(f"test_{i % 3}", "call")

        summary = get_suppression_summary()
        assert isinstance(summary, dict)

        # Должны быть ключи с количеством > max_repetitions
        for key, count in summary.items():
            assert count > 2

    def test_reset_clears_summary(self):
        """Проверяем, что reset очищает сводку."""
        reset_filter()

        for i in range(10):
            should_log("test", "call")

        assert len(get_suppression_summary()) > 0
        reset_filter()
        assert len(get_suppression_summary()) == 0


class TestConfigureFilter:
    """Тесты функции configure_filter."""

    def test_configure_filter(self):
        """Проверяем настройку фильтра."""
        filter_obj = LogFilter()

        configure_filter(
            suppress_repetitive=False,
            max_repetitions=10,
            show_suppression_summary=False
        )

        assert filter_obj.suppress_repetitive is False
        assert filter_obj.max_repetitions == 10
        assert filter_obj.show_suppression_summary is False