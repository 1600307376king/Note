#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/3/20 21:10
# @Author : jjc
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user

plan_index = Blueprint('plan_page', __name__)


@plan_index.route('/plan/', methods=('GET', 'POST'))
def display_plans():
    res = {}
    if current_user.is_active:
        res['user_info'] = {'username': current_user.adminName}
    return render_template('plans.html', res=res)