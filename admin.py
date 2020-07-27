from flask_admin import Admin,BaseView,AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user,login_required
from flask import redirect

from models import User,Goods,Type
from mid import db 


admin = Admin(name=u'51商城后台管理系统',index_view=AdminIndexView(
        name='导航栏',
        url='/admin'
    ))


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_super == True:
            return True
        else:
            return False


admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(Type,db.session))
admin.add_view(MyModelView(Goods,db.session))



