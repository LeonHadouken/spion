# tests/test_decorators/test_context_final.py
"""
Финальные тесты для CallContext.
"""

import pytest
from datetime import datetime
from spion.decorators.core.context import CallContext


class TestCallContextFinal:
    """Добиваем покрытие context.py до 95%"""

    def test_context_creation_with_caller_info(self):
        """Тест создания контекста с информацией о caller."""

        def test_func():
            context = CallContext.create(
                func=test_func,
                args=(1, 2),
                kwargs={"x": 3},
                call_id=42,
                timestamp=datetime.now()
            )
            return context

        context = test_func()
        assert context.call_id == 42
        assert context.args == (1, 2)
        assert context.kwargs == {"x": 3}
        assert context.caller_info is not None

    def test_context_to_dict(self):
        """Тест преобразования в словарь."""

        def func():
            pass

        context = CallContext.create(
            func=func,
            args=(1,),
            kwargs={},
            call_id=100,
            timestamp=datetime.now()
        )

        data = context.to_dict()
        assert data['call_id'] == 100
        assert data['args_count'] == 1
        assert data['kwargs_count'] == 0
        assert 'caller' in data

    def test_context_timestamp_str(self):
        """Тест строкового представления timestamp."""
        now = datetime(2025, 1, 1, 12, 30, 45, 123456)
        context = CallContext(1, now, (), {}, None)

        timestamp = context.timestamp_str
        assert "12:30:45.123" in timestamp

    def test_context_without_caller(self):
        """Тест контекста без информации о caller."""
        context = CallContext(1, datetime.now(), (), {}, None)
        assert context.caller_info is None
        assert context.to_dict()['caller'] is None# tests/test_decorators/test_context_coverage.py
"""
Тесты для непокрытых строк в context.py
"""

import pytest
from datetime import datetime
from spion.decorators.core.context import CallContext


class TestContextCoverage:
    """Тесты для непокрытых строк context.py"""

    def test_context_caller_info_with_deep_stack(self):
        """Тест получения caller info из глубокого стека."""

        def level3():
            return CallContext._get_caller_info()

        def level2():
            return level3()

        def level1():
            return level2()

        caller_info = level1()
        assert caller_info is not None
        assert 'function' in caller_info
        assert 'line' in caller_info

    def test_context_caller_info_exception(self, monkeypatch):
        """Тест обработки исключения при получении caller info."""

        def broken_currentframe():
            raise ValueError("Broken")

        monkeypatch.setattr("inspect.currentframe", broken_currentframe)

        caller_info = CallContext._get_caller_info()
        assert caller_info is None