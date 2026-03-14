"""
Интеграционные тесты для проверки взаимодействия компонентов.
"""

import pytest
from debug import (
    log, log_method_chain, log_class_relationship,
    log_user_action, log_state_change,
    configure, configure_filter, add_rule,
    get_suppression_summary, reset_filter,
    LogLevel
)
from tests.conftest import captured_logs, SampleClass, Position, GameWithPlayer


class TestDecoratorCombinations:
    """Тесты комбинирования декораторов."""

    def test_log_and_relationship(self, captured_logs):
        """Проверяем комбинацию log и log_class_relationship."""

        class TestClass:
            @log(level=LogLevel.INFO)
            @log_class_relationship(show_hierarchy=True)
            def method(self, obj):
                return obj.value

        obj = TestClass()
        result = obj.method(SampleClass(value=42))

        assert result == 42
        output = captured_logs.getvalue()

        # Должны быть оба декоратора
        assert "[🔗] TestClass.method" in output
        assert "▶️ Вызов TestClass.method" in output

    def test_user_action_and_chain(self, captured_logs):
        """Проверяем комбинацию log_user_action и log_method_chain."""

        class Game:
            @log_user_action()
            @log_method_chain(max_depth=3)
            def click(self, position):
                self.highlight(position)
                return position

            def highlight(self, position):
                pass

        game = Game()
        pos = Position(row=2, col=3)  # row=2 -> 6, col=3 -> D
        game.click(pos)

        output = captured_logs.getvalue()

        # Должны быть оба декоратора
        assert "[👤] Game.click на D6" in output
        assert "[↘️] Game.click(Position(2,3))" in output

    def test_state_change_and_relationship(self, captured_logs):
        """Проверяем комбинацию log_state_change и log_class_relationship."""

        class Game:
            def __init__(self):
                self.current_player = "white"
                self.board = "board"
                self.validator = "validator"

            @log_state_change()
            @log_class_relationship(show_dependencies=True)
            def switch(self):
                self.current_player = "black"

        game = Game()
        game.switch()

        output = captured_logs.getvalue()

        # Должны быть оба
        assert "[🔄] Game.switch | Ход: white" in output
        assert "[🔗] Game.switch" in output
        assert "🔗 Зависимости: board: str, validator: str" in output

    def test_three_decorators(self, captured_logs):
        """Проверяем комбинацию трёх декораторов."""

        class ComplexSystem:
            def __init__(self):
                self.current_player = "system"
                self.db = "database"
                self.cache = "cache"

            @log(level=LogLevel.DEBUG)
            @log_user_action()
            @log_method_chain(max_depth=2)
            def process(self, position, data):
                self.validate(data)
                return "done"

            def validate(self, data):
                pass

        system = ComplexSystem()
        pos = Position(row=1, col=1)  # row=1 -> 7, col=1 -> B
        system.process(pos, {"key": "value"})

        output = captured_logs.getvalue()

        # Проверяем наличие всех трёх типов логов
        assert "[👤] ComplexSystem.process на B7" in output
        assert "[↘️] ComplexSystem.process(Position(1,1), {'key': 'value'})" in output
        assert "▶️ Вызов ComplexSystem.process с аргументами: Position(1,1), {'key': 'value'}" in output


class TestFilterIntegration:
    """Тесты интеграции с фильтрами."""

    def test_filter_with_decorators(self, captured_logs):
        """Проверяем работу фильтров с декораторами."""
        reset_filter()
        configure_filter(max_repetitions=2)

        @log()
        def test_func(n):
            return n * 2

        # Первые 2 раза - логируем
        for i in range(2):
            test_func(i)

        # Третий раз - подавляем
        test_func(2)

        output = captured_logs.getvalue()
        lines = output.strip().split('\n')
        assert len(lines) == 2

    def test_custom_rule_with_decorator(self, captured_logs):
        """Проверяем кастомные правила с декораторами."""
        reset_filter()
        add_rule("important", max_calls=1, log_once=True)

        @log()
        def important_function():
            return "important"

        @log()
        def normal_function():
            return "normal"

        important_function()  # лог
        important_function()  # не лог
        normal_function()     # лог (не подпадает под правило)
        normal_function()     # лог (пока не превышен max_repetitions)

        output = captured_logs.getvalue()
        lines = output.strip().split('\n')
        assert len(lines) == 3  # important(1) + normal(2)

    def test_suppression_summary_after_rules(self):
        """Проверяем получение сводки после применения правил."""
        reset_filter()
        configure_filter(max_repetitions=2)

        @log()
        def spammy_function():
            pass

        # Много вызовов
        for i in range(10):
            spammy_function()

        summary = get_suppression_summary()
        assert len(summary) > 0
        assert any("spammy_function" in key for key in summary.keys())


class TestConfigIntegration:
    """Тесты интеграции с конфигурацией."""

    def test_config_affects_decorators(self, captured_logs):
        """Проверяем, что глобальная конфигурация влияет на декораторы."""

        @log(level=LogLevel.DEBUG)
        def test_func():
            return 42

        # DEBUG включен
        configure(min_level=LogLevel.DEBUG)
        test_func()
        assert "▶️" in captured_logs.getvalue()

        captured_logs.truncate(0)
        captured_logs.seek(0)

        # DEBUG выключен
        configure(min_level=LogLevel.INFO)
        test_func()
        assert captured_logs.getvalue() == ""

    def test_timestamp_config(self, captured_logs):
        """Проверяем настройку временных меток."""

        @log()
        def test_func():
            pass

        # С метками
        configure(show_timestamp=True)
        test_func()
        assert "[" in captured_logs.getvalue()

        captured_logs.truncate(0)
        captured_logs.seek(0)

        # Без меток
        configure(show_timestamp=False)
        test_func()
        assert "[" not in captured_logs.getvalue()

    def test_color_config(self, captured_logs):
        """Проверяем настройку цветов."""
        # Цвета включены (по умолчанию)
        configure(color_enabled=True)

        @log(level=LogLevel.INFO)
        def test_func():
            pass

        test_func()
        output = captured_logs.getvalue()
        assert '\033[' in output  # есть ANSI код

        captured_logs.truncate(0)
        captured_logs.seek(0)

        # Цвета выключены
        configure(color_enabled=False)
        test_func()
        output = captured_logs.getvalue()
        assert '\033[' not in output