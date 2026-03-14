# filters.py
"""
Фильтры для подавления повторяющихся логов.
"""

from typing import Dict, Set, Optional, Any
from datetime import datetime, timedelta


class LogFilter:
    """
    Фильтр для логирования с поддержкой различных стратегий подавления.
    Реализует паттерн Singleton.
    """

    _instance = None
    _state: Dict[str, Set[str]] = {
        'logged': set(),
        'relationship': set(),
        'chain': set()
    }
    _counters: Dict[str, int] = {}
    _timestamps: Dict[str, datetime] = {}
    _rules: Dict[str, Dict] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.suppress_repetitive = True
        self.max_repetitions = 5
        self.suppression_window = 60  # секунд
        self.show_suppression_summary = True

    def add_rule(self, pattern: str, rule_type: str = "call",
                 max_calls: int = 1, log_once: bool = True,
                 time_window: Optional[int] = None) -> None:
        """
        Добавить правило фильтрации.

        Args:
            pattern: Шаблон для поиска
            rule_type: Тип вызова (call, relationship, chain)
            max_calls: Максимальное количество вызовов
            log_once: Логировать только один раз
            time_window: Временное окно в секундах
        """
        self._rules[pattern] = {
            'type': rule_type,
            'max_calls': max_calls,
            'log_once': log_once,
            'time_window': time_window,
            'count': 0
        }

    def should_log(self, key: str, call_type: str = "call") -> bool:
        """
        Проверить, нужно ли логировать вызов.

        Returns:
            True если нужно логировать, False если подавить
        """
        now = datetime.now()

        # Проверка правил
        for pattern, rule in self._rules.items():
            if pattern in key and rule['type'] == call_type:
                rule['count'] += 1

                # Проверка временного окна
                if rule['time_window']:
                    last = self._timestamps.get(key)
                    if last and (now - last).seconds < rule['time_window']:
                        self._increment_counter(key)
                        return False
                    self._timestamps[key] = now

                # Проверка на один раз
                if rule['log_once'] and rule['count'] > 1:
                    self._increment_counter(key)
                    return False

                # Проверка максимального количества
                if rule['count'] > rule['max_calls']:
                    self._increment_counter(key)
                    return False

                return True

        # Подавление повторений для отношений и цепочек
        if call_type in ('relationship', 'chain'):
            if key in self._state[call_type]:
                return False
            self._state[call_type].add(key)
            return True

        # Подавление повторяющихся вызовов
        if call_type == "call" and self.suppress_repetitive:
            self._increment_counter(key)
            return self._counters[key] <= self.max_repetitions

        return True

    def _increment_counter(self, key: str) -> None:
        """Увеличить счетчик подавленных вызовов."""
        self._counters[key] = self._counters.get(key, 0) + 1

    def get_summary(self) -> Dict[str, int]:
        """
        Получить сводку по подавленным вызовам.

        Returns:
            Словарь {ключ: количество подавлений}
        """
        return {k: v for k, v in self._counters.items()
                if v > self.max_repetitions}

    def reset(self) -> None:
        """Сбросить состояние фильтра."""
        for s in self._state.values():
            s.clear()
        self._counters.clear()
        self._timestamps.clear()
        self._rules.clear()


# Глобальный экземпляр фильтра
_filter = LogFilter()


# Функции для работы с фильтром

def add_rule(pattern: str, **kwargs) -> None:
    """Добавить правило фильтрации."""
    _filter.add_rule(pattern, **kwargs)


def should_log(key: str, call_type: str = "call") -> bool:
    """Проверить, нужно ли логировать."""
    return _filter.should_log(key, call_type)


def get_suppression_summary() -> Dict[str, int]:
    """Получить сводку по подавленным вызовам."""
    return _filter.get_summary()


def reset_filter() -> None:
    """Сбросить фильтр."""
    _filter.reset()


def configure_filter(**kwargs) -> None:
    """Настроить фильтр."""
    for key, value in kwargs.items():
        if hasattr(_filter, key):
            setattr(_filter, key, value)