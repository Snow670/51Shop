from flask import Blueprint, render_template, views, redirect, url_for, request
# from sqlalchemy.orm import sessionmaker
from models import Goods, Type

# session = sessionmaker(engine)()

home = Blueprint('home', __name__, url_prefix="/home/")


@home.route("/goods_list/")
def goods_list():
    """
    商品页
    """
    good_type = request.args.get('good_type')
    type = Type.query.all()
    print(type)
    page = request.args.get('page', 1, type=int)
    page_data = Goods.query.filter_by(good_type=good_type).paginate(page=page, per_page=12)
    hot_goods = Goods.query.filter_by(good_type=good_type).order_by(Goods.sales_volume.desc()).limit(7).all()
    return render_template('home/goods_list.html',page_data=page_data,hot_goods=hot_goods,good_type=good_type, type=type)


# @home.route("/goods_detail/<int:id>/", endpoint='goods_detail')
# def goods_detail(id=None):  # id 为商品ID
#     """
#     详情页
#     """
#     goods = Goods.query.get_or_404(id)

#     hot_goods = Goods.query.filter_by(good_type=goods.good_type).order_by(Goods.sales_volume.desc()).limit(5).all()
#     # 获取底部相关商品
#     similar_goods = Goods.query.filter_by(good_type=goods.good_type).order_by(Goods.add_time.desc()).limit(5).all()
#     return render_template('home/goods_detail.html',goods=goods,hot_goods=hot_goods,similar_goods=similar_goods)   # 渲染模板


@home.route("/search/")
def goods_search():
    """
    搜素功能
    """
    keywords = request.args.get('keywords','',type=str)
    print(keywords)

    if keywords :
        # 使用like实现模糊查询
        page_data = Goods.query.filter(Goods.name.like("%{keywords}%".format(keywords = keywords))).order_by(
            Goods.add_time.desc()
        ).limit(12).all()
        hot_goods = Goods.query.order_by(Goods.sales_volume.desc()).limit(7).all()

        return render_template("home/goods_search.html", page_data=page_data, keywords=keywords, hot_goods=hot_goods)
    else :
        page_data = Goods.query.order_by(
            Goods.add_time.desc()
        ).limit(12).all()
    hot_goods = Goods.query.order_by(Goods.sales_volume.desc()).limit(7).all()
    return render_template("home/goods_search.html", page_data=page_data,keywords=keywords,hot_goods=hot_goods)





