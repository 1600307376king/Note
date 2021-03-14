#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/14 22:17
# @Author  : HelloWorld
# @File    : filter_note.py
from config.base_setting import PER_PAGE_MAX_NUM
from sqlalchemy import desc
from sqlalchemy.sql import or_, and_


# 返回note筛选结果对象
def filter_func(label_name, keyword, sort_type, cur_page, model_obj):
    condition_list = (model_obj.note_labels.like('%{}%'.format(label_name)),
                      or_(model_obj.note_title.like('%{}%'.format(keyword)),
                          model_obj.note_content.like('%{}%'.format(keyword))))
    sorts = {'recommend': model_obj.click_number.desc(),
             'latest': model_obj.creation_time.desc()}
    load_result_obj = model_obj.query.filter(*condition_list).order_by(
        sorts[sort_type]).paginate(cur_page, per_page=10)

    return load_result_obj
