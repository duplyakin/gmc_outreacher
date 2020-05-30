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


def api_campaigns_get(user, client, campaign_id):
#get first
    form_data = {
        '_campaign_id' : campaign_id
    }
    url = url_for('dashboard.get_campaign_by_id')
    r = post_with_token(user=user, client=client, url=url, data=form_data)

    response_data = json.loads(r.data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

#check campaign id
    get_campaign = json.loads(response_data['campaign'])
    pprint(get_campaign)
    
    modified_fields = json.loads(response_data['modified_fields'])
    assert modified_fields, "returned empty modified fields"

    
    assert get_campaign['_id']['$oid'] == campaign_id, "Get wrong campaign id {0}".format(get_campaign['_id']['$oid'])

    return response_data

def api_campaigns_edit(user, client, campaign_id, template):

    response_data = api_campaigns_get(user=user, client=client, campaign_id=campaign_id)        

    modified_fields = response_data['modified_fields']
    get_campaign = json.loads(response_data['campaign'])

#then edit

    _req_dict = template
    try:
        _req_dict['title'] = _req_dict['title'].format(random_num())
    except:
        pass 

    json_create_data = json.dumps(_req_dict)
    form_data = {
        '_campaign_id' : get_campaign['_id']['$oid'],
        '_add_campaign' : json_create_data,
        '_modified_fields' : modified_fields
    }
    
    url = url_for('dashboard.edit_campaign')
    r = post_with_token(user=user, client=client, url=url, data=form_data)

    response_data = json.loads(r.data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

    updated_campaign = json.loads(response_data['updated'])
    pprint(updated_campaign)
    assert updated_campaign['_id']['$oid'] == get_campaign['_id']['$oid'], "Updated campaign ID not equal get campaign ID"
   
    #compare fields
    for k,v in _req_dict.items():
        if k == 'templates':
            continue

        if k == 'from_hour' or k == 'to_hour':
            v = int(v.split(':')[0])

        u_v = updated_campaign[k]
        error = "Error update key:{0} need:{1}  has:{2}".format(k, v, u_v)
        assert v == u_v, error
    
    return updated_campaign


def api_campaigns_delete(user, client, campaign_id):
    response_data = api_campaigns_get(user=user, client=client, campaign_id=campaign_id)

    #UNASSIGN_PROSPECTS
    get_campaign = json.loads(response_data['campaign'])
    campaign_id = get_campaign['_id']['$oid']

    db_campaign = Campaign.objects(id=campaign_id).first()
    if not db_campaign:
        message = "NEVER HAPPENED: there is no such campaign in database id:{0}".format(campaign_id)
        assert False, message
 
    #TODO - change to request
    db_prospects = Prospects.get_prospects(campaign_id=db_campaign.id)
    if db_prospects:
        #UNASSIGN BEFORE DELETE
        current_user = get_current_user()

        ids = [p.id for p in db_prospects]
        scheduler.Scheduler.safe_unassign_prospects(owner_id=current_user.id,
                                                        prospects_ids=ids)

    form_data = {
        '_campaign_id' : campaign_id,
    }

    url = url_for('dashboard.delete_campaign')
    r = post_with_token(user=user, client=client, url=url, data=form_data)

    response_data = json.loads(r.data)
    pprint(response_data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

#check deleted
    deleted = Campaign.objects(id=campaign_id).first()
    if deleted:
        error = "Campaign didn't deleted still in a database id={0}".format(deleted.id)
        False, error
    
    return True


def api_campaigns_pause(user, client, campaign_id):
    form_data = {
        '_campaign_id' : campaign_id,
    }

    url = url_for('dashboard.pause_campaign')
    r = post_with_token(user=user, client=client, url=url, data=form_data)

    response_data = json.loads(r.data)
    pprint(response_data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

    started = json.loads(response_data['campaign'])
    error = "Wrong campaign started  need id:{0}  has id:{1}".format(campaign_id, started['_id']['$oid'])
    assert started['_id']['$oid'] == campaign_id, error

    error = "Campaign didn't started status={0}".format(started['status'])
    assert started['status'] == PAUSED, error

    return started


def api_campaigns_start(user, client, campaign_id):
    form_data = {
        '_campaign_id' : campaign_id,
    }

    url = url_for('dashboard.start_campaign')
    r = post_with_token(user=user, client=client, url=url, data=form_data)

    response_data = json.loads(r.data)
    pprint(response_data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

    started = json.loads(response_data['campaign'])
    error = "Wrong campaign started  need id:{0}  has id:{1}".format(campaign_id, started['_id']['$oid'])
    assert started['_id']['$oid'] == campaign_id, error

    error = "Campaign didn't started status={0}".format(started['status'])
    assert started['status'] == IN_PROGRESS, error

    return started


def api_campaigns_list(user, client):
    url = url_for('dashboard.list_campaigns')
    r = post_with_token(user=user, client=client, url=url, data=None)

    response_data = json.loads(r.data)
    pprint(response_data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

#check that campaigns are GENERAL type ONLY
    campaigns = json.loads(response_data['campaigns'])
    for campaign in campaigns:
        if campaign['campaign_type'] != OUTREACH_CAMPAIGN_TYPE:
            error = "ERROR list_campaigns response: MUST show only OUTREACH_CAMPAIGN_TYPE campaigns, but have LINKEDIN campaign.id={0} campaign.title={1}".format(campaign.id, campaign.title)
            assert False, message

    return campaigns

def api_campaigns_data(user, client):
    #get data first        
    url = url_for('dashboard.data_campaigns')
    r = post_with_token(user=user, client=client, url=url, data=None)

    response_data = json.loads(r.data)
    pprint(response_data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

    try:
        funnels = json.loads(response_data['funnels'])
        
        #CHECK THAT FUNNELS of OUTREACH TYPE ONLY
        for funnel in funnels:
            if funnel['funnel_type'] != GENERAL_FUNNEL_TYPE:
                message = "_campaings_data ERROR: shour response only with GENERAL_FUNNEL_TYPE but has:{0}".format(funnel['funnel_type'])
                assert False, message
                break
    except Exception as e:
        message = "BAD TEST DATA _campaings_data: there are no funnels for campaigns: {0}".format(str(e))
        assert False, message


    try:
        lists = json.loads(response_data['lists'])
    except Exception as e:
        message = "BAD TEST DATA _campaings_data: there are no prospect lists for campaigns: {0}".format(str(e))
        assert False, message

    try:
        credentials = json.loads(response_data['credentials'])
    except Exception as e:
        message = "BAD TEST DATA _campaings_data: there are no credentials for campaigns: {0}".format(str(e))
        assert False, message

    try:
        modified_fields = json.loads(response_data['modified_fields'])
    except Exception as e:
        message = "BAD TEST DATA _campaings_data: there are no modified_fields for campaigns: {0}".format(str(e))
        assert False, message

    try:
        columns = json.loads(response_data['columns'])
    except Exception as e:
        message = "BAD TEST DATA _campaings_data: there are no columns for campaigns: {0}".format(str(e))
        assert False, message


    return response_data


def api_campaigns_create(user, client, template): 
    response_data = api_campaigns_data(user=user, client=client)

    funnels = json.loads(response_data['funnels'])
    #select funnels with both mediums
    with_funnel = None
    for f in funnels:
        root = f.get('root', '')
        if root:
            templates = f.get('templates_required', '')
            
            email = templates.get('email', '')
            linkedin = templates.get('linkedin', '')
            
            if email and linkedin:
                with_funnel = f
                break

    if with_funnel is None:
        assert False, "BAD TEST DATA: can't find funnel with 2 mediums"

    credentials = json.loads(response_data['credentials'])
    #select credentials for 2 mediums
    with_linkedin = None
    with_email = None
    for c in credentials:
        if c.get('medium') == 'email':
            with_email = c
        elif c.get('medium') == 'linkedin':
            with_linkedin = c


        if with_email and with_linkedin:
            break

    if with_linkedin is None or with_email is None:
        assert False, "BAD TEST DATA: can't find credentials for 2 mediums"


    _req_dict = template
    try:
        _req_dict['title'] = _req_dict['title'].format(random_num())
    except:
        pass

    _req_dict['credentials'].append(with_linkedin)
    _req_dict['credentials'].append(with_email)

    _req_dict['funnel'] = with_funnel

    lists = json.loads(response_data['lists'])

    list_selected = None
    for l in lists:
        if 'assign_to_none' in l.get('title'):
            list_selected = l
            break
    
    if not list_selected:
        assert False, "BROKEN TEST DATA: There is no lists with free prospects for this user"

    _req_dict['list_selected'] = list_selected

    json_create_data = json.dumps(_req_dict)
    form_data = {
        '_add_campaign' : json_create_data,
    }
    
    url = url_for('dashboard.create_campaign')
    r = post_with_token(user=user, client=client, url=url, data=form_data)

    response_data = json.loads(r.data)
    code = response_data['code']
    msg = response_data['msg']
    error_message = "msg: {0}".format(msg)
    assert code == 1, error_message

#check campaign type
    added = json.loads(response_data['added'])
    pprint(added)
    message = "Created wrong campaigntype {0}".format(added['campaign_type'])
    assert added['campaign_type'] == OUTREACH_CAMPAIGN_TYPE, message
    
    return added['_id']['$oid']


#reply from given credentials to thredid found in a task
def api_reply_to(task, 
                thread_id,
                subject,
                message_text,
                email_to, 
                credentials_id, 
                smtp=False):
    #first we need to find thread id
    prospect_id = task.prospect_id
    campaign_id = task.campaign_id

    credentials_from = Credentials.objects(id=credentials_id).first()
    if not credentials_from:
        raise Exception("Can't find credentials_from")

    email_from = credentials_from.data.get('email')

    if smtp:
        pass
    else:
        #construct message
        message = gmail_controller.GmailController.test_create_thread_message_body(email_from=email_from, 
                                                                                email_to=email_to, 
                                                                                subject=subject, 
                                                                                message_text=message_text, 
                                                                                thread_id=thread_id)


        provider = gmail_api_provider.GmailApiProvider(credentials='', credentials_id=credentials_id)
        return provider.send_reply_to_thread(message=message)

    return None

def api_find_message(email_from, credentials_id, after=None):

    provider = gmail_api_provider.GmailApiProvider(credentials='', credentials_id=credentials_id)
    
    return provider.check_reply(email_from=email_from, after=after)
