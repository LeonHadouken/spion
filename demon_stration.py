#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██╗░░░░░░█████╗░░█████╗░██╗███╗░░██╗
██║░░░░░██╔══██╗██╔══██╗██║████╗░██║
██║░░░░░██║░░██║██║░░██║██║██╔██╗██║
██║░░░░░██║░░██║██║░░██║██║██║╚████║
███████╗╚█████╔╝╚█████╔╝██║██║░╚███║
╚══════╝░╚════╝░░╚════╝░╚═╝╚═╝░░╚══╝

🕵️ SPION - ХАКЕРСКАЯ ДЕМОНСТРАЦИЯ
[ СИСТЕМА ГЛУБОКОГО НАБЛЮДЕНИЯ ЗА КОДОМ ]
"""

import time
import random
import sys
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import os


# Цвета для терминала
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


# Импортируем Spion
from spion import (
    log, watch, trace, user, state, throttle, light, silent, spy,
    log_method_chain, log_class_relationship, log_call_once,
    configure, LogLevel, add_rule, get_suppression_summary, reset_filter,
    disable_logging
)


def print_header(text: str, color: str = Colors.CYAN):
    """Красивый вывод заголовков"""
    print(f"\n{color}{'═' * 60}{Colors.END}")
    print(f"{color}{Colors.BOLD}► {text}{Colors.END}")
    print(f"{color}{'═' * 60}{Colors.END}")
    time.sleep(0.5)


def print_status(text: str, status: str = "OK", color: str = Colors.GREEN):
    """Вывод статуса"""
    print(f"{color}[{status}]{Colors.END} {text}")


def hacking_animation():
    """Анимация взлома"""
    chars = "█▓▒░█▓▒░"
    for _ in range(20):
        sys.stdout.write(f"\r{Colors.GREEN}[ВЗЛОМ] {random.choice(chars)} УСТАНОВКА СОЕДИНЕНИЯ...{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.03)
    print()


# ============================================================================
# НАСТРОЙКА
# ============================================================================

print(f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ███████╗██████╗ ██╗ ██████╗ ███╗   ██║    ██╗   ██╗ ██████╗    ║
║   ██╔════╝██╔══██╗██║██╔═══██╗████╗  ██║    ██║   ██║██╔═══██╗   ║
║   ███████╗██████╔╝██║██║   ██║██╔██╗ ██║    ██║   ██║██║   ██║   ║
║   ╚════██║██╔═══╝ ██║██║   ██║██║╚██╗██║    ╚██╗ ██╔╝██║   ██║   ║
║   ███████║██║     ██║╚██████╔╝██║ ╚████║     ╚████╔╝ ╚██████╔╝   ║
║   ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═══╝   ╚═════╝    ║
║                                                                  ║
║              🕵   Sehen alles, stören nichts.                     ║
║                — Видит всё, не мешает ничему —                   ║
║                                                                  ║
║                         ДЕМОНСТРАЦИЯ                             ║
║                           v0.1.0                                 ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.END}""")

input(f"{Colors.DIM}Нажми Enter, чтобы начать внедрение...{Colors.END}")
hacking_animation()

configure(
    enabled=True,
    min_level=LogLevel.DEBUG,
    show_timestamp=True,
    color_enabled=True,
    timestamp_format="%H:%M:%S.%f"
)

print_status("Модуль слежения активирован", "SPION")
time.sleep(0.5)

# ============================================================================
# 1. ВЗЛОМЩИК (Базовое логирование)
# ============================================================================

print_header("ФАЗА 1: ВНЕДРЕНИЕ НАБЛЮДАТЕЛЕЙ", Colors.RED)


@watch()
def access_file(filename: str) -> str:
    """Доступ к файлу"""
    return f"[ACCESS] {filename} opened"


@light()
def scan_port(port: int) -> bool:
    """Сканирование порта"""
    return port in [22, 80, 443, 8080]


@silent()
def exploit_attempt(target: str, should_fail: bool = False):
    """Попытка эксплойта (логирует только ошибки)"""
    if should_fail:
        raise RuntimeError(f"Exploit failed on {target}")
    return f"[+] {target} compromised"


print_status("Загрузка файлов...")
access_file("/etc/passwd")
access_file("/var/log/auth.log")

print_status("Сканирование портов...")
for port in [22, 23, 80, 443, 3389]:
    scan_port(port)

print_status("Попытки эксплойта...")
try:
    exploit_attempt("192.168.1.1", should_fail=True)
