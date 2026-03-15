<div align="center" style="font-family: 'Courier New', Courier, monospace; width: 100%; max-width: 720px; margin: 0 auto;">
<pre style="background: #0A0A0A; color: #32CD32; padding: 15px; border: 2px solid #1E90FF; border-radius: 8px; overflow-x: auto; white-space: pre; font-size: 13px; line-height: 1.3;">
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██████╗ ██╗ ██████╗ ███╗   ██╗                           v0.1.0    ║
║   ██╔════╝██╔══██╗██║██╔═══██╗████╗  ██║                                     ║
║   ███████╗██████╔╝██║██║   ██║██╔██╗ ██║    Sehen alles, stören nichts.      ║
║   ╚════██║██╔═══╝ ██║██║   ██║██║╚██╗██║  — Видит всё, не мешает ничему —    ║
║   ███████║██║     ██║╚██████╔╝██║ ╚████║                                     ║
║   ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
</pre>
</div>

<p align="center">
  <i>Собрано на современном стеке Arch + Omarchy для максимальной производительности</i>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7%2B-green?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/status-stable-brightgreen?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/tests-172%20passed-success?style=for-the-badge" alt="Tests">
</p>


<p align="center">
  <i>"Sehen alles, stören nichts."</i><br>
  <b>— Видит всё, не мешает ничему.</b>
</p>


<p align="center">
  <a href="#установка" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#1E90FF; border:2px solid #1E90FF; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[📦] УСТАНОВКА</a>
  <a href="#для-тех-кто-ценит-простоту" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#32CD32; border:2px solid #32CD32; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[✨] ПРОСТОТА</a>
  <a href="#для-тех-кто-не-упускает-деталей" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#FFA500; border:2px solid #FFA500; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[🔍] ДЕТАЛИ</a>
  <a href="#многоликий-spion" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#FF69B4; border:2px solid #FF69B4; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[🎭] МНОГОЛИКИЙ</a>
  <a href="#структура-проекта" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#00BFFF; border:2px solid #00BFFF; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[📁] СТРУКТУРА</a>
  <br>
  <a href="#тестирование" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#32CD32; border:2px solid #32CD32; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[✅] ТЕСТЫ</a>
  <a href="#конфигурация" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#FFA500; border:2px solid #FFA500; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[⚙️] КОНФИГУРАЦИЯ</a>
  <a href="#полное-руководство" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#1E90FF; border:2px solid #1E90FF; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[📚] ГАЙД</a>
  <a href="#синтаксический-сахар" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#FF69B4; border:2px solid #FF69B4; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[🍬] САХАР</a>
  <a href="#требования" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#00BFFF; border:2px solid #00BFFF; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[📋] ТРЕБОВАНИЯ</a>
  <a href="#дорожная-карта" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#FF4500; border:2px solid #FF4500; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[🗺️] ROADMAP</a>
  <a href="#лицензия" style="display:inline-block; padding:10px 20px; margin:5px; background:#0A0A0A; color:#32CD32; border:2px solid #32CD32; text-decoration:none; border-radius:0px; font-family:'JetBrains Mono', 'Fira Code', monospace; font-weight:bold;">[📄] ЛИЦЕНЗИЯ</a>
</p>

---

## <a name="установка"></a>Установка (Скоро на PyPI)

```bash
pip install spion
```

Или если хочешь прямо сейчас самое свежее (разрабская версия):

```bash
pip install git+https://github.com/yourname/spion.git
```

---

## <a name="для-тех-кто-ценит-простоту"></a>Для тех, кто ценит простоту spion.<span style="float:right;"><a href="#spion">⬆️</a></span>
```python
from spion import log

@log()
def hello():
    return "world"

hello()
# [14:30:25.123] ▶️ Вызов hello
```

> #### Одна строчка — и ты уже знаешь, что функция вызвалась. Никакой магии, никакой боли. Просто работает.

---

## <a name="для-тех-кто-не-упускает-деталей"></a>Для тех, кто не упускает деталей spion.<span style="float:right;"><a href="#spion">⬆️</a></span>

А когда простого лога мало — Spion достаёт тяжёлую артиллерию:

