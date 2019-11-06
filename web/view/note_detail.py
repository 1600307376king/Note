from flask import Blueprint, render_template, url_for, jsonify, request, redirect


detail_index = Blueprint('detail_page', __name__)


# 笔记详情
@detail_index.route('/det/')
def note_det():
    return render_template('note_detail.html')

