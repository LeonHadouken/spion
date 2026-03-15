# tests/test_context_manager.py
"""
Тесты для контекстного менеджера disable_logging.
"""

import pytest
from spion import configure, get_config, disable_logging, watch
from spion.decorators.core.filtering import should_log_call
from tests.conftest import clean_ansi


class TestDisableLogging:
    """Тесты для временного отключения логирования"""

    def test_disable_logging_context(self):
        """Проверяем, что внутри контекста логирование отключается"""
        # Включаем логирование
        configure(enabled=True)
        assert get_config('enabled') is True

        # Входим в контекст
        with disable_logging():
            assert get_config('enabled') is False

        # Выходим из контекста - должно восстановиться
        assert get_config('enabled') is True

    def test_disable_logging_nested(self):
        """Проверяем вложенные контексты"""
        configure(enabled=True)

        with disable_logging():
            assert get_config('enabled') is False

            with disable_logging():
                assert get_config('enabled') is False

            # После внутреннего контекста должно остаться False
            assert get_config('enabled') is False

        assert get_config('enabled') is True

    def test_disable_logging_with_error(self):
        """Проверяем, что контекст восстанавливается даже при ошибке"""
        configure(enabled=True)

        try:
            with disable_logging():
                assert get_config('enabled') is False
                raise ValueError("Тестовая ошибка")
        except ValueError:
            pass

        # Даже после ошибки конфигурация должна восстановиться
        assert get_config('enabled') is True

    def test_disable_logging_prevents_logging(self, capsys):
        """Проверяем, что внутри контекста действительно не логируется"""
        configure(enabled=True, show_timestamp=False, color_enabled=False)

        @watch()
        def test_func():
            return 42

        # Без контекста - логируется
        test_func()
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output

        # В контексте - не логируется
        with disable_logging():
            test_func()
            captured = capsys.readouterr()
            assert captured.out == ""

        # После контекста - снова логируется
        test_func()
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output

    def test_disable_logging_affects_should_log_call(self):
        """Проверяем, что should_log_call тоже реагирует на отключение"""
        configure(enabled=True)

        assert should_log_call("test", "call") is True

        with disable_logging():
            assert should_log_call("test", "call") is False

        assert should_log_call("test", "call") is True

    def test_disable_logging_restores_previous_config(self):
        """Проверяем, что восстанавливается именно предыдущая конфигурация"""
        # Разные настройки до контекста
        configure(enabled=True, show_timestamp=False, color_enabled=False)
        old_min_level = get_config('min_level')

        with disable_logging():
            # Меняем что-то внутри контекста
            configure(min_level="DEBUG")
            assert get_config('enabled') is False

        # После контекста должно восстановиться всё, включая min_level
        assert get_config('enabled') is True
        assert get_config('min_level') == old_min_level