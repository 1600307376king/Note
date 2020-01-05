#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 0030 9:26
# @Author  : HelloWorld
# @File    : admin.py
from passlib.apps import custom_app_context as pwd_context
from main import db


class Admin(db.Model):
    __table_name__ = 'admin'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(20), nullable=True)

    def __init__(self, **kwargs):
        self.admin_name = kwargs['admin_name']
        self.password = kwargs['password']

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, admin_password):
        return pwd_context.verify(admin_password, self.password)