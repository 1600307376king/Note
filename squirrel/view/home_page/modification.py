#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 0011 9:12
# @Author  : HelloWorld
# @File    : modification.py
import json
from flask import Blueprint, jsonify, request, render_template
from squirrel.view.tool.ip_log import ip_log
from main import db, csrf
from model.notes import Notes
from squirrel.mysql_con.mysql_util import query_ins
from squirrel.view.tool.common_func import get_random_string
from collections import defaultdict


mod_index = Blueprint('mod_page', __name__)


@mod_index.route('/modification/<note_id>/', methods=('GET', 'POST'))
def com_modification(note_id):
    """

    :param note_id:
    :return:
    """
    ip_log(request.url, com_modification.__name__)
    if request.method == 'POST':
        dic = defaultdict(str, request.json)
        print(request.json)
        # update_params = {
        #     'note_title': dic['note_title'],
        #     'note_labels': dic['str_labels'],
        #     'note_instructions': dic['note_instructions'],
        #     'note_content': dic['str_content']
        # }
        # result = query_ins.update_note(note_id, **update_params)
        # return jsonify({'msg': result})
    res = {'note_cur_msg': query_ins.get_notes_with_id(note_id)}
    category_obj_list = query_ins.get_all_category()
    category_name_list = [{'id': get_random_string(9), 'title': i[0],
                           'subs': [{'id': get_random_string(9), 'title': j} for j in i[1].split('|')[:-1]]}
                          for i in category_obj_list]
    res['category'] = category_name_list
    # return render_template('update_note.html', res=res)
    return jsonify(res)
