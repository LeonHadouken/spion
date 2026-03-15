Вы правы! Я действительно обрезал много примеров из оригинального GUIDE.md. Давайте вернем полную версию с сохранением всех 10 разделов, но с добавлением сахара:

```markdown
# 🔧 ПОЛНОЕ РУКОВОДСТВО ПО SPION

<p align="right">
  <a href="README.md">← Назад к README</a>
</p>

## 📋 СОДЕРЖАНИЕ
- [🍬 Синтаксический сахар](#-синтаксический-сахар)
- [1. @log() / @watch() - Базовое логирование](#1-log--watch---базовое-логирование)
- [2. @log_call_once() / @throttle() - Логирование с интервалом](#2-log_call_once--throttle---логирование-с-интервалом)
- [3. @log_user_action() / @user() - Действия пользователя](#3-log_user_action--user---действия-пользователя)
- [4. @log_state_change() / @state() - Изменения состояния](#4-log_state_change--state---изменения-состояния)
- [5. @log_class_relationship() - Связи между классами](#5-log_class_relationship---связи-между-классами)
- [6. @log_method_chain() / @trace() - Цепочки вызовов](#6-log_method_chain--trace---цепочки-вызовов)
- [7. @light() и @silent() - Специализированные декораторы](#7-light-и-silent---специализированные-декораторы)
- [8. @spy() - Комбинатор декораторов](#8-spy---комбинатор-декораторов)
- [9. Комбинирование декораторов](#9-комбинирование-декораторов)
- [10. Настройка под конкретные случаи](#10-настройка-под-конкретные-случаи)
- [11. Примеры для разных типов приложений](#11-примеры-для-разных-типов-приложений)
- [12. Полный пример с конфигурацией](#12-полный-пример-с-конфигурацией)

---

<a name="-синтаксический-сахар"></a>
## 🍬 Синтаксический сахар

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a>
</p>

Spion предоставляет удобные алиасы для всех основных декораторов. Выбирай тот стиль, который тебе ближе:

| Сахар | Оригинал | Когда использовать |
|-------|----------|-------------------|
| `@watch()` | `@log()` | Хочется сказать "слежу за функцией" |
| `@trace()` | `@log_method_chain()` | Нужна трассировка рекурсии |
| `@user()` | `@log_user_action()` | Логируем действия пользователя |
| `@state()` | `@log_state_change()` | Отслеживаем изменения состояния |
| `@throttle()` | `@log_call_once()` | Ограничиваем частоту логов |
| `@light()` | `@log(level=LogLevel.INFO)` | Только факт вызова |
| `@silent()` | `@log(level=LogLevel.ERROR)` | Только ошибки |
| `@spy()` | комбинация декораторов | Шпионим за всем сразу |

```python
from spion import watch, trace, user, state, throttle, light, silent, spy

# Твой код станет чище и понятнее
@watch()
def hello(): ...

@trace(max_depth=10)
def factorial(n): ...

@user()
def click_handler(): ...

@state()
def update_game(): ...

@throttle(interval=5)
def poll_api(): ...

@light()
def fast_func(): ...

@silent()
def risky_operation(): ...

@spy(watch(), trace(), user())
def complex_operation(): ...
```

---

<a name="1-log--watch---базовое-логирование"></a>
## **1. @log() / @watch() - Базовое логирование**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **1.1. Минимальная конфигурация**
```python
from spion import log, watch

# Два способа сделать одно и то же
@log()
def hello1():
    return "world"

@watch()
def hello2():
    return "world"

hello1()
# [14:30:25.123] 🟢 ▶️ Вызов hello1

hello2()
# [14:30:25.123] 🟢 ▶️ Вызов hello2
```

### **1.2. С уровнем логирования DEBUG**
```python
from spion import watch, LogLevel

@watch(level=LogLevel.DEBUG)
def add(a, b):
    return a + b

result = add(5, 3)
# [14:30:25.123] 🔵 ▶️ Вызов add с аргументами: 5, 3
# [14:30:25.123] 🟢 ◀️ add -> 8
```

### **1.3. С уровнем логирования INFO**
```python
@watch(level=LogLevel.INFO)
def process_data(data):
    return len(data)

process_data([1, 2, 3])
# [14:30:25.123] 🟢 ▶️ Вызов process_data
# (результат не логируется)
```

### **1.4. С уровнем логирования WARNING**
```python
@watch(level=LogLevel.WARNING)
def check_disk_space():
    return "85% full"

check_disk_space()
# [14:30:25.123] 🟡 ▶️ Вызов check_disk_space
```

### **1.5. С уровнем логирования ERROR**
```python
@watch(level=LogLevel.ERROR)
def dangerous_operation():
    if True:
        raise ValueError("Что-то пошло не так")

try:
    dangerous_operation()
except:
    pass
# [14:30:25.123] 🔴 [❌] dangerous_operation: Что-то пошло не так
# [14:30:25.123] 🔵 Traceback (most recent call last): ...
```

### **1.6. С пользовательским сообщением**
```python
@watch(message="Начинаем загрузку файла")
def load_file(filename):
    return open(filename).read()

load_file("data.txt")
# [14:30:25.123] 🟢 ▶️ Начинаем загрузку файла

@watch(message="⚠️ ВНИМАНИЕ: редкая операция")
def rare_operation():
    pass

rare_operation()
# [14:30:25.123] 🟢 ▶️ ⚠️ ВНИМАНИЕ: редкая операция
```

### **1.7. Для методов класса**
```python
class Calculator:
    @watch(level=LogLevel.INFO)
    def multiply(self, x, y):
        return x * y
    
    @watch(level=LogLevel.DEBUG)
    def divide(self, x, y):
        return x / y

calc = Calculator()
calc.multiply(4, 5)
# [14:30:25.123] 🟢 ▶️ Вызов Calculator.multiply

calc.divide(10, 2)
# [14:30:25.123] 🔵 ▶️ Вызов Calculator.divide с аргументами: 10, 2
# [14:30:25.123] 🟢 ◀️ Calculator.divide -> 5.0
```

### **1.8. С фильтрацией повторений - ограничение по количеству**
```python
from spion import watch, add_rule

@watch()
def api_call(endpoint):
    return f"Response from {endpoint}"

# Логируем только первые 3 вызова
add_rule(
    pattern="api_call",
    call_type="call",
    max_calls=3
)

for i in range(10):
    api_call(f"/users/{i}")
# Логи: вызовы 0, 1, 2
# Вызовы 3-9 без логов
```

### **1.9. С фильтрацией повторений - один раз за всё время**
```python
@watch()
def initialize_database():
    return "DB initialized"

