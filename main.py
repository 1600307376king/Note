#!/usr/bin/python3
# -*- coding: utf-8 -*-
from web.view.tool.static_file_version import CreateNewVersion
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import Flask
import os


class Main(Flask):
    def __init__(self, name, template_folder=None, static_folder=None):
        super(Main, self).__init__(name, template_folder=template_folder, static_folder=static_folder)
        self.config['JSON_AS_ASCII'] = False
        self.config.from_pyfile('config/base_setting.py')
        self.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的
        self.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间
        self.config.setdefault('SQLALCHEMY_POOL_SIZE', 100)
        # self.config.setdefault('SQLALCHEMY_MAX_OVERFLOW', 20)
        self.config.setdefault('SQLALCHEMY_POOL_RECYCLE', 3600)
        db.init_app(self)


db = SQLAlchemy()

app = Main(__name__, template_folder=os.getcwd() + '/web/templates/',
           static_folder=os.getcwd() + "/web/static/")


app.add_template_global(CreateNewVersion.get_version(), 'getVersion')


# if __name__ == '__main__':
#     handler = logging.FileHandler('./logs/flask.log', encoding='UTF-8')
#     handler.setFormatter(logging.DEBUG)
#     logging_format = logging.Formatter(
#         '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
#     )
#     handler.setFormatter(logging_format)
#     app.logger.addHandler(handler)
#     app.run(debug=True)
