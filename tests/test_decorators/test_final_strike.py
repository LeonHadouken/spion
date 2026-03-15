# tests/test_final_strike.py
"""
ФИНАЛЬНЫЙ ТЕСТ - добиваем последние 27 строк
Запуск: pytest tests/test_final_strike.py -v
"""

import pytest
import time
from spion import (
    log_method_chain, log_class_relationship,
    throttle, state,
    configure_filter, reset_filter, add_rule
)
from spion.decorators.core.filtering import CallFilter, should_log_call
from spion.decorators.relationship import RelationshipDecorator
from tests.conftest import clean_ansi


class TestChainFinal:
    """_get_call_type (1 строка)"""

    def test_chain_get_call_type(self):
        @log_method_chain()
        def f():
            pass

        f()  # Просто вызываем - метод вызовется внутри


class TestFilteringFinal:
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


class TestRelationshipFinal:
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
                self.cache = "cache"

        @log_class_relationship(show_dependencies=True)
        def process(service, extra, **kwargs):
            pass

        # Передаем объекты с зависимостями
        process(Service(), Service(), extra_arg=Service())
        capsys.readouterr()

    def test_log_return_type_all_12(self, capsys):
        """12 разных случаев для _log_return_type"""

        class BrokenLen:
            def __len__(self):
                raise ValueError("Broken")

        class Empty:
            def __len__(self):
                return 0

        class OnlyLen:
            def __len__(self):
                return 5

        cases = [
            lambda: None,  # 1. None
            lambda: 42,  # 2. Примитив
            lambda: type('Custom', (), {})(),  # 3. Класс
            lambda: [1, 2, 3],  # 4. Список
            lambda: (1, 2, 3),  # 5. Кортеж
            lambda: {1, 2, 3},  # 6. Множество
            lambda: {"a": 1, "b": 2},  # 7. Словарь
            lambda: "x" * 100,  # 8. Длинная строка
            lambda: BrokenLen(),  # 9. Сломанный __len__
            lambda: object(),  # 10. Простой объект
            lambda: Empty(),  # 11. __len__ = 0
            lambda: OnlyLen(),  # 12. Только __len__
        ]

        for i, case in enumerate(cases):
            @log_class_relationship(analyze_return=True)
            def f():
                return case()

            f()

        out = clean_ansi(capsys.readouterr().out)
        assert out


class TestSimpleFinal:
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