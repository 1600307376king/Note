#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 0030 9:20
# @Author  : HelloWorld
# @File    : admin.py
from flask import Flask, jsonify, Blueprint, request, render_template, flash, redirect, url_for
from .tool.filter_text import clean_data
from config.base_setting import *
from .form.common_form import *
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
                if admin_obj.password == login_password:
                    return redirect(url_for('home_page.home'))
                else:
                    flash([['密码错误']])
            else:
                flash('用户不存在')
        else:
            error_msg = login_form.errors
            flash(list(error_msg.values()))
    return render_template('login.html', form=login_form)
