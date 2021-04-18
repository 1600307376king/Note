#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify
from config.base_setting import *
from squirrel.view.tool.ip_log import ip_log
from squirrel.mysql_con.mysql_util import query_ins
from main import db
from model.notes import Notes


detail_index = Blueprint('detail_page', __name__)


# 笔记详情
@detail_index.route('/<note_id>/')
def note_det(note_id):
    ip_log(request.url, note_det.__name__)

    res = {'note_title': query_ins.get_recommend_notes(), 'note_det': query_ins.get_notes_detail(note_id)}

    # return render_template('note_detail.html', res=res, url=URL)
    return jsonify(res)

