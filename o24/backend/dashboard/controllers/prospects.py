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
from bson.objectid import ObjectId
from o24.backend.utils.decors import auth_required

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
        'prop' : 'email',
        'data' : True
    },
    {
        'label' : 'Linkedin',
        'prop' : 'linkedin',
        'data' : True
    },
    {
        'label' : 'First Name',
        'prop' : 'first_name',
        'data' : True
    },
    {
        'label' : 'Last name',
        'prop' : 'last_name',
        'data' : True
    },
    {
        'label' : 'Campaign',
        'prop' : 'assign_to',
        'field' : 'title'
    },
    {
        'label' : 'Prospects List',
        'prop' : 'assign_to_list',
        'field' : 'title'
    }
]


@bp_dashboard.route('/prospects/data', methods=['POST'])
@auth_required
def data_prospects():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
        'lists' : '',
        'campaigns' : '',
        'columns' : json.dumps(COLUMNS)
    }

    try:
        if request.method == 'POST':
            total, lists = ProspectsList.async_lists(owner_id=current_user.id)
            if lists:
                result['lists'] = lists

            total, campaigns = Campaign.async_campaigns_list(owner=current_user.id)
            if campaigns:
                result['campaigns'] = campaigns


            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)



@bp_dashboard.route('/prospects/list', methods=['POST'])
@auth_required
def list_prospects():

    current_user = g.user

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
        'prospects' : '',
        'pagination' : json.dumps(pagination)
    }
    list_filter = {}

    try:
        if request.method == 'POST':
            page = int(request.form.get('_page',1))
            raw_data = request.form.get('_filters', {})
            if raw_data:
                list_filter = json.loads(raw_data)


            total, prospects = Prospects.async_prospects_list(owner=current_user.id,
                                                list_filter=list_filter,
                                                page=page)    
            if prospects:
                result['prospects'] = prospects
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
@auth_required
def remove_prospect():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'deleted' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_delete']

            js_data = json.loads(raw_data)
            if type(js_data) != list:
                js_data = [js_data]

            ids = [x["_id"]["$oid"] for x in js_data]

            res = Prospects.delete_prospects(owner_id=current_user.id,
                                            prospects_ids=ids)
            
            result['code'] = 1
            result['deleted'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)

@bp_dashboard.route('/prospects/list/add', methods=['POST'])
@auth_required
def add_prospect_to_list():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'added' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_prospects']
            _list_id = request.form['_list_id']

            _list_id = ObjectId(_list_id)

            js_data = json.loads(raw_data)
            if type(js_data) != list:
                js_data = [js_data]

            ids = [x["_id"]["$oid"] for x in js_data]

            res = Prospects.add_to_list(owner_id=current_user.id,
                                            prospects_ids=ids,
                                            list_id=_list_id)
            
            result['code'] = 1
            result['added'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)


@bp_dashboard.route('/prospects/list/remove', methods=['POST'])
@auth_required
def remove_prospect_from_list():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'deleted' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_prospects']

            js_data = json.loads(raw_data)
            if type(js_data) != list:
                js_data = [js_data]

            ids = [x["_id"]["$oid"] for x in js_data]

            res = Prospects.remove_from_list(owner_id=current_user.id,
                                            prospects_ids=ids)

            result['code'] = 1
            result['deleted'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)



@bp_dashboard.route('/prospects/campaign/unassign', methods=['POST'])
@auth_required
def unassign_prospect():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'unassigned' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_unassign']

            js_data = json.loads(raw_data)
            if type(js_data) != list:
                js_data = [js_data]

            ids = [x["_id"]["$oid"] for x in js_data]

            res = scheduler.Scheduler.safe_unassign_prospects(owner_id=current_user.id,
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


@bp_dashboard.route('/prospects/campaign/assign', methods=['POST'])
@auth_required
def assign_prospect():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'assigned' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_prospects']
            campaign_id = request.form.get('_campaign_id','')
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            js_data = json.loads(raw_data)
            if type(js_data) != list:
                js_data = [js_data]

            ids = [x["_id"]["$oid"] for x in js_data]

            res = scheduler.Scheduler.safe_assign_prospects(owner_id=current_user.id,
                                                            campaign=campaign,
                                                            prospects_ids=ids)

            result['code'] = 1
            result['assigned'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)


#only data field can be edited
@bp_dashboard.route('/prospects/edit', methods=['POST'])
@auth_required
def edit_prospect():
    current_user = g.user
    
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

            exist.update_data(data=data, _reload=True)

            result['code'] = 1
            result['updated'] = exist.to_json()
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['msg'] = 'EDIT SERVER ERROR: ' + str(e)

    return jsonify(result)


@bp_dashboard.route('/prospects/create', methods=['POST'])
@auth_required
def create_prospect():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'updated' : ''
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_prospect']
            
            prospect_data = JSProspectData(raw_data=raw_data)

            if prospect_data.assign_to_list():
                assign_to_list = ProspectsList.objects(owner=current_user.id, id=prospect_data.assign_to_list()).first()
                if not assign_to_list:
                    raise Exception("There is no such prospects list")
            
            create_fields = Prospects.get_create_fields()
            new_prospect = Prospects.async_create(owner_id=current_user.id,
                                                create_fields=create_fields,
                                                prospect_data=prospect_data)
            if not new_prospect:
                raise Exception("Something went wrong contact support.")

            #ALWAYS need this: as we create objecId from Json, need mongo to update it with object
            #new_prospect.reload()

            result['code'] = 1
            result['updated'] = new_prospect.serialize()

        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)

@bp_dashboard.route('/prospects/upload', methods=['POST'])
@auth_required
def upload_prospects ():
    current_user = g.user

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
            _update_existing = int(js_data['fields_mapped'].get('_update_existing', 0))
            _csv_array = js_data['fields_mapped']['_csv']
            _csv_header = js_data['fields_mapped']['_csv'][0]

            _columns_checked = js_data['fields_mapped']['columnsChecked']

            #we receive csv_header and need to upload only fields that are checked by user
            # index_map_to_fields - will contain indexes of headers that we need to upload
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
                    raise Exception('Error creating the list')
            else:
                _add_to_list = ProspectsList.objects(owner=current_user.id, id=_add_to_list).first()
                if not _add_to_list:
                    raise Exception('List not found')


            res = Prospects.upload(owner_id=current_user.id,
                                    csv_with_header=_csv_array,
                                    map_to=index_map_to_fields,
                                    list_id=_add_to_list.id,
                                    update_existing=_update_existing)

            result['code'] = 1
            result['uploaded'] = res
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)
