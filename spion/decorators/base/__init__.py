# spion/decorators/base/__init__.py (исправленный)
"""
Базовые классы и утилиты для декораторов.
"""

from .decorator import LoggerDecorator
from .composer import DecoratorComposer
from .metadata import with_metadata
from .context import disable_logging

__all__ = [
    'LoggerDecorator',
    'DecoratorComposer',
    'with_metadata',
    'disable_logging',
]