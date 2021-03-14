#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/11 13:31
# @Author : jjc

import pymysql


class MysqlUtil(object):
    def __init__(self, host, port, username, password, db_name,  charset):
        """
        :param host: mysql IP
        :param port: 端口
        :param username: 用户名
        :param password: 面膜
        :param charset: 字符集
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.charset = charset
        self.db_name = db_name
        self.conn = None
        self.cur = None

    def connect(self):

        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            db=self.db_name,
            charset=self.charset
        )

    def execute_insert(self, sql, data):
        if self.conn:
            try:
                self.cur = self.conn.cursor()
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as ex:
                self.conn.rollback()
                print(ex)

            self.conn.close()

    def execute_many_insert(self, sql, data):
        if self.conn:
            try:
                self.cur = self.conn.cursor()
                self.cur.executemany(sql, data)
                self.conn.commit()
                print(1)
            except Exception as ex:
                self.conn.rollback()
                print(ex)

            self.conn.close()

    def execute_query_ret_all(self, sql):
        res = []
        if self.conn:
            try:
                self.cur = self.conn.cursor()
                self.cur.execute(sql)
                res = self.cur.fetchone()
            except Exception as ex:
                print(ex)
            self.conn.close()
        return res
