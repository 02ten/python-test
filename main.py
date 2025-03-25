import sys

from PyQt5.QtWidgets import QApplication

from Win import Win

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec())