```python
from spion import log_method_chain, log_class_relationship, log_state_change

@log_method_chain(max_depth=10)
@log_class_relationship()
@log_state_change()
def complex_operation(self, data):
    # Теперь ты видишь ВСЁ
    pass
```

| | Хочешь... | Используй | Сахар 🍬 | Пример вывода |
|-|-----------|-----------|----------|---------------|
| 🔍 | Увидеть рекурсию | `@log_method_chain()` | `@trace()` | `[↘️] fib(3) (depth=1)` |
| 🏛️ | Иерархию классов | `@log_class_relationship()` | — | `📊 Иерархия: Dog -> Animal -> object` |
| 🔄 | Изменения состояния | `@log_state_change()` | `@state()` | `[🔄] switch | Ход: white` |
| ⏱️ | Логи без спама | `@log_call_once()` | `@throttle()` | `[🔄] poll (интервал=2с)` |
| 👤 | Действия пользователя | `@log_user_action()` | `@user()` | `[👤] click на E5` |
| 👁️ | Просто о вызове | `@log()` | `@watch()` | `▶️ Вызов hello` |
| 💡 | Только вход | `@log(level=LogLevel.INFO)` | `@light()` | `▶️ fast_operation` |
| 🤫 | Только ошибки | `@log(level=LogLevel.ERROR)` | `@silent()` | `[❌] risky: ошибка` |
| 🎭 | Всё сразу | комбинация | `@spy()` | Всё вышеперечисленное |
---

## <a name="многоликий-spion"></a>Многоликий Spion spion.<span style="float:right;"><a href="#spion">⬆️</a></span>

| Уровень | Декоратор | Что внутри                    |
|---------|-----------|-------------------------------|
| 🟢 **Новичок** | `@log()` | *Просто "пинг" о вызове*      |
| 🔵 **Любитель** | `@log_call_once()` | *Логи с интервалом*           |
| 🟡 **Опытный** | `@log_user_action()` | *Действия пользователя*       |
| 🟠 **Профи** | `@log_state_change()` | *Изменения состояния*         |
| 🔴 **Мастер** | `@log_class_relationship()` | *Связи между классами*        |
| ⚫ **Гуру** | `@log_method_chain()` | *Цепочки вызовов с отступами* |

- *Начинающим* — `@log()` и порядок.  
- *Профессионалам* — `@log_method_chain(max_depth=20)` и полный контроль.

> ***Spion не заставляет выбирать между простотой и глубиной. Он даёт и то, и другое. Бери то, что нужно именно сейчас.***

---

## <a name="структура-проекта"></a>Структура проекта spion.<span style="float:right;"><a href="#spion">⬆️</a></span>

```
spion/
├── __init__.py              # Публичный API библиотеки
├── config.py                 # Конфигурация и уровни логирования
├── filters.py                # Обёртка для фильтров (обратная совместимость)
├── decorators/
│   ├── __init__.py           # Экспорт всех декораторов
│   ├── base/
│   │   ├── __init__.py
│   │   ├── decorator.py      # Базовый класс LoggerDecorator
│   │   ├── composer.py       # Композитор декораторов
│   │   ├── metadata.py       # Добавление метаданных
│   │   └── context.py        # Контекстный менеджер отключения логирования
│   ├── core/
│   │   ├── __init__.py
│   │   ├── stats.py          # Статистика вызовов
│   │   ├── signature.py      # Форматирование сигнатур
│   │   ├── context.py        # Контекст вызова
│   │   ├── filtering.py      # Фильтрация вызовов
│   │   └── utils.py          # Утилиты логирования
│   ├── simple.py              # Простые декораторы (log, log_call_once, и т.д.)
│   ├── chain.py               # Декоратор для цепочек вызовов
│   └── relationship.py        # Декоратор для связей между классами
tests/
├── __init__.py
├── conftest.py                # Фикстуры pytest
├── test_config.py             # Тесты конфигурации
├── test_context_manager.py    # Тесты отключения внутри рабочего пространства
├── test_config_environments.py # Тесты окружений
├── test_filters.py            # Тесты фильтров
├── test_real_integration.py   # Реальные интеграционные тесты
├── test_utils.py              # Тесты утилит
├── test_simple.py             # Простые тесты
├── test_with_capsys.py        # Тесты с фикстурой capsys
├── test_minimal.py            # Минимальные тесты
└── test_decorators/
    ├── test_base.py           # Тесты базового декоратора
    ├── test_chain.py          # Тесты цепочек вызовов
    ├── test_imports.py        # Тесты публичного API
    ├── test_integration.py    # Интеграционные тесты
    ├── test_relationship.py   # Тесты связей между классами
    ├── test_sugar.py          # Тесты сахара
    └── test_simple.py         # Тесты простых декораторов
```

