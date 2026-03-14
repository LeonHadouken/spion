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
  <a href="#установка">Установка</a> •
  <a href="#для-тех-кто-ценит-простоту">Простота</a> •
  <a href="#для-тех-кто-не-упускает-деталей">Детали</a> •
  <a href="#многоликий-spion">Многоликий Spion</a> •
  <a href="#полное-руководство">Гайд</a> •
  <a href="#синтаксический-сахар-скоро">Сахар</a> •
  <a href="#требования">Требования</a> •
  <a href="#лицензия">Лицензия</a>
</p>

---

## <a name="установка"></a>Установка <a href="#">⬆️ Наверх</a>

```bash
pip install spion
```

Или если хочешь самое свежее (разрабская версия):

```bash
pip install git+https://github.com/yourname/spion.git
```

---

## <a name="для-тех-кто-ценит-простоту"></a>Для тех, кто ценит простоту <a href="#spion">⬆️ Наверх</a>
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

## <a name="для-тех-кто-не-упускает-деталей"></a>Для тех, кто не упускает деталей <a href="#spion">⬆️ Наверх</a>

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

| Хочешь...                                                        | Spion даст... |
|------------------------------------------------------------------|---------------|
| *Увидеть, как рекурсия пожирает стек?*                           | `@log_method_chain()` |
| *Понять, кто на ком стоит в иерархии классов?*                   | `@log_class_relationship()` |
| *Отследить, как меняется состояние объекта?*                     | `@log_state_change()` |
| *Логи без спама (даже если функцию дёргают 1000 раз в секунду)?* | `@log_call_once()` |
| *Понятные сообщения о действиях пользователя?*                   | `@log_user_action()` |

---

## <a name="многоликий-spion"></a>Многоликий Spion <a href="#spion">⬆️ Наверх</a>

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
## <a name="полное-руководство"></a>Полное руководство <a href="#spion">⬆️ Наверх</a>

**[GUIDE.md](GUIDE.md)** — это не документация к библиотеке. Это **тренажёр по чтению и отладке кода**. 60+ живых примеров, которые показывают:

- 🧠 **Как думать о рекурсии** — увидишь, как стек растёт и схлопывается
- 🔍 **Где прячутся баги** — спам-логи, неочевидные состояния, запутанные связи
- 🏗️ **Как связаны объекты** — иерархии, зависимости, композиция
- 🎮 **Как живой код работает под капотом** — от Flask до игрового движка

***Это не про Spion. Это **про тебя и твой код**.***

> 👉 **[ОТКРЫТЬ ПОЛНОЕ РУКОВОДСТВО →](GUIDE.md)** 👈

---

## <a name="синтаксический-сахар-скоро"></a>Синтаксический сахар (скоро) <a href="#spion">⬆️ Наверх</a>

> Я точно знаю, что отладка не должна быть болью. Поэтому готовлю обёртки, которые сделают код ещё чище:

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
> 💬 **Хочешь повлиять на синтаксис?** — [открывай issue](https://github.com/leonhadouken/spion/issues) на GitHub, обсудим!

---
## <a name="требования"></a>Требования <a href="#spion">⬆️ Наверх</a>
- Python 3.7+
- Любовь к чистому коду 💙
---

## <a name="лицензия"></a>Лицензия <a href="#spion">⬆️ Наверх</a>

MIT © [Ivan Shaikov](https://github.com/leonhadouken)

---

<p align="center">
  <a href="#">⬆️ Наверх</a> •
  <a href="https://github.com/yourname/spion">GitHub</a> •
  <a href="https://github.com/yourname/spion/issues">Сообщить о баге</a> •
  <a href="https://github.com/yourname/spion/discussions">Обсуждения</a>
</p>
```
