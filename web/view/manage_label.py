#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/3 18:21
# @Author  : HelloWorld
# @File    : manage_label.py
from flask import Flask, render_template, jsonify, Blueprint, request
from .tool.filter_text import clean_data


bind_index = Blueprint('bind_page', __name__)

from model.top_category import TopCategory
from model.notes import Notes
from main import db


@bind_index.route('/bl/', methods=['POST', 'GET'])
def manage_label():
    res = dict()
    if request.method == 'POST':
        category = request.json.get('category', '')
        unbound_labels = request.json.get('unbound_labels', '')
        print(category, unbound_labels)
        label_obj = TopCategory.query.filter(TopCategory.top_category_name == category).first()
        label_obj.sec_category = label_obj.sec_category + '|'.join(unbound_labels.split(',')) + '|'
        db.session.commit()
        return jsonify({'msg': 'ok'})
    note_labels = [list(map(clean_data, i.note_labels.split('|')[:-1])) for i in Notes.query.all()]
    temp_list = []
    for j in note_labels:
        temp_list.extend(j)
    note_set = set(temp_list)

    category = [k.top_category_name.strip() for k in TopCategory.query.all()]
    temp_list = []
    category_labels = [list(map(clean_data, k.sec_category.split('|')[:-1])) for k in TopCategory.query.all()]
    for m in category_labels:
        temp_list.extend(m)
    cate_set = set(temp_list)

    new_labels = note_set - (cate_set | set(category))

    dt = [{'text': str(v), "val": str(i + 1)} for i, v in enumerate(new_labels)]
    res['category'] = category


    return render_template('admin/bind_label.html', res=res, data=dt)