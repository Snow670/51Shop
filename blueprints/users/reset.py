from flask import Blueprint,views,request,render_template,redirect,url_for,Response
from werkzeug.security import generate_password_hash,check_password_hash

from models import User,MailSendRecord
from send_email import send_mail
from mid import db


blue_reset = Blueprint('reset',__name__,url_prefix='/reset/')


class ResetUser(views.MethodView):
    def get(self,code):
        code_email = MailSendRecord.query.filter_by(code=code).first()
        if code_email:
            context = {"msg":"请输入新密码~~~"}
            return render_template('user/reset.html',**context)
        else:
            return render_template('user/activate_err.html')
    def post(self,code):
        newpwd1 = request.form.get('newpwd1',None)
        newpwd2 = request.form.get('newpwd2',None)
        if newpwd1 == newpwd2:
            code_email = MailSendRecord.query.filter_by(code=code).first()
            email_user = User.query.filter_by(email=code_email.recipient).first()
            email_user.password = generate_password_hash(newpwd1)
            db.session.commit()
            return redirect('/login')
        else:
            context = {"msg":"两次密码不一致~~~"}
            return render_template('user/reset.html',**context)


class ForgetUser(views.MethodView):
    def get(self):
        context = {"msg":"请输入忘记密码的邮箱"}
        return render_template('user/forget.html',**context)
    def post(self):
        email = request.form.get('email',None)
        if User.query.filter_by(email=email).first():
            send_mail(email,send_type='forget')
            context = {"msg":"请到接收邮件修改密码~~~"}
            return render_template('user/forget.html',**context)
        else:
            context = {"msg":"您输入的邮箱有误！！！"}
            return render_template('user/forget.html',**context)
        

blue_reset.add_url_rule("forget/<code>",view_func=ResetUser.as_view("ResetUser"))
blue_reset.add_url_rule("",view_func=ForgetUser.as_view("ForgetUser"))