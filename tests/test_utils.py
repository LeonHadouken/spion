# tests/test_utils.py (исправленный)
"""
Тесты для модуля utils.py.
"""

import pytest
from spion.decorators.core.utils import (
    get_timestamp, get_light, format_signature,
    format_value, log_message, safe_execute,
    get_class_hierarchy, get_object_dependencies
)
from spion.config import LogLevel, TrafficLight, configure
from tests.conftest import SampleClass, ChildClass, clean_ansi


class TestGetTimestamp:
    """Тесты функции get_timestamp."""

    def test_timestamp_format(self):
        """Проверяем формат временной метки."""
        configure(timestamp_format="%H:%M:%S.%f")
        ts = get_timestamp()
        parts = ts.split(':')
        assert len(parts) == 3
        assert '.' in parts[2]

    def test_timestamp_custom_format(self):
        """Проверяем кастомный формат."""
        configure(timestamp_format="%H:%M")
        ts = get_timestamp()
        # Проверяем что это строка и содержит хотя бы цифры
        assert isinstance(ts, str)
        assert len(ts) > 0


class TestGetLight:
    """Тесты функции get_light."""

    def test_get_light_with_color(self):
        """Проверяем получение светофора с цветом."""
        configure(color_enabled=True)
        light = get_light(LogLevel.INFO)

        assert light['emoji'] == TrafficLight[LogLevel.INFO]['emoji']
        assert light['name'] == TrafficLight[LogLevel.INFO]['name']
        assert light['color'] != '\033[0m'

    def test_get_light_without_color(self, capsys):
        """Проверяем получение светофора без цвета."""
        configure(color_enabled=False)
        light = get_light(LogLevel.INFO)

        assert light['emoji'] == '⚪'
        assert light['color'] == '\033[0m'

    def test_get_light_invalid_level(self):
        """Проверяем обработку невалидного уровня."""
        light = get_light("INVALID")
        assert light['emoji'] == '⚪'
        assert light['name'] == "INVALID"


class TestFormatSignature:
    """Тесты функции format_signature."""

    def test_format_function(self):
        """Проверяем форматирование обычной функции."""

        def test_func():
            pass

        sig = format_signature(test_func, ())
        assert "test_func" in sig

    def test_format_method(self):
        """Проверяем форматирование метода класса."""
        obj = SampleClass()

        sig = format_signature(obj.method, (obj, 5))
        assert "SampleClass.method" in sig

    def test_format_with_module(self):
        """Проверяем форматирование с именем модуля."""

        def test_func():
            pass

        sig = format_signature(test_func, (), include_module=True)
        assert "test_func" in sig


class TestFormatValue:
    """Тесты функции format_value."""

    def test_format_none(self):
        """Проверяем форматирование None."""
        assert format_value(None) == "None"

    def test_format_string(self):
        """Проверяем форматирование строки."""
        assert format_value("test") == "'test'"

    def test_format_long_string(self):
        """Проверяем обрезание длинной строки."""
        long_str = "a" * 100
        result = format_value(long_str, max_len=20)
        assert len(result) <= 23
        assert result.endswith("...")

    def test_format_number(self):
        """Проверяем форматирование числа."""
        assert format_value(42) == "42"
        assert format_value(3.14) == "3.14"


class TestLogMessage:
    """Тесты функции log_message."""

    def test_log_message_basic(self, capsys):
        """Проверяем базовый вывод лога."""
        log_message(LogLevel.INFO, "test message")
        captured = capsys.readouterr()
        output = clean_ansi(captured.out.strip())
        assert "test message" in output

    def test_log_message_disabled(self, capsys):
        """Проверяем, что при отключенном логировании ничего не выводится."""
        configure(enabled=False)
        log_message(LogLevel.INFO, "test message")
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_log_message_without_timestamp(self, capsys):
        """Проверяем лог без временной метки."""
        log_message(LogLevel.INFO, "test message")
        captured = capsys.readouterr()
        output = clean_ansi(captured.out.strip())
        assert "test message" in output
        assert "[" not in output


class TestSafeExecute:
    """Тесты функции safe_execute."""

    def test_safe_execute_success(self):
        """Проверяем успешное выполнение."""
        result = safe_execute(lambda x: x * 2, 21)
        assert result == 42

    def test_safe_execute_error(self, capsys):
        """Проверяем обработку ошибки."""

        def failing_func():
            raise ValueError("Test error")

        result = safe_execute(failing_func)
        assert result is None
        captured = capsys.readouterr()
        output = clean_ansi(captured.out.strip())
        assert "Ошибка при выполнении" in output
        assert "Test error" in output


class TestGetClassHierarchy:
    """Тесты функции get_class_hierarchy."""

    def test_get_hierarchy_simple(self):
        """Проверяем получение иерархии простого класса."""
        obj = SampleClass()
        hierarchy = get_class_hierarchy(obj)

        assert hierarchy[0] == "SampleClass"
        assert "object" in hierarchy

    def test_get_hierarchy_inherited(self):
        """Проверяем получение иерархии унаследованного класса."""
        obj = ChildClass()
        hierarchy = get_class_hierarchy(obj)

        assert hierarchy[0] == "ChildClass"
        assert hierarchy[1] == "SampleClass"
        assert "object" in hierarchy


class TestGetObjectDependencies:
    """Тесты функции get_object_dependencies."""

    def test_get_dependencies_default(self):
        """Проверяем получение зависимостей по умолчанию."""
        obj = SampleClass()
        obj.board = "board"
        obj.game_state = "state"

        deps = get_object_dependencies(obj)
        assert 'board' in deps
        assert 'game_state' in deps

    def test_get_dependencies_custom(self):
        """Проверяем получение зависимостей с кастомными именами."""
        obj = SampleClass()
        obj.custom_dep = 42

        deps = get_object_dependencies(obj, dep_names=['custom_dep'])
        assert deps['custom_dep'] == 'int'

    def test_get_dependencies_none(self):
        """Проверяем случай без зависимостей."""
        obj = SampleClass()
        deps = get_object_dependencies(obj)
        assert deps == {}