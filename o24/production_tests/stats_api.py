import os
import o24.config as config
import random
import string
import json
from pprint import pprint
from bson.objectid import ObjectId
from datetime import datetime
import pytz
from o24.globals import *
from flask import url_for
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList

from o24.production_tests.test_data import *
from o24.production_tests.utils import *
from o24.backend.models.inbox.mailbox import MailBox

import o24.backend.google.provider.gmail_api_provider as gmail_api_provider
import o24.backend.google.provider.gmail_smtp_provider as gmail_smtp_provider
import o24.backend.google.provider.oauth_provider as oauth_provider
import o24.backend.gmail.controller as gmail_controller


def api_get_stats_total(user, client):
#get first
    url = url_for('dashboard.statistics_total')
    r = post_with_token(user=user, client=client, url=url, data=None)

    response_data = json.loads(r.data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

    return response_data

def api_get_stats_campaign(user, client, campaign_id, from_date, to_date):

    form_data = {
        '_campaign_id' : campaign_id,
        '_from_date' : from_date,
        '_to_date' : to_date
    }
    
    url = url_for('dashboard.statistics_campaign')
    r = post_with_token(user=user, client=client, url=url, data=form_data)

    response_data = json.loads(r.data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message
    
    return response_data