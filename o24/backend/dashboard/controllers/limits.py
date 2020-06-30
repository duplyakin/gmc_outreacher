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
from o24.backend.utils.decors import auth_required

EMAIL_LIMITS = [
    {
        'label' : 'Daily sending maximum',
        'prop' : EMAIL_SEND_MESSAGE_ACTION,
        'explanation' : 'The maximum amount of emails you can send per 24 hours period'
    },
]

LINKEDIN_LIMITS = [
    {
        'label' : 'Account daily maximum',
        'prop' : 'account_maximum',
        'explanation' : 'Number of all actions you can do from your linkedin account per 24 hour period.'
    },
    {
        'label' : 'Search pages parse maximum',
        'prop' : LINKEDIN_SEARCH_ACTION,
        'explanation' : 'Maximum number of search pages, that you can parse per 24 hour period.'

    },
    {
        'label' : 'Profiles parse maximum',
        'prop' : LINKEDIN_PARSE_PROFILE_ACTION,
        'explanation' : 'Maximum number of profile parsed per 24 hour period.'

    },
    {
        'label' : 'Profile visit action maximum',
        'prop' : LINKEDIN_VISIT_PROFILE_ACTION,
        'explanation' : 'Maximum number of profiles you can automatically visit per 24 hour period.'

    },
    {
        'label' : 'Linkedin connect request maximum',
        'prop' : LINKEDIN_CONNECT_ACTION,
        'explanation' : 'Maximum number connection requests you can send per 24 hour period.'

    },
    {
        'label' : 'Linkedin messages maximum',
        'prop' : LINKEDIN_SEND_MESSAGE_ACTION,
        'explanation' : 'Maximum number of messages you can send per 24 hour period.'
    },
]



@bp_dashboard.route('/limits/show', methods=['POST'])
@auth_required
def limits_show():

    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
        'email_columns' : json.dumps(EMAIL_LIMITS),
        'linkedin_columns' : json.dumps(LINKEDIN_LIMITS)
    }

    try:
        if request.method == 'POST':
            credentials_id = request.form.get('_credentials_id','')
            if not credentials_id:
                raise Exception("Bad credentials_id")

            credentials = Credentials.objects(owner=current_user.id, id=credentials_id).first()
            if not credentials:
                raise Exception("No such credentials")

            limits = credentials.get_limits()
            if not limits:
                raise Exception("No limits for credentials")
                
            result['limits'] = limits
            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/limits/edit', methods=['POST'])
@auth_required
def limits_edit():

    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request',
    }

    try:
        if request.method == 'POST':
            credentials_id = request.form.get('_credentials_id','')
            if not credentials_id:
                raise Exception("Bad credentials_id")

            credentials = Credentials.objects(owner=current_user.id, id=credentials_id).first()
            if not credentials:
                raise Exception("No such credentials")

            raw_data = request.form.get('_limits_data', '')
            if not raw_data:
                raise Exception("_limits_data missed: don't know what to modify")

            limits_data = JSLimitsData(raw_data=raw_data)

            new_limits = credentials.update_limits(limits_data)
            if not new_limits:
                raise Exception("Try again")
                
            new_limits.reload()

            result['limits'] = new_limits.to_json()
            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)