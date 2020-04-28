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

COLUMNS = [
    {
        'label' : 'account',
        'prop' : 'account'
    },
    {
        'label' : 'sender',
        'prop' : 'sender',
        'data' : True
    },
    {
        'label' : 'Linkedin cookie',
        'prop' : 'li_at',
        'data' : True
   
    },
    {
        'label' : 'status',
        'prop' : 'status'
    },
    {
        'label' : 'Limit per day',
        'prop' : 'limit_per_day'
    }
]

CORS(app, resources={r'/*': {'origins': '*'}})

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user


@bp_dashboard.route('/credentials', methods=['POST'])
#@login_required
def list_credentials():

    current_user = get_current_user()

    per_page = config.CREDENTIALS_PER_PAGE
    page = 1

    pagination = {
            'perPage' : per_page,
            'currentPage' : page,
            'total' : 0
    }

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
        'credentials' : '',
        'pagination' : json.dumps(pagination),
        'columns' : json.dumps(COLUMNS)
    }

    try:
        if request.method == 'POST':
            page = int(request.form.get('_page',1))

            total, credentials = Credentials.async_credentials(owner=current_user.id,
                                                page=page)    
            if credentials:
                result['credentials'] = credentials.to_json()
                result['pagination'] = json.dumps({
                    'perPage' : per_page,
                    'currentPage' : page,
                    'total' : total
                })

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
#@login_required
def edit_credentials():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'updated' : ''
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_credentials']

            js_data = json.loads(raw_data)

            credentials_id = js_data['_id']['$oid']
            
            exist = Credentials.objects(owner=current_user.id, id=credentials_id).first()
            if not exist:
                raise Exception('Account does not exist')

            exist.update_data(data=js_data)
            exist.reload()

            result['code'] = 1
            result['updated'] = exist.to_json()
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['msg'] = 'EDIT SERVER ERROR: ' + str(e)

    return jsonify(result)


@bp_dashboard.route('/credentials/delete', methods=['POST'])
#@login_required
def delete_credentials():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'deleted' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_delete']

            js_data = json.loads(raw_data)

            ids = [x["_id"]["$oid"] for x in js_data]

            res = Credentials.delete_credentials(owner_id=current_user.id,
                                                credentials_ids=ids)

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
#@login_required
def add_credentials():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'added' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_add_credentials']
            js_data = json.loads(raw_data)

            credentials_type = js_data['selected_type']
            if not credentials_type:
                raise Exception('Wrong account type')
            
            new_credentials = None
            if credentials_type == 'Linkedin':
                linkedin_data = js_data['linkedin']
                data = {
                    'medium' : 'linkedin',
                    'data' : {
                        'account' : 'Linkedin: ' + str(linkedin_data.get('login')),
                        'sender' : 'linkedin',
                        'login' : linkedin_data.get('login'),
                        'password' : linkedin_data.get('password')
                    }
                }
                new_credentials = Credentials.create_credentials(owner=current_user.id, 
                                                                data=data)
            elif credentials_type == 'Gmail/Gsuite':
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
