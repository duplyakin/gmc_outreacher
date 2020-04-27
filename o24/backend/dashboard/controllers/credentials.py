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

COLUMNS = [
    {
        'label' : 'account',
        'prop' : 'account'
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