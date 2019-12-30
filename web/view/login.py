#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 0030 9:20
# @Author  : HelloWorld
# @File    : admin.py
from flask import Flask, jsonify, Blueprint, request, render_template
from flask_wtf.file import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


login_index = Blueprint('login_page', __name__)

from model.admin import Admin
from main import db


class LoginForm(FlaskForm):
    name = StringField('用户名：', validators=[DataRequired(), validators.length(min=1, max=10, message='666')])
    password = PasswordField('密码：')
    submit = SubmitField('确定')


@login_index.route('/login/', methods=['POST', 'GET'])
def go_login():
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            login_name = login_form.name.data
            login_password = login_form.password.data
            print(login_name, login_password)
    return render_template('login.html', form=login_form)
