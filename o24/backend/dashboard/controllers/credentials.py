# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from flask import Flask, jsonify
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Credentials, User, ProspectsList, Campaign
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import o24.config as config
from o24.backend.utils.serialize import JSONEncoder
import json
import traceback
from o24.backend.google.provider.oauth_provider import GoogleOauthProvider
from o24.backend.dashboard.serializers import JSCredentialsData
from o24.backend.utils.decors import auth_required


COLUMNS = [
    {
        'label' : 'account',
        'prop' : 'account',
        'data' : True
    },
    {
        'label' : 'status',
        'prop' : 'status'
    },
    {
        'label' : 'Sender',
        'prop' : 'sender',
        'data' : True
    },
    {
        'label' : 'Linkedin cookie',
        'prop' : 'li_at',
        'data' : True
   
    },
    {
        'label' : 'Limit per day',
        'prop' : 'limit_per_day'
    },
    {
        'label' : 'Actions done today',
        'prop' : 'current_daily_counter'
    }
]



@bp_dashboard.route('/credentials/list', methods=['POST'])
@auth_required
def list_credentials():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
        'credentials' : '',
        'columns' : json.dumps(COLUMNS)
    }

    try:
        if request.method == 'POST':
            page = int(request.form.get('_page', 1))

            total, credentials = Credentials.async_credentials(owner=current_user.id,
                                                page=page)    
            if credentials:
                result['credentials'] = credentials

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/credentials/edit', methods=['POST'])
@auth_required
def edit_credentials():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'updated' : ''
    }
    if request.method == 'POST':
        try:
            credentials_id = request.form.get('_credentials_id','')            
            if not credentials_id:
                raise Exception("Bad credentials_id")

            credentials = Credentials.objects(owner=current_user.id, id=credentials_id).first()
            if not credentials:
                raise Exception("Credentials don't exist")

            raw_data = request.form.get('_credentials','')
            if not raw_data:
                raise Exception("There is no _credentials form parameter")

            credentials_data = JSCredentialsData(raw_data=raw_data)

            credentials.safe_update_credentials(credentials_data=credentials_data)

            result['code'] = 1
            result['updated'] = credentials.to_json()
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['msg'] = 'EDIT SERVER ERROR: ' + str(e)

    return jsonify(result)


@bp_dashboard.route('/credentials/delete', methods=['POST'])
@auth_required
def delete_credentials():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'deleted' : 0
    }
    if request.method == 'POST':
        try:
            credentials_id = request.form.get('_credentials_id','')            
            if not credentials_id:
                raise Exception("Bad credentials_id")

            credentials = Credentials.objects(owner=current_user.id, id=credentials_id).first()
            if not credentials:
                raise Exception("Credentials don't exist")
            
            res = credentials.safe_delete_credentials()

            result['code'] = 1
            result['deleted'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)


@bp_dashboard.route('/credentials/add', methods=['POST'])
@auth_required
def add_credentials():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'added' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form.get('_credentials','')
            if not raw_data:
                raise Exception("There is no _credentials form parameter")

            credentials_data = JSCredentialsData(raw_data=raw_data)

            credentials_type = credentials_data.get_type()
            if not credentials_type:
                raise Exception("Credentials type can't be empty")
            
            new_credentials = None
            if credentials_type == 'linkedin':
                medium='linkedin'
                new_credentials = Credentials.create_credentials(owner=current_user.id, 
                                                                new_data=credentials_data.get_data(), 
                                                                medium=medium, 
                                                                limit_per_day=credentials_data.get_limit_per_day())
            elif credentials_type == 'gmail/gsuite':
                result['code'] = 1
                result['redirect'] = url_for('dashboard.dashboard_oauth_button')
                
                return jsonify(result)
            else:
                raise Exception('Unsupported credentials type')


            if not new_credentials:
                raise Exception('Credentials creation error - contact support')

            result['code'] = 1
            result['added'] = new_credentials.to_json()
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)
