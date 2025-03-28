import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def send_email():
    # Получаем данные из тела запроса
    data = request.get_json()

    # Извлекаем параметры
    addr_from = data.get('addrFrom')
    subject = data.get('subject')
    text = data.get('text')
    password = data.get('password')
    server = data.get('server')
    addr_to = data.get('addrTo')

    # Проверяем, что все параметры присутствуют
    if not all([addr_from, subject, text, addr_to, password, server]):
        return jsonify({'error': 'Missing required parameters'}), 400

    status = sendmail(addr_from, subject, text, addr_to, password, server)

    response = {
        'status': status,
        'message': 'Email data received',
        'data': {
            'from': addr_from,
            'to': addr_to,
            'subject': subject,
            'text': text
        }
    }

    return jsonify(response), 200


def sendmail(addr_from, subject, text, addr_to, password, server):
    try:
        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = Header(subject, 'utf-8')
        msg.attach(MIMEText(text, 'plain', 'utf-8'))

        server = choose_server(server)
        server.login(addr_from, password)
        server.sendmail(addr_from, [addr_to], msg.as_string())
        server.quit()
        return 'Success'
    except Exception as err:
        print(err)
        return 'Error'

def choose_server(server):
    if server == 'yandex':
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    elif server == 'mail':
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    else :
        raise Exception('Unknown server')
    return server

if __name__ == '__main__':
    app.run(debug=True)