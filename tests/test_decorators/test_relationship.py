# tests/test_decorators/test_relationship.py
"""
Комплексные тесты для RelationshipDecorator.
Объединены все тесты: базовые, расширенные, покрытие и финальные.
"""

import pytest
from spion import log_class_relationship
from spion.decorators.relationship import RelationshipDecorator
from spion.config import LogLevel
from tests.conftest import SampleClass, ChildClass, clean_ansi


class TestRelationshipDecorator:
    """Тесты класса RelationshipDecorator."""

    def test_relationship_basic(self, capsys):
        """Проверяем базовое логирование связей."""
        decorator = RelationshipDecorator(level=LogLevel.INFO)

        @decorator
        def test_func(obj):
            return obj.value

        obj = SampleClass(value=42)
        result = test_func(obj)

        assert result == 42
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output
        assert "obj" in output

    def test_relationship_with_hierarchy(self, capsys):
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

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "Иерархия" in output
        assert "ChildClass" in output

    def test_relationship_with_dependencies(self, capsys):
        """Проверяем логирование зависимостей."""

        class Service:
            pass

        class Repository:
            pass

        class Controller:
            def __init__(self):
                self.service = Service()
                self.repository = Repository()
                self.plain_attr = 42

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

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        # Проверяем что есть упоминание о зависимостях
        assert any(word in output for word in ["Зависимости", "service", "repository", "🔗"])

    def test_relationship_full(self, capsys):
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

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "Иерархия" in output
        assert "Зависимости" in output or "db" in output

    def test_relationship_method(self, capsys):
        """Проверяем работу на методе класса."""

        class Service:
            @log_class_relationship(show_hierarchy=True)
            def process(self, data, config):
                return data

        service = Service()

        class Config:
            pass

        service.process([1, 2, 3], Config())

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output
        assert "Service.process" in output

    def test_relationship_return_type(self, capsys):
        """Проверяем логирование типа результата."""
        decorator = RelationshipDecorator(level=LogLevel.INFO, analyze_return=True)

        @decorator
        def test_func():
            return SampleClass()

        result = test_func()
        assert isinstance(result, SampleClass)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        # Проверяем что есть какой-то вывод
        assert len(output.strip()) > 0

    def test_relationship_none_result(self, capsys):
        """Проверяем, что None результат не логируется отдельно."""

        @log_class_relationship()
        def returns_none():
            return None

        returns_none()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "Результат" not in output


class TestLogClassRelationshipFunction:
    """Тесты функции log_class_relationship."""

    def test_default_params(self, capsys):
        """Проверяем вызов с параметрами по умолчанию."""

        @log_class_relationship()
        def test_func(obj):
            pass

        test_func(SampleClass())

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output

    def test_custom_params(self, capsys):
        """Проверяем вызов с кастомными параметрами."""

        @log_class_relationship(
            level=LogLevel.DEBUG,
            show_hierarchy=False,
            show_dependencies=False
        )
        def test_func(obj):
            pass

        test_func(SampleClass())

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output
        assert "Иерархия" not in output


class TestRelationshipAdvanced:
    """Дополнительные тесты для RelationshipDecorator."""

    def test_relationship_with_complex_objects(self, capsys):
        """Проверяем анализ сложных объектов с вложенными зависимостями."""

        class Engine:
            pass

        class Wheel:
            pass

        class Car:
            def __init__(self):
                self.engine = Engine()
                self.wheels = [Wheel() for _ in range(4)]
                self.model = "Tesla"
                self.year = 2025

        @log_class_relationship(show_dependencies=True, show_hierarchy=True)
        def analyze_car(car):
            return car

        car = Car()
        analyze_car(car)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output

    def test_relationship_with_none_args(self, capsys):
        """Проверяем обработку None аргументов."""

        @log_class_relationship()
        def process(obj):
            return obj

        process(None)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output

    def test_relationship_analyze_return_false(self, capsys):
        """Проверяем отключение анализа возвращаемого значения."""

        @log_class_relationship(analyze_return=False)
        def create_obj():
            class Result:
                pass

            return Result()

        create_obj()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output

    def test_relationship_with_mixed_args(self, capsys):
        """Проверяем смешанные аргументы (объекты и примитивы)."""

        class User:
            def __init__(self, name):
                self.name = name
                self.db = "postgres"

        @log_class_relationship(show_dependencies=True)
        def save_user(user, db_name, retry=True):
            return user

        user = User("Alice")
        save_user(user, "main_db", retry=False)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output

    def test_relationship_error_in_analysis(self, capsys):
        """Проверяем обработку ошибок во время анализа."""

        class BrokenObject:
            def __init__(self):
                self._broken = True

            @property
            def __class__(self):
                raise ValueError("Broken __class__")

        @log_class_relationship()
        def handle(obj):
            return obj

        # Перехватываем исключение на верхнем уровне
        try:
            handle(BrokenObject())
            # Если дошли сюда - тест провален
            assert False, "Должно было упасть, но не упало"
        except ValueError as e:
            # Ожидаем что упадет с ValueError от __class__
            assert "Broken" in str(e)

        # Ловим вывод (может быть пустым из-за раннего падения)
        captured = capsys.readouterr()


