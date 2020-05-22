# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from o24.backend.dashboard.models import User, Credentials
from jinja2 import TemplateNotFound

from o24.backend.google.provider.oauth_provider import GoogleOauthProvider
from o24.backend.google.models import GoogleAppSetting
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from datetime import datetime
import pytz
from o24.backend.dashboard.serializers import JSGoogleAppSettingsData

import json
import traceback
from o24.backend.utils.decors import admin_required, get_token
from dateutil.parser import parse

USER_COLUMNS = [
    {
        'label' : 'Email',
        'prop' : 'email'
    },
    {
        'label' : 'Role',
        'prop' : 'role'
    },
    {
        'label' : 'Registration data',
        'prop' : 'created'   
    },
    {
        'label' : 'Personal invitation code',
        'prop' : 'invite_code'   
    },
    {
        'label' : 'Invited by',
        'prop' : 'invited_by'   
    }
]

GOOGLE_SETTINGS = [
    {
        'label' : 'Title',
        'prop' : 'title'
    },
    {
        'label' : 'Gmail Api Name',
        'prop' : 'gmail_api_name'
    },
    {
        'label' : 'Gmail Api Version',
        'prop' : 'gmail_api_version'   
    },
    {
        'label' : 'Active',
        'prop' : 'active'   
    },
    {
        'label' : 'Created',
        'prop' : 'created'   
    }
]

GOOGLE_SETTINGS_CREATE_FIELDS = [
    {
        'label' : 'Title',
        'prop' : 'title'
    },
    {
        'label' : 'credentials',
        'prop' : 'credentials'
    },
    {
        'label' : 'redirect_uri',
        'prop' : 'redirect_uri'
    },
    {
        'label' : 'gmail_scopes',
        'prop' : 'gmail_scopes'   
    },
    {
        'label' : 'gmail_access_type',
        'prop' : 'gmail_access_type'   
    },
    {
        'label' : 'gmail_include_granted_scopes',
        'prop' : 'gmail_include_granted_scopes'   
    },
    {
        'label' : 'gmail_api_name',
        'prop' : 'gmail_api_name'   
    },
    {
        'label' : 'gmail_api_version',
        'prop' : 'gmail_api_version'   
    },
    {
        'label' : 'active (1 or 0)',
        'prop' : 'active'   
    }
]

CREDENTIALS_TABLE_COLUMNS = [
    {
        'label' : 'Owner',
        'prop' : 'owner'   
    },
    {
        'label' : 'medium',
        'prop' : 'medium'   
    },
    {
        'label' : 'Status',
        'prop' : 'status'   
    },
    {
        'label' : 'error',
        'prop' : 'error'   
    },
    {
        'label' : 'next_action',
        'prop' : 'next_action'   
    },
    {
        'label' : 'current_daily_counter',
        'prop' : 'current_daily_counter'   
    }
]


@bp_dashboard.route('/admin/users/list', methods=['POST'])
@admin_required
def admin_users_list():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
        'roles' : ['admin', 'user'],
        'columns' : json.dumps(USER_COLUMNS)
    }

    try:
        if request.method == 'POST':
            users = User.objects()
            if users:
                result['users'] = users.to_json()

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)

@bp_dashboard.route('/admin/password/change', methods=['POST'])
@admin_required
def admin_change_user_password():
    current_user = g.user
    if current_user.role != 'admin':
        return jsonify(msg='Permision denied'), 403
    
    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            user_id = request.form.get('_user_id','')
            if not user_id:
                raise Exception("Bad _user_id")

            user = User.objects(id=user_id).get()
            if not user:
                raise Exception("No such user")

            new_password = request.form.get('_new_password','')
            if not new_password:
                raise Exception("Password can't be empty")

            
            user.admin_change_password(new_password=new_password)
            user.reload()

            result['code'] = 1
            result['msg'] = 'Success'
            result['user'] = user.to_json()
            result['new_password'] = new_password
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/admin/roles/change', methods=['POST'])
@admin_required
def admin_change_user_role():
    current_user = g.user
    if current_user.role != 'admin':
        return jsonify(msg='Permision denied'), 403
    
    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            user_id = request.form.get('_user_id','')
            if not user_id:
                raise Exception("Bad _user_id")

            user = User.objects(id=user_id).get()
            if not user:
                raise Exception("No such user")

            new_role = request.form.get('_new_role','')
            if not new_role:
                raise Exception("Bad new_role")

            user.role = new_role
            user._commit()
            user.reload()

            result['code'] = 1
            result['msg'] = 'Success'
            result['user'] = user.to_json()
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)

@bp_dashboard.route('/admin/google/settings/list', methods=['POST'])
@admin_required
def admin_google_settings_list():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
        'columns' : json.dumps(GOOGLE_SETTINGS)
    }

    try:
        if request.method == 'POST':
            google_settings = GoogleAppSetting.objects()
            if google_settings:
                result['google_settings'] = google_settings.to_json()

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)

