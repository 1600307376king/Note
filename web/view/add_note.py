from flask import Blueprint, render_template, url_for, jsonify, request, redirect


add_index = Blueprint('add_page', __name__)


@add_index.route('/add/')
def home():
    return render_template('add_note.html')

