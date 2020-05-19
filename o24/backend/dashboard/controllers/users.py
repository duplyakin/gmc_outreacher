# Import flask dependencies
from flask import request, g, redirect, url_for, jsonify, session
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from werkzeug.security import check_password_hash, generate_password_hash
from o24.backend.dashboard.models import User, Credentials

from o24.backend import db
from o24.backend import app
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import json
import traceback
from o24.backend.utils.decors import auth_required
from o24.backend.dashboard.serializers import JSUserData


def get_token(user):
    return create_access_token(identity=str(user.id))

@bp_dashboard.route('/sign_in', methods=['POST'])
def sign_in():
    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            raw_data = request.form.get('_auth_data', '')
            if not raw_data:
                raise Exception("Bad _user")
            
            user_data = JSUserData(raw_data)
            
            current_user = User.authenticate(user_data=user_data)
            if not current_user:
                raise Exception("Authentication error")

            
            
            result['code'] = 1
            result['msg'] = 'Success'
            result['token'] = get_token(current_user)
            result['role'] = current_user.role
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)

@bp_dashboard.route('/sign_up', methods=['POST'])
def sign_up():
    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            raw_data = request.form.get('_auth_data', '')
            if not raw_data:
                raise Exception("Bad _user")
            
            user_data = JSUserData(raw_data)
            
            current_user = User.register(user_data=user_data)
            
            if not current_user:
                raise Exception("Error register the User")
            
            current_user._commit(_reload=True)

            
            result['code'] = 1
            result['msg'] = 'Success'
            result['token'] = get_token(current_user)
            result['role'] = current_user.role
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/profile', methods=['POST'])
@auth_required
def profile():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            result['code'] = 1
            result['msg'] = 'Success'
            result['user'] = current_user.to_json()
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/verify-token', methods=['POST'])
@auth_required
def verify_token():
    return jsonify({'success': True}), 200
