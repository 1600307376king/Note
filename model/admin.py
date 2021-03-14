#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 0030 9:26
# @Author  : HelloWorld
# @File    : admin_manage.py
from flask_login import UserMixin
from main import db
from datetime import datetime


class AdminInfo(db.Model, UserMixin):
    __table_name__ = 'AdminInfo'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    adminName = db.Column(db.String(21), nullable=True)
    passwordHash = db.Column(db.String(255), nullable=True)

    def __unicode__(self):
        return self.adminName
''

class User(db.Model):
    __table_name__ = 'User'
    user_id = db.Column(db.INT, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False, comment='用户名')
    user_password = db.Column(db.String(100), nullable=False, comment='密码')
    user_nickname = db.Column(db.String(50), nullable=False, comment='昵称')
    user_phone_number = db.Column(db.String(50), nullable=True, comment='手机号')
    user_email = db.Column(db.String(100), nullable=True, comment='邮箱')
    user_create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    user_last_login_time = db.Column(db.DateTime, nullable=False, comment='最近登录时间')
    user_login_count = db.Column(db.INT, default=1, comment='登录次数')

    def __repr__(self):
        return self.UserId

