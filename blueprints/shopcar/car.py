from flask import Blueprint, render_template,request,redirect,url_for,flash
from models import User,Goods,Car,OrderForm,Address,Order
from mid import db
from flask import views
from flask_login import current_user
from alipay import *
from flask import session
import datetime

car_bp = Blueprint('car',__name__,url_prefix='/car')


#显示商品详情并添加至购物车
@car_bp.route('/detail/',methods=["post","get"])
def detail():
    
    id = request.args.get("id")
    good = Goods.query.filter(Goods.id == id).first()
    #热门商品
    hot_goods = Goods.query.order_by(Goods.sales_volume.desc()).limit(5).all()
    # 获取底部相关商品
    similar_goods = Goods.query.filter_by(good_type=good.good_type).order_by(Goods.add_time.desc()).limit(5).all()
    context = {
        'good':good,
        'hot_goods':hot_goods,
        'similar_goods':similar_goods,
        'msg':'不能为空'
    }
    if request.method == "POST":
        if current_user.is_authenticated:
            quantity = request.form.get('quantity')
            if quantity:
                prices = float(int(quantity)*float(good.price))
                obj = Car(good_num=quantity,all_price=prices,good_car=id,user_car=current_user.id)
                db.session.add(obj)
                db.session.commit()
                return redirect(url_for('car.list'))
            else:
                return render_template('home/goods_detail.html',**context)
        else:
            flash('请登陆')
            return redirect('/login')

    return render_template('home/goods_detail.html',**context)





#查看购物车
@car_bp.route('/list/')
def list():
    if current_user.is_authenticated:
        car = Car.query.filter(Car.user_car == current_user.id).all()
        if len(car) == 0:
            return render_template('home/empty_cart.html')
        else:
            total = 0
            for tt in car:
                total += tt.all_price

            id = request.args.get('id')
            site = Address.query.filter(Address.id == id).first()
            if site:
                session['site_id'] = site.id
            context = {
                'car':car,
                'site':site,
                'total':total
            }
            return render_template('home/shopping_cart.html',**context)
    else:
        flash('请登陆')
        return redirect('/login')


#添加物流信息
@car_bp.route('/add_site/')
def add_site():
    all_address = Address.query.filter(Address.user_address == current_user.id).all()
    context = {
        'all_address': all_address,
    }
    return render_template('home/add_site.html',**context)


#生成订单
@car_bp.route('/order/')
def order():
    if current_user.is_authenticated:
        car = Car.query.filter(Car.user_car == current_user.id).all()
        total = 0
        for tt in car:
            total += tt.all_price
        id = session.get('site_id')
        try:
            del session['site_id']
        except:
            pass
        obj = Order(order_mount=total,user_of=current_user.id,address_of=id)
        db.session.add(obj)
        db.session.commit()
        for goods in car:
            num = goods.good_num
            prices = goods.all_price
            gid = goods.good_car
            # 销量和库存
            sales_volumes = int(int(goods.car_good.sales_volume)+int(num))
            inventorys = int(int(goods.car_good.inventory) - int(num))
            #添加至订单详情
            obj2 = OrderForm(good_num=num,all_price=prices,good_of=gid,order_of=obj.id)
            db.session.add(obj2)
            #更新销量和库存
            Goods.query.filter(Goods.id == gid).update({"sales_volume":sales_volumes,"inventory":inventorys})
            db.session.commit()
        # 添加至订单后删除购物车
        Car.query.filter(Car.user_car == current_user.id).delete()
        db.session.commit()
        flash('订单生成')
        return redirect(url_for('car.order_list'))
    else:
        flash('请登陆')
        return redirect('/login')



# 清空购物车
@car_bp.route('/delete/')
def delete():
    if current_user.is_authenticated:
        Car.query.filter(Car.user_car == current_user.id).delete()
        db.session.commit()
        return render_template('home/empty_cart.html')
    else:
        flash('请登陆')
        return redirect('/login')



#查看历史订单
@car_bp.route('/order_list/')
def order_list():
    if current_user.is_authenticated:
        orders = OrderForm.query.join(Order).filter(Order.user_of == current_user.id).all()
        return render_template('home/order_list.html', orders=orders)
    else:
        flash('请登陆')
        return redirect('/login')




class Pay(views.MethodView):
    def post(self):
        # 获取订单号，根据订单生成 支付订单
        # 支付订单包括: 订单号、支付金额、订单名称
        id = request.form.get('id')
        time = datetime.datetime.now()
        no = int(str(time.hour)+str(time.minute)+str(time.second)+str(id))
        total = request.form.get('total')
        print(id,total)
        # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，
        url = alipay.direct_pay(
            subject="订单",  # 订单名称
            # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
            out_trade_no=no,  # 订单号
            total_amount=total,  # 支付金额
            return_url="http://127.0.0.1:5000/result/"  # 支付成功后，跳转url 【客户端显示】
        )

        # 将前面后的支付参数，拼接到支付网关
        # 注意：下面支付网关是沙箱环境，最终进行签名后组合成支付宝的url请求
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        # 返回的是支付宝的支付地址
        return {'re_url': re_url}




class Paynotify(views.MethodView):  # 异步支付通知
    def get(self):
        # 获取 支付成功的 订单号
        # 修改订单状态以及其他操作

        # 返回支付宝success，否则会不间断的调用该回调
        return {'msg': 'success'}


# 添加资源
car_bp.add_url_rule('paytest/', view_func=Pay.as_view('pay'))
car_bp.add_url_rule('payno/', view_func=Paynotify.as_view('paynot'))