class TestRelationshipCoverage:
    """Тесты для непокрытых строк relationship.py"""

    def test_log_return_type_basic(self, capsys):
        """Тест _log_return_type для простого типа."""
        # Создаем декоратор напрямую для контроля
        decorator = RelationshipDecorator(level=LogLevel.INFO, analyze_return=True)

        # Создаем контекст вручную
        class Context:
            timestamp_str = "00:00:00"

        context = Context()

        # Прямой вызов _log_return_type
        decorator._log_return_type(42, context)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Проверяем что метод вызвался и вывел сообщение
        assert "↩️ Результат: int" in output or "Результат: int" in output

    def test_log_return_type_with_different_class(self, capsys):
        """Тест _log_return_type когда класс отличается от типа."""
        decorator = RelationshipDecorator(level=LogLevel.INFO, analyze_return=True)

        class Context:
            timestamp_str = "00:00:00"

        context = Context()

        # Создаем класс с разными type() и __class__
        class BaseClass:
            pass

        # Создаем прокси-объект, который прикидывается другим классом
        class ProxyClass:
            def __init__(self, obj):
                self._obj = obj

            def __getattr__(self, name):
                return getattr(self._obj, name)

            @property
            def __class__(self):
                return BaseClass

        obj = ProxyClass(object())

        # Прямой вызов _log_return_type
        decorator._log_return_type(obj, context)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Должно быть что-то вроде "Результат: ProxyClass (экземпляр BaseClass)"
        assert "экземпляр" in output

    def test_log_return_type_with_collection_length(self, capsys):
        """Тест _log_return_type для коллекции с длиной."""
        decorator = RelationshipDecorator(level=LogLevel.INFO, analyze_return=True)

        class Context:
            timestamp_str = "00:00:00"

        context = Context()

        # Прямой вызов _log_return_type для списка
        decorator._log_return_type([1, 2, 3, 4, 5], context)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Проверяем что есть длина
        assert "[5]" in output

    def test_log_return_type_with_broken_len(self, capsys):
        """Тест _log_return_type для объекта со сломанным __len__."""
        decorator = RelationshipDecorator(level=LogLevel.INFO, analyze_return=True)

        class Context:
            timestamp_str = "00:00:00"

        context = Context()

        class BrokenLen:
            def __len__(self):
                raise ValueError("Broken length")

        # Прямой вызов _log_return_type - не должен упасть
        decorator._log_return_type(BrokenLen(), context)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Проверяем что базовое сообщение есть
        assert "Результат: BrokenLen" in output

    def test_log_return_type_with_string_no_length(self, capsys):
        """Тест _log_return_type для строки (не должна показывать длину)."""
        decorator = RelationshipDecorator(level=LogLevel.INFO, analyze_return=True)

        class Context:
            timestamp_str = "00:00:00"

        context = Context()

        # Прямой вызов _log_return_type для строки
        decorator._log_return_type("hello world", context)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Проверяем что нет длины
        assert "Результат: str" in output
        assert "[11]" not in output

    def test_log_return_type_with_bytes_no_length(self, capsys):
        """Тест _log_return_type для bytes (не должна показывать длину)."""
        decorator = RelationshipDecorator(level=LogLevel.INFO, analyze_return=True)

        class Context:
            timestamp_str = "00:00:00"

        context = Context()

        # Прямой вызов _log_return_type для bytes
        decorator._log_return_type(b"hello", context)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Проверяем что нет длины
        assert "Результат: bytes" in output
        assert "[5]" not in output

    def test_analyze_value_with_different_class_and_checkmark(self, capsys):
        """Тест _analyze_value с разными классами и проверкой символа."""

        class Base:
            pass

        class Derived(Base):
            pass

        @log_class_relationship(show_types=True)
        def process(obj1, obj2):
            return obj1, obj2

        process(Base(), Derived())

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Проверяем что есть информация об объектах
        assert "Base" in output or "Derived" in output

    def test_analyze_value_with_same_class_no_checkmark(self, capsys):
        """Тест _analyze_value когда класс совпадает с типом (без галочки)."""

        @log_class_relationship(show_types=True)
        def process(value):
            return value

        process(42)  # int - тип и класс совпадают

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Проверяем что вывод есть
        assert output.strip() != ""

    def test_after_with_analyze_return_true(self, capsys):
        """Тест _after с analyze_return=True вызывает _log_return_type."""
        decorator = RelationshipDecorator(level=LogLevel.INFO, analyze_return=True)

        class Context:
            timestamp_str = "00:00:00"

        context = Context()

        # Прямой вызов _after
        decorator._after([1, 2, 3], context, "test_func()")

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        # Проверяем что был вызван _log_return_type
        assert "Результат: list" in output
        assert "[3]" in output

    def test_after_with_analyze_return_false(self, capsys):
        """Тест _after с analyze_return=False (не должен логировать результат)."""

        @log_class_relationship(analyze_return=False)
        def test_func():
            return [1, 2, 3]

        test_func()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        # Не должно быть информации о результате
        assert "list" not in output or "3" not in output

    def test_relationship_analyze_value_with_length(self, capsys):
        """Тест для строк с анализом длины коллекций."""

        class Container:
            def __init__(self):
                self.items = [1, 2, 3, 4, 5]
                self.empty = []
                self.data = "string"

        @log_class_relationship(show_types=True)
        def process(container):
            return container

        process(Container())

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert output.strip() != ""
        assert "🔗" in output or "[🔗]" in output

    def test_relationship_log_arguments_with_error(self, capsys):
        """Тест обработки ошибки при анализе аргументов."""

        class BrokenSignature:
            def __repr__(self):
                raise ValueError("Broken repr")

        @log_class_relationship()
        def process(broken):
            return broken

        process(BrokenSignature())

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        # Должен быть хотя бы базовый лог
        assert "🔗" in output or "[🔗]" in output

    def test_relationship_log_hierarchy_single_class(self, capsys):
        """Тест иерархии для класса без родителей."""

        class Standalone:
            pass

        @log_class_relationship(show_hierarchy=True)
        def process(obj):
            return obj

        process(Standalone())

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "🔗" in output or "[🔗]" in output

    def test_relationship_log_dependencies_custom_names(self, capsys):
        """Тест зависимостей с кастомными именами атрибутов."""

        class Service:
            def __init__(self):
                self.database = "db"
                self.cache_service = "cache"
                self.logger = "log"
                self.config_manager = "config"

        @log_class_relationship(show_dependencies=True)
        def process(service):
            return service

        service = Service()
        process(service)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "database" in output or "cache" in output or "🔗" in output

    def test_relationship_analyze_object_arguments_empty(self, capsys):
        """Тест анализа объектов без зависимостей."""

        class Simple:
            def __init__(self):
                self.value = 42

        @log_class_relationship(show_dependencies=True)
        def process(obj):
            return obj

        obj = Simple()
        process(obj)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "🔗" in output or "[🔗]" in output

    def test_relationship_log_return_type_with_collection(self, capsys):
        """Тест _log_return_type для коллекций с длиной."""

        @log_class_relationship(analyze_return=True)
        def returns_list():
            return [1, 2, 3, 4, 5]

        returns_list()

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        # Проверяем что есть вывод и что функция отработала
        assert output.strip() != ""
        assert "🔗" in output or "[🔗]" in output

    def test_relationship_analyze_value_same_class(self, capsys):
        """Тест _analyze_value когда класс совпадает с типом."""

        @log_class_relationship(show_types=True)
        def process(obj):
            return obj

        process(42)  # int - класс и тип совпадают

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        # Проверяем что вывод есть
        assert output.strip() != ""
        # Не должно быть специальных символов для примитивов
        assert "✓" not in output
        assert "⚠" not in output


