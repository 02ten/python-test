import sys

import psycopg2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QLabel, 
                            QLineEdit, QPushButton, QListWidget, QTextEdit, QTableWidget,
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt
import sqlite3

class DatabaseHandler:
    def __init__(self):
        self.conn = None
        self.connected = False

    def connect(self, db_name):
        try:
            self.conn = psycopg2.connect(dbname=db_name, host="localhost", user="postgres", password="root", port="5432",
                                         options="-c search_path=dbo,public")
            self.connected = True
            return True
        except Exception as e:
            print(e)
            QMessageBox.critical(None, "Ошибка", f"Не удалось подключиться: {str(e)}")
            return False

    def get_tables(self):
        if self.connected:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
                return [table[0] for table in cursor.fetchall()]
            except Exception as e:
                print(e)
        return []

    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()

            # Получаем данные и заголовки столбцов
            data = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description] if cursor.description else []
            return data, headers
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка запроса: {str(e)}")
            return None, None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseHandler()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SQL Database Manager")
        self.setGeometry(300, 300, 800, 600)

        # Создаем вкладки
        tabs = QTabWidget()
        tabs.addTab(self.create_connection_tab(), "Подключение")
        tabs.addTab(self.create_dml_tab(), "DML операции")
        tabs.addTab(self.create_table_management_tab(), "Управление таблицами")
        tabs.addTab(self.create_sql_tab(), "SQL-запросы")

        self.setCentralWidget(tabs)

    def create_sql_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Текстовое поле для ввода запроса
        self.sql_editor = QTextEdit()
        self.sql_editor.setPlaceholderText("Введите SQL-запрос...")

        # Кнопка выполнения
        execute_btn = QPushButton("Выполнить запрос")
        execute_btn.clicked.connect(self.execute_sql_query)

        # Таблица для результатов
        self.result_table = QTableWidget()
        self.result_table.setSortingEnabled(True)

        layout.addWidget(QLabel("SQL-запрос:"))
        layout.addWidget(self.sql_editor)
        layout.addWidget(execute_btn)
        layout.addWidget(QLabel("Результаты:"))
        layout.addWidget(self.result_table)

        widget.setLayout(layout)
        return widget

    def execute_sql_query(self):
        query = self.sql_editor.toPlainText()
        if not query:
            QMessageBox.warning(self, "Ошибка", "Введите SQL-запрос")
            return

        data, headers = self.db.execute_query(query)

        if data is None:  # Обработка ошибок
            return

        # Очистка предыдущих результатов
        self.result_table.clear()
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(0)

        if headers:  # Для SELECT-запросов
            self.result_table.setColumnCount(len(headers))
            self.result_table.setHorizontalHeaderLabels(headers)

            self.result_table.setRowCount(len(data))
            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.result_table.setItem(row_idx, col_idx, item)

            self.result_table.resizeColumnsToContents()
        else:  # Для UPDATE/INSERT/DELETE
            QMessageBox.information(self, "Успех", f"Запрос выполнен. Затронуто строк: {len(data) if data else 0}")

        # Обновляем список таблиц если был DDL-запрос
        if any(keyword in query.upper() for keyword in ["CREATE", "DROP", "ALTER"]):
            self.update_tables_list()

    def create_sql_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Текстовое поле для ввода запроса
        self.sql_editor = QTextEdit()
        self.sql_editor.setPlaceholderText("Введите SQL-запрос...")

        # Кнопка выполнения
        execute_btn = QPushButton("Выполнить запрос")
        execute_btn.clicked.connect(self.execute_sql_query)

        # Таблица для результатов
        self.result_table = QTableWidget()
        self.result_table.setSortingEnabled(True)

        layout.addWidget(QLabel("SQL-запрос:"))
        layout.addWidget(self.sql_editor)
        layout.addWidget(execute_btn)
        layout.addWidget(QLabel("Результаты:"))
        layout.addWidget(self.result_table)

        widget.setLayout(layout)
        return widget

    def create_connection_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Поле для имени БД
        self.db_input = QLineEdit(":memory:")
        connect_btn = QPushButton("Подключиться")
        connect_btn.clicked.connect(self.connect_db)

        # Список таблиц
        self.tables_list = QListWidget()
        refresh_btn = QPushButton("Обновить список")
        refresh_btn.clicked.connect(self.update_tables_list)

        layout.addWidget(QLabel("Имя базы данных:"))
        layout.addWidget(self.db_input)
        layout.addWidget(connect_btn)
        layout.addWidget(QLabel("Таблицы в базе:"))
        layout.addWidget(self.tables_list)
        layout.addWidget(refresh_btn)

        widget.setLayout(layout)
        return widget

    def create_dml_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Поля для вставки данных
        self.table_input = QLineEdit()
        self.field_input = QLineEdit()
        self.value_input = QLineEdit()
        insert_btn = QPushButton("Вставить запись")
        insert_btn.clicked.connect(self.insert_data)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Таблица:"))
        form_layout.addWidget(self.table_input)
        form_layout.addWidget(QLabel("Поле:"))
        form_layout.addWidget(self.field_input)
        form_layout.addWidget(QLabel("Значение:"))
        form_layout.addWidget(self.value_input)
        form_layout.addWidget(insert_btn)

        # Отображение данных
        self.data_table = QTableWidget()

        layout.addLayout(form_layout)
        layout.addWidget(self.data_table)
        widget.setLayout(layout)
        return widget

    def create_table_management_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Создание таблицы
        self.new_table_input = QLineEdit()
        create_btn = QPushButton("Создать таблицу")
        create_btn.clicked.connect(self.create_table)

        # Удаление таблицы
        self.del_table_input = QLineEdit()
        del_btn = QPushButton("Удалить таблицу")
        del_btn.clicked.connect(self.delete_table)

        layout.addWidget(QLabel("Новая таблица:"))
        layout.addWidget(self.new_table_input)
        layout.addWidget(create_btn)
        layout.addWidget(QLabel("Удалить таблицу:"))
        layout.addWidget(self.del_table_input)
        layout.addWidget(del_btn)

        widget.setLayout(layout)
        return widget

    def connect_db(self):
        if self.db.connect(self.db_input.text()):
            self.update_tables_list()
            QMessageBox.information(self, "Успех", "Подключение установлено")

    def update_tables_list(self):
        self.tables_list.clear()
        self.tables_list.addItems(self.db.get_tables())

    def insert_data(self):
        table = self.table_input.text()
        field = self.field_input.text()
        value = self.value_input.text()

        if not all([table, field, value]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        query = f"INSERT INTO {table} ({field}) VALUES ('{value}')"
        self.db.execute_query(query)

    def create_table(self):
        table_name = self.new_table_input.text()
        if not table_name:
            QMessageBox.warning(self, "Ошибка", "Введите имя таблицы")
            return

        query = f"CREATE TABLE {table_name} (id BIGSERIAL PRIMARY KEY);"
        self.db.execute_query(query)
        self.update_tables_list()

    def delete_table(self):
        table_name = self.del_table_input.text()
        if not table_name:
            QMessageBox.warning(self, "Ошибка", "Введите имя таблицы")
            return

        query = f"DROP TABLE {table_name}"
        self.db.execute_query(query)
        self.update_tables_list()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