# Только один раз за всю программу
add_rule(
    pattern="initialize_database",
    call_type="call",
    log_once=True
)

initialize_database()  # Лог
initialize_database()  # Без лога
initialize_database()  # Без лога
```

### **1.10. С фильтрацией повторений - с временным окном**
```python
import time

@watch()
def check_status():
    return "OK"

# Не чаще раза в 5 секунд
add_rule(
    pattern="check_status",
    call_type="call",
    max_calls=1,
    time_window=5  # секунд
)

for _ in range(10):
    check_status()
    time.sleep(1)
# Логи: на 0й, 5й, 10й секундах
```

### **1.11. С фильтрацией повторений - комбинированные правила**
```python
@watch()
def heavy_computation(n):
    return n ** 2

# Максимум 5 раз, но не чаще раза в 2 секунды
add_rule(
    pattern="heavy_computation",
    call_type="call",
    max_calls=5,
    time_window=2
)

for i in range(20):
    heavy_computation(i)
    time.sleep(0.5)
# Логи: примерно на 0, 2, 4, 6, 8 секундах (5 раз)
```

### **1.12. Разные уровни для разных методов**
```python
class FileProcessor:
    @watch(level=LogLevel.ERROR)
    def read_file(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        return open(filename).read()
    
    @watch(level=LogLevel.DEBUG)
    def _internal_parse(self, content):
        lines = content.split('\n')
        return [line.strip() for line in lines]
    
    @watch(level=LogLevel.INFO)
    def process(self, filename):
        content = self.read_file(filename)
        return self._internal_parse(content)

processor = FileProcessor()
processor.process("data.txt")
# INFO: [14:30:25.123] 🟢 ▶️ Вызов FileProcessor.process
# DEBUG: [14:30:25.123] 🔵 ▶️ Вызов FileProcessor._internal_parse с аргументами: 'line1\nline2'
# DEBUG: [14:30:25.123] 🟢 ◀️ FileProcessor._internal_parse -> ['line1', 'line2']
```

---

<a name="2-log_call_once--throttle---логирование-с-интервалом"></a>
## **2. @log_call_once() / @throttle() - Логирование с интервалом**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **2.1. Интервал 1 секунда**
```python
from spion import throttle
import time

@throttle(interval=1.0)
def update_display():
    return "display updated"

for i in range(50):
    update_display()
    time.sleep(0.05)  # 50ms
# Только первый вызов залогирован: [14:30:25.123] [🔄] update_display
```

### **2.2. Интервал 5 секунд**
```python
@throttle(interval=5.0)
def check_connection():
    return "connected"

start = time.time()
while time.time() - start < 30:
    check_connection()
    time.sleep(1)
# Логи: на 0, 5, 10, 15, 20, 25 секундах
```

### **2.3. Интервал 60 секунд (для мониторинга)**
```python
@throttle(interval=60.0)
def report_metrics():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    return f"CPU: {cpu}%, RAM: {memory}%"

# В главном цикле приложения
while True:
    report_metrics()  # Лог раз в минуту
    time.sleep(5)
    # ... остальная логика
```

### **2.4. Для мониторинга очереди**
```python
class QueueMonitor:
    def __init__(self):
        self.queue = []
        self.processed = 0
    
    @throttle(interval=10.0)
    def log_queue_status(self):
        return f"Queue: {len(self.queue)}, Processed: {self.processed}"
    
    def add_to_queue(self, item):
        self.queue.append(item)
        self.log_queue_status()  # Лог не чаще 10 секунд
    
    def process_queue(self):
        while self.queue:
            item = self.queue.pop(0)
            self.processed += 1
            self.log_queue_status()  # Лог не чаще 10 секунд

monitor = QueueMonitor()
for i in range(100):
    monitor.add_to_queue(f"item_{i}")
    monitor.process_queue()
# Будет ~1-2 лога за всё время
```

### **2.5. Для отладки производительности**
```python
@throttle(interval=30.0)
def log_performance_stats():
    import gc
    objects = len(gc.get_objects())
    return f"Active objects: {objects}"

class DataProcessor:
    def process_batch(self, items):
        for item in items:
            self._process_item(item)
            log_performance_stats()  # Раз в 30 секунд
    
    def _process_item(self, item):
        # ... обработка
        pass
```

### **2.6. Комбинация с разными интервалами**
```python
class SystemMonitor:
    @throttle(interval=1.0)
    def log_fast_metrics(self):
        return f"Fast metrics: {time.time()}"
    
    @throttle(interval=60.0)
    def log_slow_metrics(self):
        return f"Slow metrics: {time.time()}"
    
    def monitor(self):
        while True:
            self.log_fast_metrics()   # Каждую секунду
            self.log_slow_metrics()   # Каждую минуту
            time.sleep(0.1)
```

---

<a name="3-log_user_action--user---действия-пользователя"></a>
## **3. @log_user_action() / @user() - Действия пользователя**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **3.1. Стандартное использование с Position**
```python
from spion import user

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Game:
    @user()
    def click(self, position):
        return f"Clicked at {position.row}, {position.col}"

game = Game()
game.click(Position(3, 1))
# [14:30:25.123] [👤] Game.click на B5 (если доска 8x8: col=1 → B, row=3 → 5)
```

### **3.2. С другими именами атрибутов**
```python
class Point:
    def __init__(self, x, y):
        self.row = y  # Адаптируем под ожидаемый формат
        self.col = x

@user()
def on_click(point):
    pass

on_click(Point(2, 4))
# [14:30:25.123] [👤] on_click на E2
```

### **3.3. Без определения координат**
```python
@user()
def login(username, password):
    return authenticate(username, password)

login("user123", "pass")
# [14:30:25.123] [👤] login
```

### **3.4. Для методов с несколькими параметрами**
```python
class Editor:
    @user()
    def insert_text(self, position, text, cursor_pos):
        """position - объект с row/col, остальное игнорируется"""
        return f"Inserted '{text}' at {position.row}:{position.col}"

editor = Editor()
pos = Position(5, 10)
editor.insert_text(pos, "Hello", 3)
# [14:30:25.123] [👤] Editor.insert_text на F11 (row=5 → F, col=10 → 11)
```

### **3.5. Для разных типов пользовательских действий**
```python
class GameController:
    @user()
    def select_piece(self, position):
        """Выбор шашки"""
        pass
    
    @user()
    def move_piece(self, from_pos, to_pos):
        """Ход шашкой - логируется только from_pos"""
        pass
    
    @user()
    def menu_click(self, menu_item):
        """Клик в меню - без координат"""
        pass

controller = GameController()
controller.select_piece(Position(2, 3))  # [👤] на D4
controller.move_piece(Position(2, 3), Position(4, 4))  # [👤] на D4
controller.menu_click("New Game")  # [👤] menu_click
```

### **3.6. Для веб-приложения**
```python
class WebApp:
    @user()
    def handle_request(self, request):
        """Из request извлекаем координаты если есть"""
        if hasattr(request, 'x') and hasattr(request, 'y'):
            # Адаптируем под формат декоратора
            request.row = request.y
            request.col = request.x
        return "OK"

app = WebApp()

class ClickRequest:
    def __init__(self, x, y):
        self.x = x
        self.y = y

req = ClickRequest(100, 200)
app.handle_request(req)
# [14:30:25.123] [👤] WebApp.handle_request на Y200 (нестандартные координаты)
```

---

<a name="4-log_state_change--state---изменения-состояния"></a>
## **4. @log_state_change() / @state() - Изменения состояния**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **4.1. С автоматическим определением current_player**
```python
from spion import state
from enum import Enum

class Player(Enum):
    WHITE = "белые"
    BLACK = "черные"

class Game:
    def __init__(self):
        self.current_player = Player.WHITE
    
    @state()
    def next_turn(self):
        self.current_player = Player.BLACK

game = Game()
game.next_turn()
# [14:30:25.123] [🔄] Game.next_turn | Ход: белые
```

### **4.2. С другим именем атрибута игрока**
```python
class ChessGame:
    def __init__(self):
        self.turn = "white"  # Не current_player, а turn
    
    @state()
    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"
    # Декоратор не найдет current_player, будет просто [🔄] switch_turn

# Чтобы работало, нужно адаптировать:
class ChessGameFixed:
    def __init__(self):
        self._turn = "white"
    
    @property
    def current_player(self):
        return self._turn
    
    @state()
    def switch_turn(self):
        self._turn = "black" if self._turn == "white" else "white"

game = ChessGameFixed()
game.switch_turn()
# [14:30:25.123] [🔄] ChessGameFixed.switch_turn | Ход: white
```

### **4.3. Без определения игрока**
```python
class Counter:
    def __init__(self):
        self.value = 0
    
    @state()
    def increment(self):
        self.value += 1
    
    @state()
    def reset(self):
        self.value = 0

counter = Counter()
counter.increment()  # [14:30:25.123] [🔄] Counter.increment
counter.reset()      # [14:30:25.123] [🔄] Counter.reset
```

### **4.4. Для сложного состояния**
```python
class GameBoard:
    def __init__(self):
        self.current_player = "X"
        self.move_count = 0
        self.last_move = None
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
    
    @state()
    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.move_count += 1
            self.last_move = (row, col)
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

game = GameBoard()
game.make_move(0, 0)  # [14:30:25.123] [🔄] GameBoard.make_move | Ход: X
game.make_move(1, 1)  # [14:30:25.123] [🔄] GameBoard.make_move | Ход: O
```

### **4.5. Для нескольких состояний**
```python
class TrafficLight:
    def __init__(self):
        self.current_color = "red"
        self.current_player = "cars"  # Для декоратора
    
    @state()
    def change_color(self):
        colors = ["red", "yellow", "green"]
        idx = colors.index(self.current_color)
        self.current_color = colors[(idx + 1) % 3]
        # Обновляем current_player в зависимости от цвета
        self.current_player = "cars" if self.current_color != "red" else "pedestrians"

light = TrafficLight()
light.change_color()  # [14:30:25.123] [🔄] TrafficLight.change_color | Ход: cars
```

### **4.6. Для мониторинга изменений**
```python
class TemperatureController:
    def __init__(self):
        self.current_player = "system"  # Для декоратора
        self.temperature = 20
        self.target = 22
        self.heater_on = False
    
    @state()
    def set_temperature(self, new_temp):
        old_temp = self.temperature
        self.temperature = new_temp
        self.heater_on = self.temperature < self.target
        return old_temp != new_temp

controller = TemperatureController()
controller.set_temperature(21)  # [14:30:25.123] [🔄] set_temperature | Ход: system
```

---

<a name="5-log_class_relationship---связи-между-классами"></a>
## **5. @log_class_relationship() - Связи между классами**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **5.1. Только иерархия (show_hierarchy=True, show_dependencies=False)**
```python
from spion import log_class_relationship

class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    @log_class_relationship(show_hierarchy=True, show_dependencies=False)
    def bark(self):
        return "Woof!"

dog = Dog()
dog.bark()
# [14:30:25.123] [🔗] Dog.bark
#   📊 Иерархия: Dog -> Mammal -> Animal -> object
#   ↩️ Результат: str
```

### **5.2. Только зависимости (show_hierarchy=False, show_dependencies=True)**
```python
class Engine:
    pass

class Transmission:
    pass

class Car:
    def __init__(self):
        self.engine = Engine()
        self.transmission = Transmission()
        self.wheels = 4
    
    @log_class_relationship(show_hierarchy=False, show_dependencies=True)
    def start(self):
        return "Vroom!"

car = Car()
car.start()
# [14:30:25.123] [🔗] Car.start
#   🔗 Зависимости: engine: Engine, transmission: Transmission
#   ↩️ Результат: str
```

### **5.3. Полный анализ (оба параметра True)**
```python
class BaseModel:
    pass

class User(BaseModel):
    def __init__(self):
        self.db = Database()
        self.cache = Cache()
        self.logger = Logger()

class Database:
    pass

class Cache:
    pass

class Logger:
    pass

user = User()

@log_class_relationship(show_hierarchy=True, show_dependencies=True)
def save_user(user):
    return "saved"

save_user(user)
# [14:30:25.123] [🔗] save_user
#   • user: User (экземпляр User) ✓
#   📊 Иерархия: User -> BaseModel -> object
#   🔗 Зависимости: db: Database, cache: Cache, logger: Logger
#   ↩️ Результат: str
```

### **5.4. С разными типами аргументов**
```python
class Processor:
    @log_class_relationship(level=LogLevel.DEBUG)
    def process(self, data, config, callback):
        """
        data - список чисел
        config - объект конфига
        callback - функция
        """
        return [callback(x) for x in data]

p = Processor()
p.process([1, 2, 3], Config(), lambda x: x*2)
# [14:30:25.123] 🔵 [🔗] Processor.process
#   • data: list (экземпляр list) ⚠
#   • config: Config (экземпляр Config) ✓
#   • callback: function
#   📊 Иерархия: Processor -> object
#   ↩️ Результат: list
```

### **5.5. Для вложенных объектов**
```python
class Address:
    def __init__(self, street, city):
        self.street = street
        self.city = city

class Company:
    def __init__(self, name):
        self.name = name
        self.address = Address("Main St", "NYC")
        self.employees = []

class Employee:
    def __init__(self, name, company):
        self.name = name
        self.company = company
        self.company.employees.append(self)

@log_class_relationship()
def transfer_employee(emp, new_company):
    emp.company = new_company
    return True

emp = Employee("John", Company("Old Corp"))
new_co = Company("New Corp")
transfer_employee(emp, new_co)
# [14:30:25.123] [🔗] transfer_employee
#   • emp: Employee ✓
#   • new_company: Company ✓
#   📊 Иерархия: Employee -> object
#   🔗 Зависимости emp: company: Company
#   🔗 Зависимости new_company: address: Address
#   ↩️ Результат: bool
```

### **5.6. С кастомными зависимостями**
```python
class CustomAnalyzer:
    @log_class_relationship()
    def analyze(self, obj):
        # Декоратор автоматически ищет зависимости по списку:
        # ['board', 'game_state', 'renderer', 'model', 'view', 'controller']
        pass

class MyClass:
    def __init__(self):
        self.board = Board()        # будет найдено
        self.custom = Custom()      # НЕ будет найдено (не в списке)
        self.model = Model()        # будет найдено

obj = MyClass()
analyzer = CustomAnalyzer()
analyzer.analyze(obj)
# [14:30:25.123] [🔗] CustomAnalyzer.analyze
#   • obj: MyClass ✓
#   🔗 Зависимости: board: Board, model: Model
#   ↩️ Результат: NoneType
```

### **5.7. Для отслеживания наследования**
```python
class Shape:
    pass

class Polygon(Shape):
    pass

class Rectangle(Polygon):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area_calculator = AreaCalculator()

class Square(Rectangle):
    @log_class_relationship()
    def __init__(self, side):
        super().__init__(side, side)
        self.side = side

square = Square(5)
# [14:30:25.123] [🔗] Square.__init__
#   • side: int
#   📊 Иерархия: Square -> Rectangle -> Polygon -> Shape -> object
#   🔗 Зависимости: area_calculator: AreaCalculator
#   ↩️ Результат: NoneType
```

---

<a name="6-log_method_chain--trace---цепочки-вызовов"></a>
## **6. @log_method_chain() / @trace() - Цепочки вызовов**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **6.1. Ограниченная глубина (max_depth=2)**
```python
from spion import trace

@trace(max_depth=2)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

factorial(4)
# [14:30:25.123] 🔵 [↘️] factorial(4)
#   [14:30:25.123] 🔵 [↘️] factorial(3)
#     [14:30:25.123] 🔵 [↘️] factorial(2)  (уже за глубиной, без отступа)
#     [14:30:25.123] 🔵 [↗️] factorial(2) -> 2
#   [14:30:25.123] 🔵 [↗️] factorial(3) -> 6
# [14:30:25.123] 🔵 [↗️] factorial(4) -> 24
```

### **6.2. Средняя глубина (max_depth=5, по умолчанию)**
```python
@trace()  # max_depth=5
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci(4)
# [14:30:25.123] 🔵 [↘️] fibonacci(4)
#   [14:30:25.123] 🔵 [↘️] fibonacci(3)
#     [14:30:25.123] 🔵 [↘️] fibonacci(2)
#       [14:30:25.123] 🔵 [↘️] fibonacci(1)
#       [14:30:25.123] 🔵 [↗️] fibonacci(1) -> 1
#       [14:30:25.123] 🔵 [↘️] fibonacci(0)
#       [14:30:25.123] 🔵 [↗️] fibonacci(0) -> 0
#     [14:30:25.123] 🔵 [↗️] fibonacci(2) -> 1
#     [14:30:25.123] 🔵 [↘️] fibonacci(1)
#     [14:30:25.123] 🔵 [↗️] fibonacci(1) -> 1
#   [14:30:25.123] 🔵 [↗️] fibonacci(3) -> 2
#   [14:30:25.123] 🔵 [↘️] fibonacci(2)
#     [14:30:25.123] 🔵 [↘️] fibonacci(1)
#     [14:30:25.123] 🔵 [↗️] fibonacci(1) -> 1
#     [14:30:25.123] 🔵 [↘️] fibonacci(0)
#     [14:30:25.123] 🔵 [↗️] fibonacci(0) -> 0
#   [14:30:25.123] 🔵 [↗️] fibonacci(2) -> 1
# [14:30:25.123] 🔵 [↗️] fibonacci(4) -> 3
```

### **6.3. Большая глубина (max_depth=10)**
```python
@trace(max_depth=10)
def ackermann(m, n):
    """Функция Аккермана - глубоко рекурсивная"""
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))

