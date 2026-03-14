# 🕵️ Spion

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7%2B-green?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/status-dev-yellow?style=for-the-badge" alt="Status">
</p>

<p align="center">
  <b>Spion</b> — это шпион в мире вашего кода. Невидимый, тихий, но всё видящий.
</p>

<p align="center">
  <a href="#🚀-установка">Установка</a> •
  <a href="#🎯-для-тех-кто-ценит-простоту">Простота</a> •
  <a href="#🔬-для-тех-кто-не-упускает-деталей">Детали</a> •
  <a href="#🍬-синтаксический-сахар-скоро">Сахар</a> •
  <a href="#📚-полное-руководство">Гайд</a> •
  <a href="#📄-лицензия">Лицензия</a>
</p>

---

## 🚀 Установка

```bash
pip install spion
```

Или если хочешь самое свежее (разрабская версия):

```bash
pip install git+https://github.com/LeonHadouken/spion.git
```

---

## 🎯 Для тех, кто ценит простоту

```python
from spion import log

@log()
def hello():
    return "world"

hello()
# [14:30:25.123] ▶️ Вызов hello
```

Одна строчка — и ты уже знаешь, что функция вызвалась. Никакой магии, никакой боли. Просто работает.

[👉 Подробнее про @log() →](GUIDE.md#1-log---базовое-логирование)

---

## 🔬 Для тех, кто не упускает деталей

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

| Хочешь... | Spion даст... | Подробнее |
|-----------|---------------|-----------|
| Увидеть, как рекурсия пожирает стек? | `@log_method_chain()` | [📖](GUIDE.md#6-log_method_chain---цепочки-вызовов) |
| Понять, кто на ком стоит в иерархии классов? | `@log_class_relationship()` | [📖](GUIDE.md#5-log_class_relationship---связи-между-классами) |
| Отследить, как меняется состояние объекта? | `@log_state_change()` | [📖](GUIDE.md#4-log_state_change---изменения-состояния) |
| Логи без спама (даже если функцию дёргают 1000 раз в секунду)? | `@log_call_once()` | [📖](GUIDE.md#2-log_call_once---логирование-с-интервалом) |
| Понятные сообщения о действиях пользователя? | `@log_user_action()` | [📖](GUIDE.md#3-log_user_action---действия-пользователя) |

---

## 🎭 Многоликий Spion

| Уровень | Декоратор | Что внутри | Подробнее |
|---------|-----------|------------|-----------|
| 🟢 **Новичок** | `@log()` | Просто "пинг" о вызове | [📖](GUIDE.md#1-log---базовое-логирование) |
| 🔵 **Любитель** | `@log_call_once()` | Логи с интервалом | [📖](GUIDE.md#2-log_call_once---логирование-с-интервалом) |
| 🟡 **Опытный** | `@log_user_action()` | Действия пользователя | [📖](GUIDE.md#3-log_user_action---действия-пользователя) |
| 🟠 **Профи** | `@log_state_change()` | Изменения состояния | [📖](GUIDE.md#4-log_state_change---изменения-состояния) |
| 🔴 **Мастер** | `@log_class_relationship()` | Связи между классами | [📖](GUIDE.md#5-log_class_relationship---связи-между-классами) |
| ⚫ **Гуру** | `@log_method_chain()` | Цепочки вызовов с отступами | [📖](GUIDE.md#6-log_method_chain---цепочки-вызовов) |

Начинающим — `@log()` и порядок.  
Профессионалам — `@log_method_chain(max_depth=20)` и полный контроль.

> Spion не заставляет выбирать между простотой и глубиной. Он даёт и то, и другое. Бери то, что нужно именно сейчас.

---
## 📚 Полное руководство

**[GUIDE.md](GUIDE.md)** — это не документация к библиотеке. Это **тренажёр по чтению и отладке кода**. 60+ живых примеров, которые показывают:

- 🧠 **Как думать о рекурсии** — увидишь, как стек растёт и схлопывается
- 🔍 **Где прячутся баги** — спам-логи, неочевидные состояния, запутанные связи
- 🏗️ **Как связаны объекты** — иерархии, зависимости, композиция
- 🎮 **Как живой код работает под капотом** — от Flask до игрового движка

Это не про Spion. Это **про тебя и твой код**.

> 👉 **[ОТКРЫТЬ ПОЛНОЕ РУКОВОДСТВО →](GUIDE.md)** 👈

---

## 🍬 Синтаксический сахар (скоро)

Я точно знаю, что отладка не должна быть болью. Поэтому готовлю обёртки, которые сделают код ещё чище:

| Сахар | Вместо | Результат |
|-------|--------|-----------|
| `@watch()` | `@log()` | Просто следим |
| `@trace(max_depth=10)` | `@log_method_chain(max_depth=10)` | Трассировка цепочек |
| `@spy()` | `@log()` + `@log_class_relationship()` + ... | Всё и сразу |
| `@light()` | `@log(level=LogLevel.INFO)` | Минимализм |
| `@deep_inspect()` | Полный фарш | Максимум деталей |

```python
from spion import watch, trace, spy

@watch()
def hello():
    return "world"

@trace(max_depth=5)
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

@spy()
def complex_operation(self, data):
    # Здесь будет видно вообще всё
    pass
```

> 🚧 **Статус:** В разработке. API может измениться.
> 💬 **Хочешь повлиять на синтаксис?** — [открывай issue](https://github.com/LeonHadouken/spion/issues) на GitHub, обсудим!

---

## 🧪 Требования

- Python 3.7+
- Любовь к чистому коду 💙

---

## 📄 Лицензия

MIT © [Ivan Shaikov](https://github.com/LeonHadouken)

> Проект распространяется под лицензией MIT. Подробнее — в файле [LICENSE](LICENSE).

---

<p align="center">
  <a href="#">⬆️ Наверх</a> •
  <a href="https://github.com/LeonHadouken/spion">GitHub</a> •
  <a href="https://github.com/LeonHadouken/spion/issues">Сообщить о баге</a> •
  <a href="https://github.com/LeonHadouken/spion/discussions">Обсуждения</a>
</p>
