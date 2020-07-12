# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from o24.backend.dashboard.models import User, Credentials
from jinja2 import TemplateNotFound
import o24.backend.dashboard.models as models
from o24.backend.google.provider.oauth_provider import GoogleOauthProvider
from o24.backend.google.models import GoogleAppSetting
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from datetime import datetime
from datetime import timedelta
import pytz
from o24.backend.dashboard.serializers import JSGoogleAppSettingsData

import json
import traceback
from o24.backend.utils.decors import admin_required, get_token
from dateutil.parser import parse
import o24.backend.scheduler.models as scheduler_models

@bp_dashboard.route('/admin/campaigns/list', methods=['POST'])
@admin_required
def admin_campaigns_list():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    try:
        if request.method == 'POST':
            page = int(request.form.get('_page',1))

            total, campaigns = models.Campaign.admin_async_campaigns_list(page=page)    
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
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)

@bp_dashboard.route('/admin/campaigns/actions/list', methods=['POST'])
@admin_required
def admin_campaigns_actions_list():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : 'Unknown request'
    }

    now = pytz.utc.localize(datetime.utcnow())
    from_date = now - timedelta(days=TOTAL_STATS_DAYS_DEFAULT)

    default_filter = {
        'status' : [FAILED_NEED_ACTION, FAILED],
        'step' : 'handler',
        'from_date' : from_date,
        'to_date' : now
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = models.Campaign.objects(id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")
            
            actions_filter = request.form.get('_actions_filter', '')
            if not actions_filter:
                actions_filter = default_filter
            else:
                actions_filter = json.loads(actions_filter)
                
            actions = scheduler_models.ActionLog.admin_get_actions(campaign_id=campaign_id,
                                                                    filter_by=actions_filter)
            actions = 
            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)