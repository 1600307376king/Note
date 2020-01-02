#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from flask import Flask
import logging

import os


class Main(Flask):
    def __init__(self, name, template_folder=None, static_folder=None):
        super(Main, self).__init__(name, template_folder=template_folder, static_folder=static_folder)
        self.config['JSON_AS_ASCII'] = False
        self.config.from_pyfile('config/base_setting.py')
        self.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除
        self.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间
        self.config.setdefault('SQLALCHEMY_POOL_SIZE', 100)
        # self.config.setdefault('SQLALCHEMY_MAX_OVERFLOW', 20)
        self.config.setdefault('SQLALCHEMY_POOL_RECYCLE', 3600)

        db.init_app(self)
        # csrf.init_app(self)


# csrf = CSRFProtect()
db = SQLAlchemy()

app = Main(__name__, template_folder=os.getcwd() + '/web/templates/',
           static_folder=os.getcwd() + "/web/static/")


# 设置404页面
@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return 'This page does not exist', 404


from web.view.home import home_index
from web.view.add_note import add_index
from web.view.note_detail import detail_index
from web.view.modification import mod_index
from web.view.test import test_index
from web.view.login import login_index
from web.view.tool.static_file_version import CreateNewVersion

app.add_template_global(CreateNewVersion.get_version(), 'getVersion')

app.register_blueprint(home_index, url_prefix='/')
app.register_blueprint(add_index, url_prefix='/')
app.register_blueprint(detail_index, url_prefix='/detail/')
app.register_blueprint(mod_index, url_prefix='/')
app.register_blueprint(test_index, url_prefix='/')
app.register_blueprint(login_index, url_prefix='/login/')

# if __name__ == '__main__':
#     handler = logging.FileHandler('./logs/flask.log', encoding='UTF-8')
#     handler.setFormatter(logging.DEBUG)
#     logging_format = logging.Formatter(
#         '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
#     )
#     handler.setFormatter(logging_format)
#     app.logger.addHandler(handler)
#     app.run(debug=True)
