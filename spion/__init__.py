# spion/__init__.py (исправленный - добавляем light и silent)
"""
Пакет для отладки и диагностики приложения.
"""
from .decorators.base.context import disable_logging
from .config import LogLevel, BaseColors, TrafficLight, configure, get_config
from .decorators.core.filtering import (
    should_log_call as should_log,
    add_rule,
    get_suppression_summary,
    reset_filter,
    configure_filter,
    CallFilter as LogFilter
)
from .decorators import (
    # Основные декораторы
    log,
    log_class_relationship,
    log_method_chain,
    log_call_once,
    log_user_action,
    log_state_change,

    # Классы
    LogDecorator,
    RelationshipDecorator,
    ChainDecorator,

    # Синтаксический сахар ✨
    watch, trace, light, silent,  # добавили light и silent
    user, state, throttle,
    spy
)

__all__ = [
    # Основные классы
    'LogLevel',
    'BaseColors',
    'TrafficLight',
    'LogFilter',

    # Основные декораторы
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

    # Синтаксический сахар ✨
    'watch',  # @watch() — следить за функцией
    'trace',  # @trace() — трассировка цепочек
    'light',  # @light() — лёгкое логирование
    'silent',  # @silent() — только ошибки
    'user',  # @user() — действия пользователя
    'state',  # @state() — изменения состояния
    'throttle',  # @throttle() — ограничение по частоте
    'spy',  # @spy() — комбо-декоратор

    # Контекстный менеджер
    'disable_logging',

    # Функции управления
    'configure',
    'get_config',
    'should_log',
    'add_rule',
    'get_suppression_summary',
    'reset_filter',
    'configure_filter',
]

__version__ = '1.0.0'