# tests/test_real_integration.py
"""
Реальные интеграционные тесты с Flask, сокетами и tkinter.
"""

import pytest
import time
import socket
import threading
from flask import Flask, request, jsonify
import tkinter as tk
from tkinter import Text
from spion import watch, user, throttle, trace, configure
from tests.conftest import clean_ansi


# ============================================================================
# 11.1 Реальный тест Flask
# ============================================================================

class TestRealFlask:
    """Реальный тест Flask-приложения"""

    def test_flask_endpoint_with_logging(self, capsys):
        """Тестируем Flask endpoint с декораторами"""
        app = Flask(__name__)

        class WebServer:
            @user()
            @watch()
            def handle_request(self, user_id, endpoint):
                return {"user_id": user_id, "endpoint": endpoint, "status": "ok"}

        server = WebServer()

        @app.route('/api/<user_id>/<endpoint>')
        def api_endpoint(user_id, endpoint):
            result = server.handle_request(user_id, endpoint)
            return jsonify(result)

        # Тестируем с тестовым клиентом Flask
        with app.test_client() as client:
            response = client.get('/api/123/data')
            assert response.status_code == 200
            assert response.json == {"user_id": "123", "endpoint": "data", "status": "ok"}

            # Проверяем логи
            captured = capsys.readouterr()
            output = clean_ansi(captured.out)
            assert "[👤]" in output
            assert "handle_request" in output
            assert "▶️" in output

    def test_flask_error_logging(self, capsys):
        """Тестируем логирование ошибок во Flask"""
        app = Flask(__name__)

        class WebServer:
            @watch(level="ERROR")
            def database_call(self, query):
                if "DROP" in query:
                    raise ValueError("Dangerous query!")
                return {"result": "success"}

        server = WebServer()

        @app.route('/query')
        def query_endpoint():
            query = request.args.get('q', '')
            try:
                result = server.database_call(query)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        with app.test_client() as client:
            # Успешный запрос - может логироваться, но это не важно
            response = client.get('/query?q=SELECT')
            assert response.status_code == 200
            captured1 = capsys.readouterr()

            # Ошибочный запрос - должен быть лог с ошибкой
            response = client.get('/query?q=DROP')
            assert response.status_code == 500
            captured2 = capsys.readouterr()
            output2 = clean_ansi(captured2.out)

            # Проверяем что есть лог ошибки
            assert "[❌]" in output2 or "Dangerous query!" in output2


# ============================================================================
# 11.4 Реальный тест сокетов
# ============================================================================

class TestRealSocket:
    """Реальный тест TCP-сервера с сокетами"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.server = None
        self.server_thread = None
        self.received_data = []

    def echo_server(self, host='localhost', port=0):
        """Простой эхо-сервер с логированием"""
        import socket

        class EchoHandler:
            @trace(max_depth=2)
            def handle_client(self, conn, addr):
                data = conn.recv(1024)
                if data:
                    conn.sendall(data)
                conn.close()
                return data.decode()

        handler = EchoHandler()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(1)
        self.server_port = server_socket.getsockname()[1]

        def server_loop():
            while not self.server_stop:
                try:
                    server_socket.settimeout(1.0)
                    conn, addr = server_socket.accept()
                    data = handler.handle_client(conn, addr)
                    self.received_data.append(data)
                except socket.timeout:
                    continue
                except Exception:
                    break

        self.server_thread = threading.Thread(target=server_loop)
        self.server_thread.daemon = True
        self.server_thread.start()
        return self.server_port

    def test_tcp_echo_server(self, capsys):
        """Тестируем TCP эхо-сервер"""
        self.server_stop = False
        port = self.echo_server()

        # Клиент
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', port))
        test_data = b"Hello, Server!"
        client.sendall(test_data)
        response = client.recv(1024)
        client.close()

        # Останавливаем сервер
        self.server_stop = True
        if self.server_thread:
            self.server_thread.join(timeout=2)

        # Проверяем результат
        assert response == test_data
        assert self.received_data == [test_data.decode()]

        # Проверяем логи
        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[↘️]" in output
        assert "handle_client" in output


# ============================================================================
# 11.5 Реальный тест tkinter
# ============================================================================

class TestRealTkinter:
    """Реальный тест GUI с tkinter"""

    @pytest.fixture
    def tk_root(self):
        """Фикстура для tkinter root окна"""
        root = tk.Tk()
        root.withdraw()  # Прячем окно
        yield root
        root.destroy()

    def test_text_editor_actions(self, tk_root, capsys):
        """Тестируем реальный текстовый редактор на tkinter"""

        class TextEditor:
            def __init__(self, root):
                self.root = root
                self.text = Text(root, height=10, width=50)
                self.text.pack()
                self.modified = False

                # Привязываем события
                self.text.bind('<Button-1>', self.on_click)
                self.text.bind('<Key>', self.on_key)

            @user()
            def on_click(self, event):
                """Клик мыши"""
                # Конвертируем координаты в позицию текста
                index = self.text.index(f"@{event.x},{event.y}")
                line, col = map(int, index.split('.'))
                click_pos = type('Pos', (), {'row': line, 'col': col})()
                return click_pos

            @watch()
            def on_key(self, event):
                """Нажатие клавиши"""
                self.modified = True
                return event.char

            @throttle(interval=0.5)
            def update_status(self, line, col):
                """Обновление статуса (не чаще 0.5 сек)"""
                return f"Cursor at {line}:{col}"

        editor = TextEditor(tk_root)

        # Эмулируем клик
        event = type('Event', (), {'x': 50, 'y': 30})()
        editor.on_click(event)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "[👤]" in output
        assert "on_click" in output

        # Эмулируем нажатие клавиши
        event = type('Event', (), {'char': 'a'})()
        editor.on_key(event)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        assert "▶️" in output
        assert "on_key" in output
        assert editor.modified is True

        # Проверяем throttle
        for i in range(5):
            editor.update_status(i, i * 10)
            time.sleep(0.1)

        captured = capsys.readouterr()
        output = clean_ansi(captured.out)
        lines = [line for line in output.strip().split('\n') if line.strip()]
        assert len(lines) <= 2  # Не чаще 0.5 сек


# ============================================================================
# Комплексный тест с реальными компонентами
# ============================================================================

class TestRealIntegration:
    """Комплексный тест с реальными компонентами"""

    def test_flask_socket_integration(self, capsys):
        """Тестируем взаимодействие Flask и сокетов"""
        from flask import Flask, jsonify
        import socket
        import threading

        # Сокет-сервер
        class DataServer:
            @trace()
            def get_data(self, query):
                return f"Data for {query}"

        data_server = DataServer()

        # Flask приложение
        app = Flask(__name__)

        class WebApp:
            @user()
            @watch()
            def handle_api(self, user_id, query):
                # Запрашиваем данные через сокет (эмуляция)
                result = data_server.get_data(query)
                return {"user": user_id, "data": result}

        web_app = WebApp()

        @app.route('/api/<user_id>/<query>')
        def api(user_id, query):
            result = web_app.handle_api(user_id, query)
            return jsonify(result)

        # Тестируем
        with app.test_client() as client:
            response = client.get('/api/123/test')
            assert response.status_code == 200
            assert response.json == {"user": "123", "data": "Data for test"}

            # Проверяем логи обоих компонентов
            captured = capsys.readouterr()
            output = clean_ansi(captured.out)
            assert "[👤]" in output  # user action
            assert "handle_api" in output
            assert "get_data" in output  # trace