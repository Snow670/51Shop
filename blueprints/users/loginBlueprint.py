import json
from io import BytesIO

from flask import Blueprint, redirect, url_for, flash, make_response, session
from flask import views, render_template, request
import requests
from werkzeug.security import check_password_hash
from flask_login import logout_user, login_user

from mid import db
from .code import *

from models import User
from sqlalchemy import or_



from . import weibo


login_bp = Blueprint('login', __name__)


def user_verify(username, password):
    user = User.query.filter(or_(User.username == username, User.phone == username, User.email == username)).all()
    if user:
        try:
            if check_password_hash(user[0].password, password) and user[0].is_activate:
                print(user)
                return user[0]
        except:
            return None
        return None


class Login(views.MethodView):
    def get(self):
        return render_template('./user/login.html')

    def post(self):
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        code = request.form.get('code', None)

        if user_name and password and code:
            # if session.get('image') != code:
            #     flash('验证码错误')
            #     return render_template('./user/login.html')
            user = user_verify(user_name, password)
            if user:
                print(user)
                login_user(user, remember=True)
                return redirect('/')
            else:
                flash('不能为提供的用户信息登陆')
                return render_template('./user/login.html')

        flash('检查输入完整')
        return render_template('./user/login.html')


@login_bp.route('/weibo_login/')
def weibo_login():
    url = 'https://api.weibo.com/oauth2/' \
          'authorize?client_id='+weibo.client_id+'&response_type=code&redirect_uri='+weibo.redirect_uri

    return redirect(url)


class Bindemail(views.MethodView):
    def get(self):
        code = request.args.get('code')
        token = requests.post('https://api.weibo.com/oauth2/access_token?client_id=' + weibo.client_id + '&client_s'
                             'ecret=' + weibo.client_secret + '&grant_type=authorization_'
                                                              'code&redirect_uri=' +weibo.redirect_uri + '&code='+code)
        text = json.loads(token.text)

        if token.status_code != 200:
            flash('发生错误啦')
            return redirect('/login/')
        access_token = text['access_token']
        uid = text['uid']
        url = 'https://api.weibo.com/2/users/show.json?access_token='+access_token+'&uid='+uid
        info = json.loads(requests.get(url).text)
        username = info['idstr']
        uid = info['id']
        name = info['name']
        user = User.query.filter_by(username=username, uid=uid).all()
        if user:
            login_user(user[0], remember=True)
            return redirect('/')
        user_obj = User()
        user_obj.username = username
        user_obj.name = name
        user_obj.uid = uid
        user_obj.is_activate = True
        db.session.add(user_obj)
        db.session.commit()
        login_user(user_obj)
        return redirect('/')



class GetCode(views.MethodView):
    def get(self):
        image, str = validate_picture()
        # 将验证码图片以二进制形式写入在内存中，防止将图片都放在文件夹中，占用大量磁盘
        buf = BytesIO()
        image.save(buf, 'jpeg')
        buf_str = buf.getvalue()
        # 把二进制作为response发回前端，并设置首部字段
        response = make_response(buf_str)
        response.headers['Content-Type'] = 'image/gif'
        # 将验证码字符串储存在session中
        session['image'] = str
        return response


class Logout(views.MethodView):
    def get(self):
        logout_user()
        return redirect('/')


login_bp.add_url_rule('/', view_func=Login.as_view('login'))
login_bp.add_url_rule('code/', view_func=GetCode.as_view('code'))
login_bp.add_url_rule('bindemail/', view_func=Bindemail.as_view('bindemail'))
login_bp.add_url_rule('logout/', view_func=Logout.as_view('logout'))