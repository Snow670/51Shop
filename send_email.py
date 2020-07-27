from random import Random

from models import MailSendRecord
from flask_mail import Message,Mail
import config
from mid import db

mail = Mail()


def random_str():
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(16):
        str += chars[random.randint(0, length)]
    return str


def send_mail(recipient1,send_type='register'):
    code = random_str()
    if send_type == 'register':
        msg = Message(subject='51商城注册激活链接',sender=config.MAIL_USERNAME,recipients=[recipient1])
        msg.body = "请点击下面的链接激活你的账号: http://127.0.0.1:5000/register/activate/{}".format(code)
        add_data = MailSendRecord(recipient=recipient1,code=code,send_type=send_type)
        db.session.add(add_data)
        db.session.commit()
        mail.send(msg)
        print('邮件发送~~~')
    elif send_type == 'forget':
        msg = Message(subject='51商城修改密码链接',sender=config.MAIL_USERNAME,recipients=[recipient1])
        msg.body = "请点击下面的链接修改你的密码: http://127.0.0.1:5000/reset/forget/{}".format(code)
        add_data = MailSendRecord(recipient=recipient1,code=code,send_type=send_type)
        db.session.add(add_data)
        db.session.commit()
        mail.send(msg)
        print('邮件发送~~~')