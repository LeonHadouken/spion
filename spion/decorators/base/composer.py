# spion/decorators/base/composer.py

"""
Композитор для применения нескольких декораторов одновременно.
"""

from typing import Callable
from functools import wraps


class DecoratorComposer:
    """
    Композитор декораторов для применения нескольких декораторов одновременно.
    """

    def __init__(self, *decorators):
        self.decorators = decorators

    def __call__(self, func: Callable) -> Callable:
        for decorator in reversed(self.decorators):
            func = decorator(func)
        return func

    def __repr__(self) -> str:
        return f"DecoratorComposer({self.decorators})"