#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/9 0009 11:23
# @Author  : HelloWorld
# @File    : test.py
import re
from flask import render_template, Blueprint, request, flash
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from main import app
from flask_uploads import UploadSet, IMAGES
import os

test_index = Blueprint('test_page', __name__)


# <<<----------------------
# wtf 表单[validators.Length(min=4, max=20), validators.DataRequired()]
class TestForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), validators.Length(min=4, max=8, message='用户名格式不正确')])
    password = PasswordField('password', validators=[DataRequired()])
    verify_password = PasswordField('verify_password', validators=[DataRequired(), EqualTo('password', message='密码输入不一致')])
    # 限制图片上传格式
    photo = FileField('上传图片', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'images only!')])
    submit = SubmitField('submit')


@test_index.route('/ts/', methods=['GET', 'POST'])
def flask_test():
    test_form = TestForm()
    if request.method == 'POST':
        # username = request.form.get('username')
        # password = request.form.get('password')
        # verify_password = request.form.get('verify_password')
        f = test_form.photo.data

        if test_form.validate_on_submit():
            username = test_form.username.data
            password = test_form.password.data
            verify_password = test_form.verify_password.data

            # filename = secure_filename(f.filename)

            f.save(os.path.join(
                './web/static/images/', f.filename
            ))

            return 'success'
        else:
            a = test_form.errors
            print(a.get('username')[0])
            flash(a.get('username')[0])

            return render_template('test.html', form=test_form)

    return render_template('test.html', form=test_form)
# ------------------------>>>


