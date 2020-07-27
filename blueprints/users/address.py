from flask import Blueprint, views, render_template, request, flash, redirect, url_for
from flask_login import current_user

from mid import db
from models import Address
address_bp = Blueprint('address', __name__)


class Address_view(views.MethodView):

    def get(self):
        if current_user.is_authenticated:
            del_id = request.args.get('del', None)
            if del_id:
                Address.query.filter_by(id=del_id, user_address=current_user.id).delete()
                # db.session.delete(del_obj)
                db.session.commit()
                flash('删除完成')
                return redirect(url_for('address.address'))
            address_all = current_user.address_user_set
            return render_template('./user/address.html', address_all=address_all)
        else:
            flash('请登陆')
            return redirect('login')

    def post(self):
        address_all = current_user.address_user_set
        phone = request.form.get('phone', None)
        site = request.form.get('sit', None)
        name = request.form.get('name', None)
        if phone and site and name:
            address = Address()
            address.phone = phone
            address.site = site
            address.name = name
            address.user_address = current_user.id
            db.session.add(address)
            db.session.commit()
            flash('添加完成')
            return redirect(url_for('address.address'))
        flash('检查输入完整')
        return render_template('./user/address.html', address_all=address_all)


address_bp.add_url_rule('/', view_func=Address_view.as_view('address'))