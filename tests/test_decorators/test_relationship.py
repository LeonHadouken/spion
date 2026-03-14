"""
Тесты для декоратора log_class_relationship.
"""

import pytest
from debug.decorators.relationship import (
    RelationshipDecorator, log_class_relationship
)
from debug.config import LogLevel
from tests.conftest import captured_logs, SampleClass, ChildClass


class TestRelationshipDecorator:
    """Тесты класса RelationshipDecorator."""

    def test_relationship_basic(self, captured_logs):
        """Проверяем базовое логирование связей."""
        decorator = RelationshipDecorator(level=LogLevel.INFO)

        @decorator
        def test_func(obj):
            return obj.value

        obj = SampleClass(value=42)
        result = test_func(obj)

        assert result == 42
        output = captured_logs.getvalue()
        assert "[🔗] test_func" in output
        assert "• obj: SampleClass (экземпляр SampleClass) ✓" in output

    def test_relationship_with_hierarchy(self, captured_logs):
        """Проверяем логирование иерархии."""
        decorator = RelationshipDecorator(
            level=LogLevel.INFO,
            show_hierarchy=True,
            show_dependencies=False
        )

        @decorator
        def test_func(obj):
            return obj.value

        obj = ChildClass(value=42)
        test_func(obj)

        output = captured_logs.getvalue()
        assert "📊 Иерархия: ChildClass -> SampleClass -> object" in output

    def test_relationship_with_dependencies(self, captured_logs):
        """Проверяем логирование зависимостей."""

        class Service:
            pass

        class Repository:
            pass

        class Controller:
            def __init__(self):
                self.service = Service()
                self.repository = Repository()
                self.plain_attr = 42  # не должно попасть в зависимости

        decorator = RelationshipDecorator(
            level=LogLevel.INFO,
            show_hierarchy=False,
            show_dependencies=True
        )

        @decorator
        def handle(controller):
            pass

        ctrl = Controller()
        handle(ctrl)

        output = captured_logs.getvalue()
        assert "🔗 Зависимости: service: Service, repository: Repository" in output
        assert "plain_attr" not in output

    def test_relationship_full(self, captured_logs):
        """Проверяем полный анализ (иерархия + зависимости)."""
        decorator = RelationshipDecorator(
            level=LogLevel.INFO,
            show_hierarchy=True,
            show_dependencies=True
        )

        class Model:
            pass

        class User(Model):
            def __init__(self):
                self.db = "database"
                self.cache = "cache"

        @decorator
        def save_user(user):
            pass

        user = User()
        save_user(user)

        output = captured_logs.getvalue()
        assert "📊 Иерархия: User -> Model -> object" in output
        assert "🔗 Зависимости: db: str, cache: str" in output

    def test_relationship_method(self, captured_logs):
        """Проверяем работу на методе класса."""

        class Service:
            @log_class_relationship(show_hierarchy=True)
            def process(self, data, config):
                return data

        service = Service()

        class Config:
            pass

        service.process([1, 2, 3], Config())

        output = captured_logs.getvalue()
        assert "[🔗] Service.process" in output
        assert "• data: list (экземпляр list) ⚠" in output
        assert "• config: Config (экземпляр Config) ✓" in output
        assert "📊 Иерархия: Service -> object" in output

    def test_relationship_return_type(self, captured_logs):
        """Проверяем логирование типа результата."""
        decorator = RelationshipDecorator(level=LogLevel.INFO)

        @decorator
        def test_func():
            return SampleClass()

        result = test_func()

        output = captured_logs.getvalue()
        assert "↩️ Результат: SampleClass (экземпляр SampleClass)" in output

    def test_relationship_none_result(self, captured_logs):
        """Проверяем, что None результат не логируется отдельно."""

        @log_class_relationship()
        def returns_none():
            return None

        returns_none()

        output = captured_logs.getvalue()
        assert "↩️" not in output


class TestLogClassRelationshipFunction:
    """Тесты функции log_class_relationship."""

    def test_default_params(self, captured_logs):
        """Проверяем вызов с параметрами по умолчанию."""

        @log_class_relationship()
        def test_func(obj):
            pass

        test_func(SampleClass())

        output = captured_logs.getvalue()
        assert "[🔗] test_func" in output

    def test_custom_params(self, captured_logs):
        """Проверяем вызов с кастомными параметрами."""

        @log_class_relationship(
            level=LogLevel.DEBUG,
            show_hierarchy=False,
            show_dependencies=False
        )
        def test_func(obj):
            pass

        test_func(SampleClass())

        output = captured_logs.getvalue()
        assert "🔵 [🔗]" in output
        assert "📊" not in output
        assert "🔗" not in output  # второе вхождение - dependencies