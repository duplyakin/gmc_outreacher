# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from flask import Flask, jsonify
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Prospects, User, Campaign, ProspectsList, Credentials
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import o24.config as config
from o24.backend.utils.serialize import JSONEncoder
from o24.backend.utils.helpers import template_key_dict 
import json
import traceback

import o24.backend.models.shared as shared

COLUMNS = [
    {
        'label' : 'Campaign title',
        'prop' : 'title'
    },
    {
        'label' : 'From account',
        'prop' : 'account',
        'data' : True
   
    },
    {
        'label' : 'status',
        'prop' : 'status'
    },
    {
        'label' : 'Prospects list',
        'prop' : 'prospects_list',
        'data' : True
    },
    {
        'label' : 'Funnel title',
        'prop' : 'funnel_title',
        'data' : True
   
    }
]


CORS(app, resources={r'/*': {'origins': '*'}})

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user

@bp_dashboard.route('/campaigns', methods=['POST'])
#@login_required
def list_campaigns():

    current_user = get_current_user()

    per_page = config.CAMPAIGNS_PER_PAGE
    page = 1

    pagination = {
            'perPage' : per_page,
            'currentPage' : page,
            'total' : 0
    }

    result = {
        'code' : -1,
        'msg' : '',
        'campaigns' : '',
        'prospect_lists' : '',
        'funnels' : '',
        'credentials' : '',
        'columns' : json.dumps(COLUMNS),
        'pagination' : json.dumps(pagination),
    }

    try:
        if request.method == 'POST':
            is_init = int(request.form.get('_init', 0))
            is_create = int(request.form.get('_create', 0))
            if is_init or is_create:
                prospect_lists = ProspectsList.async_lists(owner=current_user.id)
                if prospect_lists:
                    result['prospect_lists'] = prospect_lists.to_json()
                
                funnels = shared.Funnel.async_funnels(owner=current_user.id)
                if funnels:
                    result['funnels'] = funnels.to_json()
                
                total, credentials = Credentials.async_credentials(owner=current_user.id)
                if credentials:
                    result['credentials'] = credentials.to_json()

            if not is_create:
                page = int(request.form.get('_page',1))

                total, campaigns = Campaign.async_campaigns(owner=current_user.id,
                                                    page=page)    
                if campaigns:
                    result['campaigns'] = campaigns.to_json()
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


@bp_dashboard.route('/campaigns/create', methods=['POST'])
#@login_required
def create_campaign():
    current_user = get_current_user()

    result = {
        'code' : -1,
        'msg' : '',
        'added' : 0
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_add_campaign']
            
            js_data = json.loads(raw_data)
            
            from_title = js_data['title']
            if not from_title:
                raise Exception("Campaign title can't be empty")

            from_time_table = js_data['timeTable']
            if not from_time_table:
                raise Exception("Time sending parameters can't be empty")

            from_funnel = js_data['funnel']
            from_credentials = js_data['credentials']
            from_prospect_list = js_data['prospectsList']
            
            from_templates = js_data['templates']
            if not from_templates:
                raise Exception("Can't create campaign with empty templates")
            
            mapped_templates = template_key_dict(from_templates)
            if not mapped_templates:
                raise Exception("Wrong templates format")



            funnel = shared.Funnel.objects(id=from_funnel).first()
            if not funnel:
                raise Exception("No such funnel")
            
            credentials = []
            account = ''
            for cr in from_credentials:
                n_cr = Credentials.objects(owner=current_user.id, id=cr).first()
                if not n_cr:
                    raise Exception("Wrong credentials: account data")
                credentials.append(n_cr.id)
                if not account:
                    account = n_cr.get_account()

            if not credentials:
                raise Exception("Can't create campaign with empty accounts")
            
            prospect_list = ProspectsList.objects(owner=current_user.id, id=from_prospect_list).first()
            if not prospect_list:
                raise Exception("There is not such prospects list")

            data = {
                'title' : from_title,
                'funnel' : funnel.id,
                'credentials' : credentials,
                'templates' : mapped_templates,
                'time_table' : from_time_table,
                'prospects_list' : prospect_list.id,
                'data' : {
                    'funnel_title' : funnel.title,
                    'prospects_list' : prospect_list.title,
                    'account' : account
                }
            }
            
            new_campaign = Campaign.create_campaign(owner=current_user.id, data=data)
            if not new_campaign:
                raise Exception("Something went wrong contact support.")
        
            result['code'] = 1
            result['added'] = new_campaign.to_json()
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)

@bp_dashboard.route('/campaigns/get', methods=['POST'])
#@login_required
def get_campaign_by_id():
    current_user = get_current_user()

    result = {
        'code' : 1,
        'msg' : '',
        'campaign' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')
            if not campaign_id:
                raise Exception("Bad campaign_di")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            result['code'] = 1
            result['msg'] = 'Success'
            result['campaign'] = campaign.to_json()
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)



@bp_dashboard.route('/campaigns/edit', methods=['POST'])
#@login_required
def edit_campaign():
    current_user = get_current_user()

    result = {
        'code' : 1,
        'msg' : '',
        'updated' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')
            if not campaign_id:
                raise Exception("Bad campaign_di")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            raw_data = request.form['_edit_campaign_data']

            js_data = json.loads(raw_data)

            campaign.async_edit(data=js_data)
            campaign.reload()

            result['code'] = 1
            result['msg'] = 'Success'
            result['updated'] = campaign.to_json()
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)
