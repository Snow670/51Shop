from flask import Blueprint,views,request,render_template,redirect,url_for,Response
from werkzeug.security import generate_password_hash,check_password_hash

from models import User,MailSendRecord
from send_email import send_mail
from mid import db

blue_registers = Blueprint('register',__name__,url_prefix='/register/')


class EmailRegister(views.MethodView):
    def get(self):
        context = {"msg": "请输入邮箱~~"}
        return render_template('user/register.html',**context)
    def post(self):
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        if email and password:
            if User.query.filter_by(email=email).first():
                context = {"msg": "该邮箱已注册！"}
                return render_template('user/register.html',**context)
            else:
                add_data = User(username=email,password=generate_password_hash(password),email=email)
                db.session.add(add_data)
                db.session.commit()
                send_mail(email,send_type='register')
                context = {"msg": "邮件已发送，请接收邮件激活账号"}
                return render_template('user/register.html',**context)
        else:
            context = {"msg":"信息不完整"}
            return render_template('user/register.html',**context)


class ActivateUser(views.View):
    def dispatch_request(self,code):
        email_code = MailSendRecord.query.filter_by(code=code).first()
        if email_code:
            email = email_code.recipient
            activate_user = User.query.filter_by(email=email).first()
            activate_user.is_activate = True
            db.session.commit()
            return redirect('/login')
        else:
            return render_template('user/activate_err.html')


blue_registers.add_url_rule("",view_func=EmailRegister.as_view("EmailRegister"))
blue_registers.add_url_rule("activate/<code>",view_func=ActivateUser.as_view("ActivateUser"))
