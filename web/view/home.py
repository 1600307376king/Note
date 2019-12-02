from flask import Blueprint, render_template, url_for, jsonify, request, redirect, flash
from web.view.filter_text import *
from config.base_setting import *
from flask_wtf import FlaskForm
from flask_wtf.file import *
from wtforms import *
import time
import itertools

home_index = Blueprint('home_page', __name__)
from main import db
from model.notes import Notes


class SearchForm(FlaskForm):
    keyword = StringField('关键词：', validators=[DataRequired(),
                          validators.Length(min=1, max=10, message='搜索条件为空或输入字符太长')])
    submit = SubmitField('搜索')


def clean_data(x):
    return x.strip()


@home_index.route('/home/', methods=['GET', 'POST'])
def home():
    res = dict()
    search_form = SearchForm()
    note_obj = Notes.query

    note_labels = note_obj.all()
    tmp = [obj.note_labels for obj in note_labels]

    # list({}.fromkeys(f).keys()) 去重
    res['note_labels'] = list({}.fromkeys(map(clean_data, ''.join(tmp).split('|')[:-1])).keys())

    if request.method == 'POST':
        label_name = request.form.get('label_name')
        if label_name:
            label_name = label_name.strip()
            labels_res = note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
                filter(Notes.note_labels.like('%' + label_name + '%') |
                       Notes.note_title.like('%' + label_name + '%') |
                       Notes.note_content.like('%' + label_name + '%')).all()
            res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_instructions, obj.note_labels,
                                obj.creation_time, obj.click_number] for obj in labels_res]
        else:
            if search_form.validate_on_submit():
                search_keyword = search_form.keyword.data
                search_result = note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc()). \
                    filter(Notes.note_labels.like('%' + search_keyword + '%') |
                           Notes.note_title.like('%' + search_keyword + '%') |
                           Notes.note_content.like('%' + search_keyword + '%')).all()
                res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_instructions, obj.note_labels,
                                    obj.creation_time, obj.click_number] for obj in search_result]
            else:
                error_msg = search_form.errors
                flash(error_msg.get('keyword')[0])

        return render_template('home.html', res=res, form=search_form, url=URL)

    ip = request.headers.get('Remote Address')
    is_has_cache = redis_obj.get('home' + str(ip))

    if is_has_cache:
        res['note_msg'] = [
            list(map(decode_text,
                     redis_obj.hmget('home' + str(ip) + str(i), 'uuid', 'note_title', 'note_instructions',
                                     'note_labels', 'creation_time', 'click_number')))
            for i in range(int(bytes.decode(is_has_cache)))]

        return render_template('home.html', form=search_form, res=res, url=URL)

    note_list = note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc())
    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_instructions, obj.note_labels,
                        obj.creation_time, obj.click_number] for obj in note_list]

    # 清除缓存
    # redis_obj.flushdb(asynchronous=False)
    # 添加缓存
    for i, v in enumerate(note_list):
        # redis_obj.expire('home' + str(ip) + str(i), 10)
        dic = {'uuid': str(v.uuid),
               'note_title': str(v.note_title),
               'note_instructions': str(v.note_instructions),
               'note_labels': str(v.note_labels),
               'creation_time': str(v.creation_time),
               'click_number': str(v.click_number)}

        redis_obj.hmset('home' + str(ip) + str(i), dic)

    redis_obj.set('home' + str(ip), len(res['note_msg']), ex=10)

    return render_template('home.html', res=res, form=search_form, url=URL)


@home_index.route('/update/<uuid>')
def go_update(uuid):
    res = dict()
    query_obj = Notes.query.filter(Notes.uuid == uuid).first()
    note_list = [query_obj.note_title, query_obj.note_labels, query_obj.note_instructions,
                 query_obj.note_content, query_obj.uuid]
    res['note_cur_msg'] = note_list
    return render_template('update_note.html', res=res, url=URL)


@home_index.route('/delete/<uuid>')
def delete_note(uuid):
    res = dict()
    note_obj = Notes.query
    delete_obj = note_obj.filter(Notes.uuid == uuid).first()
    db.session.delete(delete_obj)
    db.session.commit()
    note_list = note_obj.all()
    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_instructions, obj.note_labels,
                        obj.creation_time] for obj in note_list]

    return render_template('home.html', res=res, url=URL)


@home_index.route('/filter_label/')
def filter_label():
    pass


@home_index.route('/delete_cache/')
def delete_all_cache():
    redis_obj.flushdb(asynchronous=False)
    return 'ok'
