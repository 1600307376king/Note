#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 0011 9:12
# @Author  : HelloWorld
# @File    : modification.py
from flask import Blueprint, jsonify, request
from squirrel.view.tool.ip_log import ip_log
from main import db, csrf
from model.notes import Notes


mod_index = Blueprint('mod_page', __name__)


@mod_index.route('/modification/<note_id>', methods=['POST'])
@csrf.exempt
def com_modification(note_id):
    ip_log(request.url, com_modification.__name__)
    query_obj = Notes.query.get_or_404(note_id)
    query_obj.note_title = request.json.get('note_title', '')
    query_obj.note_labels = request.json.get('str_labels', '')
    query_obj.note_instructions = request.json.get('note_instructions')
    str_content = request.json.get('str_content')
    query_obj.note_content = str_content
    db.session.commit()

    return jsonify({'msg': 'ok'})