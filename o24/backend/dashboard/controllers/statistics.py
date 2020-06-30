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
import pytz
from datetime import datetime  
from datetime import timedelta  
from dateutil.parser import parse

import o24.backend.models.shared as shared
import o24.backend.scheduler.models as scheduler_models
from o24.backend.utils.decors import auth_required



STATS_TOTAL = [
    {
        'label' : 'Prospects contacted',
        'field' : 'prospects_total',
    },
    {
        'label' : 'Emails sent',
        'field' : EMAIL_SEND_MESSAGE_ACTION,
    },
    {
        'label' : 'Emails replied',
        'field' : EMAIL_CHECK_REPLY_ACTION,
    },
    {
        'label' : 'Emails opened',
        'field' : 'email_opens',
    },
    {
        'label' : 'Emails enriched',
        'field' : 'emails-enriched-success',
    },
    {
        'label' : 'Linkedin invites sent',
        'field' : LINKEDIN_CONNECT_ACTION,
    },
    {
        'label' : 'Linkedin profiles viewed',
        'field' : LINKEDIN_VISIT_PROFILE_ACTION,
    },
    {
        'label' : 'Linkedin messages sent',
        'field' : LINKEDIN_SEND_MESSAGE_ACTION,
    },
    {
        'label' : 'Linkedin replied',
        'field' : LINKEDIN_CHECK_REPLY_ACTION,
    },
    {
        'label' : 'Enrich credits left',
        'field' : 'credits-left',
    }
]


STATS_CAMPAIGN = [
    {
        'label' : 'Prospects contacted',
        'field' : 'prospects_total',
    },
    {
        'label' : 'Emails sent',
        'field' : EMAIL_SEND_MESSAGE_ACTION,
    },
    {
        'label' : 'Emails replied',
        'field' : EMAIL_CHECK_REPLY_ACTION,
    },
    {
        'label' : 'Emails opened',
        'field' : 'email_opens',
    },
    {
        'label' : 'Emails bounced',
        'field' : EMAIL_CHECK_BOUNCED_ACTION,
    },
    {
        'label' : 'Emails enriched',
        'field' : 'emails-enriched-success',
    },
    {
        'label' : 'Linkedin invites sent',
        'field' : LINKEDIN_CONNECT_ACTION,
    },
    {
        'label' : 'Linkedin profiles viewed',
        'field' : LINKEDIN_VISIT_PROFILE_ACTION,
    },
    {
        'label' : 'Linkedin messages sent',
        'field' : LINKEDIN_SEND_MESSAGE_ACTION,
    },
    {
        'label' : 'Linkedin replied',
        'field' : LINKEDIN_CHECK_REPLY_ACTION,
    },
    {
        'label' : 'Errors',
        'field' : 'errors',
    },
    {
        'label' : 'Enrich credits left',
        'field' : 'credits-left',
    }
]


@bp_dashboard.route('/statistics/total', methods=['POST'])
@auth_required
def statistics_total():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'columns' : json.dumps(STATS_TOTAL)
    }

    try:
        if request.method == 'POST':
            now = pytz.utc.localize(datetime.utcnow())
            from_date = now - timedelta(days=TOTAL_STATS_DAYS_DEFAULT)
            stats_total = scheduler_models.ActionLog.get_stats_total(owner_id=current_user.id,
                                                                    from_date=from_date,
                                                                    to_date=now)
            if stats_total:
                result['statistics'] = stats_total

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
        'columns' : json.dumps(STATS_CAMPAIGN)
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')
            if not campaign_id:
                raise Exception("Bad campaign_id")

            from_date = request.form.get('_from_date', '')
            if not from_date:
                raise Exception("Please select from_date")
            
            to_date = request.form.get('_to_date', '')
            if not from_date:
                raise Exception("Please select to_date")
            
            from_date = parse(from_date).astimezone(pytz.utc)
            to_date = parse(to_date).astimezone(pytz.utc)
            stats_campaign = scheduler_models.ActionLog.get_campaign_stats(owner_id=current_user.id, 
                                                                        campaign_id=campaign_id, 
                                                                        from_date=from_date, 
                                                                        to_date=to_date)

            if stats_campaign:
                result['statistics'] = stats_campaign
 
            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)