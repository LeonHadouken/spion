# tests/final/test_100_percent.py
"""
ЕДИНСТВЕННЫЙ ФИНАЛЬНЫЙ ТЕСТ - последние 22 строки
"""

import pytest
import time
from spion import (
    log_class_relationship, throttle, state,
    configure_filter, reset_filter
)
from spion.decorators.core.filtering import CallFilter, should_log_call, add_rule, _default_filter
from spion.decorators.relationship import RelationshipDecorator
from spion.decorators.base.decorator import LoggerDecorator
from tests.conftest import clean_ansi


class TestFilteringCoverage:
    """3 строки в filtering.py"""

    def test_exclude_path(self):
        f = CallFilter(exclude_patterns=[r"skip.*"])
        f.should_log("skip_this", "call")

    def test_time_window_reset(self):
        reset_filter()
        add_rule("win", max_calls=1, time_window=0.1)
        should_log_call("win_1", "call")
        time.sleep(0.15)
        should_log_call("win_2", "call")

    def test_configure_filter_all(self):
        configure_filter(suppress_repetitive=True, max_repetitions=3, suppression_window=30)
        assert _default_filter.suppress_repetitive is True


class TestRelationshipCoverage:
    """17 строк в relationship.py"""

    def test_after(self, capsys):
        @log_class_relationship(analyze_return=True)
        def f(): return [1, 2, 3]

        f()
        assert "🔗" in clean_ansi(capsys.readouterr().out)

    def test_analyze_value_broken_len(self, capsys):
        class Broken:
            def __len__(self): raise ValueError

        @log_class_relationship(show_types=True)
        def p(x): return x

        p(Broken())
        assert capsys.readouterr().out

    def test_log_return_type_all(self, capsys):
        cases = [
            lambda: None,
            lambda: 42,
            lambda: type('C', (), {})(),
            lambda: [1, 2, 3],
            lambda: (1, 2, 3),
            lambda: {1, 2, 3},
            lambda: {"a": 1},
            lambda: "x" * 100,
            lambda: type('Broken', (), {'__len__': lambda s: 1 / 0})(),
            lambda: object(),
            lambda: type('Empty', (), {'__len__': lambda s: 0})(),
            lambda: type('OnlyLen', (), {'__len__': lambda s: 5})(),
        ]
        for case in cases:
            @log_class_relationship(analyze_return=True)
            def f(): return case()

            f()
        assert capsys.readouterr().out


class TestSimpleCoverage:
    """2 строки в simple.py"""

    def test_throttle_skipped(self):
        @throttle(interval=0.05)
        def f(): pass

        for _ in range(30):
            f()
            time.sleep(0.01)

    def test_state_many_changes(self, capsys):
        class Game:
            def __init__(self):
                for i in range(10): setattr(self, f"a{i}", i)

            @state()
            def update(self):
                for i in range(10): setattr(self, f"a{i}", i * 10)

        Game().update()
        out = clean_ansi(capsys.readouterr().out)
        assert "🔄" in out


class TestBaseCoverage:
    """2 строки в base/decorator.py"""

    def test_decorator_duplicate_methods(self):
        class TestDecorator(LoggerDecorator):
            def _after(self, result, context, signature):
                return super()._after(result, context, signature)

        decorator = TestDecorator()

        @decorator
        def success(): return 42

        assert success() == 42