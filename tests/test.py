#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/10 18:24
# @Author  : HelloWorld
# @File    : tests.py
import unittest
from model.admin import Admin


class UserModelTestCase(unittest.TestCase):

    def test_password_setter(self):
        a = Admin(admin_name='admin_manage', password='123')
        self.assertTrue(a.password_hash is not None)

    def test_password_verification(self):
        a = Admin(admin_name='admin_manage', password='123')
        self.assertTrue(a.verify_password('123'))
        self.assertFalse(a.verify_password('wer'))

    def test_password_salts_are_random(self):
        a = Admin(admin_name='admin_manage', password='123')
        a2 = Admin(admin_name='admin_manage', password='123')
        self.assertTrue(a.password_hash != a2.password_hash)