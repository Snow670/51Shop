from flask import Blueprint,views,request,render_template,redirect,url_for,Response
from werkzeug.security import generate_password_hash,check_password_hash

from models import User,PhoneCode
from mid import db
import random,json
from yunpian import YunPian
from config import APIKEY


blue_iphone = Blueprint('iphone',__name__,url_prefix='/iphone/')


def ran_code():
    num_list = [0,1,2,3,4,5,6,7,8,9]
    ram = random.sample(num_list,4)
    str1 = '%d%d%d%d'%(ram[0],ram[1],ram[2],ram[3])
    return str1


class PhoneRegister(views.MethodView):
    def get(self):
        phone = request.args.get('phone',None)
        if User.query.filter_by(phone=phone).first():
            context = {"msg": "手机号已注册~~~"}
            return render_template('user/phone.html',**context)
        else:
            if phone:
                code1 = ran_code()
                yunpian = YunPian(APIKEY)
                status_yun = yunpian.send_sms(code=code1,mobile=phone)
                add_data = PhoneCode(phone=phone,code=code1)
                db.session.add(add_data)
                db.session.commit()
                context = {"msg": "验证码已发送~~~"}
                return render_template('user/phone.html',**context)
        context = {"msg": "请输入手机号~~~"}
        return render_template('user/phone.html',**context)
    def post(self):
        phone = request.form.get('phone',None)
        password = request.form.get('password',None)
        code = request.form.get('code',None)
        print(phone,password,code)
        if phone and password and code:
            if User.query.filter_by(phone=phone).first():
                context = {"msg": "手机号已注册~~~"}
                return render_template('user/phone.html',**context)
            else:
                print(111)
                is_code = PhoneCode.query.filter(PhoneCode.phone == phone,PhoneCode.code == code)
                if is_code:
                    print(222)
                    add_data = User(username=phone,password=generate_password_hash(password),phone=phone,is_activate=True)
                    db.session.add(add_data)
                    # db.session.delete(is_code)
                    db.session.commit()
                    return redirect('/login')
                else:
                    context = {"msg": "验证失败~~~"}
                    return render_template('user/phone.html',**context) 
        else:
            context = {"msg": "请填写完整的信息~~~"}
            return render_template('user/phone.html',**context)
        



blue_iphone.add_url_rule("",view_func=PhoneRegister.as_view("PhoneRegister"))