#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/9 0009 11:23
# @Author  : HelloWorld
# @File    : tests.py
from flask import render_template, Blueprint, request, flash
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileRequired, FileAllowed
from flask_mail import Message
from main import mail
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


# @test_index.route('/ts/', methods=('GET', 'POST'))
# def flask_test():
#     test_form = TestForm()
#     if request.method == 'POST':
#         # username = request.common_form.get('username')
#         # password = request.common_form.get('password')
#         # verify_password = request.common_form.get('verify_password')
#         f = test_form.photo.data
#
#         if test_form.validate_on_submit():
#             username = test_form.username.data
#             password = test_form.password.data
#             verify_password = test_form.verify_password.data
#
#             # filename = secure_filename(f.filename)
#
#             f.save(os.path.join(
#                 './squirrel/static/images/', f.filename
#             ))
#
#             return 'success'
#         else:
#             a = test_form.errors
#             print(a.get('username')[0])
#             flash(a.get('username')[0])
#
#             return render_template('tests.html', common_form=test_form)
#
#     return render_template('tests.html', common_form=test_form)
# # ------------------------>>>

# 发送qq邮件测试
@test_index.route('/mail_send/', methods=['POST', 'GET'])
def send_mail():
    """
    MAIL_SERVER : smtp.qq.com qq 邮箱服务器域名
    MAIL_PORT: 587
    MAIL_USERNAME : 1600307376@qq.com  # 发送者邮箱账号
    MAIL_PASSWORD : *** # 需要去邮箱页面设置里获取
    :return:
    """
    msg = Message('hello', sender='1600307376@qq.com', recipients=['438200051@qq.com'])
    msg.body = 'test'
    msg.html = '<b>testing</b>'
    mail.send(msg)
    return 'send_success'


# sendgrid 服务商发送邮件
@test_index.route('/grid_mail/', methods=['POST', 'GET'])
def send_grid_mail():
    """
    MAIL_SERVER : smtp.sendgrid.net
    MAIL_PORT: 587
    MAIL_USERNAME : apikey # 发送类型
    MAIL_PASSWORD : *** # 需要去服务商页面获取api key 密钥


    sender 为api key 名称
    :return:
    """
    msg = Message(subject='hello，im sendgrid', sender='jjcmailkey', recipients=['438200051@qq.com'])
    msg.body = 'test'
    msg.html = '<b>testing</b>'
    mail.send(msg)
    return 'send_success'

