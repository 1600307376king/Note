#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/14 22:17
# @Author  : HelloWorld
# @File    : filter_note.py
from config.base_setting import PER_PAGE_MAX_NUM


# 返回note筛选结果对象
def filter_func(filter_type, label_name, cur_page, model_obj):
    load_result_obj = None
    if filter_type == 'rec' and label_name == 'All':
        load_result_obj = model_obj.query.order_by(model_obj.click_number.desc(), model_obj.creation_time.desc()). \
            paginate(cur_page, per_page=PER_PAGE_MAX_NUM)
    elif filter_type == 'rec' and label_name != 'All':
        load_result_obj = model_obj.query.filter(model_obj.note_labels.like("%" + label_name + "%")).order_by(
            model_obj.click_number.desc(), model_obj.creation_time.desc()). \
            paginate(cur_page, per_page=PER_PAGE_MAX_NUM)
    elif filter_type == 'new' and label_name != 'All':
        load_result_obj = model_obj.query.filter(model_obj.note_labels.like("%" + label_name + "%")).order_by(
            model_obj.creation_time.desc()). \
            paginate(cur_page, per_page=PER_PAGE_MAX_NUM)
    elif filter_type == 'new' and label_name == 'All':
        load_result_obj = model_obj.query.order_by(model_obj.creation_time.desc()). \
            paginate(cur_page, per_page=PER_PAGE_MAX_NUM)
    return load_result_obj

