#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 15:19
# @Author : jjc
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from werkzeug.security import generate_password_hash, check_password_hash
from main import auth
from model.admin import AdminInfo
import flask_wtf


@auth.verify_password
def verify_password(username, password):
    """
    后台登录时验证账号密码
    :param username: 输入用户名
    :param password: 输入密码
    :return:
    """
    admin_user = AdminInfo.query.filter_by(adminName=username).first()
    if admin_user and check_password_hash(admin_user.passwordHash, password):
        return admin_user


class NewAdminInfo(ModelView):
    """
    用户管理页
    用户增删改查数据库中的用户
    """
    # 开始csrf验证
    form_base_class = flask_wtf.Form
    # 填入不想显示的字段
    column_exclude_list = ['passwordHash']
    # 指定字段的别名
    column_labels = {
        'adminName': '用户名称',
        'passwordHash': '密码'
    }
    # 对名称排序
    column_sortable_list = ('adminName',)
    # 指定允许被搜索的字段
    column_searchable_list = ('adminName',)

    # 数据被创建时对数据进行处理
    def on_model_change(self, form, model, is_created):
        if is_created:
            # 对密码进行加密
            model.passwordHash = generate_password_hash(model.passwordHash)


class MyAdminIndexView(AdminIndexView):
    """
    重写后台管理首页
    在访问时添加登录验证
    """
    @expose('/')
    @auth.login_required
    def index(self):
        return super(MyAdminIndexView, self).index()






