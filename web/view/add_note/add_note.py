#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, request
from config.base_setting import *
from web.view.tool.ip_log import ip_log
from web.view.tool.filter_text import *
import datetime
import random
import uuid
from model.top_category import TopCategory
from model.notes import Notes
from main import db


add_index = Blueprint('add_page', __name__)


def get_random_string(length):
    st = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join([random.choice(st) for _ in range(length)])


@add_index.route('/add/', methods=['POST', 'GET'])
def add_n():
    ip_log(request.url, add_n.__name__)
    res = dict()
    if request.method == 'POST':
        note_title = request.json.get('note_title', '')
        existing_label = request.json.get('existing_label', '')
        custom_labels = request.json.get('custom_labels', '')
        note_instructions = request.json.get('note_instructions', '')
        str_content = request.json.get('str_content', '')
        creation_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        needed_labels = []
        needed_labels.extend(existing_label.split('|')[:-1])
        needed_labels.extend(custom_labels.split('|')[:-1])
        db.session.add(Notes(
            uuid=str(uuid.uuid1()),
            note_title=note_title,
            note_labels='|'.join(needed_labels) + '|',
            note_instructions=note_instructions.strip(),
            note_content=filter_note_con(str_content),
            creation_time=creation_time,
            click_number=0
        ))
        db.session.commit()
        return jsonify({'msg': 'ok'})
    category_obj_list = TopCategory.query.all()
    category_name_list = [{'id': get_random_string(9), 'title': i.top_category_name,
                           'subs': [{'id': get_random_string(9), 'title': j} for j in i.sec_category.split('|')[:-1]]}
                          for i in category_obj_list]
    res['cate_name_list'] = category_name_list
    ck_token = request.cookies.get('token', '')
    arg_token = request.args.get('token', '')
    if ck_token or arg_token:
        return render_template('admin/admin_add_note.html', res=res, url=URL, data=category_name_list)
    return render_template('add_note.html', url=URL, res=res, data=category_name_list)
