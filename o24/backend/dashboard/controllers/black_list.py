# Import flask dependencies
from flask import request, g, redirect, url_for, jsonify, session
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from werkzeug.security import check_password_hash, generate_password_hash
from o24.backend.dashboard.models import User, Credentials, BlackList

from o24.backend import db
from o24.backend import app
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import json
import traceback
from o24.backend.utils.decors import auth_required, get_token
from o24.backend.dashboard.serializers import JSUserData


@bp_dashboard.route('/blacklist/list', methods=['POST'])
@auth_required
def blacklist_list():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            blacklist_list = BlackList.async_list(owner_id=current_user.id)
            if blacklist_list:
                result['data'] = blacklist_list

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/blacklist/add', methods=['POST'])
@auth_required
def blacklist_add():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            raw_data = request.form.get('entities', None)
            if not raw_data:
                raise Exception("Entities can't be empty")
            
            js_data = json.loads(raw_data)
            if not js_data:
                raise Exception("data format error")

            black_list = BlackList.get_black_list(owner_id=current_user.id)
            if not black_list:
                raise Exception("Can't create the list")

            black_list.add_list(entities=js_data)

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/blacklist/remove', methods=['POST'])
@auth_required
def blacklist_remove():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            raw_data = request.form.get('ids', None)
            if not raw_data:
                raise Exception("Entities can't be empty")
            
            js_data = json.loads(raw_data)
            if not js_data:
                raise Exception("ids format error")

            black_list = BlackList.get_black_list(owner_id=current_user.id)
            if not black_list:
                raise Exception("Can't create the list")

            black_list.remove_entities(entities=js_data)

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)
