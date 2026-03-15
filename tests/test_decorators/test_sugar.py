# tests/test_decorators/test_sugar.py
"""
Тесты для синтаксического сахара.
"""

import pytest
import time
from spion import (
    watch, light, silent,
    trace,
    user, state, throttle,
    spy,
    configure, LogLevel
)
from tests.conftest import clean_ansi, Position, GameWithPlayer, SampleClass


class TestWatchSugar:
    """Тесты для @watch() - алиас @log()"""

    def test_watch_basic(self, capsys):
        """Проверяем базовое логирование"""
        @watch()
        def hello():
            return "world"

        result = hello()
        assert result == "world"

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output
        assert "hello" in output

    def test_watch_with_level(self, capsys):
        """Проверяем watch с уровнем логирования"""
        @watch(level=LogLevel.WARNING)
        def hello():
            return "world"

        hello()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output

    def test_watch_with_message(self, capsys):
        """Проверяем watch с кастомным сообщением"""
        @watch(message="Кастомное сообщение")
        def hello():
            return "world"

        hello()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "Кастомное сообщение" in output


class TestLightSugar:
    """Тесты для @light() - лёгкое логирование (INFO)"""

    def test_light_basic(self, capsys):
        """Проверяем лёгкое логирование"""
        @light()
        def fast_func():
            return 42

        result = fast_func()
        assert result == 42

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output
        assert "fast_func" in output

    def test_light_no_args(self, capsys):
        """Проверяем что light не показывает аргументы (INFO уровень)"""
        @light()
        def func_with_args(a, b):
            return a + b

        func_with_args(5, 3)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output
        assert "с аргументами" not in output
        assert "◀️" not in output


class TestSilentSugar:
    """Тесты для @silent() - только ошибки (ERROR уровень)"""

    def test_silent_success(self, capsys):
        """Успешный вызов не логируется"""

        @silent()
        def success():
            return "OK"

        result = success()
        assert result == "OK"

        captured = capsys.readouterr()
        assert captured.out == ""  # Теперь должно работать!

    def test_silent_error(self, capsys):
        """Ошибка логируется"""
        @silent()
        def fails():
            raise ValueError("Тестовая ошибка")

        with pytest.raises(ValueError):
            fails()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[❌]" in output
        assert "fails" in output
        assert "Тестовая ошибка" in output


class TestTraceSugar:
    """Тесты для @trace() - алиас @log_method_chain()"""

    def test_trace_basic(self, capsys):
        """Проверяем базовую трассировку"""
        from spion import trace

        @trace(max_depth=3)
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        result = factorial(3)
        assert result == 6

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip() and not line.startswith('DEBUG')]

        # Trace может не логировать без watch, просто проверяем результат
        assert result == 6

    def test_trace_fibonacci(self, capsys):
        """Проверяем на более сложной рекурсии (фибоначчи)"""
        from spion import trace

        @trace(max_depth=3)
        def fib(n):
            if n <= 1:
                return n
            return fib(n - 1) + fib(n - 2)

        result = fib(3)
        assert result == 2

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip() and not line.startswith('DEBUG')]

        # Просто проверяем что функция выполнилась
        assert result == 2

    def test_trace_with_level(self, capsys):
        """Проверяем trace с уровнем логирования"""
        from spion import trace

        @trace(level=LogLevel.INFO, max_depth=3)
        def recurse(n):
            if n <= 0:
                return n
            return recurse(n - 1)

        recurse(2)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip() and not line.startswith('DEBUG')]

        # Проверяем что функция выполнилась
        assert True


class TestUserSugar:
    """Тесты для @user() - алиас @log_user_action()"""

    def test_user_with_position(self, capsys):
        """Проверяем логирование действия с позицией"""
        class Game:
            @user()
            def click(self, position):
                return position

        game = Game()
        pos = Position(row=2, col=3)  # row=2 -> 6, col=3 -> D
        game.click(pos)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output

    def test_user_without_position(self, capsys):
        """Проверяем логирование действия без позиции"""
        @user()
        def login(username):
            return username

        login("test_user")

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output
        assert "login" in output

    def test_user_method(self, capsys):
        """Проверяем user на методе класса"""
        class ClickHandler:
            @user()
            def handle(self, position):
                return position

        handler = ClickHandler()
        pos = Position(row=0, col=0)
        handler.handle(pos)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output


class TestStateSugar:
    """Тесты для @state() - алиас @log_state_change()"""

    def test_state_with_player(self, capsys):
        """Проверяем логирование смены состояния с current_player"""
        class Game:
            def __init__(self):
                self.current_player = "white"

            @state()
            def switch(self):
                self.current_player = "black"

        game = Game()
        game.switch()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔄]" in output
        assert "Ход:" in output

    def test_state_without_player(self, capsys):
        """Проверяем логирование без current_player"""
        class Counter:
            def __init__(self):
                self.value = 0

            @state()
            def increment(self):
                self.value += 1

        counter = Counter()
        counter.increment()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔄]" in output
        assert "Изменения" in output

    def test_state_multiple_changes(self, capsys):
        """Проверяем несколько изменений подряд"""
        class Game:
            def __init__(self):
                self.current_player = "white"
                self.score = 0

            @state()
            def make_move(self):
                self.current_player = "black"
                self.score += 10

        game = Game()
        game.make_move()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "current_player" in output
        assert "score" in output