ackermann(2, 2)  # Будет много вложенных вызовов, но не глубже 10
```

### **6.4. Для обхода дерева**
```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    @trace(max_depth=10)
    def inorder(self):
        results = []
        if self.left:
            results.extend(self.left.inorder())
        results.append(self.value)
        if self.right:
            results.extend(self.right.inorder())
        return results

# Создаем дерево
root = TreeNode(1,
    TreeNode(2, TreeNode(4), TreeNode(5)),
    TreeNode(3, TreeNode(6), TreeNode(7))
)

root.inorder()
# Покажет вложенность обхода с отступами
```

### **6.5. Для парсера выражений**
```python
class ExpressionParser:
    @trace(max_depth=20)
    def parse(self, tokens):
        return self.parse_expression(tokens, 0)
    
    def parse_expression(self, tokens, pos):
        left, pos = self.parse_term(tokens, pos)
        if pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            right, pos = self.parse_expression(tokens, pos + 1)
            return (op, left, right), pos
        return left, pos
    
    def parse_term(self, tokens, pos):
        if tokens[pos].isdigit():
            return int(tokens[pos]), pos + 1
        if tokens[pos] == '(':
            expr, pos = self.parse_expression(tokens, pos + 1)
            if pos < len(tokens) and tokens[pos] == ')':
                return expr, pos + 1
        raise ValueError(f"Unexpected token at {pos}")

