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
import json
import traceback

import o24.backend.models.shared as shared
import o24.backend.scheduler.models as scheduler_models
from o24.backend.utils.decors import auth_required



COLUMNS = [
    {
        'label' : 'Campaign title',
        'prop' : 'campaign_title'
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

    per_page = config.STATS_PER_PAGE
    page = 1

    pagination = {
            'perPage' : per_page,
            'currentPage' : page,
            'total' : 0
    }

    result = {
        'code' : -1,
        'msg' : '',
        'pagination' : json.dumps(pagination),
        'columns' : json.dumps(COLUMNS)
    }

    try:
        if request.method == 'POST':
            page = request.form.get('_page', 1)

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
        'msg' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')
            if not campaign_id:
                raise Exception("Bad campaign_id")
            
            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)