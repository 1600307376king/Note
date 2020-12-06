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
from main import db, cache
import uuid

home_index = Blueprint('home_page', __name__)


@home_index.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=10)
@login_required
def home():
    """
    进入首页
    :return:
    """
    ip_log(request.url, home.__name__)
    res = dict()

    all_category = TopCategory.query.all()
    res['top_categorys'] = [[i.top_category_name, i.sec_category.split('|')[:-1]] for i in all_category]

    note_obj = Notes.query
    note_labels = note_obj.all()
    tmp = [obj.note_labels for obj in note_labels]

    # list({}.fromkeys(f).keys()) 去重
    res['note_labels'] = list({}.fromkeys(map(clean_data, ''.join(tmp).split('|')[:-1])).keys())

    # 首页输入关键字搜索
    # if request.method == 'POST':
    #     if search_form.validate_on_submit():
    #         search_keyword = search_form.keyword.data
    #         search_result = note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
    #             filter(Notes.note_labels.like('%' + search_keyword + '%') |
    #                    Notes.note_title.like('%' + search_keyword + '%')). \
    #             paginate(1, per_page=PER_PAGE_MAX_NUM).items
    #         res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_labels,
    #                             obj.creation_time, obj.click_number] for obj in search_result]
    #         return render_template('home.html', res=res, form=search_form, url=URL)
    #     else:
    #         error_msg = search_form.errors
    #         flash(error_msg.get('keyword')[0])

    note_list = note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
        paginate(1, per_page=PER_PAGE_MAX_NUM).items

    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_labels,
                        obj.creation_time, obj.click_number] for obj in note_list]

    res['user_info'] = {'username': current_user.adminName}
    ck_token = request.cookies.get('token', '')
    arg_token = request.args.get('token', '')
    if ck_token or arg_token:
        return render_template('admin_manage/admin_home.html', res=res, url=URL)

    return render_template('home.html', res=res, url=URL)


# 进入修改页
@home_index.route('/update/<note_uuid>/')
def go_update(note_uuid):
    ip_log(request.url, go_update.__name__)
    res = dict()
    query_obj = Notes.query.get_or_404(note_uuid)
    note_list = [query_obj.note_title, query_obj.note_labels, query_obj.note_instructions,
                 query_obj.note_content, query_obj.uuid]
    res['note_cur_msg'] = note_list
    ck_token = request.cookies.get('token', '')
    arg_token = request.args.get('token', '')
    if ck_token or arg_token:
        return render_template('admin_manage/admin_update_note.html', res=res, url=URL)
    return render_template('update_note.html', res=res, url=URL)


# 删除当前note
@home_index.route('/delete/<note_uuid>/', methods=['POST'])
def delete_note(note_uuid):
    ip_log(request.url, delete_note.__name__)
    res = dict()
    filter_type = request.json.get('filter_type', 'rec')
    label_name = request.json.get('label_name', 'All')
    label_name = label_name.capitalize()

    delete_obj = Notes.query.get_or_404(note_uuid)
    db.session.delete(delete_obj)
    db.session.commit()
    note_obj = filter_func(filter_type, label_name, 1, Notes)
    if note_obj:
        res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_labels,
                            obj.creation_time, obj.click_number] for obj in note_obj.items]

    return jsonify(res)


# 条件排序
@home_index.route('/filter_col/', methods=['POST'])
def filter_sort():
    ip_log(request.url, filter_sort.__name__)
    res = dict()
    filter_type = request.json.get('filter_type', 'rec')
    label_name = request.json.get('label_name', 'All')
    label_name = label_name.capitalize()
    note_obj = filter_func(filter_type, label_name, 1, Notes)
    if note_obj:
        res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_labels,
                            obj.creation_time, obj.click_number] for obj in note_obj.items]

    return jsonify(res)


# 页面向下滚动加载
@home_index.route('/load_data/', methods=['GET'])
def loading_data():
    ip_log(request.url, loading_data.__name__)
    cur_page = request.args.get('page', 2)
    filter_type = request.args.get('type', 'rec')
    label_name = request.args.get('label', 'All')
    label_name = label_name.capitalize()
    cur_page = int(cur_page)
    msg = dict()
    msg['msg'] = 'None'
    msg['res'] = ''
    msg['cur_num'] = cur_page
    try:
        load_data_obj = filter_func(filter_type, label_name, cur_page, Notes)
        if load_data_obj:
            msg['res'] = [[obj.uuid, obj.note_title, obj.note_labels,
                           obj.creation_time, obj.click_number] for obj in load_data_obj.items]

            if len(msg['res']) == PER_PAGE_MAX_NUM:
                msg['msg'] = 'continue'
                msg['cur_num'] += 1
            if len(msg['res']) < PER_PAGE_MAX_NUM:
                msg['msg'] = 'continue'
                msg['warning'] = 'break'

    except Exception as e:
        print(e)

    return jsonify(msg)


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
