from flask import Flask,render_template
from flask_mail import Mail
from flask_login import LoginManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash

from blueprints.users import loginBlueprint
from blueprints.users import address
from blueprints.users import info_update
from blueprints.shopcar.car import car_bp
from blueprints.home.home import home

from mid import db
import models
from models import User,Goods, Type
from blueprints.users.register import blue_registers,EmailRegister,ActivateUser
from blueprints.users.iphone import blue_iphone
from blueprints.users.reset import blue_reset,ResetUser,ForgetUser
from send_email import mail
from admin import admin

app = Flask(__name__)
app.config.from_pyfile('./config.py')
app.secret_key = '51sx'  # 设置表单交互密钥
login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'login/'  # 设置用户登录视图函数 endpoint
db.init_app(app)
mail.init_app(app)
admin.init_app(app)
CORS(app, resources=r'/*')
# app.config['SECRET_KEY'] = '0'
app.register_blueprint(blue_registers)
app.register_blueprint(blue_reset)
app.register_blueprint(blue_iphone)
app.register_blueprint(car_bp)
app.register_blueprint(home)

@app.route('/',endpoint='index')
def index():
    # db.drop_all()
    # db.create_all()
    # add_data = User(username='admin',password=generate_password_hash('123456'),is_super=True,is_activate=True)
    # db.session.add(add_data)
    # db.session.commit()
    """
    首页
    """
    type = Type.query.all()
    # print(type[0].name)

    # 获取2个热门商品
    hot_goods = Goods.query.order_by(Goods.sales_volume.desc()).limit(2).all()
    # 获取12个新品
    new_goods = Goods.query.filter_by(is_new=1).order_by(
                    Goods.add_time.desc()
                        ).limit(12).all()
    # 获取12个打折商品
    sale_goods = Goods.query.filter_by(is_sale=1).order_by(
                    Goods.add_time.desc()
                        ).limit(12).all()
    return render_template('home/index.html',new_goods=new_goods,sale_goods=sale_goods,hot_goods=hot_goods, type=type) # 渲染模板


app.register_blueprint(loginBlueprint.login_bp, url_prefix='/login/')
app.register_blueprint(address.address_bp, url_prefix='/address/')
app.register_blueprint(info_update.infoUpdate_bp, url_prefix='/info/')


@login_manager.user_loader
def load_user(user_id):

    user = db.session.query(models.User).get(user_id)
    return user



if __name__ == '__main__':
    app.run(debug=True)
