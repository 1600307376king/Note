#!/usr/bin/python3
# -*- coding: utf-8 -*-
from web.view.tool.static_file_version import CreateNewVersion
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mail import Mail
from flask import Flask
import os


class Main(Flask):
    def __init__(self, name, template_folder=None, static_folder=None):
        super(Main, self).__init__(name, template_folder=template_folder, static_folder=static_folder)
        self.config['JSON_AS_ASCII'] = False
        self.config.from_pyfile('config/base_setting.py')
        # self.config['MAIL_SERVER'] = 'localhost'
        # self.config['MAIL_PORT'] = 25
        # self.config['MAIL_USE_TLS'] = True
        # self.config['MAIL_USERNAME'] = ''
        # self.config['MAIL_PASSWORD'] = ''
        self.config.setdefault('SQLALCHEMY_POOL_SIZE', 100)
        # self.config.setdefault('SQLALCHEMY_MAX_OVERFLOW', 20)
        self.config.setdefault('SQLALCHEMY_POOL_RECYCLE', 3600)
        db.init_app(self)
        cache.init_app(self)
        # mail.init_app(self)


db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})
# mail = Mail()

app = Main(__name__, template_folder=os.getcwd() + '/web/templates/',
           static_folder=os.getcwd() + "/web/static/")
app.add_template_global(CreateNewVersion.get_version(), 'getVersion')