---

## <a name="тестирование"></a>Тестирование <span style="float:right;"><a href="#spion">⬆️</a></span>
Spion имеет **полное тестовое покрытие** — **172 теста**, которые проверяют каждый уголок библиотеки.

👉 **[Подробный отчёт о тестировании](TEST_LOG.md)**

[![Tests](https://img.shields.io/badge/tests-172%20passed-32CD32?style=for-the-badge&logo=pytest&logoColor=white)](TEST_LOG.md)
[![Time](https://img.shields.io/badge/time-4.42s-1E90FF?style=for-the-badge&logo=clockify&logoColor=white)](TEST_LOG.md)
<img src="https://img.shields.io/badge/Built%20on-OMARCHY-FF6B6B?style=for-the-badge&logo=arch-linux&logoColor=white&labelColor=0A0A0A" alt="Built on Omarchy">
### Запуск тестов

```bash
# Установка зависимостей для тестирования
pip install pytest flask

# Запуск всех тестов
pytest tests/ -v

# Запуск с кратким отчётом
pytest tests/ --tb=short

# Запуск конкретного файла
pytest tests/test_decorators/test_chain.py -v

# Запуск конкретного теста
pytest tests/test_decorators/test_sugar.py::TestTraceSugar::test_trace_basic -v
```
### Результаты тестирования

### Что тестируется:

| Категория                | Файл                          | Количество тестов | Что проверяется |
|--------------------------|-------------------------------|-------------------|------------------|
| **Конфигурация**         | `test_config.py`              | 13                | Уровни логирования, цвета, настройки |
| **Окружения**            | `test_config_environments.py` | 17                | Production, Development, Test конфигурации |
| **Фильтры**              | `test_filters.py`             | 11                | Подавление повторений, временные окна, правила |
| **Контекстный менеджер** | `test_context_manager.py`     | 6                 | Временное отключение логирования |
| **Утилиты**              | `test_utils.py`               | 15                | Форматирование, таймстампы, иерархии классов |
| **Базовый декоратор**    | `test_base.py`                | 12                | Наследование, сигнатуры, обработка ошибок |
| **Цепочки вызовов**      | `test_chain.py`               | 11                | Рекурсия, глубина, независимость вызовов |
| **Связи классов**        | `test_relationship.py`        | 11                | Иерархии, зависимости, типы аргументов |
| **Простые декораторы**   | `test_simple.py`              | 20                | Логирование, интервалы, действия пользователя |
| **Синтаксический сахар** | `test_sugar.py`               | 31                | Все алиасы: watch, trace, light, silent, user, state, throttle, spy |
| **Интеграция**           | `test_integration.py`         | 12                | Комбинации декораторов, фильтры, конфигурация |
| **Публичное API**        | `test_imports.py`             | 8                 | Доступность всех экспортируемых объектов |
| **Реальная интеграция**  | `test_real_integration.py`    | 5                 | Flask, сокеты, tkinter |

### Покрытие кода

```
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
spion/__init__.py                               24      0   100%
spion/config.py                                  46      0   100%
spion/decorators/__init__.py                     11      0   100%
spion/decorators/base/__init__.py                 4      0   100%
spion/decorators/base/composer.py                 9      0   100%
spion/decorators/base/context.py                  8      0   100%
spion/decorators/base/decorator.py               80      0   100%
spion/decorators/base/metadata.py                11      0   100%
spion/decorators/chain.py                        62      0   100%
spion/decorators/core/__init__.py                14      0   100%
spion/decorators/core/context.py                 24      0   100%
spion/decorators/core/filtering.py               86      0   100%
spion/decorators/core/signature.py               44      0   100%
spion/decorators/core/stats.py                   23      0   100%
spion/decorators/core/utils.py                   56      0   100%
spion/decorators/relationship.py                 94      0   100%
spion/decorators/simple.py                       98      0   100%
spion/filters.py                                  7      0   100%
----------------------------------------------------------------
TOTAL                                            701      0   100%
```

### Особые кейсы        <span style="float:right;"><a href="#spion">⬆️</a></span>

```python
# Рекурсия Фибоначчи — 5 вызовов, всё видно
@log_method_chain(max_depth=3)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

fib(3)
# [↘️] fib(3) (depth=1)
#   [↘️] fib(2) (depth=2)
#     [↘️] fib(1) (depth=3)
#     [↗️] fib(1) -> 1 (depth=3)
#     [↘️] fib(0) (depth=3)
#     [↗️] fib(0) -> 0 (depth=3)
#   [↗️] fib(2) -> 1 (depth=2)
#   [↘️] fib(1) (depth=2)
#   [↗️] fib(1) -> 1 (depth=2)
# [↗️] fib(3) -> 2 (depth=1)
```

```python
# Временное окно — 2 вызова, потом пауза
@log_call_once(interval=2.0)
def api_call():
    return "data"

for _ in range(5):
    api_call()  # Логируется только раз в 2 секунды
    time.sleep(0.5)
```

### Непрерывная интеграция <span style="float:right;"><a href="#spion">⬆️</a></span>

Проект использует **GitHub Actions** для автоматического запуска тестов при каждом пуше:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install pytest flask
        sudo apt-get update
        sudo apt-get install -y python3-tk
    - name: Run tests
      run: |
        pytest tests/ -v
```

> ✅ **Все 166 тестов проходят на всех поддерживаемых версиях Python (3.7-3.12)**

---

## <a name="конфигурация"></a>⚙️ Конфигурация — настрой под себя.<span style="float:right;"><a href="#spion">⬆️</a></span>

Spion даёт полный контроль над тем, **что**, **когда** и **как** логировать.

### Глобальная конфигурация

```python
from spion import configure, LogLevel

# Базовая настройка
configure(
    enabled=True,                    # Включить/выключить логирование
    min_level=LogLevel.INFO,          # Минимальный уровень для логирования
    show_timestamp=True,              # Показывать временные метки
    timestamp_format="%H:%M:%S.%f",   # Формат времени (с миллисекундами)
    color_enabled=True                # Цветной вывод
)
```

### Предустановленные конфигурации

#### 🏭 Production — только ошибки и предупреждения

```python
def setup_production():
    configure(
        enabled=True,
        min_level=LogLevel.WARNING,
        show_timestamp=True,
        color_enabled=False
    )
    configure_filter(
        suppress_repetitive=True,
        max_repetitions=3
    )
```

#### 🛠️ Development — максимум информации

```python
def setup_development():
    configure(
        enabled=True,
        min_level=LogLevel.DEBUG,
        show_timestamp=True,
        color_enabled=True,
        timestamp_format="%H:%M:%S.%f"
    )
    configure_filter(
        suppress_repetitive=False
    )
```

#### 🧪 Test — для юнит-тестов

```python
def setup_test():
    configure(
        enabled=True,
        min_level=LogLevel.DEBUG,
        show_timestamp=False,  # Без времени для стабильности
        color_enabled=False
    )
    configure_filter(
        suppress_repetitive=False
    )
```

### Динамическая конфигурация

Меняй настройки на лету:

```python
class DebugController:
    def __init__(self):
        self.debug_mode = False
    
    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
        
        if self.debug_mode:
            configure(min_level=LogLevel.DEBUG)
            configure_filter(suppress_repetitive=False)
            print("🔧 Debug mode ON")
        else:
            configure(min_level=LogLevel.INFO)
            configure_filter(suppress_repetitive=True)
            
            # Показываем статистику подавленных вызовов
            from spion import get_suppression_summary
            stats = get_suppression_summary()
            print(f"📊 Подавлено вызовов: {stats}")
            print("🔧 Debug mode OFF")
```

### Конфигурация через переменные окружения

```python
import os

def setup_by_environment():
    env = os.getenv('APP_ENV', 'development')
    
    configs = {
        'production': {
            'min_level': LogLevel.ERROR,
            'color_enabled': False,
            'suppress_repetitive': True,
            'max_repetitions': 3
        },
        'staging': {
            'min_level': LogLevel.WARNING,
            'color_enabled': True,
            'suppress_repetitive': True,
            'max_repetitions': 5
        },
        'development': {
            'min_level': LogLevel.DEBUG,
            'color_enabled': True,
            'suppress_repetitive': False,
            'max_repetitions': 100
        },
        'test': {
            'min_level': LogLevel.DEBUG,
            'color_enabled': False,
            'show_timestamp': False,
            'suppress_repetitive': False
        }
    }
    
    cfg = configs.get(env, configs['development'])
    
    configure(
        enabled=True,
        min_level=cfg['min_level'],
        show_timestamp=cfg.get('show_timestamp', True),
        color_enabled=cfg['color_enabled']
    )
    
    configure_filter(
        suppress_repetitive=cfg['suppress_repetitive'],
        max_repetitions=cfg['max_repetitions']
    )
    
    print(f"🔧 Logging configured for {env} environment")
```

### Фильтрация вызовов

```python
from spion import configure_filter, add_rule, reset_filter, get_suppression_summary

# Настройка глобальных фильтров
configure_filter(
    suppress_repetitive=True,     # Подавлять повторяющиеся вызовы
    max_repetitions=5,            # Максимум повторений до подавления
    show_suppression_summary=True  # Показывать статистику
)

# Добавление правил для конкретных функций
add_rule(
    pattern="health_check",        # Паттерн имени функции
    call_type="call",              # Тип вызова (call, chain, relationship)
    max_calls=10,                  # Максимум вызовов
    time_window=60,                # Временное окно в секундах
    log_once=False                 # Логировать только один раз
)

# Сброс всех фильтров
reset_filter()

# Получение статистики подавленных вызовов
stats = get_suppression_summary()
# {'health_check': 15, 'status': 3, ...}
```

### Временное отключение логирования

```python
from spion import disable_logging

with disable_logging():
    # Этот код не будет логироваться
    noisy_function()
    spammy_operation()
    
# Здесь логирование снова работает
```

### Полный пример конфигурации для разных сред

```python
# config.py
import os
from spion import configure, configure_filter, add_rule, LogLevel

class LoggingConfig:
    @staticmethod
    def load():
        env = os.getenv('APP_ENV', 'development')
        
        # Базовая конфигурация
        configure(
            enabled=True,
            min_level=LogLevel.INFO if env == 'production' else LogLevel.DEBUG,
            show_timestamp=True,
            color_enabled=env != 'production',
            timestamp_format="%H:%M:%S.%f" if env == 'development' else "%H:%M:%S"
        )
        
        # Настройка фильтров
        configure_filter(
            suppress_repetitive=env == 'production',
            max_repetitions=3 if env == 'production' else 10
        )
        
        # Специфичные правила
        if env == 'production':
            add_rule("health_check", max_calls=10, time_window=60)
            add_rule("metrics", log_once=True)
        elif env == 'development':
            add_rule("debug_*", max_calls=1000)
        
        print(f"✅ Logging configured for {env}")

# main.py
from config import LoggingConfig

LoggingConfig.load()
```

---

## <a name="полное-руководство"></a>Полное руководство spion.<span style="float:right;"><a href="#spion">⬆️</a></span>

**[GUIDE.md](GUIDE.md)** — это не документация к библиотеке. Это **тренажёр по чтению и отладке кода**. 60+ живых примеров, которые показывают:

- 🧠 **Как думать о рекурсии** — увидишь, как стек растёт и схлопывается
- 🔍 **Где прячутся баги** — спам-логи, неочевидные состояния, запутанные связи
- 🏗️ **Как связаны объекты** — иерархии, зависимости, композиция
- 🎮 **Как живой код работает под капотом** — от Flask до игрового движка

***Это не про Spion. Это **про тебя и твой код**.***

> 👉 **[ОТКРЫТЬ ПОЛНОЕ РУКОВОДСТВО →](GUIDE.md)** 👈

---

## <a name="синтаксический-сахар"></a>🍬 Синтаксический сахар — пиши код чище spion.<span style="float:right;"><a href="#spion">⬆️</a></span>

> Декораторы — это круто, но иногда хочется, чтобы код читался как естественный язык.  
> **Spion** даёт тебе синтаксический сахар для самых частых сценариев.

### 📋 Полная таблица сахара

| Сахар | Оригинал | Что делает |
|-------|----------|------------|
| `@watch()` | `@log()` | Следит за функцией — логирует каждый вызов |
| `@light()` | `@log(level=LogLevel.INFO)` | Лёгкое логирование — только вход |
| `@silent()` | `@log(level=LogLevel.ERROR)` | Тихий режим — только ошибки |
| `@trace(max_depth=5)` | `@log_method_chain(max_depth=5)` | Трассирует цепочки вызовов (рекурсия, стек) |
| `@user()` | `@log_user_action()` | Отслеживает действия пользователя |
| `@state()` | `@log_state_change()` | Логирует изменения состояния объекта |
| `@throttle(interval=2.0)` | `@log_call_once(interval=2.0)` | Ограничивает частоту логов |
| `@spy(watch(), trace())` | `DecoratorComposer` | Комбинирует несколько декораторов |

---

### 🕵️ `@watch()` — просто следить

Самый простой способ понять, что функция вызвалась.

```python
from spion import watch

@watch()
def greet(name):
    return f"Привет, {name}!"

greet("Анна")
# [14:30:25.123] ▶️ Вызов greet (вызов #1)
```

**Когда использовать:** Всегда, когда нужно быстро понять, вызывается ли функция.

---

### 💡 `@light()` — лёгкое логирование

Только вход в функцию, без аргументов и результата. Минимализм.

```python
from spion import light

@light()
def fast_operation():
    return 42

fast_operation()
# [14:30:25.123] ▶️ Вызов fast_operation
```

**Когда использовать:** Для высоконагруженных функций, где важен только факт вызова.

---

### 🤫 `@silent()` — только ошибки

Логирует только когда функция падает с исключением. В тихом режиме.

```python
from spion import silent

@silent()
def risky_business():
    if random.random() < 0.5:
        raise ValueError("Что-то пошло не так")
    return "OK"

risky_business()  # Логируется только при ошибке
# [14:30:25.123] [❌] risky_business: Что-то пошло не так (call #1)
```

**Когда использовать:** Для кода, который должен работать тихо, но оставлять след при падении.

---

### 🔍 `@trace()` — трассировка цепочек

Видит всю рекурсию. Каждый шаг — с отступом.

```python
from spion import trace

@trace(max_depth=5)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

factorial(3)
# [14:30:25.123] [↘️] factorial(3) (depth=1)
#   [↘️] factorial(2) (depth=2)
#     [↘️] factorial(1) (depth=3)
#     [↗️] factorial(1) -> 1 (depth=3)
#   [↗️] factorial(2) -> 2 (depth=2)
# [↗️] factorial(3) -> 6 (depth=1)
```

**Параметры:**
- `max_depth` — максимальная глубина трассировки (по умолчанию 5)

**Когда использовать:** Рекурсия, обход деревьев, сложные алгоритмы.

---

### 👤 `@user()` — действия пользователя

Автоматически конвертирует координаты в шахматную нотацию.

```python
from spion import user

class Position:
    def __init__(self, row, col):
        self.row = row  # 0-7
        self.col = col  # 0-7

class Game:
    @user()
    def click(self, position):
        print(f"Обработка клика")

game = Game()
game.click(Position(3, 4))  # row=3 -> 5, col=4 -> E
# [14:30:25.123] [👤] Game.click на E5 (row=3, col=4)
```

**Когда использовать:** GUI, игры, веб-интерфейсы — везде, где есть пользовательские действия.

---

### 🔄 `@state()` — изменения состояния

Видит, что изменилось в объекте после вызова метода.

```python
from spion import state
from enum import Enum

class Player(Enum):
    WHITE = "белые"
    BLACK = "черные"

class Game:
    def __init__(self):
        self.current_player = Player.WHITE
        self.move_count = 0
    
    @state()
    def switch_player(self):
        self.current_player = (
            Player.BLACK if self.current_player == Player.WHITE 
            else Player.WHITE
        )
        self.move_count += 1

game = Game()
game.switch_player()
# [14:30:25.123] [🔄] Game.switch_player | Ход: белые | Изменения: current_player: Player.WHITE -> Player.BLACK, move_count: 0 -> 1
```

**Когда использовать:** Игры, конечные автоматы, системы с состоянием.

---

### ⏱️ `@throttle()` — ограничение частоты

Логирует не чаще 1 раза в N секунд. Спасение от спама.

```python
from spion import throttle
import time

@throttle(interval=2.0)
def poll_sensor():
    return 42

for _ in range(5):
    print(poll_sensor())
    time.sleep(0.5)

# [14:30:25.123] [🔄] poll_sensor (интервал=2.0с)  # первый
# 42
# 42  # без лога
# 42  # без лога
# [14:30:27.123] [🔄] poll_sensor (интервал=2.0с)  # через 2 секунды
# 42
```

**Параметры:**
- `interval` — минимальный интервал между логами в секундах

**Когда использовать:** Мониторинг, polling API, часто вызываемые функции.

---

### 🎭 `@spy()` — комбо-декоратор

Объединяет несколько декораторов в один. Шпион видит всё.

```python
from spion import spy, watch, trace, user

@spy(
    watch(),                    # базовый лог
    trace(max_depth=3),         # трассировка
    user()                      # действия пользователя
)
def process_click(self, position, data):
    # Здесь будет логироваться всё сразу
    return result
```

**Когда использовать:** Когда нужно применить несколько декораторов к одной функции.

---

### 🎯 Сравнение сахара с оригиналами

| Сахар | Длина | Читаемость |
|-------|-------|------------|
| `@watch()` | 9 символов | 😊 Понятно сразу |
| `@log()` | 6 символов | 🙂 Тоже неплохо |
| `@trace(max_depth=5)` | 18 символов | 🔍 Очевидно про трассировку |
| `@log_method_chain(max_depth=5)` | 33 символа | 📚 Документация, но многословно |

---

### 💡 Почему это удобно?

1. **Короче** — меньше печатать, проще читать
2. **Понятнее** — `@watch()` говорит само за себя
3. **Семантично** — сразу ясно, что делает декоратор
4. **Совместимо** — все алиасы работают как оригиналы

> 🚀 **Совет:** Используй сахар в повседневном коде,  
> а оригинальные имена — когда нужна максимальная явность или autocomplete.

```python
from spion import watch, trace, user, state, throttle

# Твой код станет чище и понятнее
@watch()
def hello(): ...

@trace(max_depth=10)
def deep_recursion(): ...

@user()
def click_handler(): ...

@state()
def update_game(): ...

@throttle(interval=5)
def poll_api(): ...
```

---

## <a name="дорожная-карта"></a>🗺️ Дорожная карта — что дальше? spion.<span style="float:right;"><a href="#spion">⬆️</a></span>

> **Spion** постоянно развивается. Вот что мы планируем добавить в ближайших релизах:

### 📐 Системы координат (уже в разработке!)
Абстрагируем `@user_action()` от шахматной доски — сможешь использовать любую систему координат:

```python
from spion import user
from spion.coordinates import *

# 1D: Линейные координаты
@user(coordinate_system=IndexCoordinates())
def select_item(item): ...  # [👤] select_item на [5]

# 2D: Таблицы и матрицы
@user(coordinate_system=ExcelCoordinates())
def edit_cell(cell): ...    # [👤] edit_cell на D3

# 3D: Пространство
@user(coordinate_system=SpaceCoordinates(unit="m"))
def place_block(pos): ...   # [👤] place_block на (10m, 20m, 5m)

# Временные метки
@user(coordinate_system=TimeCoordinates())
def schedule_event(event): ... # [👤] schedule_event на 15:30:45
```

### 🗄️ SQL-логирование (в планах)
Специальные декораторы для баз данных:

```python
from spion import sql, transaction

@sql(track_queries=True)
def get_users():
    return session.query(User).all()
# [14:30:25.123] [SQL] SELECT * FROM users (0.002s, 10 rows)

@transaction
def update_order():
    order.save()
    payment.process()
# [14:30:25.123] [TX] BEGIN
# [14:30:25.124] [TX] COMMIT (0.001s)

@sql.explain
def slow_query():
    return db.execute(complex_query)
# [14:30:25.123] [EXPLAIN] Seq Scan on users...
```

### 🔢 Системы счисления (в планах)
Для математиков, криптографов и низкоуровневого кода:

```python
from spion import bits, hexdump, binary

@bits(endian="little")
def pack_data(value):
    return struct.pack('<I', value)
# [14:30:25.123] [BITS] 0xdeadbeef → [ef be ad de]

@hexdump
def read_binary(filename):
    return open(filename, 'rb').read()
# [14:30:25.123] [HEX] 0000: 7f 45 4c 46 02 01 01 00 | .ELF....

@binary(format="64bit")
def calculate_mask(a, b):
    return a & b
# [14:30:25.123] [BIN] 0b1010 & 0b1100 = 0b1000
```

### 🎮 Геймдев-специфика (в планах)
Для разработчиков игр:

```python
from spion import game

@game.physics
def update_physics(dt):
    # Логирование коллизий, скорости, ускорения
    pass

@game.input
def handle_keypress(key):
    # Логирование нажатий с привязкой к кадрам
    pass

@game.network(lag_compensation=True)
def sync_state(player_state):
    # Логирование сетевого квинтэссенции
    pass
```

### 📊 Визуализация (в планах)
Экспорт логов в понятные форматы:

```python
from spion import export

@export.chart(type="flame")
def recursive_function(n):
    # Построит flame graph из цепочки вызовов
    pass

@export.timeline
def request_handler():
    # Покажет timeline выполнения
    pass
```

### 🤖 AI-логирование (в планах)
Для проектов с машинным обучением:

```python
from spion import ai

@ai.training
def train_epoch(model, data):
    # Логирование loss, accuracy, градиентов
    pass

@ai.inference
def predict(model, input):
    # Логирование времени инференса, уверенности
    pass
```

---

## 💬 Хочешь повлиять на развитие?

У тебя есть шанс сделать Spion именно такой библиотекой, которая нужна тебе!

- 🐞 **Нашел баг?** — [Создай issue](https://github.com/leonhadouken/spion/issues)
- 💡 **Есть идея?** — [Расскажи в discussions](https://github.com/leonhadouken/spion/discussions)
- 🔧 **Хочешь помочь?** — PRы всегда открыты!

Следующие версии будут зависеть от фидбека сообщества. **Что бы ты хотел видеть в первую очередь?**

- [ ] Системы координат (1D, 2D, 3D, время)
- [ ] SQL-логирование (запросы, транзакции, EXPLAIN)
- [ ] Системы счисления (hex, binary, bits)
- [ ] Геймдев-инструменты (физика, ввод, сеть)
- [ ] Визуализация (flame graphs, timelines)
- [ ] AI/ML (тренировка, инференс)

> 👉 [**Голосуй в issues!**](https://github.com/leonhadouken/spion/issues) Самые востребованные фичи будут реализованы в первую очередь.

---

**Spion** — это не просто библиотека, это **сообщество**. Давай делать отладку удобной вместе! 🚀

---

## <a name="требования"></a>Требования spion.<span style="float:right;"><a href="#spion">⬆️</a></span>
- Python 3.7+
- Любовь к чистому коду 💙

---

## <a name="лицензия"></a>Лицензия

MIT © [Ivan Shaikov](https://github.com/leonhadouken)

---

<p align="center">
  <a href="#">⬆️ Наверх</a> •
  <a href="https://github.com/leonhadouken/spion">GitHub</a> •
  <a href="https://github.com/leonhadouken/spion/issues">Сообщить о баге</a> •
  <a href="https://github.com/leonhadouken/spion/discussions">Обсуждения</a>
</p>