parser = ExpressionParser()
parser.parse(['(', '3', '+', '4', ')', '*', '(', '5', '-', '2', ')'])
# Покажет всю вложенность парсинга
```

### **6.6. Для обхода графа**
```python
class Graph:
    def __init__(self):
        self.graph = {}
    
    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)
    
    @trace(max_depth=10)
    def dfs(self, node, visited=None):
        if visited is None:
            visited = set()
        
        if node in visited:
            return []
        
        visited.add(node)
        result = [node]
        
        for neighbor in self.graph.get(node, []):
            result.extend(self.dfs(neighbor, visited))
        
        return result

g = Graph()
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(2, 4)
g.add_edge(2, 5)
g.add_edge(3, 6)
g.dfs(1)
# Покажет рекурсивный обход графа с отступами
```

### **6.7. С разными уровнями логирования**
```python
@trace(max_depth=3, level=LogLevel.INFO)
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

quicksort([3, 6, 8, 10, 1, 2, 1])
# Все вызовы будут с 🟢 вместо 🔵
```

---

<a name="7-light-и-silent---специализированные-декораторы"></a>
## **7. @light() и @silent() - Специализированные декораторы**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **7.1. @light() - только вход в функцию**
```python
from spion import light

@light()
def fast_operation():
    return 42

