#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/11/29 21:02
# @Author : jjc
import string
import random
from flask_wtf.csrf import generate_csrf
from flask import session


class CsrfToken(object):
    @staticmethod
    def get_csrf_token():
        # global_csrf_token = generate_csrf()
        # session['csrf_token'] = global_csrf_token
        return generate_csrf()


def get_random_string(length):
    """
    生成固定长度的字符串，包含数字和大小写字母
    :param length:
    :return:
    """
    st = string.digits + string.ascii_letters
    return ''.join(random.sample(st, length))