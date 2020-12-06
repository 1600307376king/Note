#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 0030 9:26
# @Author  : HelloWorld
# @File    : admin_manage.py
from flask_login import UserMixin
from main import db


class AdminInfo(db.Model, UserMixin):
    __table_name__ = 'AdminInfo'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    adminName = db.Column(db.String(21), nullable=True)
    passwordHash = db.Column(db.String(255), nullable=True)

    def __unicode__(self):
        return self.adminName

