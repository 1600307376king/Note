from flask import Blueprint, render_template, url_for, jsonify, request, redirect
from config.base_setting import *
from web.view.filter_text import *

home_index = Blueprint('home_page', __name__)
from main import db
from model.notes import Notes


@home_index.route('/home/')
def home():
    res = dict()
    note_list = Notes.query.all()
    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_instructions, obj.note_labels.split('|')[:-1], obj.creation_time] for obj in note_list]
    url = 'http://' + IP + ':' + SERVER_PORT
    return render_template('home.html', res=res, url=url)


@home_index.route('/update/<uuid>')
def go_update(uuid):
    res = dict()
    query_obj = Notes.query.filter(Notes.uuid == uuid).first()
    note_list = [query_obj.note_title, query_obj.note_labels.split('|')[:-1], query_obj.note_instructions,
                 query_obj.note_content, query_obj.uuid]
    res['note_cur_msg'] = note_list
    print(query_obj.note_labels.split('|')[:-1])
    return render_template('update_note.html', res=res)


@home_index.route('/modification/<uuid>', methods=['POST'])
def com_modification(uuid):
    query_obj = Notes.query.filter(Notes.uuid == uuid).first()
    query_obj.note_title = request.json.get('note_title')
    query_obj.note_labels = request.json.get('str_labels')
    query_obj.note_instructions = request.json.get('note_instructions')
    str_content = request.json.get('str_content')
    query_obj.note_content = filter_note_con(str_content)
    print(request.json.get('str_labels'))
    db.session.commit()

    return jsonify({'msg': 'ok'})