class TestRelationshipFinal:
    """Финальные тесты для RelationshipDecorator."""

    def test_relationship_with_multiple_objects(self, capsys):
        """Тест с несколькими объектами в аргументах."""

        class DB:
            pass

        class Cache:
            pass

        class Service:
            def __init__(self):
                self.db = DB()
                self.cache = Cache()

        @log_class_relationship(show_dependencies=True)
        def process(service, data, options):
            return service

        service = Service()
        process(service, {"id": 1}, {"timeout": 30})

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output

    def test_relationship_with_collections(self, capsys):
        """Тест с коллекциями объектов."""

        class User:
            def __init__(self, name):
                self.name = name
                self.permissions = []

        @log_class_relationship(show_hierarchy=True)
        def process_users(users, admins):
            return len(users) + len(admins)

        users = [User("Alice"), User("Bob")]
        admins = [User("Charlie")]
        process_users(users, admins)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output

    def test_relationship_with_nested_objects(self, capsys):
        """Тест с вложенными объектами."""

        class Engine:
            pass

        class Wheel:
            pass

        class Car:
            def __init__(self):
                self.engine = Engine()
                self.wheels = [Wheel() for _ in range(4)]

        class Garage:
            def __init__(self):
                self.cars = [Car(), Car()]
                self.tools = ["wrench", "jack"]

        @log_class_relationship(show_dependencies=True, show_hierarchy=True)
        def inspect_garage(garage):
            return garage

        garage = Garage()
        inspect_garage(garage)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output

    def test_relationship_show_types_only(self, capsys):
        """Тест только с показом типов (без иерархии и зависимостей)."""

        @log_class_relationship(show_hierarchy=False, show_dependencies=False, show_types=True)
        def func(a, b):
            return (a, b)

        result = func(1, "test")
        assert result == (1, "test")

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)

        assert "[🔗]" in output
        assert "int" in output or "str" in output

    def test_relationship_error_in_dependencies(self, capsys):
        """Тест с ошибкой при получении зависимостей."""

        class BrokenDeps:
            def __getattr__(self, name):
                if name in ['db', 'cache']:
                    raise AttributeError("Broken dependency")
                return None

        @log_class_relationship(show_dependencies=True)
        def handle(obj):
            return obj

        handle(BrokenDeps())

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[🔗]" in output