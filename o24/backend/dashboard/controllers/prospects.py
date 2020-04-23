# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from flask import Flask, jsonify
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Prospects, User, ProspectsList, Campaign
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import o24.config as config
from o24.backend.utils.serialize import JSONEncoder
import json

PROSPECTS = [
    {
        'id' : 1,
        'email' : 'ks.shilov@gmail.com',
        'name' : 'Kirill1'
    },
    {
        'id' : 2,
        'email' : 'ksshilov@yandex.ru',
        'name' : 'Kirill2'
    },
    {
        'id' : 3,
        'email' : 'ks.shilov+1@gmail.com',
        'name' : 'Kirill3'
    },
    {
        'id' : 4,
        'email' : 'ks.shilov+2@gmail.com',
        'name' : 'Kirill4'
    },

]

COLUMNS = [
    {
        'label' : 'Email',
        'prop' : 'email'
    },
    {
        'label' : 'Linkedin',
        'prop' : 'linkedin'
    },
    {
        'label' : 'First Name',
        'prop' : 'first_name'
    },
    {
        'label' : 'Last Name',
        'prop' : 'last_name'
    },
    {
        'label' : 'Assigned campaign',
        'prop' : 'assign_to'
    },
    {
        'label' : 'Assigned lists',
        'prop' : 'lists'
    }
]

CORS(app, resources={r'/*': {'origins': '*'}})

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user


@bp_dashboard.route('/prospects', defaults={'page': 1}, methods=['GET', 'POST'])
@bp_dashboard.route('/prospects/<int:page>', methods=['GET', 'POST'])
#@login_required
def list_prospects(page):

    current_user = get_current_user()
    result = {
        'code' : 1,
        'msg' : '',
        'lists' : '',
        'campaigns' : '',
        'prospects' : '',
        'columns' : json.dumps(COLUMNS)
    }
    list_filter = {}
    try:
        if request.method == 'GET':
            lists = ProspectsList.async_lists(owner=current_user.id)
            if lists:
                result['lists'] = lists.to_json()

            campaigns = Campaign.async_campaigns(owner=current_user.id)
            if campaigns:
                result['campaigns'] = campaigns.to_json()
        elif request.method == 'POST':
            raw_data = request.form['_filters']
            
            js_data = json.loads(raw_data)
            page = 2

        prospects = Prospects.async_prospects(owner=current_user.id,
                                            list_filter=list_filter,
                                            page=page)    
        if prospects:
            result['prospects'] = prospects.to_json()
    except Exception as e:
        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)

@bp_dashboard.route('/prospects/remove/<prospect_id>', methods=['GET', 'POST'])
#@login_required
def remove_prospect(prospect_id):
    return jsonify(PROSPECTS)

@bp_dashboard.route('/prospects/edit', methods=['POST'])
#@login_required
def edit_prospect():
    result = {
        'code' : -1,
        'msg' : '',
        'updated' : ''
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_prospect']

            js_data = json.loads(raw_data)
            data = js_data['data']
            if not data:
                raise Exception('Error: prospect data can not be empty')

            prospect_id = js_data['_id']['$oid']
            
            exist = Prospects.objects(id=prospect_id).first()
            if not exist:
                raise Exception('Prospect does not exist')

            exist.update_data(data=data)
            exist.reload()

            result['code'] = 1
            result['updated'] = exist.to_json()
        except Exception as e:
            result['msg'] = 'EDIT SERVER ERROR: ' + str(e)

    return jsonify(result)


@bp_dashboard.route('/prospects/add', methods=['GET', 'POST'])
#@login_required
def add_prospect():
    return jsonify(PROSPECTS)

@bp_dashboard.route('/prospects/upload', methods=['GET', 'POST'])
#@login_required
def upload_prospects ():
    return jsonify(PROSPECTS)

@bp_dashboard.route('/list/create', methods=['GET', 'POST'])
#@login_required
def create_list():
    return jsonify(PROSPECTS)