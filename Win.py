import psycopg2
from PyQt5 import QtCore,QtGui,uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem


class Win(QMainWindow):
    connection = psycopg2.connect(dbname="pr7", host="localhost", user="postgres", password="root", port="5432", schema="main")
    cursor = connection.cursor()

    def __init__(self):
        super(Win, self).__init__()
        self.ui = uic.loadUi('WindowsForm.ui', self)
        self.listener()

    def listener(self):
        self.ui.save_button.clicked.connect(self.save_file)
        self.ui.open_button.clicked.connect(self.open_file)


    def sendsql(self):
        try:
            self.cursor.execute(self.ui.sql_edit_plain.toPlainText())
            self.connection.commit()
            data = self.cursor.fetchall()
            if len(data) == 0:
                return
            colnames = [desc[0] for desc in self.cursor.description]
            columns_cnt = len(colnames)
            rows_cnt = len(data)
            self.sql_result_table.setColumnCount(columns_cnt)
            self.sql_result_table.setHorizontalHeaderLabels(colnames)
            self.sql_result_table.setRowCount(rows_cnt)
            for i in range(rows_cnt):
                for j in range(columns_cnt):
                    self.sql_result_table.setItem(i, j, QTableWidgetItem(data[i][j]))
        except psycopg2.Error as e:
            self.sql_error_plain.setPlainText(str(e))

