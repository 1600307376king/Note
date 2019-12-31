#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/31 0031 16:29
# @Author  : HelloWorld
# @File    : common_form.py
from flask_wtf import FlaskForm
from flask_wtf.file import *
from wtforms import *


class SearchForm(FlaskForm):
    keyword = StringField('关键词：', [validators.Length(min=1, max=10, message='搜索条件为空或输入字符太长')])
    submit = SubmitField('搜索')


class LoginForm(FlaskForm):
    name = StringField('用户名：', [validators.length(min=1, max=10, message='输入账号格式错误')],
                       render_kw={'placeholder': '请输入用户名'})
    password = PasswordField('密码：',  [validators.length(min=1, max=10, message='输入密码格式错误')],
                             render_kw={'placeholder': '请输入密码'})
    submit = SubmitField('确定')