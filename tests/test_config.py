# tests/test_config.py (исправленный)
"""
Тесты для модуля config.py.
"""

import pytest
from spion.config import (
    LogLevel, BaseColors, TrafficLight,
    configure, get_config, should_log
)


class TestLogLevel:
    """Тесты уровней логирования."""

    def test_levels_exist(self):
        """Проверяем, что все уровни определены."""
        assert LogLevel.DEBUG == "DEBUG"
        assert LogLevel.INFO == "INFO"
        assert LogLevel.WARNING == "WARNING"
        assert LogLevel.ERROR == "ERROR"
        assert LogLevel.CRITICAL == "CRITICAL"


class TestBaseColors:
    """Тесты базовых цветов."""

    def test_colors_are_strings(self):
        """Проверяем, что цвета - строки."""
        assert isinstance(BaseColors.RESET, str)
        assert isinstance(BaseColors.RED, str)
        assert BaseColors.RESET == '\033[0m'


class TestTrafficLight:
    """Тесты светофора."""

    def test_all_levels_present(self):
        """Проверяем, что все уровни есть в светофоре."""
        levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING,
                  LogLevel.ERROR, LogLevel.CRITICAL]

        for level in levels:
            assert level in TrafficLight

    def test_traffic_light_structure(self):
        """Проверяем структуру светофора."""
        for level, config in TrafficLight.items():
            assert 'color' in config
            assert 'emoji' in config
            assert 'name' in config
            assert isinstance(config['color'], str)
            assert isinstance(config['emoji'], str)
            assert isinstance(config['name'], str)


class TestConfigure:
    """Тесты функции configure."""

    # tests/test_config.py (исправленный)
    def test_configure_defaults(self):
        """Проверяем значения по умолчанию."""
        # Сбрасываем конфигурацию
        configure(
            enabled=True,
            min_level=LogLevel.DEBUG,
            show_timestamp=True,
            color_enabled=True
        )
        assert get_config('enabled') is True
        assert get_config('min_level') == LogLevel.DEBUG
        assert get_config('show_timestamp') is True

    def test_configure_custom_values(self):
        """Проверяем установку кастомных значений."""
        configure(
            enabled=False,
            min_level=LogLevel.ERROR,
            show_timestamp=False,
            color_enabled=False,
            timestamp_format="%H:%M"
        )

        assert get_config('enabled') is False
        assert get_config('min_level') == LogLevel.ERROR
        assert get_config('show_timestamp') is False
        assert get_config('color_enabled') is False
        assert get_config('timestamp_format') == "%H:%M"

    def test_get_config_default(self):
        """Проверяем get_config с default значением."""
        assert get_config('non_existent', 'default') == 'default'


class TestShouldLog:
    """Тесты функции should_log."""

    def test_logging_disabled(self):
        """Проверяем, что при отключенном логировании ничего не логируется."""
        configure(enabled=False)
        assert should_log(LogLevel.DEBUG) is False
        assert should_log(LogLevel.INFO) is False
        assert should_log(LogLevel.ERROR) is False

    def test_min_level_debug(self):
        """Проверяем фильтрацию при min_level=DEBUG."""
        configure(min_level=LogLevel.DEBUG)

        assert should_log(LogLevel.DEBUG) is True
        assert should_log(LogLevel.INFO) is True
        assert should_log(LogLevel.WARNING) is True
        assert should_log(LogLevel.ERROR) is True
        assert should_log(LogLevel.CRITICAL) is True

    def test_min_level_info(self):
        """Проверяем фильтрацию при min_level=INFO."""
        configure(min_level=LogLevel.INFO)

        assert should_log(LogLevel.DEBUG) is False
        assert should_log(LogLevel.INFO) is True
        assert should_log(LogLevel.WARNING) is True
        assert should_log(LogLevel.ERROR) is True
        assert should_log(LogLevel.CRITICAL) is True

    def test_min_level_warning(self):
        """Проверяем фильтрацию при min_level=WARNING."""
        configure(min_level=LogLevel.WARNING)

        assert should_log(LogLevel.DEBUG) is False
        assert should_log(LogLevel.INFO) is False
        assert should_log(LogLevel.WARNING) is True
        assert should_log(LogLevel.ERROR) is True
        assert should_log(LogLevel.CRITICAL) is True

    def test_min_level_error(self):
        """Проверяем фильтрацию при min_level=ERROR."""
        configure(min_level=LogLevel.ERROR)

        assert should_log(LogLevel.DEBUG) is False
        assert should_log(LogLevel.INFO) is False
        assert should_log(LogLevel.WARNING) is False
        assert should_log(LogLevel.ERROR) is True
        assert should_log(LogLevel.CRITICAL) is True

    def test_invalid_level(self):
        """Проверяем обработку невалидного уровня."""
        configure(min_level=LogLevel.DEBUG)
        assert should_log("INVALID_LEVEL") is True