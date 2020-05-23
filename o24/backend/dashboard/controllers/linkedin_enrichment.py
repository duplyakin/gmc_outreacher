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
from o24.backend.utils.helpers import template_key_dict, to_json_deep_dereference
import json
import traceback

import o24.backend.models.shared as shared
from o24.backend.dashboard.serializers import JSCampaignData
import o24.backend.scheduler.scheduler as scheduler
from o24.backend.utils.decors import auth_required


COLUMNS = [
    {
        'label' : 'Title',
        'prop' : 'title'
    },
    {
        'label' : 'Status',
        'prop' : 'status'
    },
    {
        'label' : 'Funnel',
        'prop' : 'funnel',
        'field' : 'title',   
    }
]

modified_fields_on_create = {
    'title' : True,
    'time_table' : True,
    'credentials' : True,
    'lists' : True,
    'from_hour' : True,
    'to_hour' : True,
    'from_minutes' : True,
    'to_minutes' : True,
    'sending_days' : True,
    'data' : True,
    'search_url': True,
    'total_pages': True,
    'interval_pages': True,
    'time_zone': True
}

modified_fields_on_edit = {
    'title' : True,
    'time_table' : True,
    'credentials' : False,
    'lists' : False,
    'from_hour' : True,
    'to_hour' : True,
    'from_minutes' : True,
    'to_minutes' : True,
    'sending_days' : True,
    'data' : True,
    'search_url': False,
    'total_pages': True,
    'interval_pages': True,
    'time_zone': True
}

@bp_dashboard.route('/campaign/linkedin/data', methods=['POST'])
@auth_required
def data_linkedin_campaign():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'lists' : '',
        'credentials' : '',
        'modified_fields' : json.dumps(modified_fields_on_create),
        'columns' : json.dumps(COLUMNS)
    }

    try:        
        if request.method == 'POST':
            lists = ProspectsList.get_lists_with_prospects_without_campaigns(owner_id=current_user.id)
            if lists:
                result['lists'] = lists

            total, credentials = Credentials.async_credentials(owner=current_user.id, medium='linkedin')
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

    return jsonify(result), 200


@bp_dashboard.route('/campaign/linkedin/list', methods=['POST'])
@auth_required
def list_linkedin_campaigns():
    current_user = g.user

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
        'modified_fields' : json.dumps(modified_fields_on_create),
        'pagination' : json.dumps(pagination),
        'columns' : json.dumps(COLUMNS)
    }

    try:
        if request.method == 'POST':
            page = int(request.form.get('_page',1))

            total, campaigns = Campaign.async_campaigns_list(owner=current_user.id,
                                                campaign_types=[LINKEDIN_PARSING_CAMPAIGN_TYPE, LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE],
                                                page=page)    
            if campaigns:
                result['campaigns'] = campaigns
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

    return jsonify(result), 200


@bp_dashboard.route('/campaign/linkedin/get', methods=['POST'])
@auth_required
def get_linkedin_campaign_by_id():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : '',
        'campaign' : '',
        'modified_fields': json.dumps(modified_fields_on_edit)
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, 
                                        id=campaign_id,
                                        campaign_type__in=[LINKEDIN_PARSING_CAMPAIGN_TYPE,LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE]).first()
            if not campaign:
                raise Exception("No such enrichment campaign")

            
            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success' 
            result['campaign'] = json.dumps(campaign_dict)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)



@bp_dashboard.route('/campaign/linkedin/parsing/create', methods=['POST'])
@auth_required
def create_linkedin_parsing_campaign():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'added' : ''
    }
    if request.method == 'POST':
        try:
            raw_data = request.form['_add_campaign']
            
            campaign_data = JSCampaignData(raw_data=raw_data)

            credentials = campaign_data.credentials()
            if not credentials:
                raise Exception("Credentials can't be empty")
            
            list_title = campaign_data.get_list_title()
            if not list_title:
                raise Exception("Prospects list can't be empty")
            
            create_fields = Campaign.get_create_fields()
            new_campaign = Campaign.async_create(owner=current_user.id, 
                                                campaign_data=campaign_data,
                                                campaign_type=LINKEDIN_PARSING_CAMPAIGN_TYPE,
                                                create_fields=create_fields)
            
            if not new_campaign or not new_campaign.id:
                raise Exception("Something went wrong contact support.")
            
            new_campaign.set_linkedin_parsing_funnel()
            #ALWAYS need this: as we create objecId from Json, need mongo to update it with object
            #new_campaign.reload()
            
            p_list = ProspectsList.create_list(owner_id=current_user.id, 
                                            title=list_title)

            new_campaign.add_data_value(key="list_id", value=str(p_list.id))
            new_campaign.reload()

            campaign_dict = to_json_deep_dereference(new_campaign)

            result['code'] = 1
            result['added'] = json.dumps(campaign_dict)
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)