fast_operation()
# [14:30:25.123] ▶️ Вызов fast_operation
# (без аргументов и результата)
```

### **7.2. @light() для высоконагруженных функций**
```python
@light()
def process_batch(items):
    total = 0
    for item in items:
        total += item.value
    return total

# Логируется только факт вызова, 
# даже если обрабатывается миллион элементов
```

### **7.3. @silent() - только ошибки**
```python
from spion import silent
import random

@silent()
def risky_operation():
    if random.random() < 0.3:
        raise ValueError("Что-то пошло не так")
    return "Успех"

# Логируется ТОЛЬКО при ошибке
for _ in range(10):
    try:
        risky_operation()
    except:
        pass
# [14:30:25.123] [❌] risky_operation: Что-то пошло не так (call #1)
```

### **7.4. @silent() для production кода**
```python
@silent()
def payment_process(card_data):
    """В проде логируем только ошибки"""
    result = process_payment(card_data)
    if not result.success:
        raise PaymentError(result.error)
    return result

# Пользователи не видят логи, но разработчики увидят ошибки
```

---

<a name="8-spy---комбинатор-декораторов"></a>
## **8. @spy() - Комбинатор декораторов**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **8.1. Комбинация двух декораторов**
```python
from spion import spy, watch, trace

@spy(
    watch(level=LogLevel.INFO),
    trace(max_depth=3)
)
def complex_function(n):
    if n <= 1:
        return n
    return complex_function(n-1) + n

complex_function(3)
# [14:30:25.123] 🟢 ▶️ Вызов complex_function  (от watch)
# [14:30:25.123] 🔵 [↘️] complex_function(3)   (от trace)
#   [14:30:25.123] 🔵 [↘️] complex_function(2)
#     [14:30:25.123] 🔵 [↘️] complex_function(1)
#     [14:30:25.123] 🔵 [↗️] complex_function(1) -> 1
#   [14:30:25.123] 🔵 [↗️] complex_function(2) -> 3
# [14:30:25.123] 🔵 [↗️] complex_function(3) -> 6
```

### **8.2. Комбинация трёх декораторов**
```python
class Game:
    def __init__(self):
        self.current_player = "white"
    
    @spy(
        user(),                    # действия пользователя
        state(),                   # изменения состояния
        trace(max_depth=5)         # трассировка
    )
    def move(self, position):
        old_player = self.current_player
        self.current_player = "black" if old_player == "white" else "white"
        return f"Moved from {old_player} to {self.current_player}"

game = Game()
game.move(Position(2, 3))
# [14:30:25.123] [👤] Game.move на D4           (от user)
# [14:30:25.123] [🔄] Game.move | Ход: white    (от state)
# [14:30:25.123] 🔵 [↘️] Game.move(Position(2,3)) (от trace)
#   [14:30:25.123] 🔵 [↘️] ...
#   [14:30:25.123] 🔵 [↗️] ...
# [14:30:25.123] 🔵 [↗️] Game.move -> "Moved from white to black"
```

### **8.3. Создание своего комбо-декоратора**
```python
from spion import spy, watch, state, user

# Создаем свой декоратор для игровой логики
def game_spy():
    return spy(
        watch(level=LogLevel.INFO),
        user(),
        state()
    )

class ChessGame:
    @game_spy()
    def make_move(self, position):
        self.current_player = "black"
        return True

# Используем как обычный декоратор
game = ChessGame()
game.make_move(Position(0, 0))
```

---

<a name="9-комбинирование-декораторов"></a>
## **9. Комбинирование декораторов**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **9.1. watch + log_class_relationship**
```python
from spion import watch, log_class_relationship

class DataService:
    @watch(level=LogLevel.INFO)
    @log_class_relationship(show_dependencies=True)
    def fetch_data(self, query, connection):
        """Сначала покажет связи, потом простой лог"""
        return connection.execute(query)

service = DataService()
conn = DatabaseConnection()
service.fetch_data("SELECT * FROM users", conn)
# [14:30:25.123] [🔗] DataService.fetch_data
#   • query: str
#   • connection: DatabaseConnection
#   🔗 Зависимости: ...
# [14:30:25.123] 🟢 ▶️ Вызов DataService.fetch_data
```

### **9.2. user + trace**
```python
class GameUI:
    @user()
    @trace(max_depth=5)
    def handle_click(self, position):
        """Для пользователя - действие, для разработчика - цепочка"""
        self.highlight_cell(position)
        self.select_piece(position)

ui = GameUI()
ui.handle_click(Position(3, 4))
# [14:30:25.123] [👤] GameUI.handle_click на D5
# [14:30:25.123] 🔵 [↘️] GameUI.handle_click(Position(3,4))
#   [14:30:25.123] 🔵 [↘️] highlight_cell(Position(3,4))
#   [14:30:25.123] 🔵 [↗️] highlight_cell -> None
#   ...
```

### **9.3. state + log_class_relationship**
```python
class GameEngine:
    def __init__(self):
        self.current_player = "X"
        self.board = Board()
        self.validator = MoveValidator()
    
    @state()
    @log_class_relationship()
    def make_move(self, position):
        """Отслеживаем изменение состояния и связи одновременно"""
        if self.validator.is_valid(position):
            self.board.place(self.current_player, position)
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

