from flask import Blueprint, views, render_template, request, flash, redirect, url_for, session
from flask_login import current_user

from mid import db
from models import User


infoUpdate_bp = Blueprint('info', __name__)


class InfoUpdate(views.MethodView):
    def get(self):
        if current_user.is_authenticated:
            return render_template('./user/info_update.html')
        flash('请登陆')
        return redirect('/login')

    def post(self):
        name = request.form.get('name')
        code = request.form.get('code')
        if name and code:
            # if session.get('image') != code:
            #     flash('验证码错误')
            #     return render_template('./user/info_update.html')
            user = User.query.get(current_user.id)
            user.name = name
            db.session.commit()
            flash('修改完成')
            return redirect('/')
        flash('检查输入完整')
        return render_template('./user/info_update.html')


infoUpdate_bp.add_url_rule('/', view_func=InfoUpdate.as_view('info'))