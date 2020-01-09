#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/8 19:55
# @Author  : HelloWorld
# @File    : ip_log.py
import time


# 保存请求url
def ip_log(u, fuc_name):
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('./logs/url.log', 'a', encoding='utf8') as f:
        f.write(str(now_time + '|' + u + '|' + fuc_name + '\n'))