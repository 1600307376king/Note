#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/3 18:46
# @Author  : HelloWorld
# @File    : blueprint_reg.py
from main import app, db, login_manager

from flask_admin import Admin
from model.admin import AdminInfo


from squirrel.view.home_page.home import home_index
from squirrel.view.test import test_index
from squirrel.view.common_form.login import login_index
from squirrel.view.home_page.add_note import add_index
from squirrel.view.common_form.errors import error_index
from squirrel.view.home_page.modification import mod_index
from squirrel.view.label_manager.manage_label import bind_index
from squirrel.view.home_page.note_detail import detail_index
from squirrel.view.my_plan.plans import plan_index

from squirrel.view.admin_manager.admin_page import NewAdminInfo, MyAdminIndexView


# 蓝图注册
app.register_blueprint(add_index, url_prefix='/')
app.register_blueprint(mod_index, url_prefix='/')
app.register_blueprint(home_index, url_prefix='/')
app.register_blueprint(test_index, url_prefix='/')
app.register_blueprint(bind_index, url_prefix='/')
app.register_blueprint(error_index, url_prefix='/')
app.register_blueprint(login_index, url_prefix='/login/')
app.register_blueprint(detail_index, url_prefix='/detail/')
app.register_blueprint(plan_index, url_prefix='/')

# 后台管理入口， 重写MyAdminIndexView后台首页
admin = Admin(app, name='后台管理', index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(NewAdminInfo(AdminInfo, db.session, name='用户管理'))


# 登录管理
login_manager.login_view = 'login_page.go_login'
