# spion/decorators/core/filtering.py (расширенная версия)

"""
Фильтрация вызовов для логирования.
"""

from typing import Optional, Callable, Pattern, Dict, Set, Any
import re
from datetime import datetime, timedelta
from ...config import get_config


class SuppressionRule:
    """Правило подавления логов."""

    def __init__(self, pattern: str, call_type: str = "call",
                 max_calls: int = 1, log_once: bool = True,
                 time_window: Optional[int] = None):
        self.pattern = re.compile(pattern)
        self.call_type = call_type
        self.max_calls = max_calls
        self.log_once = log_once
        self.time_window = time_window
        self.count = 0
        self.last_logged = None


class CallFilter:
    """
    Фильтр для вызовов функций с поддержкой подавления.
    """

    def __init__(self, include_patterns: Optional[list] = None,
                 exclude_patterns: Optional[list] = None):
        """
        Инициализация фильтра.

        Args:
            include_patterns: Паттерны для включения
            exclude_patterns: Паттерны для исключения
        """
        self.include = [re.compile(p) for p in (include_patterns or [])]
        self.exclude = [re.compile(p) for p in (exclude_patterns or [])]

        # Подавление повторений
        self.suppress_repetitive = True
        self.max_repetitions = 5
        self.suppression_window = 60  # секунд
        self.show_suppression_summary = True

        # Состояние
        self._logged_calls: Dict[str, Set[str]] = {
            'call': set(),
            'relationship': set(),
            'chain': set()
        }
        self._counters: Dict[str, int] = {}
        self._timestamps: Dict[str, datetime] = {}
        self._rules: Dict[str, SuppressionRule] = {}

    def add_rule(self, pattern: str, call_type: str = "call",
                 max_calls: int = 1, log_once: bool = True,
                 time_window: Optional[int] = None) -> None:
        """
        Добавить правило фильтрации.
        """
        self._rules[pattern] = SuppressionRule(
            pattern, call_type, max_calls, log_once, time_window
        )

    def should_log(self, signature: str, call_type: str) -> bool:
        """
        Проверить, нужно ли логировать вызов.
        """
        # Проверяем глобальную настройку
        if not get_config('enabled', True):
            return False

        # Проверяем exclude паттерны
        for pattern in self.exclude:
            if pattern.search(signature) or pattern.search(call_type):
                return False

        # Проверяем правила подавления
        for rule in self._rules.values():
            if rule.pattern.search(signature) and rule.call_type == call_type:
                return self._check_rule(rule, signature)

        # Подавление повторений для отношений и цепочек
        if call_type in ('relationship', 'chain'):
            if signature in self._logged_calls[call_type]:
                return False
            self._logged_calls[call_type].add(signature)
            return True

        # Подавление повторяющихся вызовов
        if call_type == "call" and self.suppress_repetitive:
            self._increment_counter(signature)
            return self._counters[signature] <= self.max_repetitions

        # Если есть include паттерны, проверяем их
        if self.include:
            for pattern in self.include:
                if pattern.search(signature) or pattern.search(call_type):
                    return True
            return False

        # По умолчанию разрешаем
        return True

    def _check_rule(self, rule: SuppressionRule, signature: str) -> bool:
        """Проверить правило подавления."""
        now = datetime.now()

        # Проверка временного окна
        if rule.time_window and rule.last_logged:
            time_diff = (now - rule.last_logged).total_seconds()
            if time_diff < rule.time_window:
                # Время еще не прошло - подавляем
                self._increment_counter(signature)
                return False
            else:
                # Время окна истекло - сбрасываем счетчик для этого правила
                rule.count = 0
                rule.last_logged = None  # Важно! Сбрасываем last_logged

        # Увеличиваем счетчик
        rule.count += 1
        rule.last_logged = now

        # Проверка на один раз (log_once)
        if rule.log_once and rule.count > 1:
            self._increment_counter(signature)
            return False

        # Проверка максимального количества
        if rule.count > rule.max_calls:
            self._increment_counter(signature)
            return False

        return True

    def _increment_counter(self, key: str) -> None:
        """Увеличить счетчик подавленных вызовов."""
        self._counters[key] = self._counters.get(key, 0) + 1

    def get_suppression_summary(self) -> Dict[str, int]:
        """
        Получить сводку по подавленным вызовам.
        """
        return {k: v for k, v in self._counters.items()
                if v > self.max_repetitions}

    def reset(self) -> None:
        """Сбросить состояние фильтра."""
        for s in self._logged_calls.values():
            s.clear()
        self._counters.clear()
        self._timestamps.clear()
        self._rules.clear()


# Глобальный фильтр по умолчанию
_default_filter = CallFilter()


# spion/decorators/core/filtering.py
def should_log_call(signature: str, call_type: str) -> bool:
    """
    Проверить, нужно ли логировать вызов (использует глобальный фильтр).
    """
    return _default_filter.should_log(signature, call_type)

def configure_filter(include_patterns: Optional[list] = None,
                     exclude_patterns: Optional[list] = None,
                     suppress_repetitive: Optional[bool] = None,
                     max_repetitions: Optional[int] = None,
                     suppression_window: Optional[int] = None) -> None:
    """
    Настроить глобальный фильтр.
    """
    global _default_filter

    if include_patterns is not None or exclude_patterns is not None:
        _default_filter = CallFilter(include_patterns, exclude_patterns)

    if suppress_repetitive is not None:
        _default_filter.suppress_repetitive = suppress_repetitive
    if max_repetitions is not None:
        _default_filter.max_repetitions = max_repetitions
    if suppression_window is not None:
        _default_filter.suppression_window = suppression_window


def add_rule(pattern: str, **kwargs) -> None:
    """Добавить правило фильтрации."""
    _default_filter.add_rule(pattern, **kwargs)


def get_suppression_summary() -> Dict[str, int]:
    """Получить сводку по подавленным вызовам."""
    return _default_filter.get_suppression_summary()


def reset_filter() -> None:
    """Сбросить фильтр."""
    _default_filter.reset()