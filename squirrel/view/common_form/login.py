#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 0030 9:20
# @Author  : HelloWorld
# @File    : admin_manage.py
from flask import jsonify, Blueprint, request, render_template, redirect, url_for
from squirrel.view.tool.ip_log import ip_log
from werkzeug.security import check_password_hash
from main import csrf, login_manager
from flask_login import login_user, login_required, logout_user
from flask_wtf.csrf import generate_csrf, CSRFError
from model.admin import AdminInfo

login_index = Blueprint('login_page', __name__)


@login_manager.user_loader
def load_user(user_id):
    """
    提供一个 user_loader 回调。这个回调用于从会话中存储的用户 ID 重新加载用户对象。
    它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象
    :param user_id:
    :return:
    """
    return AdminInfo.query.get(user_id)


@login_index.route('/', methods=['POST', 'GET'])
def go_login():
    """
    显示登录界面
    :return:
    """
    ip_log(request.url, go_login.__name__)
    csrf_token = generate_csrf()
    return render_template('login.html', csrf_token=csrf_token)


@csrf.exempt
@login_index.route('/verify_login/', methods=['POST'])
def verify_login():
    """
    登录验证
    :return:
    """
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = AdminInfo.query.filter_by(adminName=username).first()
        if user:
            if check_password_hash(user.passwordHash, password):
                login_user(user)
                return jsonify({'status': 'success', 'msg': '登录成功！'})

        return jsonify({'status': 'fail', 'msg': '密码错误！'})


@login_index.route('/logout/')
@login_required
def logout():
    """
    退出登录
    :return:
    """
    logout_user()
    return redirect(url_for('login_page.go_login'))


@login_index.errorhandler(CSRFError)
def csrf_error(reason):
    return 'csrf error {0}'.format(reason)