@bp_dashboard.route('/campaign/linkedin/enrichment/create', methods=['POST'])
@auth_required
def create_linkedin_enrichment_campaign():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'added' : ''
    }
    if request.method == 'POST':
        try:
            raw_data = request.form.get('_add_campaign', '')
            if not raw_data:
                raise Exception("_add_campaign can't be empty")
 
            campaign_data = JSCampaignData(raw_data=raw_data)

            credentials = campaign_data.credentials()
            if not credentials:
                raise Exception("Credentials can't be empty")
            
            prospects_list = ProspectsList.objects(owner=current_user.id, id=campaign_data.prospects_list()).first()
            if not prospects_list:
                raise Exception("There is no such prospects list")
            
            create_fields = Campaign.get_create_fields()
            new_campaign = Campaign.async_create(owner=current_user.id, 
                                                campaign_data=campaign_data,
                                                campaign_type=LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE,
                                                create_fields=create_fields)
            
            if not new_campaign or not new_campaign.id:
                raise Exception("Something went wrong contact support.")
            
            new_campaign.set_linkedin_enrichment_funnel()
            new_campaign.add_data_value(key="list_id", value=str(prospects_list.id))

            #assign prospects
            prospects = Prospects.objects(owner=current_user.id, assign_to_list=prospects_list.id)
            if prospects:
                ids = [p.id for p in prospects]
                if ids:
                    Prospects._assign_campaign_on_create(owner_id=current_user.id, campaign_id=new_campaign.id, prospects_ids=ids)


            new_campaign.reload()
            campaign_dict = to_json_deep_dereference(new_campaign)

            result['code'] = 1
            result['added'] = json.dumps(campaign_dict)
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)



@bp_dashboard.route('/campaign/linkedin/edit', methods=['POST'])
@auth_required
def edit_linkedin_campaign():
    current_user = g.user

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

            if campaign.inprogress():
                raise Exception("Campaign in progress: stop progress first")
            
            raw_fields = request.form.get('_modified_fields', '')
            if not raw_fields:
                raise Exception("_modified_fields can't be empty")
            
            modified_fields = json.loads(raw_fields)
            if not modified_fields:
                raise Exception("_modified_fields missed: don't know what to modify")

            raw_data = request.form.get('_add_campaign', '')
            if not raw_data:
                raise Exception("Edit error: _add_campaign can't be empty")

            campaign_data = JSCampaignData(raw_data=raw_data)

            edit_fields = [k for k, v in modified_fields.items() if v]
            if not edit_fields:
                raise Exception("edit_fields can't be empty")  

            campaign.async_edit(owner=current_user.id, campaign_data=campaign_data, edit_fields=edit_fields)

            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success'
            result['updated'] = json.dumps(campaign_dict)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/campaign/linkedin/delete', methods=['POST'])
@auth_required
def delete_linkedin_campaign():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')            
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            scheduler.Scheduler.safe_delete_campaign(owner_id=current_user.id, campaign=campaign, _unassign=True)

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/campaign/linkedin/start', methods=['POST'])
@auth_required
def start_linkedin_campaign():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')            
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            
            scheduler.Scheduler.safe_start_campaign(owner=current_user.id, campaign=campaign)
            campaign.reload()

            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success'
            result['started'] = json.dumps(campaign_dict)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/campaign/linkedin/pause', methods=['POST'])
@auth_required
def pause_linkedin_campaign():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')            
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            
            scheduler.Scheduler.safe_pause_campaign(campaign=campaign)

            campaign.reload()

            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success'
            result['paused'] = json.dumps(campaign_dict)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)