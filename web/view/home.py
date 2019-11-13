from flask import Blueprint, render_template, url_for, jsonify, request, redirect
from config.base_setting import *
from web.view.filter_text import *

home_index = Blueprint('home_page', __name__)
from main import db
from model.notes import Notes


@home_index.route('/home/')
def home():
    res = dict()
    note_list = Notes.query.order_by(Notes.click_number.desc(), Notes.creation_time.desc())
    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_instructions, obj.note_labels.split('|')[:-1],
                        obj.creation_time, obj.click_number] for obj in note_list]

    return render_template('home.html', res=res, url=URL)


@home_index.route('/update/<uuid>')
def go_update(uuid):
    res = dict()
    query_obj = Notes.query.filter(Notes.uuid == uuid).first()
    note_list = [query_obj.note_title, query_obj.note_labels.split('|')[:-1], query_obj.note_instructions,
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
    res['note_msg'] = [[obj.uuid, obj.note_title, obj.note_instructions, obj.note_labels.split('|')[:-1],
                        obj.creation_time] for obj in note_list]

    return render_template('home.html', res=res, url=URL)


