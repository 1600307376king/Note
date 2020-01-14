#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, request, flash
from .tool.filter_text import clean_data
from config.base_setting import *
from .tool.ip_log import ip_log
from .form.common_form import *
import uuid

home_index = Blueprint('home_page', __name__)

from model.top_category import TopCategory
from model.notes import Notes
from main import db


@home_index.route('/', methods=['GET', 'POST'])
def home():
    ip_log(request.url, home.__name__)
    res = dict()
    search_form = SearchForm()
    all_category = TopCategory.query.all()
    res['top_categorys'] = [[i.top_category_name, i.sec_category.split('|')[:-1]] for i in all_category]

    note_obj = Notes.query
    note_labels = note_obj.all()
    tmp = [obj.note_labels for obj in note_labels]

    # list({}.fromkeys(f).keys()) 去重
    res['note_labels'] = list({}.fromkeys(map(clean_data, ''.join(tmp).split('|')[:-1])).keys())

    # 首页输入关键字搜索
    if request.method == 'POST':
        if search_form.validate_on_submit():
            search_keyword = search_form.keyword.data
            search_result = note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
                filter(Notes.note_labels.like('%' + search_keyword + '%') |
                       Notes.note_title.like('%' + search_keyword + '%')). \
                paginate(1, per_page=PER_PAGE_MAX_NUM).items
            res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_labels,
                                obj.creation_time, obj.click_number] for obj in search_result]
            return render_template('home.html', res=res, form=search_form, url=URL)
        else:
            error_msg = search_form.errors
            flash(error_msg.get('keyword')[0])

    # ip = request.headers.get('Remote Address')
    # is_has_cache = redis_obj.get('home' + str(ip))

    # if is_has_cache:
    #     res['note_msg'] = [
    #         list(map(decode_text,
    #                  redis_obj.hmget('home' + str(ip) + str(i), 'uuid', 'note_title', 'note_instructions',
    #                                  'note_labels', 'creation_time', 'click_number')))
    #         for i in range(int(bytes.decode(is_has_cache)))]
    #
    #     return render_template('home.html', form=search_form, res=res, url=URL, filter=0)

    note_list = note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
        paginate(1, per_page=PER_PAGE_MAX_NUM).items

    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_labels,
                        obj.creation_time, obj.click_number] for obj in note_list]
    print(res['note_msg'][0])
    # 清除缓存
    # redis_obj.flushdb(asynchronous=False)
    # 添加缓存
    # for i, v in enumerate(note_list):
    #     dic = {'uuid': str(v.uuid),
    #            'note_title': str(v.note_title),
    #            'note_instructions': str(v.note_instructions),
    #            'note_labels': str(v.note_labels),
    #            'creation_time': str(v.creation_time),
    #            'click_number': str(v.click_number)}
    #
    #     redis_obj.hmset('home' + str(ip) + str(i), dic)

    # redis_obj.set('home' + str(ip), len(res['note_msg']), ex=1)
    ck_token = request.cookies.get('token', '')
    arg_token = request.args.get('token', '')
    if ck_token or arg_token:
        return render_template('admin/admin_home.html', res=res, form=search_form, url=URL)

    return render_template('home.html', res=res, form=search_form, url=URL)


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
        return render_template('admin/admin_update_note.html', res=res, url=URL)
    return render_template('update_note.html', res=res, url=URL)


# 删除当前note
@home_index.route('/delete/<note_uuid>/', methods=['POST'])
def delete_note(note_uuid):
    ip_log(request.url, delete_note.__name__)
    res = dict()
    note_list = []
    filter_type = request.json.get('filter_type', 'rec')
    label_name = request.json.get('label_name', 'all')
    # cur_page = int(request.json.get('cur_page', 1))
    label_name = label_name.capitalize()

    note_obj = Notes.query
    delete_obj = note_obj.get_or_404(note_uuid)
    db.session.delete(delete_obj)
    db.session.commit()

    if label_name == 'All' and filter_type == 'rec':
        note_list = Notes.query.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
            paginate(1, per_page=PER_PAGE_MAX_NUM).items
    if label_name != 'All' and filter_type != 'rec':
        note_list = Notes.query.filter(Notes.note_labels.like("%" + label_name + "%")).order_by(
            Notes.creation_time.desc()). \
            paginate(1, per_page=PER_PAGE_MAX_NUM).items
    if label_name == 'All' and filter_type != 'rec':
        note_list = Notes.query.order_by(Notes.creation_time.desc()). \
            paginate(1, per_page=PER_PAGE_MAX_NUM).items
    if label_name != 'All' and filter_type == 'rec':
        note_list = Notes.query.filter(Notes.note_labels.like("%" + label_name + "%")).order_by(
            Notes.click_number.desc(), Notes.creation_time.desc()). \
            paginate(1, per_page=PER_PAGE_MAX_NUM).items
    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_labels,
                        obj.creation_time, obj.click_number] for obj in note_list]

    return jsonify(res)


