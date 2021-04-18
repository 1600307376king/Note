#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/11 13:31
# @Author : jjc

import pymysql
from dbutils.pooled_db import PooledDB
from config.base_setting import PER_PAGE_MAX_NUM, HOST, PORT, DATABASE, USERNAME, PASSWORD, CHARSET


class MysqlUtil(object):
    def __init__(self, host, port, username, password, db_name, charset):
        """
        :param host: mysql IP
        :param port: 端口
        :param username: 用户名
        :param password: 密码
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


class MysqlPool(object):
    """
    建立数据库连接池
    """
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.database = DATABASE
        self.user = USERNAME
        self.password = PASSWORD
        self.charset = CHARSET
        self.pool_db = PooledDB(
            creator=pymysql,
            maxconnections=3,  # 最大连接数
            mincached=2,  # 初始化时创建的空闲连接数
            maxcached=5,  # 最多空闲连接数
            maxshared=3,  # 最多共享连接数
            blocking=True,  # 连接池占满后是否等待
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )

    def execute_single_record(self, execute_sql):
        """
        执行单个记录的更新或插入
        :param execute_sql:
        :return:
        """
        conn = self.pool_db.connection()
        result = 1
        try:
            cursor = conn.cursor()
            cursor.execute(execute_sql)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
            return 0
        finally:
            conn.close()
        return result

    def query_one(self, query_sql):
        """
        查询一条记录
        :param query_sql:
        :return:
        """
        conn = self.pool_db.connection()
        result = None
        try:
            cursor = conn.cursor()
            cursor.execute(query_sql)
            result = cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            conn.close()
        return result

    def query_all(self, query_sql):
        """
        获取所有查询数据
        :param query_sql:
        :return:
        """
        conn = self.pool_db.connection()
        result = None
        try:
            cursor = conn.cursor()
            cursor.execute(query_sql)
            result = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            conn.close()
        return result

    def update_one_row(self, update_sql):
        """
        更新一条记录
        :param update_sql:
        :return:
        """
        return self.execute_single_record(update_sql)

    def insert_one_row(self, insert_sql):
        """
        插入一条记录
        :param insert_sql:
        :return:
        """
        return self.execute_single_record(insert_sql)


class MysqlQuery(object):
    def __init__(self):
        self.pool_mysql = MysqlPool()

    def get_all_category(self):
        """
        查询所有标签
        :return:
        """
        category_sql = "select top_category_name, sec_category from top_category"
        all_category = self.pool_mysql.query_all(category_sql)
        return all_category

    def get_notes_with_id(self, note_id):
        """
        根据note_id查询记录
        :param note_id:
        :return:
        """
        query_sql = "select note_title, note_labels, note_instructions, note_content from" \
                    " notes where note_id = {0}".format(note_id)
        return self.pool_mysql.query_one(query_sql)

    def get_notes_detail(self, note_id):
        query_sql = "select note_id, note_title, creation_time, note_labels, note_instructions," \
                    " note_content, click_number from notes where note_id = {0}".format(note_id)
        return self.pool_mysql.query_one(query_sql)

    def get_recommend_notes(self):
        """
        获取前12个推荐的
        :return:
        """
        query_sql = "select note_id, note_title from notes order by click_number desc, creation_time desc limit 12 "
        return self.pool_mysql.query_all(query_sql)

    def get_filter_notes(self, keyword, sort_type, label_name, cur_page):
        """
        按条件筛选
        :param keyword: 关键字
        :param sort_type: 排序方式
        :param label_name: 标签
        :param cur_page: 当前页
        :return:
        """
        start_index = max((cur_page - 1) * PER_PAGE_MAX_NUM, 0)
        end_index = max(cur_page * PER_PAGE_MAX_NUM, PER_PAGE_MAX_NUM)
        sorts = {'recommend': 'click_number desc, creation_time desc',
                 'latest': 'creation_time desc'}
        filter_sql = "select note_id, note_title, note_labels, creation_time, click_number from " \
                     "(select * from notes where note_labels like '%{0}%'" \
                     " union distinct select * from notes where note_title like '%{1}%'" \
                     " union distinct select * from notes where note_content like '%{1}%')" \
                     " as n order by {2}"\
            .format(label_name, keyword, sorts[sort_type], start_index, end_index)
        all_notes = self.pool_mysql.query_all(filter_sql)
        all_notes_length = len(all_notes)
        pages = all_notes_length // PER_PAGE_MAX_NUM if all_notes_length % PER_PAGE_MAX_NUM == 0\
            else (all_notes_length // PER_PAGE_MAX_NUM) + 1
        all_notes = all_notes[start_index:end_index]
        return all_notes, pages

    def update_note(self, note_id, **kwargs):
        """
        更新一个笔记
        :param note_id:
        :param kwargs:
        :return:
        """
        update_note_sql = "update notes set {0} where note_id = {1}"\
            .format(','.join((i + "='" + v + "'" for i, v in zip(kwargs.keys(), kwargs.values()))), note_id)
        return self.pool_mysql.update_one_row(update_note_sql)

    def insert_note(self, **kwargs):
        insert_sql = "insert into notes({0}) values({1})".format(
            ','.join((key for key in kwargs.keys())),
            ','.join(("'" + val + "'" for val in kwargs.values())))
        return self.pool_mysql.insert_one_row(insert_sql)


query_ins = MysqlQuery()
