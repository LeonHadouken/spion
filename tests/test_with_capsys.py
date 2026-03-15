# tests/test_with_capsys.py (исправленный)
"""
Тесты с использованием встроенной фикстуры capsys.
"""

import pytest
import sys
import os
import re

# Добавляем путь к корневой директории
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spion.config import configure, LogLevel
from spion.decorators.core.utils import log_message


def clean_ansi(text):
    """Удаляет ANSI коды из строки."""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


@pytest.fixture(autouse=True)
def setup_logging():
    """Настраиваем логирование для всех тестов."""
    configure(
        enabled=True,
        min_level=LogLevel.DEBUG,
        show_timestamp=False,
        color_enabled=False
    )
    yield


def test_log_message_basic(capsys):
    """Тест логирования с capsys."""
    log_message(LogLevel.INFO, "test message")
    captured = capsys.readouterr()
    cleaned = clean_ansi(captured.out)
    assert "test message" in cleaned


def test_log_message_without_timestamp(capsys):
    """Тест логирования без временной метки."""
    log_message(LogLevel.INFO, "no timestamp")
    captured = capsys.readouterr()
    cleaned = clean_ansi(captured.out)
    assert "no timestamp" in cleaned
    assert "[" not in cleaned


def test_log_message_disabled(capsys):
    """Тест отключенного логирования."""
    configure(enabled=False)
    log_message(LogLevel.INFO, "should not appear")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_log_decorator_basic(capsys):
    """Тест декоратора log с capsys."""
    from spion import log

    @log(level=LogLevel.INFO)
    def test_func():
        return 42

    result = test_func()
    assert result == 42

    captured = capsys.readouterr()
    cleaned = clean_ansi(captured.out)
    assert "▶️" in cleaned
    assert "test_func" in cleaned


def test_log_decorator_debug(capsys):
    """Тест декоратора log с уровнем DEBUG."""
    from spion import log

    @log(level=LogLevel.DEBUG)
    def test_func(x, y=10):
        return x + y

    result = test_func(5, y=3)
    assert result == 8

    captured = capsys.readouterr()
    cleaned = clean_ansi(captured.out)
    assert "▶️" in cleaned
    assert "с аргументами" in cleaned
    assert "◀️" in cleaned


def test_log_decorator_custom_message(capsys):
    """Тест декоратора log с кастомным сообщением."""
    from spion import log

    @log(level=LogLevel.INFO, message="Custom message")
    def test_func():
        return 42

    result = test_func()
    assert result == 42

    captured = capsys.readouterr()
    cleaned = clean_ansi(captured.out)
    assert "▶️ Custom message" in cleaned