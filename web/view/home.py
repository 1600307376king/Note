from flask import Blueprint, render_template, url_for, jsonify, request, redirect
from config.base_setting import *

home_index = Blueprint('home_page', __name__)
from main import db
from model.notes import Notes


@home_index.route('/')
def home():
    res = dict()
    note_list = Notes.query.all()
    res['note_msg'] = [[obj.n_id, obj.note_title, obj.note_instructions, obj.note_labels.split('|')[:-1], obj.creation_time] for obj in note_list]
    url = 'http://' + IP + ':' + SERVER_PORT
    return render_template('home.html', res=res, url=url)

