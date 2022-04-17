#!/usr/bin/python3
# -*- coding: utf-8 -*-
from squirrel.view.tool.static_file_version import CreateNewVersion
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_caching import Cache
from flask_babelex import Babel
from datetime import timedelta
from flask_mail import Mail
from celery import Celery
from flask import Flask


class Main(Flask):
    """
    生产环境中相关密钥需要从环境变量中读取
    """
    def __init__(self, name):
        super(Main, self).__init__(name, static_url_path='')
        self.config['JSON_AS_ASCII'] = False
        # jwt密钥 用于登录验证
        self.config['JWT_SECRET_KEY'] = 'hello-world'
        self.config.from_pyfile('config/base_setting.py')
        self.config.setdefault('SQLALCHEMY_POOL_SIZE', 100)
        # self.config.setdefault('SQLALCHEMY_MAX_OVERFLOW', 20)
        self.config.setdefault('SQLALCHEMY_POOL_RECYCLE', 3600)
        # 设置flask_admin风格,主题网站https://bootswatch.com/3/
        self.config['FLASK_ADMIN_SWATCH'] = 'united'
        self.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
        # 设置静态文件缓存过期时间
        # self.send_file_max_age_default = timedelta(seconds=1)
        self.permanent_session_lifetime = timedelta(days=1)

        db.init_app(self)
        cache.init_app(self)
        mail.init_app(self)
        # toolbar.init_app(self)
        csrf.init_app(self)
        babel.init_app(self)
        login_manager.init_app(self)


# 权限验证
auth = HTTPBasicAuth()
# 数据库管理
db = SQLAlchemy()
# 缓存管理
cache = Cache(config={'CACHE_TYPE': 'redis'})
# 异步任务
cel = Celery()
# 邮箱管理
mail = Mail()
# 页面右侧添加工具栏
# toolbar = DebugToolbarExtension()

jwt = JWTManager()
csrf = CSRFProtect()
# flask_admin界面中文显示
babel = Babel()
# 登录管理
login_manager = LoginManager()

app = Main(__name__)

app.add_template_global(CreateNewVersion.get_version(), 'getVersion')



