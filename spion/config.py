# spion/config.py
"""
Конфигурация отладки и логирования.
"""

from typing import Dict, Any, Optional


# Уровни логирования
class LogLevel:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# Базовые цвета
class BaseColors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BLUE = '\033[94m'  # Для временных меток
    PURPLE = '\033[95m'  # Для системных вызовов
    YELLOW = '\033[93m'  # Для предупреждений
    RED = '\033[91m'  # Для ошибок
    GREEN = '\033[92m'  # Для информации
    CYAN = '\033[96m'  # Для отладки


# Светофор - словарь с цветами для разных уровней
TrafficLight = {
    # Красный - опасность, ошибки
    LogLevel.ERROR: {'color': BaseColors.RED, 'emoji': '🔴', 'name': 'ОШИБКА'},
    LogLevel.CRITICAL: {'color': f'{BaseColors.RED}{BaseColors.BOLD}', 'emoji': '💥', 'name': 'КРИТИЧНО'},

    # Желтый - внимание, предупреждения
    LogLevel.WARNING: {'color': BaseColors.YELLOW, 'emoji': '🟡', 'name': 'ПРЕДУПРЕЖДЕНИЕ'},

    # Зеленый - все хорошо, информация
    LogLevel.INFO: {'color': BaseColors.GREEN, 'emoji': '🟢', 'name': 'ИНФО'},

    # Синий - отладка
    LogLevel.DEBUG: {'color': BaseColors.CYAN, 'emoji': '🔵', 'name': 'ОТЛАДКА'},
}

# Глобальная конфигурация
_config = {
    'enabled': True,
    'min_level': LogLevel.DEBUG,
    'show_timestamp': True,
    'timestamp_format': "%H:%M:%S.%f",
    'color_enabled': True,
}


def configure(**kwargs) -> None:
    """
    Настроить глобальную конфигурацию логирования.

    Args:
        enabled: Включить/выключить логирование
        min_level: Минимальный уровень для логирования
        show_timestamp: Показывать временные метки
        timestamp_format: Формат временных меток
        color_enabled: Включить цветной вывод
    """
    global _config
    for key, value in kwargs.items():
        if key in _config:
            _config[key] = value


def get_config(key: str, default: Any = None) -> Any:
    """Получить значение конфигурации."""
    return _config.get(key, default)


def should_log(level: str) -> bool:
    """Проверить, нужно ли логировать уровень."""
    if not _config['enabled']:
        return False

    levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING,
              LogLevel.ERROR, LogLevel.CRITICAL]

    try:
        min_idx = levels.index(_config['min_level'])
        current_idx = levels.index(level)
        return current_idx >= min_idx
    except ValueError:
        return True