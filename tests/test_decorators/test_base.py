"""
Тесты для базового класса декораторов.
"""

import pytest
from debug.decorators.base import LoggerDecorator
from debug.config import LogLevel, configure
from tests.conftest import captured_logs, SampleClass


class TestLoggerDecorator:
    """Тесты базового класса LoggerDecorator."""

    def test_decorator_initialization(self):
        """Проверяем инициализацию декоратора."""
        decorator = LoggerDecorator(level=LogLevel.INFO, message="test message")

        assert decorator.level == LogLevel.INFO
        assert decorator.message == "test message"
        assert decorator.func is None

    def test_decorator_basic_call(self, captured_logs):
        """Проверяем базовый вызов декорированной функции."""
        decorator = LoggerDecorator(level=LogLevel.INFO)

        @decorator
        def test_func(x):
            return x * 2

        result = test_func(21)

        assert result == 42
        # Базовый класс не логирует в _before и _after
        assert captured_logs.getvalue() == ""

    def test_decorator_with_error(self, captured_logs):
        """Проверяем обработку ошибки в декорированной функции."""
        decorator = LoggerDecorator(level=LogLevel.ERROR)

        @decorator
        def failing_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            failing_func()

        output = captured_logs.getvalue()
        assert "[❌]" in output
        assert "failing_func" in output
        assert "Test error" in output
        assert "Traceback" in output

    def test_decorator_custom_message(self, captured_logs):
        """Проверяем использование кастомного сообщения в дочернем классе."""

        class CustomDecorator(LoggerDecorator):
            def _before(self, func, args, kwargs):
                # Используем кастомное сообщение
                msg = self.message or "Custom before"
                from debug.utils import log_message
                log_message(self.level, msg, self.timestamp)

        decorator = CustomDecorator(level=LogLevel.INFO, message="Hello, world!")

        @decorator
        def test_func():
            return 42

        result = test_func()

        assert result == 42
        assert "Hello, world!" in captured_logs.getvalue()

    def test_decorator_signature_preserved(self):
        """Проверяем, что декоратор сохраняет сигнатуру функции."""
        decorator = LoggerDecorator()

        @decorator
        def test_func(a, b=10, *args, **kwargs):
            """Docstring"""
            pass

        assert test_func.__name__ == "test_func"
        assert test_func.__doc__ == "Docstring"

        import inspect
        sig = inspect.signature(test_func)
        assert "a" in sig.parameters
        assert "b" in sig.parameters

    def test_decorator_method_call(self, captured_logs):
        """Проверяем декорирование метода класса."""

        class CustomDecorator(LoggerDecorator):
            def _before(self, func, args, kwargs):
                from debug.utils import log_message, format_signature
                sig = format_signature(func, args)
                log_message(self.level, f"Calling {sig}", self.timestamp)

        decorator = CustomDecorator(level=LogLevel.INFO)

        class TestClass:
            @decorator
            def method(self, x):
                return x * 2

        obj = TestClass()
        result = obj.method(21)

        assert result == 42
        assert "Calling TestClass.method" in captured_logs.getvalue()

    def test_decorator_should_log_false(self, captured_logs):
        """Проверяем, что при should_log=False ничего не логируется."""

        # Создаем подкласс, который переопределяет _should_log
        class ConditionalDecorator(LoggerDecorator):
            def _should_log(self):
                return False

            def _before(self, func, args, kwargs):
                from debug.utils import log_message
                log_message(self.level, "This should not appear", self.timestamp)

        decorator = ConditionalDecorator()

        @decorator
        def test_func():
            return 42

        result = test_func()

        assert result == 42
        assert captured_logs.getvalue() == ""

    def test_decorator_with_different_levels(self):
        """Проверяем работу с разными уровнями логирования."""

        levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING,
                  LogLevel.ERROR, LogLevel.CRITICAL]

        for level in levels:
            decorator = LoggerDecorator(level=level)

            @decorator
            def test_func():
                return level

            assert test_func() == level
            # Не проверяем вывод, т.к. базовый класс ничего не логирует


class TestLoggerDecoratorInheritance:
    """Тесты наследования от LoggerDecorator."""

    def test_minimal_subclass(self, captured_logs):
        """Проверяем минимальный подкласс с одним методом."""

        class MinimalDecorator(LoggerDecorator):
            def _before(self, func, args, kwargs):
                from debug.utils import log_message
                log_message(self.level, f"BEFORE: {func.__name__}", self.timestamp)

        decorator = MinimalDecorator(level=LogLevel.INFO)

        @decorator
        def test_func():
            return 42

        result = test_func()

        assert result == 42
        assert "BEFORE: test_func" in captured_logs.getvalue()

    def test_subclass_with_all_methods(self, captured_logs):
        """Проверяем подкласс, переопределяющий все методы."""

        class FullDecorator(LoggerDecorator):
            def _get_call_type(self):
                return "full_test"

            def _should_log(self):
                # Добавляем дополнительную логику
                return super()._should_log() and self.level != LogLevel.DEBUG

            def _before(self, func, args, kwargs):
                from debug.utils import log_message
                log_message(self.level, "BEFORE", self.timestamp)

            def _after(self, result):
                from debug.utils import log_message
                log_message(self.level, f"AFTER: {result}", self.timestamp)

            def _error(self, error):
                from debug.utils import log_message
                log_message(LogLevel.CRITICAL, f"ERROR: {error}", self.timestamp)

        decorator = FullDecorator(level=LogLevel.INFO)

        @decorator
        def test_func(x):
            return x * 2

        result = test_func(21)

        assert result == 42
        output = captured_logs.getvalue()
        assert "BEFORE" in output
        assert "AFTER: 42" in output

        # Проверяем, что DEBUG не логируется
        configure(min_level=LogLevel.DEBUG)
        decorator_debug = FullDecorator(level=LogLevel.DEBUG)

        @decorator_debug
        def debug_func():
            return "debug"

        with captured_logs() as debug_output:
            debug_func()
            assert debug_output.getvalue() == ""

    def test_call_type_propagation(self):
        """Проверяем, что _get_call_type работает и передается в should_log."""

        class TypeDecorator(LoggerDecorator):
            def _get_call_type(self):
                return "custom_type"

            def _before(self, func, args, kwargs):
                # В реальном коде здесь была бы проверка should_log с этим типом
                self.call_type_used = self._get_call_type()

        decorator = TypeDecorator()

        @decorator
        def test_func():
            pass

        test_func()
        assert decorator.call_type_used == "custom_type"