# spion/decorators/__init__.py (исправленный - добавляем light и silent)
"""
Декораторы для логирования и отладки.
"""

from .simple import (
    LogDecorator, log, log_call_once, log_user_action, log_state_change,
    # Синтаксический сахар
    watch, light, silent,  # добавили light и silent
    user, state, throttle,
    spy
)
from .chain import ChainDecorator, log_method_chain, trace
from .relationship import RelationshipDecorator, log_class_relationship

__all__ = [
    # Классы декораторов
    'LogDecorator',
    'RelationshipDecorator',
    'ChainDecorator',

    # Основные декораторы
    'log',
    'log_class_relationship',
    'log_method_chain',
    'log_call_once',
    'log_user_action',
    'log_state_change',

    # Синтаксический сахар ✨
    'watch',    # следить за функцией
    'trace',    # трассировка цепочек
    'light',    # лёгкое логирование
    'silent',   # только ошибки
    'user',     # действия пользователя
    'state',    # изменения состояния
    'throttle', # ограничение по частоте
    'spy',      # комбо-декоратор
]