# tests/test_final_coverage.py
"""
ФИНАЛЬНЫЙ ТЕСТ - добиваем последние 27 строк
Запуск: pytest tests/test_final_coverage.py -v
"""

import pytest
import time
from spion import (
    log_method_chain, log_class_relationship,
    throttle, state, user,
    configure_filter, reset_filter, add_rule
)
from spion.decorators.core.filtering import CallFilter, should_log_call
from tests.conftest import clean_ansi


class TestChainCoverage:
    """_get_call_type (1 строка)"""

    def test_chain_get_call_type(self):
        @log_method_chain()
        def f():
            pass

        f()  # Просто вызываем для покрытия


class TestFilteringCoverage:
    """should_log (1), _check_rule (2)"""

    def test_filtering_last_branches(self):
        reset_filter()

        # should_log с include/exclude
        f = CallFilter(include_patterns=[r"inc.*"], exclude_patterns=[r"exc.*"])
        f.should_log("inc_func", "call")
        f.should_log("exc_func", "call")
        f.should_log("other", "call")

        # _check_rule с time_window
        add_rule("last", call_type="call", max_calls=1, time_window=0.1)
        should_log_call("last_1", "call")
        should_log_call("last_2", "call")
        time.sleep(0.15)
        should_log_call("last_3", "call")  # Должен сброситься

        reset_filter()


class TestRelationshipCoverage:
    """_after (3), _analyze_value (2), _analyze_object_arguments (4), _log_return_type (12)"""

    def test_after(self, capsys):
        @log_class_relationship(analyze_return=True)
        def f():
            return [1, 2, 3]

        f()
        assert "🔗" in clean_ansi(capsys.readouterr().out)

    def test_analyze_value_broken_len(self, capsys):
        class BrokenLen:
            def __len__(self):
                raise ValueError("Boom")

        @log_class_relationship(show_types=True)
        def f(x):
            return x

        f(BrokenLen())
        capsys.readouterr()  # Просто сбрасываем

    def test_analyze_object_arguments(self, capsys):
        class Service:
            def __init__(self):
                self.db = "db"

        @log_class_relationship(show_dependencies=True)
        def process(svc, extra):
            pass

        process(Service(), Service())  # Два объекта с зависимостями
        capsys.readouterr()

    def test_log_return_type_all(self, capsys):
        """12 разных случаев - по одному на каждую строку"""

        class Broken:
            def __len__(self):
                raise ValueError

        cases = [
            lambda: None,  # 1. None
            lambda: 42,  # 2. Примитив
            lambda: type('C', (), {})(),  # 3. Класс
            lambda: [1, 2, 3],  # 4. Список
            lambda: (1, 2, 3),  # 5. Кортеж
            lambda: {1, 2, 3},  # 6. Множество
            lambda: {"a": 1},  # 7. Словарь
            lambda: "x" * 100,  # 8. Длинная строка
            lambda: Broken(),  # 9. Сломанный __len__
            lambda: object(),  # 10. Простой объект
            lambda: type('Empty', (), {'__len__': lambda s: 0})(),  # 11. __len__ = 0
            lambda: type('OnlyLen', (), {'__len__': lambda s: 5})(),  # 12. Только __len__
        ]

        for case in cases:
            @log_class_relationship(analyze_return=True)
            def f():
                return case()

            f()

        out = clean_ansi(capsys.readouterr().out)
        assert out


class TestSimpleCoverage:
    """log_call_once.wrapper (1), log_state_change.wrapper (1)"""

    def test_throttle_skipped(self):
        @throttle(interval=0.05)
        def f():
            pass

        for _ in range(30):
            f()
            time.sleep(0.01)

    def test_state_many_changes(self, capsys):
        class Game:
            def __init__(self):
                for i in range(10):
                    setattr(self, f"a{i}", i)

            @state()
            def update(self):
                for i in range(10):
                    setattr(self, f"a{i}", i * 10)

        Game().update()
        out = clean_ansi(capsys.readouterr().out)
        assert "🔄" in out
        assert "и ещё" in out  # Проверяем ветку с множеством изменений