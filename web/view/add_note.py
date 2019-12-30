from flask import Blueprint, render_template, jsonify, request
from web.view.tool.filter_text import *
from config.base_setting import *
import datetime
import uuid

add_index = Blueprint('add_page', __name__)

from main import db
from model.notes import Notes
from model.top_category import TopCategory


@add_index.route('/add/', methods=['POST', 'GET'])
def add_n():
    res = dict()
    if request.method == 'POST':
        note_title = request.json.get('note_title', "")
        category_name = request.json.get('category_name', "")
        str_labels = request.json.get('str_labels', "")
        note_instructions = request.json.get('note_instructions', "")
        str_content = request.json.get('str_content', "")
        creation_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

        category_labels = TopCategory.query.filter(TopCategory.top_category_name == category_name.strip()).first()
        needed_labels = []
        cur_labels_list = category_labels.sec_category.split("|")[:-1]
        for i in str_labels.split("|"):
            if i not in cur_labels_list:
                needed_labels.append(i)
        cur_labels_list.extend(needed_labels)

        category_labels.sec_category = '|'.join(cur_labels_list)

        db.session.add(Notes(
            uuid=str(uuid.uuid1()),
            note_title=note_title,
            note_labels=str_labels,
            note_instructions=note_instructions.strip(),
            note_content=str_content,
            creation_time=creation_time,
            click_number=0
        ))
        db.session.commit()
        return jsonify({'msg': 'ok'})
    category_obj_list = TopCategory.query.all()
    category_name_list = [i.top_category_name for i in category_obj_list]
    res['cate_name_list'] = category_name_list
    s = 'a'

    return render_template('add_note.html', url=URL, res=res, data=s)
