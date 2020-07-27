from flask_login import UserMixin

from mid import db
import datetime



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(64), default="不知名的家伙")
    phone = db.Column(db.BigInteger,default='0')
    email = db.Column(db.String(50))
    is_super = db.Column(db.Boolean, default=False)
    is_activate = db.Column(db.Boolean, default=False)
    uid = db.Column(db.BigInteger, unique=True)


class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(10))

    def __str__(self):
        return self.type_name


class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))
    img = db.Column(db.String(20))
    price = db.Column(db.Float)
    is_new = db.Column(db.Integer, default=1)
    is_sale = db.Column(db.Integer, default=1)    # 打折商品
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 商品添加时间
    sales_volume = db.Column(db.Integer) # 销量
    inventory = db.Column(db.Integer) # 库存
    good_type = db.Column(db.Integer, db.ForeignKey('type.id', ondelete='CASCADE'), nullable=False)
    type_good = db.relationship("Type", backref="type_good_set")


    def __str__(self):
        return self.name

class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    good_num = db.Column(db.Integer)
    all_price = db.Column(db.Integer)
    good_car = db.Column(db.Integer, db.ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    car_good = db.relationship("Goods", backref="car_good_set")
    user_car = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    car_user = db.relationship("User", backref="car_user_set")


#订单
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_mount = db.Column(db.Float,default=0.0)
    user_of = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    of_user = db.relationship("User", backref="of_user_set")
    address_of = db.Column(db.Integer, db.ForeignKey('address.id', ondelete='CASCADE'), nullable=False)
    of_address = db.relationship("Address", backref="of_address_set")
    add_time = db.Column(db.DATETIME, default=datetime.datetime.now)


# 订单详情
class OrderForm(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    good_num = db.Column(db.Integer)
    all_price = db.Column(db.Integer)
    good_of = db.Column(db.Integer, db.ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    of_good = db.relationship("Goods", backref="of_good_set")
    order_of = db.Column(db.Integer, db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    of_order = db.relationship("Order", backref="of_order_set")



class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))
    site = db.Column(db.String(40))
    phone = db.Column(db.BigInteger)
    user_address = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    address_user = db.relationship("User", backref="address_user_set")


class MailSendRecord(db.Model):
    __tablename__ = 'mailsendrecord'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient = db.Column(db.String(200))
    code = db.Column(db.String(200))
    send_type = db.Column(db.String(64))


class PhoneCode(db.Model):
    __tablename__ = 'phonecode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(200))
    code = db.Column(db.String(200))