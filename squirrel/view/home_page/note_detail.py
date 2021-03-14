#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from config.base_setting import *
from squirrel.view.tool.ip_log import ip_log
from main import db
from model.notes import Notes


detail_index = Blueprint('detail_page', __name__)


# 笔记详情
@detail_index.route('/<note_id>/')
def note_det(note_id):
    ip_log(request.url, note_det.__name__)

    res = dict()
    note_obj = Notes.query
    res['note_title'] = [[obj.note_id, obj.note_title] for obj in
                         note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc()).limit(12)]

    query_obj = note_obj.get_or_404(note_id)
    query_obj.click_number += 1
    note_list = [query_obj.note_id, query_obj.note_title, query_obj.creation_time, query_obj.note_labels,
                 query_obj.note_instructions, query_obj.note_content, query_obj.click_number]
    res['note_det'] = note_list
    db.session.commit()
    # ck_token = request.cookies.get('token', '')
    # arg_token = request.args.get('token', '')
    # if ck_token or arg_token:
    #     return render_template('note_detail.html', res=res, url=URL)

    return render_template('note_detail.html', res=res, url=URL)


