#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, request
from squirrel.view.tool.filter_note import filter_func
from squirrel.view.tool.filter_text import clean_data
from flask_login import login_required, current_user
from squirrel.view.tool.ip_log import ip_log
from model.top_category import TopCategory
from config.base_setting import *
from model.notes import Notes
from main import db, cache, csrf
import uuid

home_index = Blueprint('home_page', __name__)


@home_index.route('/', methods=['GET', 'POST'])
def home():
    """
    进入首页
    :return:
    """
    # ip_log(request.url, home.__name__)
    cur_page = request.args.get('page', 1)
    sort_type = request.args.get('generalScreen', 'recommend')
    keyword = request.args.get('keyword', '')
    label_name = request.args.get('secondaryClass', '')
    res = {}
    try:
        all_category = TopCategory.query.all()
        res['top_categorys'] = ((i.top_category_name, i.sec_category.split('|')[:-1]) for i in all_category)
        load_data_obj = filter_func(label_name, keyword, sort_type, int(cur_page), Notes)

        res['note_msg'] = ((obj.note_id, obj.note_title, obj.note_labels,
                            obj.creation_time, obj.click_number) for obj in load_data_obj.items)
        res['pages'] = load_data_obj.pages
        res['page'] = load_data_obj.page
        if current_user.is_active:
            res['user_info'] = {'username': current_user.adminName}

    except Exception as ex:
        print(ex)

    return render_template('home.html', res=res, url=URL)


@home_index.route('/update/<note_id>/')
def go_update(note_id):
    """
    进入修改页
    :param note_id:
    :return:
    """
    ip_log(request.url, go_update.__name__)
    res = {}
    query_obj = Notes.query.get_or_404(note_id)
    res['note_cur_msg'] = (query_obj.note_title, query_obj.note_labels, query_obj.note_instructions,
                           query_obj.note_content, query_obj.note_id)
    return render_template('update_note.html', res=res, url=URL)


@home_index.route('/delete/<note_id>/', methods=['POST'])
def delete_note(note_id):
    """
    删除当前note
    :param note_id:
    :return:
    """
    ip_log(request.url, delete_note.__name__)
    res = {}
    filter_type = request.json.get('filter_type', 'rec')
    label_name = request.json.get('label_name', 'All')
    label_name = label_name.capitalize()

    delete_obj = Notes.query.get_or_404(note_id)
    db.session.delete(delete_obj)
    db.session.commit()
    note_obj = filter_func(filter_type, label_name, 1, Notes)
    if note_obj:
        res['note_msg'] = [[obj.note_id, obj.note_title, obj.note_labels,
                            obj.creation_time, obj.click_number] for obj in note_obj.items]

    return jsonify(res)


# 条件排序
@home_index.route('/filter_col/', methods=['POST'])
@csrf.exempt
def filter_sort():
    ip_log(request.url, filter_sort.__name__)
    res = {}
    cur_page = request.json.get('curPage', 1)
    keyword = request.json.get('keyword', '')
    sort_type = request.json.get('generalScreen', 'recommend')
    label_name = request.json.get('secondaryClass', '')
    label_name = label_name.capitalize()
    note_obj = filter_func(label_name, keyword, sort_type, int(cur_page), Notes)
    all_category = TopCategory.query.all()
    res['top_categorys'] = [(i.top_category_name, i.sec_category.split('|')[:-1]) for i in all_category]
    res['note_msg'] = [(obj.note_id, obj.note_title, obj.note_labels,
                        obj.creation_time, obj.click_number) for obj in note_obj.items]
    res['page_count'] = note_obj.pages
    res['cur_page'] = note_obj.page
    return jsonify(res)


# 页面向下滚动加载
@home_index.route('/load_data/', methods=['GET'])
def loading_data():
    ip_log(request.url, loading_data.__name__)
    cur_page = request.args.get('page', 2)
    sort_type = request.args.get('generalScreen', 'recommend')
    keyword = request.args.get('keyword', '')
    # label_name = request.args.get('secondaryClass', '')
    # label_name = label_name.capitalize()
    cur_page = int(cur_page)
    res = {}
    try:
        load_data_obj = filter_func("", keyword, sort_type, cur_page, Notes)
        all_category = TopCategory.query.all()
        res['top_categorys'] = [(i.top_category_name, i.sec_category.split('|')[:-1]) for i in all_category]
        if load_data_obj:
            res['note_msg'] = [(obj.note_id, obj.note_title, obj.note_labels,
                           obj.creation_time, obj.click_number) for obj in load_data_obj.items]

    except Exception as e:
        print(e)

    return render_template('home.html', res=res, url=URL)


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


@home_index.route('/delete_cache/')
def delete_all_cache():
    ip_log(request.url, delete_all_cache.__name__)
    redis_obj.flushdb(asynchronous=False)
    return 'ok'
