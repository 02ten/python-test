from PyQt5 import QtCore,QtGui,uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog

class Win(QMainWindow):

    def __init__(self):
        super(Win, self).__init__()
        self.ui = uic.loadUi('WindowsForm.ui', self)
        self.listener()

    def listener(self):
        self.ui.save_button.clicked.connect(self.save_file)
        self.ui.open_button.clicked.connect(self.open_file)


    def save_file(self):
        filepath = self.ui.file_label.text()
        with open(filepath, 'w') as fp:
            fp.write(self.edit.toPlainText())
            fp.close()

    def open_file(self):
        filepath, _filter = QFileDialog.getOpenFileName(None, u'Открыть файл', "./", filter='text (*.txt)')
        if not filepath:
            self.ui.file_label.setText('Файл не найден')
            return
        self.ui.file_label.setText(filepath)
        with open(filepath) as fp:
            self.ui.edit.setPlainText(fp.read())
            fp.close()
