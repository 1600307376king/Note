#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/10 20:53
# @Author  : HelloWorld
# @File    : errors.py
from flask import Blueprint
from main import app

error_index = Blueprint('error_page', __name__)


# 设置404页面
@error_index.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return 'This page does not exist', 404
