"""
Тесты для проверки публичного API.
"""

import pytest
import debug


class TestPublicAPI:
    """Тесты для проверки, что все нужные объекты доступны."""

    def test_log_level_available(self):
        """Проверяем доступность LogLevel."""
        assert hasattr(debug, 'LogLevel')
        assert debug.LogLevel.DEBUG == "DEBUG"
        assert debug.LogLevel.INFO == "INFO"

    def test_base_colors_available(self):
        """Проверяем доступность BaseColors."""
        assert hasattr(debug, 'BaseColors')
        assert hasattr(debug.BaseColors, 'RESET')

    def test_traffic_light_available(self):
        """Проверяем доступность TrafficLight."""
        assert hasattr(debug, 'TrafficLight')
        assert debug.LogLevel.INFO in debug.TrafficLight

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
            assert hasattr(debug, dec), f"Missing {dec}"

    def test_decorator_classes_available(self):
        """Проверяем доступность классов декораторов."""
        classes = [
            'LogDecorator',
            'RelationshipDecorator',
            'ChainDecorator'
        ]

        for cls in classes:
            assert hasattr(debug, cls), f"Missing {cls}"

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
            assert hasattr(debug, func), f"Missing {func}"

    def test_utils_available(self):
        """Проверяем доступность утилит."""
        utils = [
            'get_timestamp',
            'log_message',
            'format_signature',
            'format_value',
            'get_class_hierarchy',
            'get_object_dependencies'
        ]

        for util in utils:
            assert hasattr(debug, util), f"Missing {util}"

    def test_version_available(self):
        """Проверяем наличие версии."""
        assert hasattr(debug, '__version__')
        assert isinstance(debug.__version__, str)