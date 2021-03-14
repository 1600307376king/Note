#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, request
from config.base_setting import *
from squirrel.view.tool.ip_log import ip_log
from squirrel.view.tool.filter_text import filter_note_con
import datetime
from model.top_category import TopCategory
from squirrel.view.tool.common_func import get_random_string
from model.notes import Notes
from main import db, csrf


add_index = Blueprint('add_page', __name__)


@add_index.route('/add/', methods=['POST', 'GET'])
def add_new_note():
    ip_log(request.url, add_new_note.__name__)
    res = {}
    if request.method == 'POST':
        note_title = request.json.get('note_title', '')
        existing_label = request.json.get('existing_label', '')
        custom_labels = request.json.get('custom_labels', '')
        note_instructions = request.json.get('note_instructions', '')
        str_content = request.json.get('str_content', '')
        creation_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        db.session.add(Notes(

            note_title=note_title,
            note_labels=existing_label + custom_labels,
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
    # res['cate_name_list'] = category_name_list
    # ck_token = request.cookies.get('token', '')
    # arg_token = request.args.get('token', '')
    # if ck_token or arg_token:
    #     return render_template('add_note.html', res=res, url=URL, data=category_name_list)
    return render_template('add_note.html', url=URL, res=res, data=category_name_list)
