# tests/test_decorators/test_metadata.py
"""
Тесты для модуля metadata.py (сейчас покрытие 44%).
"""

import pytest
from spion.decorators.base.metadata import with_metadata
from datetime import datetime


class TestWithMetadata:
    """Тесты для декоратора with_metadata."""

    def test_metadata_added_to_function(self):
        """Проверяем, что декоратор добавляет метаданные к функции."""

        @with_metadata
        def test_func(a, b):
            return a + b

        assert hasattr(test_func, '__metadata__')
        assert 'decorated_at' in test_func.__metadata__
        assert 'original_name' in test_func.__metadata__
        assert test_func.__metadata__['original_name'] == 'test_func'

    def test_metadata_preserves_functionality(self):
        """Проверяем, что функция работает как обычно."""

        @with_metadata
        def add(a, b):
            return a + b

        assert add(2, 3) == 5
        assert add(a=5, b=7) == 12

    def test_metadata_timestamp_format(self):
        """Проверяем формат временной метки."""

        @with_metadata
        def func():
            pass

        decorated_at = func.__metadata__['decorated_at']
        # Должен быть ISO формат: YYYY-MM-DDTHH:MM:SS
        assert 'T' in decorated_at
        parts = decorated_at.split('T')
        assert len(parts) == 2
        assert len(parts[0].split('-')) == 3  # год-месяц-день

    def test_metadata_preserves_docstring(self):
        """Проверяем, что докстринг сохраняется."""

        @with_metadata
        def documented_func():
            """This is a test docstring."""
            pass

        assert documented_func.__doc__ == "This is a test docstring."
        assert documented_func.__metadata__['original_doc'] == "This is a test docstring."

    def test_metadata_preserves_module(self):
        """Проверяем, что модуль сохраняется."""
        import sys

        @with_metadata
        def func():
            pass

        assert func.__module__ == __name__
        assert func.__metadata__['original_module'] == __name__

    def test_metadata_on_method(self):
        """Проверяем работу на методах класса."""

        class TestClass:
            @with_metadata
            def method(self, x):
                return x * 2

        obj = TestClass()
        assert obj.method(5) == 10
        assert hasattr(TestClass.method, '__metadata__')
        assert TestClass.method.__metadata__['original_name'] == 'method'

    def test_metadata_on_classmethod(self):
        """Проверяем работу на classmethod."""

        class TestClass:
            @classmethod
            @with_metadata
            def cls_method(cls, x):
                return x * 3

        assert TestClass.cls_method(5) == 15
        assert hasattr(TestClass.cls_method, '__metadata__')
        assert TestClass.cls_method.__metadata__['original_name'] == 'cls_method'

    def test_metadata_on_staticmethod(self):
        """Проверяем работу на staticmethod."""

        class TestClass:
            @staticmethod
            @with_metadata
            def static_method(x):
                return x * 4

        assert TestClass.static_method(5) == 20
        assert hasattr(TestClass.static_method, '__metadata__')

    def test_metadata_multiple_functions(self):
        """Проверяем, что каждая функция получает свои метаданные."""

        @with_metadata
        def func1():
            pass

        @with_metadata
        def func2():
            pass

        assert func1.__metadata__['original_name'] == 'func1'
        assert func2.__metadata__['original_name'] == 'func2'
        assert func1.__metadata__['decorated_at'] != func2.__metadata__['decorated_at']

    def test_metadata_not_overwritten(self):
        """Проверяем, что существующие атрибуты не затираются."""

        def func():
            pass

        func.custom_attr = "hello"

        decorated = with_metadata(func)

        assert decorated.custom_attr == "hello"
        assert hasattr(decorated, '__metadata__')