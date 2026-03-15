# tests/conftest.py (обновленный)
"""
Фикстуры для тестов spion.
"""

import pytest
import re
from typing import Generator

from spion.config import configure, LogLevel
from spion.decorators.core.filtering import reset_filter


def clean_ansi(text: str) -> str:
    """Удаляет ANSI коды из строки."""
    if not text:
        return text
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
    reset_filter()
    yield
    # Не восстанавливаем конфигурацию


# Вспомогательные классы для тестов
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