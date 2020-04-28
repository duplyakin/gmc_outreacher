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
            if is_init:
                prospect_lists = ProspectsList.async_lists(owner=current_user.id)
                if prospect_lists:
                    result['prospect_lists'] = prospect_lists.to_json()
                
                funnels = shared.Funnel.async_funnels(owner=current_user.id)
                if funnels:
                    result['funnels'] = funnels.to_json()
                
                total, credentials = Credentials.async_credentials(owner=current_user.id)
                if credentials:
                    result['credentials'] = credentials.to_json()


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


