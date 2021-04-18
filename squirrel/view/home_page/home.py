#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, request
from squirrel.view.tool.filter_note import filter_func
from flask_login import login_required, current_user
from squirrel.view.tool.ip_log import ip_log
from model.top_category import TopCategory
from config.base_setting import *
from model.notes import Notes
from main import db, cache, csrf
from squirrel.mysql_con.mysql_util import query_ins
from flask_wtf.csrf import generate_csrf
import uuid

home_index = Blueprint('home_page', __name__)


@home_index.after_request
def after_request(response):
    # 调用函数生成csrf token
    csrf_token = generate_csrf()
    # 设置cookie传给前端
    response.set_cookie('csrf_token', csrf_token)
    return response


@home_index.route('/', methods=('GET', ))
def home():
    """
    进入首页
    :return:
    """
    # ip_log(request.url, home.__name__)
    res = {}
    try:
        all_category = query_ins.get_all_category()
        res['top_categorys'] = [(i[0], i[1].split('|')[:-1]) for i in all_category]
        all_notes, pages = query_ins.get_filter_notes('', 'recommend', '', 1)
        res['note_msg'] = all_notes
        res['pages'] = pages
        if current_user.is_active:
            res['user_info'] = {'username': current_user.adminName}

    except Exception as ex:
        print(ex)

    # return render_template('home.html', res=res, url=URL)
    return jsonify(res)


@home_index.route('/delete/<note_id>/', methods=('POST', ))
def delete_note(note_id):
    """
    删除当前note
    :param note_id:
    :return:
    """
    # ip_log(request.url, delete_note.__name__)
    # res = {}
    # filter_type = request.json.get('filter_type', 'rec')
    # label_name = request.json.get('label_name', 'All')
    # label_name = label_name.capitalize()
    #
    # delete_obj = Notes.query.get_or_404(note_id)
    # db.session.delete(delete_obj)
    # db.session.commit()
    # note_obj = filter_func(filter_type, label_name, 1, Notes)
    # if note_obj:
    #     res['note_msg'] = [[obj.note_id, obj.note_title, obj.note_labels,
    #                         obj.creation_time, obj.click_number] for obj in note_obj.items]
    pass
    # return jsonify(res)


@home_index.route('/filter_col/', methods=('POST', ))
def filter_sort():
    """
    条件排序和筛选
    :return:
    """
    # print(request.json)
    ip_log(request.url, filter_sort.__name__)
    res = {}
    cur_page = request.json.get('curPage', 1)
    keyword = request.json.get('keyword', '')
    sort_type = request.json.get('generalScreen', 'recommend')
    label_name = request.json.get('secondaryClass', '')
    label_name = label_name.capitalize()
    all_category = query_ins.get_all_category()
    res['top_categorys'] = [(i[0], i[1].split('|')[:-1]) for i in all_category]
    all_notes, pages = query_ins.get_filter_notes(keyword, sort_type, label_name, int(cur_page))
    res['note_msg'] = all_notes
    res['pages'] = pages
    return jsonify(res)


# 添加新的一级类
@home_index.route('/add_top_cate/', methods=['POST'])
def add_top_category():
    ip_log(request.url, add_top_category.__name__)
    top_category_name = request.json.get('top_name', '')
    sec_category = request.json.get('sec_category', '')
    str_uuid = str(uuid.uuid4())

    has_common_name = TopCategory.query.filter(TopCategory.top_category_name == top_category_name.lower()).first()
    if not has_common_name:
        db.session.add(TopCategory(
            uuid=str_uuid,
            top_category_name=top_category_name,
            sec_category=sec_category,
        ))

        db.session.commit()

    return 'ok'


@home_index.route('/test/', methods=['GET'])
def vue_test():
    return jsonify({'a': 1})