engine = GameEngine()
engine.make_move(Position(0, 0))
# [14:30:25.123] [🔗] GameEngine.make_move
#   • position: Position
#   📊 Иерархия: GameEngine -> object
#   🔗 Зависимости: board: Board, validator: MoveValidator
# [14:30:25.123] [🔄] GameEngine.make_move | Ход: X
```

### **9.4. throttle + trace**
```python
class CacheManager:
    @throttle(interval=60.0)
    @trace(max_depth=3)
    def cleanup_old_entries(self):
        """Раз в минуту запускаем цепочку очистки"""
        self.scan_entries()
        self.remove_expired()
        return "cleanup done"

cache = CacheManager()
for _ in range(100):
    cache.cleanup_old_entries()  # Лог только раз в минуту
    time.sleep(10)
```

### **9.5. Три декоратора одновременно**
```python
class ComplexSystem:
    @watch(level=LogLevel.DEBUG)
    @user()
    @trace(max_depth=5)
    def process_user_request(self, user_id, request_data, position):
        """Максимальная информация"""
        result = self.validate(request_data)
        if result and position:
            self.execute(position)
        return result
```

### **9.6. Разный порядок декораторов**
```python
class OrderTest:
    @watch(level=LogLevel.INFO)
    @log_class_relationship()
    def method1(self):
        """Сначала relationship, потом simple"""
        pass
    
    @log_class_relationship()
    @watch(level=LogLevel.INFO)
    def method2(self):
        """Сначала simple, потом relationship"""
        pass
```

---

<a name="10-настройка-под-конкретные-случаи"></a>
## **10. Настройка под конкретные случаи**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **10.1. Для продакшена - минимум логов**
```python
from spion import configure, configure_filter, LogLevel, add_rule

def setup_production():
    """Только ошибки и предупреждения"""
    configure(
        enabled=True,
        min_level=LogLevel.WARNING,  # WARNING и выше
        show_timestamp=True,
        color_enabled=False  # В лог-файлах цвета не нужны
    )
    
    configure_filter(
        suppress_repetitive=True,
        max_repetitions=3,
        show_suppression_summary=True
    )
    
    # Подавляем частые логи
    add_rule("health_check", call_type="call", max_calls=10, time_window=3600)  # 10 раз в час
    add_rule("status", call_type="call", log_once=True)  # Только один раз

setup_production()
```

### **10.2. Для разработки - максимум информации**
```python
def setup_development():
    """Всё подряд, с цветами и деталями"""
    configure(
        enabled=True,
        min_level=LogLevel.DEBUG,
        show_timestamp=True,
        color_enabled=True,
        timestamp_format="%H:%M:%S.%f"  # С миллисекундами
    )
    
    configure_filter(
        suppress_repetitive=False,  # Не подавляем повторы
        show_suppression_summary=True
    )

setup_development()
```

### **10.3. Для отладки конкретной функции**
```python
def setup_debug_for_parser():
    """Тихо всё, кроме парсера"""
    configure(min_level=LogLevel.ERROR)  # Только ошибки
    
    # А для парсера - всё подряд
    add_rule(
        pattern="parse_",
        call_type="call",
        max_calls=1000,  # Много раз
        log_once=False
    )
    add_rule(
        pattern="parse_",
        call_type="chain",
        max_calls=1000
    )
    
    from spion import watch, trace
    
    class Parser:
        @watch(level=LogLevel.DEBUG)
        @trace(max_depth=20)
        def parse_expression(self, tokens):
            pass

setup_debug_for_parser()
```

### **10.4. Для тестирования**
```python
import unittest

def setup_test_logging():
    """Логирование для юнит-тестов"""
    configure(
        enabled=True,
        min_level=LogLevel.DEBUG,
        show_timestamp=False,  # Без времени для стабильности
        color_enabled=False
    )
    
    configure_filter(
        suppress_repetitive=False,
        show_suppression_summary=False
    )

class TestGame(unittest.TestCase):
    def setUp(self):
        from spion import reset_filter
        reset_filter()  # Свежий фильтр для каждого теста
        setup_test_logging()
    
    def test_move(self):
        @watch()
        def make_move():
            pass
        # Логи будут без timestamp, что упрощает сравнение
```

### **10.5. Динамическая настройка в рантайме**
```python
class DebugController:
    def __init__(self):
        self.debug_mode = False
        self.stats = {}
    
    @state()
    def toggle_debug(self):
        """Переключение режима отладки на лету"""
        self.debug_mode = not self.debug_mode
        
        if self.debug_mode:
            configure(min_level=LogLevel.DEBUG)
            configure_filter(suppress_repetitive=False)
            print("🔧 Debug mode ON")
        else:
            configure(min_level=LogLevel.INFO)
            configure_filter(suppress_repetitive=True)
            
            # Показываем статистику
            from spion import get_suppression_summary
            self.stats = get_suppression_summary()
            print("📊 Suppression summary:", self.stats)
            print("🔧 Debug mode OFF")
    
    @watch()
    def important_function(self):
        pass
```

### **10.6. Для разных окружений**
```python
import os

def setup_by_environment():
    """Автоматическая настройка в зависимости от окружения"""
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

setup_by_environment()
```

---

<a name="11-примеры-для-разных-типов-приложений"></a>
## **11. Примеры для разных типов приложений**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **11.1. Веб-сервер на Flask**
```python
from flask import Flask, request
from spion import watch, throttle, user, LogLevel

app = Flask(__name__)

class WebServer:
    @throttle(interval=60)
    def health_check(self):
        """Проверка здоровья - раз в минуту"""
        return {"status": "ok"}
    
    @user()
    @watch(level=LogLevel.INFO)
    def handle_request(self, user_id, endpoint):
        """Действие пользователя с логированием"""
        return f"Processed {endpoint} for user {user_id}"
    
    @watch(level=LogLevel.ERROR)
    def database_operation(self, query):
        """Только ошибки базы данных"""
        try:
            return db.execute(query)
        except Exception as e:
            raise

server = WebServer()

@app.route('/api/data')
def api_endpoint():
    user_id = request.args.get('user_id')
    server.handle_request(user_id, '/api/data')
    return server.health_check()
```

### **11.2. Игровой движок с сахаром**
```python
class GameEngine:
    def __init__(self):
        self.current_player = "white"
        self.board = Board()
        self.physics = PhysicsEngine()
        self.renderer = Renderer()
    
    @trace(max_depth=5)
    def update(self, delta_time):
        """Отслеживаем всю цепочку обновления"""
        self.physics.update(delta_time)
        self.check_collisions()
        self.renderer.prepare_frame()
    
    @state()
    def change_level(self, level_name):
        """Логируем смену уровня"""
        self.current_level = level_name
        self.load_level(level_name)
        self.current_player = "white"
    
    @user()
    def handle_input(self, key, mouse_pos):
        """Действия игрока"""
        if mouse_pos:
            self.select_piece(mouse_pos)
    
    @throttle(interval=5.0)
    def log_fps(self, fps):
        """FPS не чаще 5 секунд"""
        print(f"FPS: {fps}")
