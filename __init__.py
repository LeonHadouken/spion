# debug/__init__.py
"""
Пакет для отладки и диагностики приложения.
Предоставляет декораторы для логирования, отслеживания связей и цепочек вызовов.
"""

from .config import LogLevel, BaseColors, TrafficLight, configure, get_config
from .filters import LogFilter, add_rule, get_suppression_summary, reset_filter, configure_filter, should_log
from .utils import get_timestamp, log_message, format_signature, format_value, get_class_hierarchy, \
    get_object_dependencies
from .decorators import (
    log,
    log_class_relationship,
    log_method_chain,
    log_call_once,
    log_user_action,
    log_state_change,
    LogDecorator,
    RelationshipDecorator,
    ChainDecorator
)

__all__ = [
    # Основные классы
    'LogLevel',
    'BaseColors',
    'TrafficLight',
    'LogFilter',

    # Декораторы
    'log',
    'log_class_relationship',
    'log_method_chain',
    'log_call_once',
    'log_user_action',
    'log_state_change',

    # Классы декораторов
    'LogDecorator',
    'RelationshipDecorator',
    'ChainDecorator',

    # Функции управления
    'configure',
    'get_config',
    'add_rule',
    'get_suppression_summary',
    'reset_filter',
    'configure_filter',  # ← ДОБАВЛЕНО!
    'should_log',  # ← ДОБАВЛЕНО!

    # Утилиты
    'get_timestamp',
    'log_message',
    'format_signature',
    'format_value',
    'get_class_hierarchy',
    'get_object_dependencies',
]

__version__ = '1.0.0'