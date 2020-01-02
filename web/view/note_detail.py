#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, jsonify, request, redirect
from config.base_setting import *


detail_index = Blueprint('detail_page', __name__)
from main import db
from model.notes import Notes


# 笔记详情
@detail_index.route('/<uuid>/')
def note_det(uuid):

    if uuid:
        res = dict()
        note_obj = Notes.query
        res['note_title'] = [[obj.uuid, obj.note_title] for obj in
                             note_obj.order_by(Notes.click_number.desc(), Notes.creation_time.desc()).limit(12)]
        query_obj = note_obj.filter(Notes.uuid == uuid).first()

        query_obj.click_number += 1
        note_list = [query_obj.uuid, query_obj.note_title, query_obj.creation_time, query_obj.note_labels,
                     query_obj.note_instructions, query_obj.note_content, query_obj.click_number]
        res['note_det'] = note_list
        db.session.commit()

        ck_token = request.cookies.get('token', '')
        arg_token = request.args.get('token', '')
        if ck_token or arg_token:
            return render_template('admin/admin_note_detail.html', res=res, url=URL)

        return render_template('note_detail.html', res=res, url=URL)
    else:
        return redirect(url_for('home_page.home'))