```

### **11.3. Обработка данных**
```python
import pandas as pd
import numpy as np

class DataPipeline:
    def __init__(self):
        self.stats = {}
        self.cache = {}
        self.validator = DataValidator()
    
    @watch(level=LogLevel.INFO)
    def load_data(self, filename):
        """Загрузка данных"""
        return pd.read_csv(filename)
    
    @trace(max_depth=3)
    def process_pipeline(self, data):
        """Конвейер обработки"""
        data = self.clean_data(data)
        data = self.transform_data(data)
        data = self.aggregate_data(data)
        return data
    
    @watch(level=LogLevel.DEBUG)
    def clean_data(self, data):
        """Детальная очистка"""
        data = data.dropna()
        data = data[data['value'] > 0]
        return data
    
    @throttle(interval=30.0)
    def log_progress(self, percent):
        """Прогресс не чаще 30 секунд"""
        self.stats['progress'] = percent
        print(f"Progress: {percent}%")
    
    @watch(level=LogLevel.ERROR)
    def validate_result(self, data):
        """Проверка результата - только ошибки"""
        if not self.validator.is_valid(data):
            raise ValueError("Invalid data")
```

### **11.4. Сетевое приложение**
```python
import socket
import threading

class NetworkServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.running = False
    
    @throttle(interval=60)
    def log_stats(self):
        """Статистика раз в минуту"""
        return f"Connected clients: {len(self.clients)}"
    
    @watch(level=LogLevel.INFO)
    def start(self):
        """Запуск сервера"""
        self.running = True
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        
        while self.running:
            client, addr = self.socket.accept()
            self.handle_client(client, addr)
    
    @trace(max_depth=3)
    def handle_client(self, client, addr):
        """Обработка клиента"""
        self.clients.append(client)
        data = self.receive_data(client)
        response = self.process_request(data)
        self.send_response(client, response)
        self.clients.remove(client)
    
    @watch(level=LogLevel.DEBUG)
    def receive_data(self, client):
        """Детальный прием данных"""
        data = client.recv(1024)
        return data.decode()
    
    @watch(level=LogLevel.ERROR)
    def send_response(self, client, response):
        """Отправка ответа - только ошибки"""
        try:
            client.send(response.encode())
        except Exception as e:
            raise
```

### **11.5. GUI приложение**
```python
import tkinter as tk
from spion import watch, user, state, throttle

class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.text = tk.Text(self.root)
        self.text.pack()
        self.filename = None
        self.modified = False
    
    @user()
    def on_click(self, event):
        """Клик мыши в тексте"""
        pos = self.text.index(f"@{event.x},{event.y}")
        line, col = map(int, pos.split('.'))
        click_pos = type('Pos', (), {'row': line, 'col': col})()
        return click_pos
    
    @state()
    def on_key(self, event):
        """Изменение текста"""
        self.modified = True
        self.update_title()
    
    @watch(level=LogLevel.INFO)
    def save_file(self):
        """Сохранение файла"""
        if self.filename:
            content = self.text.get('1.0', tk.END)
            with open(self.filename, 'w') as f:
                f.write(content)
            self.modified = False
            self.update_title()
    
    @throttle(interval=1.0)
    def update_cursor_position(self, event=None):
        """Обновление позиции курсора - не чаще 1 раза в секунду"""
        pos = self.text.index(tk.INSERT)
        line, col = pos.split('.')
        self.status_bar.config(text=f"Line: {line}, Col: {col}")
```

---

<a name="12-полный-пример-с-конфигурацией"></a>
## **12. Полный пример с конфигурацией**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

```python
"""
Полный пример использования всех возможностей spion
с реальной игрой в шашки и синтаксическим сахаром
"""

from spion import (
    # Конфигурация
    configure, configure_filter, add_rule, reset_filter,
    get_suppression_summary,
    
    # Уровни логирования
    LogLevel,
    
    # Синтаксический сахар ✨
    watch, trace, user, state, throttle, light, silent, spy,
    
    # Оригинальные декораторы (для сложных случаев)
    log_class_relationship,
    
    # Утилиты
    log_message, get_timestamp
)

import time
from enum import Enum

# ===== НАСТРОЙКА ЛОГИРОВАНИЯ =====
def setup_game_logging(debug_mode=False):
    """Настройка логирования для игры"""
    
    if debug_mode:
        # Режим отладки - всё видно
        configure(
            enabled=True,
            min_level=LogLevel.DEBUG,
            show_timestamp=True,
            color_enabled=True
        )
        configure_filter(
            suppress_repetitive=False,
            max_repetitions=100
        )
    else:
        # Production режим - только важное
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
    
    # Правила для конкретных функций
    add_rule("get_valid_moves", call_type="call", max_calls=10, time_window=60)
    add_rule("draw_board", call_type="call", log_once=True)
    add_rule("_calculate_moves", call_type="chain", max_calls=50)

# ===== МОДЕЛИ =====
class Player(Enum):
    WHITE = "белые"
    BLACK = "черные"

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def to_chess_notation(self):
        return f"{chr(65 + self.col)}{8 - self.row}"

class Piece:
    def __init__(self, pos, player):
        self.pos = pos
        self.player = player
        self.id = id(self)

# ===== ИГРОВАЯ ЛОГИКА =====
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_initial_position()
    
    @light()  # Только факт вызова
    def setup_initial_position(self):
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece(Position(row, col), Player.BLACK)
        
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece(Position(row, col), Player.WHITE)
    
    @watch(level=LogLevel.DEBUG)
    def get_piece(self, pos):
        if 0 <= pos.row < 8 and 0 <= pos.col < 8:
            return self.grid[pos.row][pos.col]
        return None
    
    @trace(max_depth=2)
    def move_piece(self, from_pos, to_pos):
        piece = self.get_piece(from_pos)
        if piece:
            self.grid[to_pos.row][to_pos.col] = piece
            self.grid[from_pos.row][from_pos.col] = None
            piece.pos = to_pos
            return True
        return False

