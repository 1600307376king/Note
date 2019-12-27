#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 0011 9:12
# @Author  : HelloWorld
# @File    : modification.py
from flask import Blueprint, jsonify, request
from web.view.tool.filter_text import *

mod_index = Blueprint('mod_page', __name__)
from main import db
from model.notes import Notes


@mod_index.route('/modification/<uuid>', methods=['POST'])
def com_modification(uuid):
    query_obj = Notes.query.filter(Notes.uuid == uuid).first()
    query_obj.note_title = request.json.get('note_title')
    query_obj.note_labels = request.json.get('str_labels')
    query_obj.note_instructions = request.json.get('note_instructions')
    str_content = request.json.get('str_content')
    query_obj.note_content = str_content
    db.session.commit()

    return jsonify({'msg': 'ok'})