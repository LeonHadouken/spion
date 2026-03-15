# spion/decorators/base/metadata.py

"""
Декоратор для добавления метаданных к функциям.
"""

from functools import wraps
from typing import Callable
from datetime import datetime


def with_metadata(func: Callable) -> Callable:
    """
    Декоратор для добавления метаданных к функции.

    Args:
        func: Функция для декорирования

    Returns:
        Callable: Функция с дополнительными метаданными

    Example:
        >>> @with_metadata
        ... def test():
        ...     '''Docstring'''
        ...     pass
        >>> test.__metadata__['decorated_at']
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Добавляем метаданные
    wrapper.__metadata__ = {
        'decorated_at': datetime.now().isoformat(),
        'original_name': func.__name__,
        'original_module': func.__module__,
        'original_doc': func.__doc__,
    }

    return wrapper