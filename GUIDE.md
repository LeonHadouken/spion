Отлично! Добавим навигацию и ссылки на README. Вот исправленный `GUIDE.md` с рабочими ссылками и кнопкой "Назад к README":

---

```markdown
# 🔧 ПОЛНОЕ РУКОВОДСТВО ПО SPION

<p align="right">
  <a href="README.md">← Назад к README</a>
</p>

## 📋 СОДЕРЖАНИЕ
- [1. @log() - Базовое логирование](#1-log---базовое-логирование)
- [2. @log_call_once() - Логирование с интервалом](#2-log_call_once---логирование-с-интервалом)
- [3. @log_user_action() - Действия пользователя](#3-log_user_action---действия-пользователя)
- [4. @log_state_change() - Изменения состояния](#4-log_state_change---изменения-состояния)
- [5. @log_class_relationship() - Связи между классами](#5-log_class_relationship---связи-между-классами)
- [6. @log_method_chain() - Цепочки вызовов](#6-log_method_chain---цепочки-вызовов)
- [7. Комбинирование декораторов](#7-комбинирование-декораторов)
- [8. Настройка под конкретные случаи](#8-настройка-под-конкретные-случаи)
- [9. Примеры для разных типов приложений](#9-примеры-для-разных-типов-приложений)
- [10. Полный пример с конфигурацией](#10-полный-пример-с-конфигурацией)

---

<a name="1-log---базовое-логирование"></a>
## **1. @log() - Базовое логирование**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **1.1. Минимальная конфигурация**
```python
from spion import log

@log()
def hello():
    return "world"

hello()
# [14:30:25.123] 🟢 ▶️ Вызов hello
```

### **1.2. С уровнем логирования DEBUG**
```python
from spion import log, LogLevel

@log(level=LogLevel.DEBUG)
def add(a, b):
    return a + b

result = add(5, 3)
# [14:30:25.123] 🔵 ▶️ Вызов add с аргументами: 5, 3
# [14:30:25.123] 🟢 ◀️ add -> 8
```

### **1.3. С уровнем логирования INFO**
```python
@log(level=LogLevel.INFO)
def process_data(data):
    return len(data)

process_data([1, 2, 3])
# [14:30:25.123] 🟢 ▶️ Вызов process_data
# (результат не логируется)
```

### **1.4. С уровнем логирования WARNING**
```python
@log(level=LogLevel.WARNING)
def check_disk_space():
    return "85% full"

check_disk_space()
# [14:30:25.123] 🟡 ▶️ Вызов check_disk_space
```

### **1.5. С уровнем логирования ERROR**
```python
@log(level=LogLevel.ERROR)
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
@log(message="Начинаем загрузку файла")
def load_file(filename):
    return open(filename).read()

load_file("data.txt")
# [14:30:25.123] 🟢 ▶️ Начинаем загрузку файла

@log(message="⚠️ ВНИМАНИЕ: редкая операция")
def rare_operation():
    pass

rare_operation()
# [14:30:25.123] 🟢 ▶️ ⚠️ ВНИМАНИЕ: редкая операция
```

### **1.7. Для методов класса**
```python
class Calculator:
    @log(level=LogLevel.INFO)
    def multiply(self, x, y):
        return x * y
    
    @log(level=LogLevel.DEBUG)
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
from spion import log, add_rule

@log()
def api_call(endpoint):
    return f"Response from {endpoint}"

# Логируем только первые 3 вызова
add_rule(
    pattern="api_call",
    rule_type="call",
    max_calls=3
)

for i in range(10):
    api_call(f"/users/{i}")
# Логи: вызовы 0, 1, 2
# Вызовы 3-9 без логов
```

### **1.9. С фильтрацией повторений - один раз за всё время**
```python
@log()
def initialize_database():
    return "DB initialized"

# Только один раз за всю программу
add_rule(
    pattern="initialize_database",
    rule_type="call",
    log_once=True
)

initialize_database()  # Лог
initialize_database()  # Без лога
initialize_database()  # Без лога
```

### **1.10. С фильтрацией повторений - с временным окном**
```python
import time

@log()
def check_status():
    return "OK"