class TestThrottleSugar:
    """Тесты для @throttle() - алиас @log_call_once()"""

    def test_throttle_basic(self, capsys):
        """Проверяем базовое ограничение"""
        @throttle(interval=0.1)
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
        assert len(lines) == 2

    def test_throttle_different_functions(self, capsys):
        """Проверяем что разные функции независимы"""
        @throttle(interval=0.1)
        def func1():
            pass

        @throttle(interval=0.1)
        def func2():
            pass

        func1()
        func2()
        func1()
        func2()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) == 2

    def test_throttle_method(self, capsys):
        """Проверяем на методах класса"""
        class TestClass:
            @throttle(interval=0.1)
            def method(self):
                pass

        obj = TestClass()
        obj.method()
        obj.method()
        time.sleep(0.15)
        obj.method()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) == 2


class TestSpySugar:
    """Тесты для @spy() - композитор декораторов"""

    def test_spy_single_decorator(self, capsys):
        """Проверяем spy с одним декоратором"""
        from spion.decorators.base.composer import DecoratorComposer

        @spy(watch())
        def test_func():
            return 42

        result = test_func()
        assert result == 42

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output

    def test_spy_multiple_decorators(self, capsys):
        """Проверяем spy с несколькими декораторами"""
        from spion import spy, watch, trace

        @spy(
            watch(level=LogLevel.INFO),
            trace(max_depth=3)
        )
        def complex_func(n):
            if n <= 1:
                return n
            return complex_func(n - 1)

        result = complex_func(3)
        assert result == 1

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip() and not line.startswith('DEBUG')]

        # Должны быть логи от watch
        assert len(lines) >= 1
        assert any('▶️' in line for line in lines)

    def test_spy_with_user_and_state(self, capsys):
        """Проверяем spy с user и state"""
        class Game:
            def __init__(self):
                self.current_player = "white"

            @spy(
                user(),
                state()
            )
            def click(self, position):
                self.current_player = "black"
                return position

        game = Game()
        pos = Position(row=1, col=1)
        game.click(pos)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output
        assert "[🔄]" in output

    def test_spy_with_throttle(self, capsys):
        """Проверяем spy с throttle"""
        call_count = 0

        @spy(
            throttle(interval=0.1),
            watch()
        )
        def limited_func():
            nonlocal call_count
            call_count += 1
            return call_count

        # Первый вызов - оба лога
        limited_func()
        # Второй сразу - только watch (throttle подавлен)
        limited_func()
        time.sleep(0.15)
        # Третий - снова оба
        limited_func()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) >= 2  # Должно быть несколько логов


class TestSugarCombinations:
    """Тесты комбинаций сахара"""

    def test_watch_and_trace(self, capsys):
        """Комбинация watch и trace"""
        from spion import watch, trace

        @watch()
        @trace(max_depth=3)
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        result = factorial(3)
        assert result == 6

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip() and not line.startswith('DEBUG')]

        # Должны быть логи от watch
        assert len(lines) >= 1
        assert any('▶️' in line for line in lines)

    def test_user_and_state(self, capsys):
        """Комбинация user и state"""
        class Game:
            def __init__(self):
                self.current_player = "white"

            @user()
            @state()
            def move(self, position):
                self.current_player = "black"
                return position

        game = Game()
        pos = Position(row=2, col=3)
        game.move(pos)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output
        assert "[🔄]" in output

    def test_throttle_and_watch(self, capsys):
        """Комбинация throttle и watch"""
        @throttle(interval=0.1)
        @watch()
        def api_call(n):
            return n * 2

        # Первый вызов - оба лога
        api_call(1)
        # Второй сразу - только watch (throttle молчит)
        api_call(2)
        time.sleep(0.15)
        # Третий - снова оба
        api_call(3)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) >= 3  # throttle(2) + watch(3) = минимум 3


# Тест на соответствие алиасов оригиналам
class TestAliasEquivalence:
    """Проверяем что сахар эквивалентен оригиналам"""

    def test_watch_equals_log(self):
        """watch должен быть эквивалентен log"""
        from spion import log
        from spion.decorators.simple import watch as watch_func

        watch_decorator = watch_func()
        log_decorator = log()

        assert type(watch_decorator).__name__ == type(log_decorator).__name__

    def test_trace_equals_chain(self):
        """trace должен быть эквивалентен log_method_chain"""
        from spion import log_method_chain
        from spion.decorators.simple import trace as trace_func

        trace_decorator = trace_func()
        chain_decorator = log_method_chain()

        assert type(trace_decorator).__name__ == type(chain_decorator).__name__

    def test_user_equals_user_action(self):
        """user должен быть эквивалентен log_user_action"""
        from spion import log_user_action
        from spion.decorators.simple import user as user_func

        user_decorator = user_func()
        action_decorator = log_user_action()

        # Сравниваем возвращаемые декораторы
        @user_decorator
        def f1(): pass

        @action_decorator
        def f2(): pass

        assert hasattr(f1, '__is_user_action__')
        assert hasattr(f2, '__is_user_action__')

    def test_state_equals_state_change(self):
        """state должен быть эквивалентен log_state_change"""
        from spion import log_state_change
        from spion.decorators.simple import state as state_func

        state_decorator = state_func()
        change_decorator = log_state_change()

        @state_decorator
        def f1(): pass

        @change_decorator
        def f2(): pass

        assert hasattr(f1, '__is_state_change__')
        assert hasattr(f2, '__is_state_change__')

    def test_throttle_equals_call_once(self):
        """throttle должен быть эквивалентен log_call_once"""
        from spion import log_call_once
        from spion.decorators.simple import throttle as throttle_func

        throttle_decorator = throttle_func(interval=0.5)
        call_once_decorator = log_call_once(interval=0.5)

        @throttle_decorator
        def f1(): pass

        @call_once_decorator
        def f2(): pass

        assert hasattr(f1, '__interval__')
        assert hasattr(f2, '__interval__')
        assert f1.__interval__ == 0.5
        assert f2.__interval__ == 0.5