import csv
import mimetypes
import os.path
import smtplib
from email import encoders
from email.header import Header
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5 import QtCore,QtGui,uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog


class Win(QMainWindow):



    def __init__(self):
        super(Win, self).__init__()
        self.ui = uic.loadUi('WindowsForm.ui', self)
        self.listener()

    def listener(self):
        self.ui.send_mail.clicked.connect(self.sendmail)
        self.ui.choose_file.clicked.connect(self.open_file)

    def sendmail(self):
        try:
            if hasattr(self, 'path'):
                with open(self.ui.path, mode='r') as file:
                    csvfile = csv.reader(file)
                    for lines in csvfile:
                        print(lines)
                        row = lines[0].split(";")
                        msg = MIMEMultipart()
                        addr_to = row[0]
                        msg['From'] = self.ui.addr_from.text()
                        msg['To'] = addr_to
                        del row[0]
                        if len(row) > 1:
                            self.process_attachment(msg, row)
                        msg['Subject'] = Header(self.ui.msg_subj.text(), 'utf-8')
                        msg.attach(MIMEText(self.ui.msg_text.toPlainText(), 'plain', 'utf-8'))
                        server = self.choose_server()
                        server.login(self.ui.addr_from.text(), self.ui.msg_password.text())
                        server.sendmail(self.ui.addr_from.text(), addr_to, msg.as_string())
                        server.quit()
        except Exception as err:
            print(err)

    def choose_server(self):
        if self.ui.server.currentIndex() == 0:
            server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        else:
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        return server

    def open_file(self):
        filename = QFileDialog.getOpenFileName(
            self,
            'choose_file',
            '.',
            'csv (*.csv)'
        )
        print(filename)
        if filename:
            self.ui.path = filename[0]


    def process_attachment(self, msg, files):
        for f in files:
            if os.path.isfile(f):
                self.attach_file(msg, f)
            elif os.path.exists(f):
                dir=os.listdir(f)
                for file in dir:
                    self.attach_file(msg, file)

    def attach_file(self, msg, filepath):
        filename=os.path.basename(filepath)
        ctype, encoding = mimetypes.guess_type(filepath)
        if ctype is None or encoding is not None:
            ctype='application/octet-stream'
        maintype, subtype=ctype.split('/', 1)
        if maintype == 'text':
            with open(filepath) as fp:
                file=MIMEText(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'image':
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'audio':
            with open(filepath, 'rb') as fp:
                file = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
        else:
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)
                file.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(file)
        file.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(file)