# Не чаще раза в 5 секунд
add_rule(
    pattern="check_status",
    rule_type="call",
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
@log()
def heavy_computation(n):
    return n ** 2

# Максимум 5 раз, но не чаще раза в 2 секунды
add_rule(
    pattern="heavy_computation",
    rule_type="call",
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
    @log(level=LogLevel.ERROR)
    def read_file(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        return open(filename).read()
    
    @log(level=LogLevel.DEBUG)
    def _internal_parse(self, content):
        lines = content.split('\n')
        return [line.strip() for line in lines]
    
    @log(level=LogLevel.INFO)
    def process(self, filename):
        content = self.read_file(filename)
        return self._internal_parse(content)

processor = FileProcessor()
processor.process("data.txt")
# INFO: [14:30:25.123] 🟢 ▶️ Вызов FileProcessor.process
# DEBUG: [14:30:25.123] 🔵 ▶️ Вызов FileProcessor._internal_parse с аргументами: 'line1\nline2'
# DEBUG: [14:30:25.123] 🟢 ◀️ FileProcessor._internal_parse -> ['line1', 'line2']
```

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

<a name="2-log_call_once---логирование-с-интервалом"></a>
## **2. @log_call_once() - Логирование с интервалом**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **2.1. Интервал 1 секунда**
```python
from spion import log_call_once
import time

@log_call_once(interval=1.0)
def update_display():
    return "display updated"

for i in range(50):
    update_display()
    time.sleep(0.05)  # 50ms
# Только первый вызов залогирован: [14:30:25.123] [🔄] update_display
```

### **2.2. Интервал 5 секунд**
```python
@log_call_once(interval=5.0)
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
@log_call_once(interval=60.0)
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
    
    @log_call_once(interval=10.0)
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
@log_call_once(interval=30.0)
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
    @log_call_once(interval=1.0)
    def log_fast_metrics(self):
        return f"Fast metrics: {time.time()}"
    
    @log_call_once(interval=60.0)
    def log_slow_metrics(self):
        return f"Slow metrics: {time.time()}"
    
    def monitor(self):
        while True:
            self.log_fast_metrics()   # Каждую секунду
            self.log_slow_metrics()   # Каждую минуту
            time.sleep(0.1)
```

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

<a name="3-log_user_action---действия-пользователя"></a>
## **3. @log_user_action() - Действия пользователя**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **3.1. Стандартное использование с Position**
```python
from spion import log_user_action

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Game:
    @log_user_action()
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

@log_user_action()
def on_click(point):
    pass

on_click(Point(2, 4))
# [14:30:25.123] [👤] on_click на E2
```

### **3.3. Без определения координат**
```python
@log_user_action()
def login(username, password):
    return authenticate(username, password)

login("user123", "pass")
# [14:30:25.123] [👤] login
```

### **3.4. Для методов с несколькими параметрами**
```python
class Editor:
    @log_user_action()
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
    @log_user_action()
    def select_piece(self, position):
        """Выбор шашки"""
        pass
    
    @log_user_action()
    def move_piece(self, from_pos, to_pos):
        """Ход шашкой - логируется только from_pos"""
        pass
    
    @log_user_action()
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
    @log_user_action()
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

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

<a name="4-log_state_change---изменения-состояния"></a>
## **4. @log_state_change() - Изменения состояния**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **4.1. С автоматическим определением current_player**
```python
from spion import log_state_change
from enum import Enum

class Player(Enum):
    WHITE = "белые"
    BLACK = "черные"

class Game:
    def __init__(self):
        self.current_player = Player.WHITE
    
    @log_state_change()
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
    
    @log_state_change()
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
    
    @log_state_change()
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
    
    @log_state_change()
    def increment(self):
        self.value += 1
    
    @log_state_change()
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
    
    @log_state_change()
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
    
    @log_state_change()
    def change_color(self):
        colors = ["red", "yellow", "green"]
        idx = colors.index(self.current_color)
        self.current_color = colors[(idx + 1) % 3]
        # Обновляем current_player в зависимости от цвета
        self.current_player = "cars" if self.current_color != "red" else "pedestrians"

light = TrafficLight()
light.change_color()  # [14:30:25.123] [🔄] TrafficLight.change_color | Ход: cars
light.change_color()  # [14:30:25.123] [🔄] TrafficLight.change_color | Ход: cars? (зависит от логики)
```

### **4.6. Для мониторинга изменений**
```python
class TemperatureController:
    def __init__(self):
        self.current_player = "system"  # Для декоратора
        self.temperature = 20
        self.target = 22
        self.heater_on = False
    
    @log_state_change()
    def set_temperature(self, new_temp):
        old_temp = self.temperature
        self.temperature = new_temp
        self.heater_on = self.temperature < self.target
        return old_temp != new_temp

controller = TemperatureController()
controller.set_temperature(21)  # [14:30:25.123] [🔄] set_temperature | Ход: system
controller.set_temperature(23)  # [14:30:25.123] [🔄] set_temperature | Ход: system
```

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

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
#   • data: list (экземпляр list) ⚠ (тип совпадает с классом)
#   • config: Config (экземпляр Config) ✓
#   • callback: function
#   📊 Иерархия: Processor -> object
#   🔗 Зависимости: (нет, если нет атрибутов)
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
#   • emp: Employee (экземпляр Employee) ✓
#   • new_company: Company (экземпляр Company) ✓
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
#   • obj: MyClass (экземпляр MyClass) ✓
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

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

<a name="6-log_method_chain---цепочки-вызовов"></a>
## **6. @log_method_chain() - Цепочки вызовов**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **6.1. Ограниченная глубина (max_depth=2)**
```python
from spion import log_method_chain

@log_method_chain(max_depth=2)
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
@log_method_chain()  # max_depth=5
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
@log_method_chain(max_depth=10)
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
    
    @log_method_chain(max_depth=10)
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
# Покажет вложенность обхода:
# [↘️] TreeNode.inorder() (root)
#   [↘️] TreeNode.inorder() (left)
#     [↘️] TreeNode.inorder() (left.left)
#     [↗️] TreeNode.inorder() -> [4]
#     [↘️] TreeNode.inorder() (left.right)
#     [↗️] TreeNode.inorder() -> [5]
#   [↗️] TreeNode.inorder() -> [4,2,5]
#   [↘️] TreeNode.inorder() (right)
#     ...
#   [↗️] TreeNode.inorder() -> [6,3,7]
# [↗️] TreeNode.inorder() -> [4,2,5,1,6,3,7]
```

### **6.5. Для парсера выражений**
```python
class ExpressionParser:
    @log_method_chain(max_depth=20)
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
    
    @log_method_chain(max_depth=10)
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
@log_method_chain(max_depth=3, level=LogLevel.INFO)
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

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

<a name="7-комбинирование-декораторов"></a>
## **7. Комбинирование декораторов**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **7.1. log + log_class_relationship**
```python
from spion import log, log_class_relationship

class DataService:
    @log(level=LogLevel.INFO)
    @log_class_relationship(show_dependencies=True)
    def fetch_data(self, query, connection):
        """Сначала покажет связи, потом простой лог"""
        return connection.execute(query)

service = DataService()
conn = DatabaseConnection()
service.fetch_data("SELECT * FROM users", conn)
# [14:30:25.123] [🔗] DataService.fetch_data
#   • query: str
#   • connection: DatabaseConnection (экземпляр DatabaseConnection) ✓
#   🔗 Зависимости: (зависимости объекта service)
#   ↩️ Результат: ResultSet
# [14:30:25.123] 🟢 ▶️ Вызов DataService.fetch_data
```

### **7.2. log_user_action + log_method_chain**
```python
class GameUI:
    @log_user_action()
    @log_method_chain(max_depth=5)
    def handle_click(self, position):
        """Для пользователя - действие, для разработчика - цепочка"""
        self.highlight_cell(position)
        self.select_piece(position)
        self.show_menu()

ui = GameUI()
ui.handle_click(Position(3, 4))
# [14:30:25.123] [👤] GameUI.handle_click на D5
# [14:30:25.123] 🔵 [↘️] GameUI.handle_click(Position(3,4))
#   [14:30:25.123] 🔵 [↘️] highlight_cell(Position(3,4))
#   [14:30:25.123] 🔵 [↗️] highlight_cell -> None
#   [14:30:25.123] 🔵 [↘️] select_piece(Position(3,4))
#   [14:30:25.123] 🔵 [↗️] select_piece -> True
#   ...
# [14:30:25.123] 🔵 [↗️] GameUI.handle_click -> None
```

### **7.3. log_state_change + log_class_relationship**
```python
class GameEngine:
    def __init__(self):
        self.current_player = "X"
        self.board = Board()
        self.validator = MoveValidator()
    
    @log_state_change()
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
#   • position: Position (экземпляр Position) ✓
#   📊 Иерархия: GameEngine -> object
#   🔗 Зависимости: board: Board, validator: MoveValidator
#   ↩️ Результат: bool
# [14:30:25.123] [🔄] GameEngine.make_move | Ход: X
```

### **7.4. log_call_once + log_method_chain**
```python
class CacheManager:
    @log_call_once(interval=60.0)
    @log_method_chain(max_depth=3)
    def cleanup_old_entries(self):
        """Раз в минуту запускаем цепочку очистки"""
        self.scan_entries()
        self.remove_expired()
        self.optimize_storage()
        return "cleanup done"

cache = CacheManager()
for _ in range(100):
    cache.cleanup_old_entries()  # Лог только раз в минуту
    time.sleep(10)
```

### **7.5. Три декоратора одновременно**
```python
class ComplexSystem:
    @log(level=LogLevel.DEBUG)
    @log_user_action()
    @log_method_chain(max_depth=5)
    def process_user_request(self, user_id, request_data, position):
        """Максимальная информация"""
        result = self.validate(request_data)
        if result and position:
            self.execute(position)
        return result

system = ComplexSystem()
system.process_user_request(123, {"action": "click"}, Position(2, 3))
# [14:30:25.123] [👤] process_user_request на D4  (сначала действие)
# [14:30:25.123] 🔵 [↘️] process_user_request(123, {...}, Position(2,3))  (потом цепочка)
#   [↘️] validate(...)
#   [↗️] validate -> True
#   [↘️] execute(Position(2,3))
#   [↗️] execute -> None
# [14:30:25.123] 🔵 [↗️] process_user_request -> True
# [14:30:25.123] 🔵 ▶️ Вызов process_user_request с аргументами: 123, {...}, Position(2,3)  (потом простой лог)
# [14:30:25.123] 🟢 ◀️ process_user_request -> True
```

### **7.6. Разный порядок декораторов**
```python
class OrderTest:
    @log(level=LogLevel.INFO)
    @log_class_relationship()
    def method1(self):
        """Сначала relationship, потом simple"""
        pass
    
    @log_class_relationship()
    @log(level=LogLevel.INFO)
    def method2(self):
        """Сначала simple, потом relationship"""
        pass

test = OrderTest()
test.method1()
# [🔗] ...  (relationship)
# 🟢 ▶️ ...  (simple)

test.method2()
# 🟢 ▶️ ...  (simple)
# [🔗] ...  (relationship)
```

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

<a name="8-настройка-под-конкретные-случаи"></a>
## **8. Настройка под конкретные случаи**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **8.1. Для продакшена - минимум логов**
```python
from spion import configure, configure_filter, LogLevel

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
    from spion import add_rule
    add_rule("health_check", max_calls=10, time_window=3600)  # 10 раз в час
    add_rule("status", log_once=True)  # Только один раз

setup_production()
```

### **8.2. Для разработки - максимум информации**
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

### **8.3. Для отладки конкретной функции**
```python
def setup_debug_for_parser():
    """Тихо всё, кроме парсера"""
    configure(min_level=LogLevel.ERROR)  # Только ошибки
    
    # А для парсера - всё подряд
    from spion import add_rule
    add_rule(
        pattern="parse_",
        rule_type="call",
        max_calls=1000,  # Много раз
        log_once=False
    )
    add_rule(
        pattern="parse_",
        rule_type="chain",
        max_calls=1000
    )
    
    # Специальные декораторы для парсера
    from spion import log, log_method_chain
    
    class Parser:
        @log(level=LogLevel.DEBUG)
        @log_method_chain(max_depth=20)
        def parse_expression(self, tokens):
            pass

setup_debug_for_parser()
```

### **8.4. Для тестирования**
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
        @log()
        def make_move():
            pass
        # Логи будут без timestamp, что упрощает сравнение

if __name__ == '__main__':
    unittest.main()
```

### **8.5. Динамическая настройка в рантайме**
```python
class DebugController:
    def __init__(self):
        self.debug_mode = False
        self.stats = {}
    
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
    
    @log()
    def important_function(self):
        pass

# В главном цикле
ctrl = DebugController()
while True:
    key = get_key()
    if key == 'F1':
        ctrl.toggle_debug()  # Можно включить/выключить отладку
    ctrl.important_function()
```

### **8.6. Для анализа производительности**
```python
import time

def setup_performance_logging():
    """Логирование для поиска узких мест"""
    configure(
        enabled=True,
        min_level=LogLevel.DEBUG,
        show_timestamp=True,
        color_enabled=True
    )
    
    from spion import add_rule
    # Логируем медленные функции
    add_rule("slow_function", max_calls=100)
    
    # Специальный декоратор для замера времени
    from functools import wraps
    from spion import log_message, get_timestamp
    
    def log_time(threshold=0.1):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                elapsed = time.time() - start
                
                if elapsed > threshold:
                    log_message(
                        LogLevel.WARNING,
                        f"⚠️ {func.__name__} took {elapsed:.3f}s",
                        get_timestamp()
                    )
                return result
            return wrapper
        return decorator
    
    return log_time

log_time = setup_performance_logging()

class Database:
    @log_time(threshold=0.5)  # Логируем если дольше 0.5 сек
    def slow_query(self):
        time.sleep(1)
        return "data"
```

### **8.7. Для разных окружений**
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

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

<a name="9-примеры-для-разных-типов-приложений"></a>
## **9. Примеры для разных типов приложений**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

### **9.1. Веб-сервер на Flask**
```python
from flask import Flask, request
from spion import log, log_call_once, log_user_action, LogLevel

app = Flask(__name__)

class WebServer:
    @log_call_once(interval=60)
    def health_check(self):
        """Проверка здоровья - раз в минуту"""
        return {"status": "ok"}
    
    @log_user_action()
    @log(level=LogLevel.INFO)
    def handle_request(self, user_id, endpoint):
        """Действие пользователя с логированием"""
        return f"Processed {endpoint} for user {user_id}"
    
    @log(level=LogLevel.ERROR)
    def database_operation(self, query):
        """Только ошибки базы данных"""
        try:
            return db.execute(query)
        except Exception as e:
            raise
    
    @log(level=LogLevel.DEBUG)
    def _parse_request_data(self, data):
        """Детальная отладка парсинга"""
        return data.strip()

server = WebServer()

@app.route('/api/data')
def api_endpoint():
    user_id = request.args.get('user_id')
    server.handle_request(user_id, '/api/data')
    return server.health_check()

@app.route('/api/query')
def query_endpoint():
    try:
        result = server.database_operation("SELECT * FROM users")
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}, 500
```

### **9.2. Игровой движок**
```python
class GameEngine:
    def __init__(self):
        self.current_player = "white"
        self.board = Board()
        self.physics = PhysicsEngine()
        self.renderer = Renderer()
        self.audio = AudioSystem()
    
    @log_method_chain(max_depth=5)
    def update(self, delta_time):
        """Отслеживаем всю цепочку обновления"""
        self.physics.update(delta_time)
        self.check_collisions()
        self.update_ai()
        self.renderer.prepare_frame()
    
    @log_class_relationship()
    def render_scene(self, camera):
        """Анализируем связи при рендеринге"""
        self.renderer.set_camera(camera)
        self.renderer.draw_board(self.board)
        self.renderer.draw_pieces(self.board.pieces)
    
    @log_state_change()
    def change_level(self, level_name):
        """Логируем смену уровня"""
        self.current_level = level_name
        self.load_level(level_name)
        self.current_player = "white"
    
    @log_user_action()
    def handle_input(self, key, mouse_pos):
        """Действия игрока"""
        if key == 'space':
            self.pause()
        elif mouse_pos:
            self.select_piece(mouse_pos)
    
    @log_call_once(interval=5.0)
    def log_fps(self, fps):
        """FPS не чаще 5 секунд"""
        print(f"FPS: {fps}")

engine = GameEngine()

# Главный цикл
while running:
    dt = clock.tick(60)
    engine.update(dt)
    engine.render_scene(camera)
    engine.log_fps(clock.get_fps())
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            engine.handle_input(event.key, None)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            engine.handle_input(None, event.pos)
```

### **9.3. Обработка данных**
```python
import pandas as pd
import numpy as np

class DataPipeline:
    def __init__(self):
        self.stats = {}
        self.cache = {}
        self.validator = DataValidator()
    
    @log(level=LogLevel.INFO)
    def load_data(self, filename):
        """Загрузка данных"""
        return pd.read_csv(filename)
    
    @log_method_chain(max_depth=3)
    def process_pipeline(self, data):
        """Конвейер обработки"""
        data = self.clean_data(data)
        data = self.transform_data(data)
        data = self.aggregate_data(data)
        return data
    
    @log(level=LogLevel.DEBUG)
    def clean_data(self, data):
        """Детальная очистка"""
        data = data.dropna()
        data = data[data['value'] > 0]
        return data
    
    @log_class_relationship()
    def transform_data(self, data):
        """Анализ типов при трансформации"""
        data['normalized'] = (data['value'] - data['value'].mean()) / data['value'].std()
        return data
    
    @log_call_once(interval=30.0)
    def log_progress(self, percent):
        """Прогресс не чаще 30 секунд"""
        self.stats['progress'] = percent
        print(f"Progress: {percent}%")
    
    @log(level=LogLevel.ERROR)
    def validate_result(self, data):
        """Проверка результата - только ошибки"""
        if not self.validator.is_valid(data):
            raise ValueError("Invalid data")

pipeline = DataPipeline()

# Обработка большого датасета
data = pipeline.load_data("large_dataset.csv")
total = len(data)

for i, chunk in enumerate(np.array_split(data, 100)):
    processed = pipeline.process_pipeline(chunk)
    pipeline.validate_result(processed)
    
    if i % 10 == 0:  # Каждые 10%
        pipeline.log_progress(i)
```

### **9.4. Сетевое приложение**
```python
import socket
import threading

class NetworkServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.running = False
    
    @log_call_once(interval=60)
    def log_stats(self):
        """Статистика раз в минуту"""
        return f"Connected clients: {len(self.clients)}"
    
    @log(level=LogLevel.INFO)
    def start(self):
        """Запуск сервера"""
        self.running = True
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        
        while self.running:
            client, addr = self.socket.accept()
            self.handle_client(client, addr)
    
    @log_method_chain(max_depth=3)
    def handle_client(self, client, addr):
        """Обработка клиента"""
        self.clients.append(client)
        data = self.receive_data(client)
        response = self.process_request(data)
        self.send_response(client, response)
        self.clients.remove(client)
    
    @log(level=LogLevel.DEBUG)
    def receive_data(self, client):
        """Детальный прием данных"""
        data = client.recv(1024)
        return data.decode()
    
    @log_class_relationship()
    def process_request(self, data):
        """Анализ запроса"""
        if data.startswith('GET'):
            return self.handle_get(data)
        elif data.startswith('POST'):
            return self.handle_post(data)
        return "ERROR"
    
    @log(level=LogLevel.ERROR)
    def send_response(self, client, response):
        """Отправка ответа - только ошибки"""
        try:
            client.send(response.encode())
        except Exception as e:
            raise

server = NetworkServer('localhost', 8080)
threading.Thread(target=server.start).start()
```

### **9.5. GUI приложение**
```python
import tkinter as tk
from spion import log, log_user_action, log_state_change

class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.text = tk.Text(self.root)
        self.text.pack()
        self.filename = None
        self.modified = False
    
    @log_user_action()
    def on_click(self, event):
        """Клик мыши в тексте"""
        pos = self.text.index(f"@{event.x},{event.y}")
        line, col = map(int, pos.split('.'))
        # Создаем объект с row/col для декоратора
        click_pos = type('Pos', (), {'row': line, 'col': col})()
        return click_pos
    
    @log_state_change()
    def on_key(self, event):
        """Изменение текста"""
        self.modified = True
        self.update_title()
    
    @log(level=LogLevel.INFO)
    def save_file(self):
        """Сохранение файла"""
        if self.filename:
            content = self.text.get('1.0', tk.END)
            with open(self.filename, 'w') as f:
                f.write(content)
            self.modified = False
            self.update_title()
    
    @log_call_once(interval=1.0)
    def update_cursor_position(self, event=None):
        """Обновление позиции курсора - не чаще 1 раза в секунду"""
        pos = self.text.index(tk.INSERT)
        line, col = pos.split('.')
        self.status_bar.config(text=f"Line: {line}, Col: {col}")
    
    def run(self):
        self.text.bind('<Button-1>', self.on_click)
        self.text.bind('<Key>', self.on_key)
        self.text.bind('<KeyRelease>', self.update_cursor_position)
        self.root.mainloop()
```

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

<a name="10-полный-пример-с-конфигурацией"></a>
## **10. Полный пример с конфигурацией**

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад</a>
</p>

```python
"""
Полный пример использования всех возможностей spion
с реальной игрой в шашки
"""

from spion import (
    # Конфигурация
    configure, configure_filter, add_rule, reset_filter,
    get_suppression_summary,
    
    # Уровни логирования
    LogLevel,
    
    # Декораторы
    log, log_call_once, log_user_action, log_state_change,
    log_class_relationship, log_method_chain,
    
    # Утилиты
    log_message, get_timestamp
)

import time
from enum import Enum

# ===== МОДЕЛИ =====
class Player(Enum):
    WHITE = "белые"
    BLACK = "черные"

class PieceType(Enum):
    MAN = "шашка"
    KING = "дамка"

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def to_chess_notation(self):
        """Конвертация в шахматную нотацию (A1, H8 и т.д.)"""
        return f"{chr(65 + self.col)}{8 - self.row}"

class Piece:
    def __init__(self, pos, player, piece_type=PieceType.MAN):
        self.pos = pos
        self.player = player
        self.type = piece_type
        self.id = id(self)

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_initial_position()
    
    def setup_initial_position(self):
        """Начальная расстановка"""
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece(Position(row, col), Player.BLACK)
        
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece(Position(row, col), Player.WHITE)
    
    def get_piece(self, pos):
        if 0 <= pos.row < 8 and 0 <= pos.col < 8:
            return self.grid[pos.row][pos.col]
        return None
    
    def move_piece(self, from_pos, to_pos):
        piece = self.get_piece(from_pos)
        if piece:
            self.grid[to_pos.row][to_pos.col] = piece
            self.grid[from_pos.row][from_pos.col] = None
            piece.pos = to_pos
            return True
        return False

# ===== ВАЛИДАТОР =====
class MoveValidator:
    def __init__(self, board):
        self.board = board
        self._cache = {}
    
    @log_call_once(interval=2.0)
    def get_valid_moves(self, piece):
        """Получение допустимых ходов - не чаще 2 секунд"""
        cache_key = (piece.id, piece.pos.row, piece.pos.col)
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        moves = self._calculate_moves(piece)
        self._cache[cache_key] = moves
        return moves
    
    @log_method_chain(max_depth=3)
    def _calculate_moves(self, piece):
        """Расчет ходов с цепочкой вызовов"""
        if piece.type == PieceType.MAN:
            return self._get_man_moves(piece)
        else:
            return self._get_king_moves(piece)
    
    @log(level=LogLevel.DEBUG)
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
    
    def _get_king_moves(self, piece):
        """Ходы дамки"""
        # Упрощенно для примера
        return []

# ===== ИГРОВОЕ СОСТОЯНИЕ =====
class GameState:
    def __init__(self):
        self.board = Board()
        self.validator = MoveValidator(self.board)
        self.current_player = Player.WHITE
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.move_count = 0
    
    @log_state_change()
    def switch_player(self):
        """Смена игрока"""
        self.current_player = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE
        self.selected_piece = None
        self.valid_moves = []
    
    @log_user_action()
    def select_piece(self, position):
        """Выбор шашки пользователем"""
        piece = self.board.get_piece(position)
        
        if piece and piece.player == self.current_player:
            self.selected_piece = piece
            self.valid_moves = self.validator.get_valid_moves(piece)
            return True
        return False
    
    @log_class_relationship(show_hierarchy=True, show_dependencies=True)
    def make_move(self, to_pos):
        """Совершение хода"""
        if not self.selected_piece or to_pos not in self.valid_moves:
            return False
        
        from_pos = self.selected_piece.pos
        
        # Проверка на дамку
        became_king = False
        if self.selected_piece.type == PieceType.MAN:
            if (self.selected_piece.player == Player.WHITE and to_pos.row == 0) or \
               (self.selected_piece.player == Player.BLACK and to_pos.row == 7):
                self.selected_piece.type = PieceType.KING
                became_king = True
        
        # Перемещение
        self.board.move_piece(from_pos, to_pos)
        
        # Сохраняем в историю
        self.move_history.append({
            'piece': self.selected_piece.id,
            'from': from_pos.to_chess_notation(),
            'to': to_pos.to_chess_notation(),
            'player': self.current_player.value,
            'became_king': became_king,
            'move_number': self.move_count + 1
        })
        self.move_count += 1
        
        # Смена игрока
        self.switch_player()
        return True
    
    @log(level=LogLevel.INFO)
    def check_game_over(self):
        """Проверка окончания игры"""
        white_pieces = 0
        black_pieces = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(Position(row, col))
                if piece:
                    if piece.player == Player.WHITE:
                        white_pieces += 1
                    else:
                        black_pieces += 1
        
        if white_pieces == 0:
            self.game_over = True
            self.winner = Player.BLACK
        elif black_pieces == 0:
            self.game_over = True
            self.winner = Player.WHITE
        
        return self.game_over

# ===== РЕНДЕРЕР =====
class GameRenderer:
    def __init__(self):
        self.show_coordinates = True
        self.highlight_selected = True
        self.last_click = None
    
    @log_call_once(interval=1.0)
    def draw_board(self, game_state):
        """Отрисовка доски - не чаще 1 раза в секунду"""
        board = game_state.board
        selected = game_state.selected_piece
        moves = game_state.valid_moves
        
        # Имитация отрисовки
        print("\n" + "="*40)
        print(f"Ход: {game_state.current_player.value}")
        print(f"Счет: W:{self._count_pieces(board, Player.WHITE)} B:{self._count_pieces(board, Player.BLACK)}")
        
        if selected:
            print(f"Выбрана: {selected.pos.to_chess_notation()} ({selected.type.value})")
        
        if moves:
            moves_str = [pos.to_chess_notation() for pos in moves]
            print(f"Доступные ходы: {', '.join(moves_str)}")
        
        print("="*40)
    
    @log(level=LogLevel.DEBUG)
    def _count_pieces(self, board, player):
        """Подсчет фигур игрока"""
        count = 0
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(Position(row, col))
                if piece and piece.player == player:
                    count += 1
        return count

# ===== ГЛАВНЫЙ КЛАСС ИГРЫ =====
class CheckersGame:
    def __init__(self):
        self.game_state = GameState()
        self.renderer = GameRenderer()
        self.running = True
        self.debug_mode = False
        self.setup_logging()
    
    def setup_logging(self):
        """Настройка логирования"""
        # Глобальная конфигурация
        configure(
            enabled=True,
            min_level=LogLevel.DEBUG if self.debug_mode else LogLevel.INFO,
            show_timestamp=True,
            color_enabled=True
        )
        
        # Настройка фильтров
        configure_filter(
            suppress_repetitive=True,
            max_repetitions=5,
            show_suppression_summary=True
        )
        
        # Добавление правил
        add_rule("get_valid_moves", max_calls=10, time_window=60)
        add_rule("draw_board", log_once=True)
        add_rule("_get_man_moves", max_calls=20)
        
        # Для отладки конкретной функции
        if self.debug_mode:
            add_rule("_calculate_moves", max_calls=100)
    
    @log_user_action()
    def handle_click(self, position):
        """Обработка клика пользователя"""
        log_message(LogLevel.DEBUG, f"Клик в позиции {position.to_chess_notation()}")
        
        if self.game_state.game_over:
            print(f"Игра окончена! Победитель: {self.game_state.winner.value}")
            return
        
        if self.game_state.selected_piece:
            # Пробуем сделать ход
            if position in self.game_state.valid_moves:
                success = self.game_state.make_move(position)
                if success:
                    self.game_state.check_game_over()
            else:
                # Пробуем выбрать другую шашку
                self.game_state.select_piece(position)
        else:
            # Выбираем шашку
            self.game_state.select_piece(position)
    
    @log_state_change()
    def toggle_debug(self):
        """Переключение режима отладки"""
        self.debug_mode = not self.debug_mode
        self.setup_logging()
        
        if self.debug_mode:
            print("🔧 Режим отладки ВКЛЮЧЕН")
        else:
            # Показываем статистику при выключении
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
                # Конвертация: например "3e" -> row=3, col=4 (e=4)
                row = 8 - int(cmd[0])  # 8-3=5 (в нашей системе 0 сверху)
                col = ord(cmd[1]) - ord('a')
                
                if 0 <= row < 8 and 0 <= col < 8:
                    self.handle_click(Position(row, col))
                else:
                    print("❌ Некорректная позиция")
            else:
                print("❌ Неизвестная команда")
        
        # Финальная статистика
        summary = get_suppression_summary()
        if summary:
            print("\n📊 Итоговая статистика:")
            for key, count in summary.items():
                print(f"  {key}: подавлено {count} вызовов")

# ===== ЗАПУСК =====
if __name__ == "__main__":
    game = CheckersGame()
    
    # Пример автоматической игры для демонстрации
    print("\n=== ДЕМОНСТРАЦИЯ ЛОГИРОВАНИЯ ===\n")
    
    # Несколько тестовых ходов
    test_moves = [
        Position(5, 0),  # Выбор белой шашки A3
        Position(4, 1),  # Ход на B4
        Position(2, 1),  # Выбор черной шашки B2? (неправильно, сейчас ход белых)
        Position(5, 2),  # Выбор другой белой шашки C3
        Position(4, 3),  # Ход на D4
    ]
    
    for pos in test_moves:
        game.handle_click(pos)
    
    print("\n" + "="*50)
    print("Запуск интерактивного режима")
    print("="*50 + "\n")
    
    # Запуск интерактивного режима
    game.run()
```

<p align="right">
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a> • <a href="README.md">← Назад к README</a>
</p>

---

### **Ключевые выводы:**

<p align="right">
  <a href="README.md">← Вернуться в README</a>
</p>

1. **Каждый декоратор решает свою задачу**:
   - `@log` - базовое логирование
   - `@log_call_once` - борьба со спамом
   - `@log_user_action` - действия пользователя
   - `@log_state_change` - изменения состояния
   - `@log_class_relationship` - анализ связей
   - `@log_method_chain` - отслеживание вложенности

2. **Можно комбинировать** для получения максимальной информации

3. **Гибкая настройка** через `configure()` и `add_rule()`

4. **Фильтрация** помогает не захламлять лог

5. **Статистика** (`get_suppression_summary()`) показывает эффективность фильтрации

---

<p align="center">
  <a href="README.md">← Назад к README</a> •
  <a href="#-полное-руководство-по-spion">↑ К содержанию</a>
</p>
```