except:
    pass

time.sleep(1)

# ============================================================================
# 2. DOS-АТАКА (Throttle)
# ============================================================================

print_header("ФАЗА 2: DOS-АТАКА (SPAM-ЗАЩИТА)", Colors.YELLOW)


@throttle(interval=1.5)
def dos_attack(target: str) -> str:
    """DOS-атака с ограничением"""
    return f"[DOS] Packets sent to {target}"


print_status("Запуск распределённой атаки...")
targets = ["localhost", "127.0.0.1", "test.local", "sandbox.dev"]

for i in range(20):
    target = random.choice(targets)
    result = dos_attack(target)
    if result:
        print(f"  {result}")
    time.sleep(0.2)

print_status("Статистика атаки:", "INFO")
stats = get_suppression_summary()
for key, value in stats.items():
    if "dos_attack" in key:
        print(f"  └─ {key}: подавлено {value} попыток")

time.sleep(1)

# ============================================================================
# 3. ФИЗИЧЕСКОЕ ПРОНИКНОВЕНИЕ (User Actions)
# ============================================================================

print_header("ФАЗА 3: ФИЗИЧЕСКОЕ ПРОНИКНОВЕНИЕ", Colors.GREEN)


@dataclass
class Coordinates:
    """Координаты на карте"""
    x: int
    y: int
    z: Optional[int] = None


class InfiltrationTeam:
    def __init__(self):
        self.position = Coordinates(0, 0, 0)
        self.stealth = 100

    @user()
    def move_to(self, coords: Coordinates):
        """Перемещение по координатам"""
        self.position = coords
        return coords

    @user()
    def hack_terminal(self, terminal_id: str):
        """Взлом терминала"""
        return f"[HACK] Terminal {terminal_id} compromised"


team = InfiltrationTeam()
team.move_to(Coordinates(45.4642, 9.1900, 2))  # Милан, 2й этаж
team.hack_terminal("MAINFRAME-01")
team.move_to(Coordinates(41.9028, 12.4964))  # Рим
team.hack_terminal("SECURE-GW-01")

time.sleep(1)

# ============================================================================
# 4. ИЗМЕНЕНИЕ СОСТОЯНИЯ СИСТЕМЫ (State)
# ============================================================================

print_header("ФАЗА 4: МАНИПУЛЯЦИЯ СОСТОЯНИЕМ", Colors.BLUE)


class SecurityLevel(Enum):
    GREEN = "низкий"
    YELLOW = "средний"
    RED = "высокий"
    BLACK = "КРИТИЧЕСКИЙ"


class TargetSystem:
    def __init__(self):
        self.security_level = SecurityLevel.RED
        self.firewall_active = True
        self.alerts = 0
        self.current_player = "attacker"  # для @state

    @state()
    def disable_firewall(self):
        """Отключение фаервола"""
        self.firewall_active = False
        self.security_level = SecurityLevel.YELLOW
        return True

    @state()
    def trigger_alert(self):
        """Срабатывание тревоги"""
        self.alerts += 1
        if self.alerts > 3:
            self.security_level = SecurityLevel.BLACK
        return self.alerts


system = TargetSystem()
print_status("Попытка отключения защиты...")
system.disable_firewall()

print_status("Провокация срабатываний...")
for _ in range(5):
    system.trigger_alert()
    time.sleep(0.3)

time.sleep(1)

# ============================================================================
# 5. АНАЛИЗ ЦЕЛИ (Class Relationships)
# ============================================================================

print_header("ФАЗА 5: РАЗВЕДКА ЦЕЛИ", Colors.CYAN)


class NetworkInterface:
    def __init__(self, ip: str):
        self.ip = ip
        self.mac = f"00:1A:2B:{random.randint(10, 99)}:{random.randint(10, 99)}:{random.randint(10, 99)}"


class Firewall:
    def __init__(self):
        self.rules = ["ALLOW 22", "ALLOW 443", "DROP ALL ELSE"]


class Database:
    def __init__(self):
        self.type = "postgres"
        self.tables = ["users", "passwords", "credit_cards"]


class Server:
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.nic = NetworkInterface(f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}")
        self.firewall = Firewall()
        self.db = Database()
        self.os = "Linux 5.15"

    @log_class_relationship(show_hierarchy=True, show_dependencies=True)
    def scan_vulnerabilities(self):
        """Сканирование уязвимостей"""
        return f"[SCAN] {self.hostname} - найдено {random.randint(3, 10)} уязвимостей"


