"""
Фикстуры для тестов spion.
"""

import pytest
from io import StringIO
import sys
from contextlib import contextmanager
from typing import Generator, List

from debug.config import configure, LogLevel
from debug.filters import reset_filter
from debug.utils import log_message


@pytest.fixture(autouse=True)
def reset_logging_config():
    """Сбрасываем конфигурацию логирования перед каждым тестом."""
    configure(
        enabled=True,
        min_level=LogLevel.DEBUG,
        show_timestamp=False,
        color_enabled=False
    )
    reset_filter()
    yield


@contextmanager
def capture_logs() -> Generator[StringIO, None, None]:
    """
    Контекстный менеджер для захвата логов.

    Example:
        with capture_logs() as output:
            log_message(LogLevel.INFO, "test")
            assert "test" in output.getvalue()
    """
    old_stdout = sys.stdout
    string_io = StringIO()
    sys.stdout = string_io
    try:
        yield string_io
    finally:
        sys.stdout = old_stdout


@pytest.fixture
def captured_logs() -> Generator[StringIO, None, None]:
    """Фикстура для захвата логов."""
    with capture_logs() as output:
        yield output


class SampleClass:
    """Простой класс для тестов."""

    def __init__(self, value: int = 42):
        self.value = value
        self.board = None
        self.game_state = None

    def method(self, x: int) -> int:
        return x * 2


class ChildClass(SampleClass):
    """Дочерний класс для тестов иерархии."""

    def method(self, x: int) -> int:
        return x * 3


class Position:
    """Класс позиции для тестов log_user_action."""

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col


class GameWithPlayer:
    """Класс с current_player для тестов log_state_change."""

    def __init__(self, player: str = "white"):
        self.current_player = player

    def switch(self):
        self.current_player = "black" if self.current_player == "white" else "white"