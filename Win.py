import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5 import QtCore,QtGui,uic
from PyQt5.QtWidgets import QMainWindow


class Win(QMainWindow):
    def __init__(self):
        super(Win, self).__init__()
        self.ui = uic.loadUi('C:\Code\Email\emailPy\WindowsForm.ui', self)
        self.listener()

    def listener(self):
        self.ui.send_mail.clicked.connect(self.sendmail)


    def sendmail(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.ui.addr_from.text()
            msg['To'] = self.ui.addr_to.text()
            msg['Subject'] = Header(self.ui.msg_subj.text(), 'utf-8')
            msg.attach(MIMEText(self.ui.msg_text.toPlainText(), 'plain', 'utf-8'))
            server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
            server.login(self.ui.addr_from.text(), self.ui.msg_password.text())
            server.sendmail(self.ui.addr_from.text(), [self.ui.addr_to.text()], msg.as_string())
            server.quit()
        except Exception as err:
            print(err)