# 条件排序
@home_index.route('/filter_col/', methods=['POST'])
def filter_sort():
    ip_log(request.url, filter_sort.__name__)
    res = dict()
    note_list = []
    filter_type = request.json.get('filter_type', 'rec')
    label_name = request.json.get('label_name', 'all')
    label_name = label_name.capitalize()

    if label_name == 'All' and filter_type == 'rec':
        note_list = Notes.query.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
            paginate(1, per_page=PER_PAGE_MAX_NUM).items
    if label_name != 'All' and filter_type != 'rec':
        note_list = Notes.query.filter(Notes.note_labels.like("%" + label_name + "%")).order_by(
            Notes.creation_time.desc()). \
            paginate(1, per_page=PER_PAGE_MAX_NUM).items
    if label_name == 'All' and filter_type != 'rec':
        note_list = Notes.query.order_by(Notes.creation_time.desc()). \
            paginate(1, per_page=PER_PAGE_MAX_NUM).items
    if label_name != 'All' and filter_type == 'rec':
        note_list = Notes.query.filter(Notes.note_labels.like("%" + label_name + "%")).order_by(
            Notes.click_number.desc(), Notes.creation_time.desc()). \
            paginate(1, per_page=PER_PAGE_MAX_NUM).items

    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_labels,
                        obj.creation_time, obj.click_number] for obj in note_list]

    return jsonify(res)


# 页面向下滚动加载
@home_index.route('/load_data/', methods=['GET'])
def loading_data():
    ip_log(request.url, loading_data.__name__)
    cur_page = request.args.get('page', 2)
    filter_type = request.args.get('type', 'rec')
    label_name = request.args.get('label', 'all')
    label_name = label_name.capitalize()
    cur_page = int(cur_page)
    msg = dict()
    msg['msg'] = 'None'
    msg['res'] = ''
    msg['cur_num'] = cur_page
    try:
        load_result_obj = None
        if filter_type == 'rec' and label_name == 'All':
            load_result_obj = Notes.query.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
                paginate(cur_page, per_page=PER_PAGE_MAX_NUM)
        elif filter_type == 'rec' and label_name != 'All':
            load_result_obj = Notes.query.filter(Notes.note_labels.like("%" + label_name + "%")).order_by(
                Notes.click_number.desc(), Notes.creation_time.desc()). \
                paginate(cur_page, per_page=PER_PAGE_MAX_NUM)
        elif filter_type == 'new' and label_name != 'All':
            load_result_obj = Notes.query.filter(Notes.note_labels.like("%" + label_name + "%")).order_by(
                Notes.creation_time.desc()). \
                paginate(cur_page, per_page=PER_PAGE_MAX_NUM)
        elif filter_type == 'new' and label_name == 'All':
            load_result_obj = Notes.query.order_by(Notes.creation_time.desc()). \
                paginate(cur_page, per_page=PER_PAGE_MAX_NUM)
        if load_result_obj:
            load_data_list = load_result_obj.items

            msg['res'] = [[obj.uuid, obj.note_title, obj.note_labels,
                           obj.creation_time, obj.click_number] for obj in load_data_list]

            if len(msg['res']) == PER_PAGE_MAX_NUM:
                msg['msg'] = 'continue'
                msg['cur_num'] += 1
            if len(msg['res']) < PER_PAGE_MAX_NUM:
                msg['msg'] = 'continue'
                msg['warning'] = 'break'

    except Exception as e:
        print(e)

    return jsonify(msg)


# @home_index.route('/load_label/', methods=['POST'])
# def load_labels():
#     res = dict()
#     top_category = request.json.get('top_category')
#     print(top_category)
#     label_obj = TopCategory.query.filter(TopCategory.top_category_name == top_category).first()
#     label_list = [i for i in label_obj.sec_category.split('|')[:-1]]
#     print(label_list)
#     res['label_list'] = label_list
#     return jsonify(res)


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
