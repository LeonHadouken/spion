# tests/test_decorators/test_simple.py (исправленный)
"""
Тесты для простых декораторов (simple.py).
"""

import pytest
import time
from spion.decorators.simple import (
    LogDecorator, log, log_call_once,
    log_user_action, log_state_change
)
from spion.config import LogLevel, configure
from tests.conftest import SampleClass, Position, GameWithPlayer, clean_ansi


class TestLogDecorator:
    """Тесты класса LogDecorator."""

    # tests/test_decorators/test_simple.py (исправляем)
    def test_log_decorator_basic(self, capsys):
        """Проверяем базовое логирование."""
        decorator = LogDecorator(level=LogLevel.INFO)

        @decorator
        def test_func():
            return 42

        result = test_func()

        assert result == 42
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output
        assert "test_func" in output

    def test_log_decorator_debug(self, capsys):
        """Проверяем DEBUG уровень с аргументами и результатом."""
        decorator = LogDecorator(level=LogLevel.DEBUG)

        @decorator
        def test_func(a, b=10):
            return a + b

        result = test_func(5, b=3)

        assert result == 8
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output
        assert "с аргументами" in output
        assert "◀️" in output

    def test_log_decorator_method(self, capsys):
        """Проверяем логирование метода класса."""
        decorator = LogDecorator(level=LogLevel.DEBUG)

        class TestClass:
            @decorator
            def method(self, x):
                return x * 2

        obj = TestClass()
        result = obj.method(21)

        assert result == 42
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "TestClass.method" in output

    def test_log_decorator_custom_message(self, capsys):
        """Проверяем кастомное сообщение."""
        decorator = LogDecorator(level=LogLevel.INFO, message="Custom message")

        @decorator
        def test_func():
            return 42

        test_func()
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "Custom message" in output


class TestLogFunction:
    """Тесты функции log (декоратора)."""

    def test_log_default(self, capsys):
        """Проверяем log() с параметрами по умолчанию."""

        @log()
        def test_func():
            return 42

        test_func()
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output

    def test_log_with_level(self, capsys):
        """Проверяем log с указанием уровня."""

        @log(level=LogLevel.WARNING)
        def test_func():
            return 42

        test_func()
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output

    def test_log_with_message(self, capsys):
        """Проверяем log с кастомным сообщением."""

        @log(message="Hello from test")
        def test_func():
            return 42

        test_func()
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "Hello from test" in output


class TestLogCallOnce:
    """Тесты декоратора log_call_once."""

    def test_log_call_once_basic(self, capsys):
        """Проверяем логирование с интервалом."""

        @log_call_once(interval=0.1)
        def test_func():
            return time.time()

        # Первый вызов - логируем
        test_func()
        # Второй сразу - не логируем
        test_func()
        # Ждем и третий - логируем
        time.sleep(0.15)
        test_func()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) == 2  # Должно быть 2 лога

    def test_log_call_once_different_functions(self, capsys):
        """Проверяем, что разные функции независимы."""

        @log_call_once(interval=0.1)
        def func1():
            pass

        @log_call_once(interval=0.1)
        def func2():
            pass

        func1()  # лог
        func2()  # лог (другая функция)
        func1()  # не лог (слишком рано)
        func2()  # не лог

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) == 2

    def test_log_call_once_method(self, capsys):
        """Проверяем работу на методах класса."""

        class TestClass:
            @log_call_once(interval=0.1)
            def method(self):
                pass

        obj = TestClass()
        obj.method()  # лог
        obj.method()  # не лог
        time.sleep(0.15)
        obj.method()  # лог

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) == 2


class TestLogUserAction:
    """Тесты декоратора log_user_action."""

    def test_log_user_action_with_position(self, capsys):
        """Проверяем логирование действия с позицией."""

        @log_user_action()
        def click(position):
            return position

        pos = Position(row=3, col=4)
        click(pos)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output

    def test_log_user_action_without_position(self, capsys):
        """Проверяем логирование действия без позиции."""

        @log_user_action()
        def login(username):
            return username

        login("user123")

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output

    def test_log_user_action_method(self, capsys):
        """Проверяем логирование метода класса с позицией."""

        class Game:
            @log_user_action()
            def click(self, position):
                return position

        game = Game()
        pos = Position(row=0, col=0)
        game.click(pos)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output

    def test_log_user_action_with_non_position_attrs(self, capsys):
        """Проверяем, что ищутся именно атрибуты row/col."""

        class ClickEvent:
            def __init__(self, x, y):
                self.row = y
                self.col = x

        @log_user_action()
        def handle_click(event):
            pass

        event = ClickEvent(2, 4)
        handle_click(event)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output


class TestLogStateChange:
    """Тесты декоратора log_state_change."""

    def test_log_state_change_with_player(self, capsys):
        """Проверяем логирование смены состояния с current_player."""

        class Game:
            def __init__(self):
                self.current_player = "white"

            @log_state_change()
            def switch(self):
                self.current_player = "black"

        game = Game()
        game.switch()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔄]" in output

    def test_log_state_change_with_enum_player(self, capsys):
        """Проверяем работу с Enum."""

        from enum import Enum

        class Player(Enum):
            WHITE = "белые"
            BLACK = "черные"

        class Game:
            def __init__(self):
                self.current_player = Player.WHITE

            @log_state_change()
            def switch(self):
                self.current_player = Player.BLACK

        game = Game()
        game.switch()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔄]" in output

    def test_log_state_change_without_player(self, capsys):
        """Проверяем логирование без current_player."""

        class Counter:
            def __init__(self):
                self.value = 0

            @log_state_change()
            def increment(self):
                self.value += 1

        counter = Counter()
        counter.increment()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔄]" in output

    def test_log_state_change_after_change(self, capsys):
        """Проверяем, что логируется состояние ДО изменения."""

        class Game:
            def __init__(self):
                self.current_player = "white"

            @log_state_change()
            def switch(self):
                self.current_player = "black"

        game = Game()
        game.switch()  # лог с "white"
        game.switch()  # лог с "black"

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) == 2