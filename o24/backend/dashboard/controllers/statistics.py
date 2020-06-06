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
        'label' : 'Campaign title',
        'prop' : 'campaig'
    },
    {
        'label' : 'Sequence title',
        'prop' : 'status'
    },
    {
        'label' : 'Leads list',
        'prop' : 'funnel',
        'field' : 'title',   
    },
    {
        'label' : 'Leads contacted',
        'prop' : 'status'
    },
    {
        'label' : 'Emails opened',
        'prop' : 'status'
    },
    {
        'label' : 'Emails bounced',
        'prop' : 'status'
    },
    {
        'label' : 'Ln 404',
        'prop' : 'status'
    },
    {
        'label' : 'Ln sent failed',
        'prop' : 'status'
    },
    {
        'label' : 'Ln connect accepted',
        'prop' : 'status'
    },
    {
        'label' : 'Replies',
        'prop' : 'status'
    }
]

@bp_dashboard.route('/statistics/data', methods=['POST'])
@auth_required
def statistics_data():
    current_user = g.user

    result = {
        'code' : -1,
        'columns' : json.dumps(COLUMNS)
    }

    try:        
        if request.method == 'POST':
            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result), 200


@bp_dashboard.route('/statistics/list', methods=['POST'])
@auth_required
def statistics_list():
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

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result), 200


@bp_dashboard.route('/statistics/campaign', methods=['POST'])
@auth_required
def statistics_campaign():
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

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")


            if not campaign.valid_funnel():
                modified_fields_on_edit['funnel'] = True
                modified_fields_on_edit['credentials'] = True

            #check that the list has prospects and funnel exists
            
            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success'
            result['campaign'] = json.dumps(campaign_dict)
            result['modified_fields'] = json.dumps(modified_fields_on_edit)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)