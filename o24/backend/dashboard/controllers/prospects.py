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
        'label' : 'email',
        'prop' : 'email'
    },
    {
        'label' : 'linkedin',
        'prop' : 'linkedin'
    },
    {
        'label' : 'first_name',
        'prop' : 'first_name'
    },
    {
        'label' : 'last_name',
        'prop' : 'last_name'
    },
    {
        'label' : 'assign_to',
        'prop' : 'assign_to'
    },
    {
        'label' : 'lists',
        'prop' : 'lists'
    }
]

CORS(app, resources={r'/*': {'origins': '*'}})

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user


@bp_dashboard.route('/prospects', methods=['POST'])
#@login_required
def list_prospects():

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
        'campaigns' : '',
        'prospects' : '',
        'pagination' : json.dumps(pagination),
        'columns' : json.dumps(COLUMNS)
    }
    list_filter = {}

    try:
        if request.method == 'POST':
            is_init = request.form.get('_init', 0)
            if int(is_init):
                lists = ProspectsList.async_lists(owner=current_user.id)
                if lists:
                    result['lists'] = lists.to_json()

                campaigns = Campaign.async_campaigns(owner=current_user.id)
                if campaigns:
                    result['campaigns'] = campaigns.to_json()

            page = int(request.form.get('_page',1))
            raw_data = request.form.get('_filters', {})
            if raw_data:
                list_filter = json.loads(raw_data)


            total, prospects = Prospects.async_prospects(owner=current_user.id,
                                                list_filter=list_filter,
                                                page=page)    
            if prospects:
                result['prospects'] = prospects.to_json()
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

@bp_dashboard.route('/prospects/remove', methods=['POST'])
#@login_required
def remove_prospect():
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

            res = Prospects.delete_prospects(owner_id=current_user.id,
                                            prospects_ids=ids)
            print(res)

            result['code'] = 1
            result['deleted'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)

@bp_dashboard.route('/prospects/assign', methods=['POST'])
#@login_required
def assign_prospect():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'assigned' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_prospects']
            _campaign_id = request.form['_campaign_id']

            js_data = json.loads(raw_data)

            ids = [x["_id"]["$oid"] for x in js_data]

            res = Prospects.assign_prospects(owner_id=current_user.id,
                                            prospects_ids=ids,
                                            campaign_id=_campaign_id)

            result['code'] = 1
            result['assigned'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)



@bp_dashboard.route('/prospects/unassign', methods=['POST'])
#@login_required
def unassign_prospect():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'unassigned' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_unassign']

            js_data = json.loads(raw_data)

            ids = [x["_id"]["$oid"] for x in js_data]

            res = Prospects.unassign_prospects(owner_id=current_user.id,
                                            prospects_ids=ids)

            result['code'] = 1
            result['unassigned'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)



@bp_dashboard.route('/prospects/edit', methods=['POST'])
#@login_required
def edit_prospect():
    current_user = get_current_user()

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
            
            exist = Prospects.objects(owner=current_user.id, id=prospect_id).first()
            if not exist:
                raise Exception('Prospect does not exist')

            exist.update_data(data=data)
            exist.reload()

            result['code'] = 1
            result['updated'] = exist.to_json()
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['msg'] = 'EDIT SERVER ERROR: ' + str(e)

    return jsonify(result)


@bp_dashboard.route('/prospects/create', methods=['POST'])
#@login_required
def create_prospect():
    current_user = get_current_user()

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

            email = data['email']
            
            exist = Prospects.objects(data__email=email).first()
            if exist:
                raise Exception('Prospect with this email already exist')

            prospect = Prospects.create_prospect(owner_id=current_user.id, data=data)

            result['code'] = 1
            result['updated'] = prospect.to_json()
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)

@bp_dashboard.route('/prospects/upload', methods=['POST'])
#@login_required
def upload_prospects ():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'uploaded' : 0
    }

    if request.method == 'POST':
        try:
            raw_data = request.form['_upload_data']

            js_data = json.loads(raw_data)

            #headers as the first row
            _csv_array = js_data['fields_mapped']['_csv']
            _csv_header = js_data['fields_mapped']['_csv'][0]

            _columns_checked = js_data['fields_mapped']['columnsChecked']

            index_map_to_fields = {}
            for ch in _columns_checked:
                header = ch.get('header','')
                map_selected = ch.get('map_selected', '')

                if header and map_selected:
                    index = _csv_header.index(header)
                    index_map_to_fields[index] = map_selected
            
            _add_to_list = js_data['list_selected']['list']['list_selected_id']
            _create_new = js_data['list_selected']['createNew']
            if _create_new:
                _add_to_list = js_data['list_selected']['list']['list_new_label']
                _add_to_list = ProspectsList.create_list(owner_id=current_user.id, title=_add_to_list)
                if not _add_to_list:
                    raise Exception('Error creatin the list')
            else:
                _add_to_list = ProspectsList.get_lists(owner=current_user.id, id=_add_to_list)
                if not _add_to_list:
                    raise Exception('List not found')


            res = Prospects.upload(owner_id=current_user.id,
                                    csv_with_header=_csv_array,
                                    map_to=index_map_to_fields,
                                    add_to_list=_add_to_list)

            if not res:
                raise Exception('Prospects creation error - 0 prospects created')

            result['code'] = 1
            result['uploaded'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)
