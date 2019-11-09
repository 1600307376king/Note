from flask import Blueprint, render_template, url_for, jsonify, request, redirect


detail_index = Blueprint('detail_page', __name__)
from main import db
from model.notes import Notes


# 笔记详情
@detail_index.route('/<uuid>')
def note_det(uuid):
    res = dict()
    query_obj = Notes.query.filter(Notes.uuid == uuid).first()
    note_list = [query_obj.note_title, query_obj.creation_time, query_obj.note_labels.split('|')[:-1],
                 query_obj.note_content]
    res['note_det'] = note_list
    return render_template('note_detail.html', res=res)

