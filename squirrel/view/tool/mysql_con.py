#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/3/3 20:54
# @Author : jjc
import pymysql


class MysqlTool(object):
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def update_db(self):

        query_sql = "select * from notes"
        con = pymysql.connect(self.host, self.user, self.password, self.db)
        cursor = con.cursor()
        cursor.execute(query_sql)
        res = cursor.fetchall()
        print(cursor.description)
        # for i, r in enumerate(res):
        #     update_sql = "update notes set note_id='{0}' where note_id = '{1}'".format(i + 1, r[0])
        #     cursor.execute(update_sql)
        #     cursor.commit()
        con.close()


if __name__ == '__main__':

    c = MysqlTool('localhost', 'root', '123456', 'note')
    c.update_db()
