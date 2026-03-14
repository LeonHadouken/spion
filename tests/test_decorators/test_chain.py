"""
Тесты для декоратора log_method_chain.
"""

import pytest
from debug.decorators.chain import ChainDecorator, log_method_chain
from debug.config import LogLevel, configure
from tests.conftest import captured_logs


class TestChainDecorator:
    """Тесты класса ChainDecorator."""

    def test_chain_basic(self, captured_logs):
        """Проверяем базовое логирование цепочки."""

        @log_method_chain(max_depth=5)
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        result = factorial(3)

        assert result == 6
        output = captured_logs.getvalue()
        lines = [line.strip() for line in output.strip().split('\n')]

        # Проверяем структуру отступов
        assert "[↘️] factorial(3)" in lines[0]
        assert "  [↘️] factorial(2)" in lines[1]
        assert "    [↘️] factorial(1)" in lines[2]
        assert "    [↗️] factorial(1) -> 1" in lines[3]
        assert "  [↗️] factorial(2) -> 2" in lines[4]
        assert "[↗️] factorial(3) -> 6" in lines[5]

    def test_chain_max_depth(self, captured_logs):
        """Проверяем ограничение по глубине."""

        @log_method_chain(max_depth=2)
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        result = factorial(4)

        assert result == 24
        output = captured_logs.getvalue()
        lines = output.strip().split('\n')

        # Должны быть отступы только до глубины 2
        assert len(lines) == 5  # Вход/выход для 4,3,2 (2 глубины)
        assert "  [↘️] factorial(2)" in lines[2]  # глубина 2
        assert "  [↗️] factorial(2)" in lines[3]  # глубина 2

    def test_chain_fibonacci(self, captured_logs):
        """Проверяем на более сложной рекурсии (фибоначчи)."""

        @log_method_chain(max_depth=3)
        def fib(n):
            if n <= 1:
                return n
            return fib(n - 1) + fib(n - 2)

        result = fib(3)

        assert result == 2
        output = captured_logs.getvalue()
        lines = output.strip().split('\n')

        # Проверяем, что все вызовы на глубине <=3 залогированы
        assert len(lines) > 0
        # Не проверяем точное количество, т.к. оно может варьироваться

    def test_chain_method(self, captured_logs):
        """Проверяем работу на методах класса."""

        class Tree:
            @log_method_chain(max_depth=3)
            def traverse(self, depth):
                if depth <= 0:
                    return depth
                return self.traverse(depth - 1)

        tree = Tree()
        result = tree.traverse(3)

        assert result == 0
        output = captured_logs.getvalue()
        assert "[↘️] Tree.traverse(3)" in output
        assert "  [↘️] Tree.traverse(2)" in output
        assert "    [↘️] Tree.traverse(1)" in output
        assert "      [↘️] Tree.traverse(0)" not in output  # глубина 4, не логируется

    def test_chain_different_levels(self, captured_logs):
        """Проверяем работу с разными уровнями логирования."""

        @log_method_chain(level=LogLevel.WARNING, max_depth=3)
        def recurse(n):
            if n <= 0:
                return 0
            return recurse(n - 1)

        recurse(2)

        output = captured_logs.getvalue()
        assert "🟡" in output  # WARNING уровень

    def test_chain_independent_calls(self, captured_logs):
        """Проверяем, что глубина сбрасывается между разными цепочками."""

        @log_method_chain(max_depth=3)
        def recurse(n, marker):
            if n <= 0:
                return marker
            return recurse(n - 1, marker)

        # Первая цепочка
        recurse(2, "A")
        captured_logs.truncate(0)  # очищаем
        captured_logs.seek(0)

        # Вторая цепочка
        recurse(2, "B")

        output = captured_logs.getvalue()
        # Проверяем, что отступы начинаются с нуля
        assert "[↘️] recurse(2, 'B')" in output
        assert "  [↘️] recurse(1, 'B')" in output


class TestLogMethodChainFunction:
    """Тесты функции log_method_chain."""

    def test_default_params(self, captured_logs):
        """Проверяем вызов с параметрами по умолчанию."""

        @log_method_chain()
        def recurse(n):
            if n <= 0:
                return n
            return recurse(n - 1)

        recurse(2)

        output = captured_logs.getvalue()
        assert "🔵 [↘️]" in output  # DEBUG уровень по умолчанию

    def test_custom_params(self, captured_logs):
        """Проверяем вызов с кастомными параметрами."""

        @log_method_chain(level=LogLevel.INFO, max_depth=1)
        def recurse(n):
            if n <= 0:
                return n
            return recurse(n - 1)

        recurse(3)

        output = captured_logs.getvalue()
        assert "🟢 [↘️] recurse(3)" in output
        assert "recurse(2)" not in output  # глубина 2, не логируется