@bp_dashboard.route('/admin/google/settings/get', methods=['POST'])
@admin_required
def admin_google_settings_get():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
    }

    try:
        if request.method == 'POST':
            settings_id = request.form.get('_settings_id','')
            if not settings_id:
                raise Exception("Bad _settings_id")

            settings = GoogleAppSetting.objects(id=settings_id).get()
            if not settings:
                raise Exception("No such settings")

            result['code'] = 1
            result['msg'] = 'Success'
            result['settings'] = settings.to_json()
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/admin/google/settings/edit', methods=['POST'])
@admin_required
def admin_google_settings_edit():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
    }

    try:
        if request.method == 'POST':
            settings_id = request.form.get('_settings_id','')
            if not settings_id:
                raise Exception("Bad _settings_id")

            settings = GoogleAppSetting.objects(id=settings_id).get()
            if not settings:
                raise Exception("No such settings")

            raw_data = request.form.get('_data','')
            if not raw_data:
                raise Exception("There is no _data, can't edit")

            new_data = JSGoogleAppSettingsData(raw_data=raw_data)

            settings.update_data(from_data=new_data)
            settings.reload()

            result['code'] = 1
            result['msg'] = 'Success'
            result['settings'] = settings.to_json()
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/admin/google/settings/delete', methods=['POST'])
@admin_required
def admin_google_settings_delete():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
    }

    try:
        if request.method == 'POST':
            settings_id = request.form.get('_settings_id','')
            if not settings_id:
                raise Exception("Bad _settings_id")

            settings = GoogleAppSetting.objects(id=settings_id).get()
            if not settings:
                raise Exception("No such settings")

            settings.delete()

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)



@bp_dashboard.route('/admin/google/settings/fields', methods=['POST'])
@admin_required
def admin_google_settings_fields():
    current_user = g.user

    result = {
        'columns' : json.dumps(GOOGLE_SETTINGS_CREATE_FIELDS)
    }

    try:
        if request.method == 'POST':

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/admin/google/settings/create', methods=['POST'])
@admin_required
def admin_google_settings_create():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
    }

    try:
        if request.method == 'POST':
            raw_data = request.form.get('_data','')
            if not raw_data:
                raise Exception("There is no _data, can't edit")
            
            new_data = JSGoogleAppSettingsData(raw_data=raw_data)

            new_settings = GoogleAppSetting.create_settings(from_data=new_data)
            new_settings.reload()

            result['code'] = 1
            result['msg'] = 'Success'
            result['settings'] = new_settings.to_json()
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/admin/login/as', methods=['POST'])
@admin_required
def admin_login_as_another_user():
    current_user = g.user
    if current_user.role != 'admin':
        return jsonify(msg='Permision denied'), 403

    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            user_id = request.form.get('_user_id', '')
            if not user_id:
                raise Exception("Bad _user_id")
                        
            user = User.objects(id=user_id).get()
            if not user:
                raise Exception("No such user")

            
            result['code'] = 1
            result['msg'] = 'Success'
            result['token'] = get_token(user)
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/admin/credentials/list', methods=['POST'])
@admin_required
def admin_list_credentials():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
        'columns' : json.dumps(CREDENTIALS_TABLE_COLUMNS)
    }

    try:
        if request.method == 'POST':
            credentials = Credentials.admin_async_credentials()
            if not credentials:
                raise Exception("No credentials found")
            
            result['code'] = 1
            result['msg'] = 'Success'
            result['credentials'] = credentials
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/admin/credentials/get', methods=['POST'])
@admin_required
def admin_get_credentials():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
    }

    try:
        if request.method == 'POST':
            cr_id = request.form.get('_credentials_id', '')
            if not cr_id:
                raise Exception("Bad _credentials_id")
                        
            credentials = Credentials.objects(id=cr_id).get()
            if not credentials:
                raise Exception("Credentials not found")

            result['code'] = 1
            result['msg'] = 'Success'
            result['credentials'] = credentials.to_json()
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/admin/credentials/edit', methods=['POST'])
@admin_required
def admin_edit_credentials():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
    }

    try:
        if request.method == 'POST':
            cr_id = request.form.get('_credentials_id', '')
            if not cr_id:
                raise Exception("Bad _credentials_id")

            credentials = Credentials.objects(id=cr_id).get()
            if not credentials:
                raise Exception("Credentials not found")

            raw_data = request.form.get('_credentials_data', '')
            if not raw_data:
                raise Exception("Bad credentials_data")
            
            credentials_data = json.loads(raw_data)
            if not credentials_data:
                raise Exception("credentials_data can't be empty")
            
            # 0 - TEXT
            # 1 - INT
            # 2 - DATE
            allow_fields = {'status' : 1, 
                            'error_message' : 0, 
                            'medium' : 0, 
                            'next_action' : 2,
                            'limit_per_day' : 1, 
                            'limit_per_hour' : 1, 
                            'limit_interval' : 1,
                            'current_daily_counter' : 1, 
                            'current_hourly_counter' : 1
                            }

            for k,v in credentials_data.items():
                if k not in allow_fields.keys():
                    continue

                if v:
                    is_type = allow_fields.get(k)
                    if is_type == 1:
                        v = int(v)
                    elif is_type == 2:
                        #2020-05-21T15:14:20.906Z
                        d_obj = parse(v)
                        v = d_obj
                    
                    setattr(credentials, k, v)

            credentials._commit(_reload=True)

            result['code'] = 1
            result['msg'] = 'Success'
            result['credentials'] = credentials.to_json()
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)
