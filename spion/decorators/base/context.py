# spion/decorators/base/context.py

"""
Контекстный менеджер для временного отключения логирования.
"""

from ...config import configure, get_config


class disable_logging:
    """
    Контекстный менеджер для временного отключения логирования.

    Example:
        >>> with disable_logging():
        ...     noisy_function()  # Не будет логироваться
    """

    def __enter__(self):
        self.old_config = get_config('enabled')
        configure(enabled=False)
        return self

    def __exit__(self, *args):
        configure(enabled=self.old_config)