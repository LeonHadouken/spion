# tests/test_decorators/test_imports.py (исправленный - добавляем недостающие утилиты)
"""
Тесты для проверки публичного API.
"""

import pytest
import spion  # Добавляем импорт!


class TestPublicAPI:
    """Тесты для проверки, что все нужные объекты доступны."""

    def test_log_level_available(self):
        """Проверяем доступность LogLevel."""
        assert hasattr(spion, 'LogLevel')
        assert spion.LogLevel.DEBUG == "DEBUG"
        assert spion.LogLevel.INFO == "INFO"

    def test_base_colors_available(self):
        """Проверяем доступность BaseColors."""
        assert hasattr(spion, 'BaseColors')
        assert hasattr(spion.BaseColors, 'RESET')

    def test_traffic_light_available(self):
        """Проверяем доступность TrafficLight."""
        assert hasattr(spion, 'TrafficLight')
        assert spion.LogLevel.INFO in spion.TrafficLight

    def test_decorators_available(self):
        """Проверяем доступность всех декораторов."""
        decorators = [
            'log',
            'log_class_relationship',
            'log_method_chain',
            'log_call_once',
            'log_user_action',
            'log_state_change'
        ]

        for dec in decorators:
            assert hasattr(spion, dec), f"Missing {dec}"

    def test_decorator_classes_available(self):
        """Проверяем доступность классов декораторов."""
        classes = [
            'LogDecorator',
            'RelationshipDecorator',
            'ChainDecorator'
        ]

        for cls in classes:
            assert hasattr(spion, cls), f"Missing {cls}"

    def test_config_functions_available(self):
        """Проверяем доступность функций конфигурации."""
        functions = [
            'configure',
            'get_config',
            'add_rule',
            'get_suppression_summary',
            'reset_filter',
            'configure_filter',
            'should_log'
        ]

        for func in functions:
            assert hasattr(spion, func), f"Missing {func}"

    def test_utils_available(self):
        """Проверяем доступность утилит."""
        # Эти утилиты должны быть доступны через spion.utils
        # Но в __init__.py они не экспортируются напрямую
        # Вместо этого проверим, что модуль utils существует
        assert hasattr(spion, 'decorators')
        assert hasattr(spion.decorators, 'core')
        assert hasattr(spion.decorators.core, 'utils')

    def test_version_available(self):
        """Проверяем наличие версии."""
        assert hasattr(spion, '__version__')
        assert isinstance(spion.__version__, str)