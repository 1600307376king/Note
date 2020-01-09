#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/3 18:46
# @Author  : HelloWorld
# @File    : blueprint_reg.py
from main import app

from web.view.home import home_index
from web.view.test import test_index
from web.view.login import login_index
from web.view.add_note import add_index
from web.view.modification import mod_index
from web.view.manage_label import bind_index
from web.view.note_detail import detail_index

app.register_blueprint(add_index, url_prefix='/')
app.register_blueprint(mod_index, url_prefix='/')
app.register_blueprint(home_index, url_prefix='/')
app.register_blueprint(test_index, url_prefix='/')
app.register_blueprint(bind_index, url_prefix='/')
app.register_blueprint(login_index, url_prefix='/login/')
app.register_blueprint(detail_index, url_prefix='/detail/')