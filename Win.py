import csv
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5 import QtCore,QtGui,uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog


def evaluate_expression(expression):
    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def apply_operator(operators, values):
        right = values.pop()
        left = values.pop()
        op = operators.pop()
        if op == '+':
            values.append(left + right)
        elif op == '-':
            values.append(left - right)
        elif op == '*':
            values.append(left * right)
        elif op == '/':
            values.append(left / right)

    def parse(tokens):
        values = []
        operators = []
        i = 0
        while i < len(tokens):
            if tokens[i] == ' ':
                i += 1
                continue
            if tokens[i] == '(':
                operators.append(tokens[i])
            elif tokens[i].isdigit() or tokens[i] == '.':
                num = ''
                while (i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.')):
                    num += tokens[i]
                    i += 1
                values.append(float(num))
                continue
            elif tokens[i] == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()  # Remove '('
            elif tokens[i] in '+-*/':
                while (operators and precedence(operators[-1]) >= precedence(tokens[i])):
                    apply_operator(operators, values)
                operators.append(tokens[i])
            i += 1

        while operators:
            apply_operator(operators, values)
        return values[0]

    return parse(expression)


class Win(QMainWindow):

    def __init__(self):
        super(Win, self).__init__()
        self.ui = uic.loadUi('WindowsForm.ui', self)
        self.listener()

    def listener(self):
        self.ui.calculate_button.clicked.connect(self.calculate)

    def calculate(self):
        expression = self.ui.input_form.text()
        print(expression)
        result = evaluate_expression(expression)
        print(result)
        self.ui.result_label.setText(str(result))
