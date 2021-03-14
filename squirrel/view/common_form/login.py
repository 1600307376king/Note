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

from model.admin import AdminInfo, User
from main import db
from datetime import datetime
from faker import Faker
from squirrel.mysql_con.mysql_util import MysqlUtil
import random

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


@login_index.route('/add_user/')
def add_user_info():
    fk = Faker(locale='zh_CN')
    print('开始插入')
    # db.session.execute(
    #     User.__table__.insert(),
    #     [
    #         {
    #             'user_name': fk.name(),
    #             'user_password': fk.password(),
    #             'user_nickname': fk.name(),
    #             'user_phone_number': fk.phone_number(),
    #             'user_email': fk.email(),
    #             'user_last_login_time': datetime.now(),
    #         } for _ in range(100000)
    #     ]
    # )
    # db.session.commit()

    # my_mysql_conn = MysqlUtil('127.0.0.1', 3306, 'root', '123456', 'utf8mb4')
    # my_mysql_conn.connect()
    # insert_sql = "insert into user(user_name, user_password, user_nickname, user_phone_number," \
    #              "user_email, user_last_login_time)" \
    #              "values(%s, %s, %s, %s, %s, %s)"
    # insert_data = [(fk.name(), fk.password(), fk.name(), fk.phone_number(), fk.email(), datetime.now()) for _ in range(1000000)]
    # t1 = datetime.now()
    # my_mysql_conn.execute_many_insert(insert_sql, insert_data)
    # t2 = datetime.now()
    # print(t2 - t1)
    my_mysql_conn = MysqlUtil('127.0.0.1', 3306, 'root', '123456', 'school', 'utf8mb4')
    my_mysql_conn.connect()
    insert_sql = "insert into student(st_name, st_age, st_sex) values(%s, %s, %s)"
    insert_data = [(fk.name(), random.randint(7, 30), random.randint(0, 1)) for _ in range(1000000)]
    t1 = datetime.now()
    my_mysql_conn.execute_many_insert(insert_sql, insert_data)
    t2 = datetime.now()
    print(t2 - t1)
    print('插入完成')
    return '666'
