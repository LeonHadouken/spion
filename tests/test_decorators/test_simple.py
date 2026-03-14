"""
Тесты для простых декораторов (simple.py).
"""

import pytest
import time
from debug.decorators.simple import (
    LogDecorator, log, log_call_once,
    log_user_action, log_state_change
)
from debug.config import LogLevel, configure
from tests.conftest import captured_logs, SampleClass, Position, GameWithPlayer


class TestLogDecorator:
    """Тесты класса LogDecorator."""

    def test_log_decorator_basic(self, captured_logs):
        """Проверяем базовое логирование."""
        decorator = LogDecorator(level=LogLevel.INFO)

        @decorator
        def test_func():
            return 42

        result = test_func()

        assert result == 42
        output = captured_logs.getvalue()
        assert "▶️ Вызов test_func" in output
        # INFO уровень не показывает результат
        assert "◀️" not in output

    def test_log_decorator_debug(self, captured_logs):
        """Проверяем DEBUG уровень с аргументами и результатом."""
        decorator = LogDecorator(level=LogLevel.DEBUG)

        @decorator
        def test_func(a, b=10):
            return a + b

        result = test_func(5, b=3)

        assert result == 8
        output = captured_logs.getvalue()
        assert "▶️ Вызов test_func с аргументами: 5, b=3" in output
        assert "◀️ test_func -> 8" in output

    def test_log_decorator_method(self, captured_logs):
        """Проверяем логирование метода класса."""
        decorator = LogDecorator(level=LogLevel.DEBUG)

        class TestClass:
            @decorator
            def method(self, x):
                return x * 2

        obj = TestClass()
        result = obj.method(21)

        assert result == 42
        output = captured_logs.getvalue()
        assert "▶️ Вызов TestClass.method с аргументами: 21" in output
        assert "◀️ TestClass.method -> 42" in output

    def test_log_decorator_custom_message(self, captured_logs):
        """Проверяем кастомное сообщение."""
        decorator = LogDecorator(level=LogLevel.INFO, message="Custom message")

        @decorator
        def test_func():
            return 42

        test_func()
        assert "▶️ Custom message" in captured_logs.getvalue()


class TestLogFunction:
    """Тесты функции log (декоратора)."""

    def test_log_default(self, captured_logs):
        """Проверяем log() с параметрами по умолчанию."""

        @log()
        def test_func():
            return 42

        test_func()
        assert "▶️ Вызов test_func" in captured_logs.getvalue()

    def test_log_with_level(self, captured_logs):
        """Проверяем log с указанием уровня."""

        @log(level=LogLevel.WARNING)
        def test_func():
            return 42

        test_func()
        output = captured_logs.getvalue()
        assert "▶️ Вызов test_func" in output
        assert "🟡" in output

    def test_log_with_message(self, captured_logs):
        """Проверяем log с кастомным сообщением."""

        @log(message="Hello from test")
        def test_func():
            return 42

        test_func()
        assert "▶️ Hello from test" in captured_logs.getvalue()


class TestLogCallOnce:
    """Тесты декоратора log_call_once."""

    def test_log_call_once_basic(self, captured_logs):
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

        output = captured_logs.getvalue()
        lines = output.strip().split('\n')
        assert len(lines) == 2  # Должно быть 2 лога

    def test_log_call_once_different_functions(self, captured_logs):
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

        output = captured_logs.getvalue()
        lines = output.strip().split('\n')
        assert len(lines) == 2

    def test_log_call_once_method(self, captured_logs):
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

        output = captured_logs.getvalue()
        lines = output.strip().split('\n')
        assert len(lines) == 2
        assert "[🔄] TestClass.method" in output


class TestLogUserAction:
    """Тесты декоратора log_user_action."""

    def test_log_user_action_with_position(self, captured_logs):
        """Проверяем логирование действия с позицией."""

        @log_user_action()
        def click(position):
            return position

        pos = Position(row=3, col=4)  # col=4 -> E, row=3 -> 5
        click(pos)

        output = captured_logs.getvalue()
        assert "[👤] click на E5" in output

    def test_log_user_action_without_position(self, captured_logs):
        """Проверяем логирование действия без позиции."""

        @log_user_action()
        def login(username):
            return username

        login("user123")

        output = captured_logs.getvalue()
        assert "[👤] login" in output

    def test_log_user_action_method(self, captured_logs):
        """Проверяем логирование метода класса с позицией."""

        class Game:
            @log_user_action()
            def click(self, position):
                return position

        game = Game()
        pos = Position(row=0, col=0)  # row=0, col=0 -> A1
        game.click(pos)

        output = captured_logs.getvalue()
        assert "[👤] Game.click на A1" in output

    def test_log_user_action_with_non_position_attrs(self, captured_logs):
        """Проверяем, что ищутся именно атрибуты row/col."""

        class ClickEvent:
            def __init__(self, x, y):
                self.row = y  # адаптируем под ожидаемый формат
                self.col = x

        @log_user_action()
        def handle_click(event):
            pass

        event = ClickEvent(2, 4)
        handle_click(event)

        output = captured_logs.getvalue()
        assert "[👤] handle_click на C4" in output  # row=4 -> 4, col=2 -> C


class TestLogStateChange:
    """Тесты декоратора log_state_change."""

    def test_log_state_change_with_player(self, captured_logs):
        """Проверяем логирование смены состояния с current_player."""

        class Game:
            def __init__(self):
                self.current_player = "white"

            @log_state_change()
            def switch(self):
                self.current_player = "black"

        game = Game()
        game.switch()

        output = captured_logs.getvalue()
        assert "[🔄] Game.switch | Ход: white" in output

    def test_log_state_change_with_enum_player(self, captured_logs):
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

        output = captured_logs.getvalue()
        assert "[🔄] Game.switch | Ход: белые" in output

    def test_log_state_change_without_player(self, captured_logs):
        """Проверяем логирование без current_player."""

        class Counter:
            def __init__(self):
                self.value = 0

            @log_state_change()
            def increment(self):
                self.value += 1

        counter = Counter()
        counter.increment()

        output = captured_logs.getvalue()
        assert "[🔄] Counter.increment" in output
        assert "Ход:" not in output

    def test_log_state_change_after_change(self, captured_logs):
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

        output = captured_logs.getvalue()
        assert "Ход: white" in output
        assert "Ход: black" in output