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
import traceback
import o24.backend.scheduler.scheduler as scheduler
from o24.backend.dashboard.serializers import JSProspectData


COLUMNS = [
    {
        'label' : 'List title',
        'prop' : 'title',
    },
    {
        'label' : 'Number of prospects',
        'prop' : 'prospects_num'
    },
]

CORS(app, resources={r'/*': {'origins': '*'}})

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')

    return user

@bp_dashboard.route('/lists/list', methods=['POST'])
#@login_required
def list_lists():

    current_user = get_current_user()

    per_page = config.PROSPECTS_PER_PAGE
    page = 1

    pagination = {
            'perPage' : per_page,
            'currentPage' : page,
            'total' : 0
    }

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
        'lists' : '',
        'pagination' : json.dumps(pagination),
        'columns' : json.dumps(COLUMNS)
    }

    try:
        if request.method == 'POST':
            page = int(request.form.get('_page',1))

            total, lists = ProspectsLists.async_lists(owner_id=current_user.id,
                                                page=page)    
            if lists:
                result['lists'] = lists
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

@bp_dashboard.route('/lists/remove', methods=['POST'])
#@login_required
def remove_lists():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'deleted' : 0
    }
    if request.method == 'POST':
        try:
            list_id = request.form['_list_id']

            prospect_list = ProspectsList.objects(owner=current_user.id, id=list_id).first()
            if not prospect_list:
                raise Exception("There is no such list")

            res = prospect_list.safe_delete()

            result['code'] = 1
            result['deleted'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)

@bp_dashboard.route('/lists/add', methods=['POST'])
#@login_required
def add_list():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'added' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_list']

            js_data = json.loads(raw_data)

            res = ProspectsList.create_list(owner_id=current_user.id,
                                            title=js_data['title'])

            result['code'] = 1
            result['added'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)


#only data field can be edited
@bp_dashboard.route('/lists/edit', methods=['POST'])
#@login_required
def edit_list():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'updated' : ''
    }
    if request.method == 'POST':
        try:
            list_id = request.form['_list_id']

            prospect_list = ProspectsList.objects(owner=current_user.id, id=list_id).first()
            if not prospect_list:
                raise Exception("There is no such list")

            title = request.form.get('title', '')
            if not title:
                raise Exception("Title can't be empty")

            prospect_list.update_data(title=title)
            prospect_list.reload()

            result['code'] = 1
            result['updated'] = prospect_list.serialize()
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['msg'] = 'EDIT SERVER ERROR: ' + str(e)

    return jsonify(result)