target = Server("PAYMENT-GATEWAY-01")
target.scan_vulnerabilities()

time.sleep(1)

# ============================================================================
# 6. РЕКУРСИВНЫЙ ВЗЛОМ (Trace / Chain)
# ============================================================================

print_header("ФАЗА 6: РЕКУРСИВНЫЙ ВЗЛОМ", Colors.RED)


@trace(max_depth=5)
def hack_network(network: str, depth: int = 0):
    """Рекурсивный взлом сети"""
    if depth > 3:
        return f"[ROOT] {network} compromised"

    subnets = [
        f"{network}.{random.randint(1, 254)}",
        f"{network}.{random.randint(1, 254)}"
    ]

    results = []
    for subnet in subnets:
        result = hack_network(subnet, depth + 1)
        results.append(result)

    return f"[+] {network} → {', '.join(results)}"


print_status("Запуск рекурсивного сканирования...")
result = hack_network("10.0")
print(f"\n{Colors.GREEN}Результат:{Colors.END} {result}")

time.sleep(1)

# ============================================================================
# 7. КОМПЛЕКСНАЯ АТАКА (Spy - всё сразу)
# ============================================================================

print_header("ФАЗА 7: КОМПЛЕКСНАЯ АТАКА", Colors.YELLOW)


class CyberWeapon:
    def __init__(self):
        self.current_player = "root"
        self.payloads = ["ransomware", "rootkit", "backdoor"]
        self.targets = []

    @spy(
        watch(level=LogLevel.INFO),
        user(),
        state(),
        trace(max_depth=3)
    )
    def deploy(self, target: str, payload: str):
        """Развёртывание кибер-оружия"""
        self.targets.append(target)
        self.current_player = "system"
        return f"[DEPLOY] {payload} → {target}"


weapon = CyberWeapon()
weapon.deploy("NSAGOV", "rootkit")
weapon.deploy("PENTAGON", "ransomware")

time.sleep(1)

# ============================================================================
# 8. РЕЖИМ НЕВИДИМКИ (Disable Logging)
# ============================================================================

print_header("ФАЗА 8: РЕЖИМ НЕВИДИМКИ", Colors.GREEN)


@watch()
def steal_credentials(service: str):
    """Кража учётных данных"""
    return f"[STEAL] Credentials from {service}"


print_status("Обычный режим (логи видны):")
steal_credentials("gmail.com")
steal_credentials("facebook.com")

print_status("\nРежим невидимки (логи отключены):")
with disable_logging():
    steal_credentials("mega-corp.local")
    steal_credentials("dark-forest.secure")
    steal_credentials("shadow-base.network")
    print(f"{Colors.DIM}  [тишина — логи не пишутся]{Colors.END}")

print_status("\nВозврат в обычный режим:")
steal_credentials("darkweb.onion")

# ============================================================================
# 9. СБРОС ФИЛЬТРОВ И ФИНАЛ
# ============================================================================

print_header("ФАЗА 9: ЗАМЕТАНИЕ СЛЕДОВ", Colors.BLUE)

reset_filter()
print_status("Фильтры сброшены", "CLEAN")
print_status("Логи очищены", "CLEAN")
print_status("Статистика подавлена", "CLEAN")

print(f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     ███████╗██████╗ ██╗ ██████╗ ███╗   ██║    ██╗   ██╗          ║
║     ██╔════╝██╔══██╗██║██╔═══██╗████╗  ██║    ██║   ██║          ║
║     ███████╗██████╔╝██║██║   ██║██╔██╗ ██║    ██║   ██║          ║
║     ╚════██║██╔═══╝ ██║██║   ██║██║╚██╗██║    ╚██╗ ██╔╝          ║
║     ███████║██║     ██║╚██████╔╝██║ ╚████║     ╚████╔╝           ║
║     ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═══╝            ║
║                                                                  ║
║              МИССИЯ ВЫПОЛНЕНА - ВСЕ ДАННЫЕ СОБРАНЫ               ║
║                                                                  ║
║        🕵️  Spion успешно проник в систему и вышел сухим          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.END}""")

print(f"\n{Colors.DIM}Демонстрация завершена. Всего протестировано декораторов: 8 основных + 7 алиасов{Colors.END}")
print(f"{Colors.DIM}Система наблюдения деактивирована. До новых встреч, агент.{Colors.END}\n")