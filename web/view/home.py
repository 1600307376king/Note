from flask import Blueprint, render_template, url_for, jsonify, request, redirect


home_index = Blueprint('home_page', __name__)


@home_index.route('/')
def home():
    return render_template('home.html')
