#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, request
from config.base_setting import *
from squirrel.view.tool.ip_log import ip_log
from squirrel.view.tool.filter_text import filter_note_con
import datetime
from model.top_category import TopCategory
from squirrel.view.tool.common_func import get_random_string
from squirrel.mysql_con.mysql_util import query_ins
from model.notes import Notes
from main import db, csrf
from collections import defaultdict


add_index = Blueprint('add_page', __name__)


@add_index.route('/add/', methods=('POST', 'GET'))
def add_new_note():
    """
    添加新的笔记
    :return:
    """
    ip_log(request.url, add_new_note.__name__)

    if request.method == 'POST':
        print(request.json)
        # request_dict = defaultdict(str, request.json)
        # insert_params = {
        #     'note_title': request_dict['note_title'],
        #     'note_labels': request_dict['existing_label'] + request_dict['custom_labels'],
        #     'note_instructions': request_dict['note_instructions'],
        #     'note_content': request_dict['str_content'],
        #     'creation_time': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        # }
        # result = query_ins.insert_note(**insert_params)
        # return jsonify({'msg': result})
    res = {}
    category_obj_list = query_ins.get_all_category()
    category_name_list = [{'id': get_random_string(9), 'title': i[0],
                           'subs': [{'id': get_random_string(9), 'title': j} for j in i[1].split('|')[:-1]]}
                          for i in category_obj_list]
    res['category'] = category_name_list
    # return render_template('add_note.html', url=URL, res=res, data=category_name_list)
    return jsonify(res)