class MoveValidator:
    def __init__(self, board):
        self.board = board
        self._cache = {}
    
    @throttle(interval=2.0)
    def get_valid_moves(self, piece):
        """Получение допустимых ходов - не чаще 2 секунд"""
        cache_key = (piece.id, piece.pos.row, piece.pos.col)
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        moves = self._calculate_moves(piece)
        self._cache[cache_key] = moves
        return moves
    
    @trace(max_depth=3)
    def _calculate_moves(self, piece):
        """Расчет ходов с цепочкой вызовов"""
        return self._get_man_moves(piece)
    
    @watch(level=LogLevel.DEBUG)
    def _get_man_moves(self, piece):
        """Ходы простой шашки"""
        moves = []
        directions = [(-1, -1), (-1, 1)] if piece.player == Player.WHITE else [(1, -1), (1, 1)]
        
        for drow, dcol in directions:
            new_row = piece.pos.row + drow
            new_col = piece.pos.col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if not self.board.get_piece(Position(new_row, new_col)):
                    moves.append(Position(new_row, new_col))
        
        return moves

# ===== ИГРОВОЕ СОСТОЯНИЕ =====
class GameState:
    def __init__(self):
        self.board = Board()
        self.validator = MoveValidator(self.board)
        self.current_player = Player.WHITE
        self.selected_piece = None
        self.valid_moves = []
        self.move_count = 0
    
    @state()
    def switch_player(self):
        """Смена игрока"""
        self.current_player = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE
        self.selected_piece = None
        self.valid_moves = []
    
    @user()
    def select_piece(self, position):
        """Выбор шашки пользователем"""
        piece = self.board.get_piece(position)
        
        if piece and piece.player == self.current_player:
            self.selected_piece = piece
            self.valid_moves = self.validator.get_valid_moves(piece)
            return True
        return False
    
    @spy(
        log_class_relationship(show_hierarchy=True),
        state()
    )
    def make_move(self, to_pos):
        """Совершение хода с полным шпионажем"""
        if not self.selected_piece or to_pos not in self.valid_moves:
            return False
        
        from_pos = self.selected_piece.pos
        
        # Перемещение
        self.board.move_piece(from_pos, to_pos)
        self.move_count += 1
        
        # Смена игрока
        self.switch_player()
        return True

# ===== РЕНДЕРЕР =====
class GameRenderer:
    def __init__(self):
        self.show_coordinates = True
    
    @throttle(interval=1.0)
    def draw_board(self, game_state):
        """Отрисовка доски - не чаще 1 раза в секунду"""
        board = game_state.board
        selected = game_state.selected_piece
        moves = game_state.valid_moves
        
        print("\n" + "="*40)
        print(f"Ход: {game_state.current_player.value}")
        
        if selected:
            print(f"Выбрана: {selected.pos.to_chess_notation()}")
        
        if moves:
            moves_str = [pos.to_chess_notation() for pos in moves]
            print(f"Доступные ходы: {', '.join(moves_str)}")
        
        print("="*40)

# ===== ГЛАВНЫЙ КЛАСС ИГРЫ =====
class CheckersGame:
    def __init__(self, debug=False):
        self.game_state = GameState()
        self.renderer = GameRenderer()
        self.running = True
        self.debug_mode = debug
        setup_game_logging(debug)
    
    @user()
    def handle_click(self, position):
        """Обработка клика пользователя"""
        log_message(LogLevel.DEBUG, f"Клик в позиции {position.to_chess_notation()}")
        
        if self.game_state.selected_piece:
            if position in self.game_state.valid_moves:
                self.game_state.make_move(position)
            else:
                self.game_state.select_piece(position)
        else:
            self.game_state.select_piece(position)
    
    @state()
    def toggle_debug(self):
        """Переключение режима отладки"""
        self.debug_mode = not self.debug_mode
        setup_game_logging(self.debug_mode)
        
        if self.debug_mode:
            print("🔧 Режим отладки ВКЛЮЧЕН")
        else:
            summary = get_suppression_summary()
            if summary:
                print("\n📊 Статистика подавленных вызовов:")
                for key, count in summary.items():
                    print(f"  {key}: {count} раз")
            print("🔧 Режим отладки ВЫКЛЮЧЕН")
    
    def run(self):
        """Главный цикл игры"""
        print("🎮 Русские шашки")
        print("Команды: [1-8][A-H] - ход, 'd' - отладка, 'q' - выход")
        
        while self.running:
            self.renderer.draw_board(self.game_state)
            
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'q':
                self.running = False
            elif cmd == 'd':
                self.toggle_debug()
            elif len(cmd) == 2 and cmd[0] in '12345678' and cmd[1] in 'abcdefgh':
                row = 8 - int(cmd[0])
                col = ord(cmd[1]) - ord('a')
                
                if 0 <= row < 8 and 0 <= col < 8:
                    self.handle_click(Position(row, col))
                else:
                    print("❌ Некорректная позиция")
            else:
                print("❌ Неизвестная команда")

# ===== ЗАПУСК =====
if __name__ == "__main__":
    # Запускаем с отладкой для демонстрации
    game = CheckersGame(debug=True)
    game.run()
```

---

### **Ключевые выводы о синтаксическом сахаре:**

<p align="right">
  <a href="README.md">← Вернуться в README</a>
</p>

1. **Читаемость** - код говорит сам за себя:
   - `@watch()` - я слежу за функцией
   - `@trace()` - я трассирую рекурсию
   - `@user()` - это действие пользователя
   - `@state()` - здесь меняется состояние
   - `@throttle()` - ограничиваю частоту
   - `@light()` - только факт вызова
   - `@silent()` - только ошибки
   - `@spy()` - шпионю за всем сразу

2. **Краткость** - меньше печатать:
   - `@trace(max_depth=5)` вместо `@log_method_chain(max_depth=5)`
   - `@throttle(interval=60)` вместо `@log_call_once(interval=60)`
   - `@watch()` вместо `@log()`
   - `@user()` вместо `@log_user_action()`
   - `@state()` вместо `@log_state_change()`

3. **Гибкость** - можно использовать оба стиля:
   - `@log()` для максимальной явности
   - `@watch()` для естественного языка
   - Миксовать в одном проекте

4. **Совместимость** - все алиасы работают как оригиналы:
   - Те же параметры
   - Те же возможности
   - Та же производительность

5. **Семантичность** - декораторы говорят о намерении:
   - `@user()` - понятно, что это действие пользователя
   - `@state()` - очевидно, что меняется состояние
   - `@trace()` - сразу ясно про трассировку

---

<p align="center">
  <a href="README.md">← Назад к README</a> •
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a>
</p>
```