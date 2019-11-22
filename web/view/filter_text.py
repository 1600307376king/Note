#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/9 0009 15:10
# @Author  : HelloWorld
# @File    : filter_text.py
import re


def filter_note_con(str_content):
    ss = re.sub('\n\d+\n', '\n', str_content)
    m = ''
    for i in ss.splitlines():
        if i != '\u200b':
            m += i + '\n'
        else:
            m += '\n'

    return m[1:].strip()


def decode_text(de):
    return str(de, encoding='utf-8')
