#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 0030 9:20
# @Author  : HelloWorld
# @File    : admin.py
from flask import Flask, jsonify, Blueprint, request, render_template, flash, redirect, url_for
from .tool.filter_text import clean_data
from config.base_setting import *
from .tool.token_fuc import generate_token
from .form.common_form import *
from passlib.apps import custom_app_context as pwd_context
from wtforms import StringField, validators, SubmitField, PasswordField


login_index = Blueprint('login_page', __name__)

from model.top_category import TopCategory
from model.admin import Admin
from model.notes import Notes
from main import db


@login_index.route('/', methods=['POST', 'GET'])
def go_login():
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            login_name = login_form.name.data
            login_password = login_form.password.data
            admin_obj = Admin.query.filter(Admin.admin_name == login_name).first()
            if admin_obj:
                if admin_obj.verify_password(login_password):
                    token = generate_token(str(admin_obj.id))
                    return redirect(url_for('home_page.home', token=token))
                else:
                    flash([['密码错误']])
            else:
                flash([['用户不存在']])
        else:
            error_msg = login_form.errors
            flash(list(error_msg.values()))
    return render_template('login.html', form=login_form)


@login_index.route('/registered/', methods=['POST'])
def go_register():
    admin_name = request.form.get('admin_name', '')
    password = request.form.get('password', '')
    if admin_name and password:
        db.session.add(Admin(
            admin_name=admin_name,
            password=pwd_context.encrypt(password)
        ))

        db.session.commit()

        return 'register ok'
    return 'register fail'
