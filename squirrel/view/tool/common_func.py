#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/11/29 21:02
# @Author : jjc

from flask_wtf.csrf import generate_csrf
from flask import session


class CsrfToken(object):
    @staticmethod
    def get_csrf_token():
        # global_csrf_token = generate_csrf()
        # session['csrf_token'] = global_csrf_token
        return generate_csrf()
