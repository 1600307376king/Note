from flask import Blueprint, render_template, url_for, jsonify, request, redirect
from web.view.filter_text import *
from config.base_setting import *
import datetime
import uuid


add_index = Blueprint('add_page', __name__)

from main import db
from model.notes import Notes


@add_index.route('/add/', methods=['POST', 'GET'])
def add_n():
    if request.method == 'POST':
        note_title = request.json.get('note_title')
        str_labels = request.json.get('str_labels')
        note_instructions = request.json.get('note_instructions')
        str_content = request.json.get('str_content')

        creation_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        db.session.add(Notes(
            uuid=str(uuid.uuid1()),
            note_title=note_title,
            note_labels=str_labels,
            note_instructions=note_instructions.strip(),
            note_content=filter_note_con(str_content),
            creation_time=creation_time,
            click_number=0
        ))
        db.session.commit()
        return jsonify({'msg': 'ok'})
    return render_template('add_note.html',  url=URL)

