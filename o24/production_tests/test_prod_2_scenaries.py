import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel
import random
import string
from flask import url_for
import json
from pprint import pprint
from bson.objectid import ObjectId
from datetime import datetime
import pytz
from o24.globals import *

from o24.production_tests.test_data import *
from o24.backend.utils.decors import get_token
import string
import random

TEST_USER_EMAIL = '1@email.com'

def random_num(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def post_with_token(user, client, url, data):
    token = get_token(user)
    headers = {
        'Authorization': 'Bearer {0}'.format(token)
    }
    print("Sending request to url:{0}".format(url))
    pprint(data)
    
    r = None
    if data:        
        r = client.post(url, data=data, content_type='multipart/form-data', headers=headers, follow_redirects=False)
    else:
        r = client.post(url, content_type='multipart/form-data', headers=headers, follow_redirects=False)

    return r

class ProdTestScenaries(unittest.TestCase):
    def setUp(self):
        pass

    def test_0_check_linkedin_campaigns_handlers(self):
        user = User.objects(email=TEST_USER_EMAIL).first()
        linkedin_credentials = Credentials.get_credentials(user_id=user.id, medium='linkedin')

        client = app.test_client()    
        with app.test_request_context():
#CREATE parse LINKEDIN campaign
            req_dict = CAMPAIGN_LINKEDIN_PARSING_CREATE
            req_dict['title'] = req_dict['title'].format(random_num())
            req_dict['list_title'] = req_dict['list_title'].format(random_num())
            
            credentials_dict = json.loads(linkedin_credentials.to_json())
            req_dict['credentials'].append(credentials_dict)

            json_create_data = json.dumps(req_dict)
            form_data = {
                '_add_campaign' : json_create_data
            }
            
            url = url_for('dashboard.create_linkedin_parsing_campaign')
            r = post_with_token(user=user, client=client, url=url, data=form_data)

            response_data = json.loads(r.data)
            code = response_data['code']
            msg = response_data['msg']
            error_message = "msg: {0}".format(msg)
            self.assertTrue(code == 1, error_message)

        #check campaign type
            added = json.loads(response_data['added'])
            pprint(added)

            message = "Created wrong campaigntype {0}".format(added['campaign_type'])
            self.assertTrue(added['campaign_type'] == LINKEDIN_PARSING_CAMPAIGN_TYPE, message)
            
        #check funnel
            message = "Created wrong funnel type {0}".format(added['funnel']['funnel_type'])
            self.assertTrue(added['funnel']['funnel_type'] == LINKEDIN_PARSING_FUNNEL_TYPE, message)

            LINKEDIN_PARSE_CAMPAIGN_ID = added['_id']['$oid']

            #LINKEDIN_ENRICHMENT_FUNNEL_TYPE = 2
            #LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE = 2

#EDIT parse LINKEDIN campaign
        #get first
            form_data = {
                '_campaign_id' : LINKEDIN_PARSE_CAMPAIGN_ID
            }
            url = url_for('dashboard.get_linkedin_campaign_by_id')
            r = post_with_token(user=user, client=client, url=url, data=form_data)

            response_data = json.loads(r.data)
            code = response_data['code']
            msg = response_data['msg']
            error_message = "msg: {0}".format(msg)
            self.assertTrue(code == 1, error_message)

        #check campaign id
            get_campaign = json.loads(response_data['campaign'])
            pprint(get_campaign)
            modified_fields = json.loads(response_data['modified_fields'])
            self.assertTrue(modified_fields, "get_linkedin_campaign_by_id returned empty modified fields")

            
            message = "Get wrong campaign id {0}".format(get_campaign['_id']['$oid'])
            self.assertTrue(get_campaign['_id']['$oid'] == LINKEDIN_PARSE_CAMPAIGN_ID, message)
            

        #then edit
            req_dict = CAMPAIGN_LINKEDIN_EDIT
            req_dict['title'] = req_dict['title'].format(random_num())
            req_dict['data']['search_url'] = req_dict['data']['search_url'].format(random_num())
            
            json_create_data = json.dumps(req_dict)
            form_data = {
                '_campaign_id' : get_campaign['_id']['$oid'],
                '_add_campaign' : json_create_data,
                '_modified_fields' : json.dumps(modified_fields)
            }
            
            url = url_for('dashboard.edit_linkedin_campaign')
            r = post_with_token(user=user, client=client, url=url, data=form_data)

            response_data = json.loads(r.data)
            code = response_data['code']
            msg = response_data['msg']
            error_message = "msg: {0}".format(msg)
            self.assertTrue(code == 1, error_message)

            updated_campaign = json.loads(response_data['updated'])
            pprint(updated_campaign)
            self.assertTrue(updated_campaign['_id']['$oid'] == get_campaign['_id']['$oid'], "Updated campaign ID not equal get campaign ID")
            #compare fields
            for k,v in CAMPAIGN_LINKEDIN_EDIT.items():
                if k == 'data':
                    u_data = updated_campaign['data']
                    for k1, v1 in v.items():
                        u_v1 = u_data[k1]
                        error = "Error update DATA need:{0}  has:{1}".format(v1, u_v1)
                        self.assertTrue(v1 == u_v1, error)
                else:
                    if k == 'from_hour' or k == 'to_hour':
                        v = int(v.split(':')[0])

                    u_v = updated_campaign[k]
                    error = "Error update key:{0} need:{1}  has:{2}".format(k, v, u_v)
                    self.assertTrue(v == u_v, error)

#CREATE enrichment LINKEDIN campaign
        #get data first        
            url = url_for('dashboard.data_linkedin_campaign')
            r = post_with_token(user=user, client=client, url=url, data=None)

            response_data = json.loads(r.data)
            pprint(response_data)
            code = response_data['code']
            msg = response_data['msg']
            error_message = "msg: {0}".format(msg)
            self.assertTrue(code == 1, error_message)

            credentials = []
            lists = []
            try:
                credentials = json.loads(response_data['credentials'])
            except Exception as e:
                error = "BROKEN TEST DATA: There is no credentials for this user, excepton: {0}".format(str(e))
                self.assertTrue(False, error)

            try:
                lists = json.loads(response_data['lists'])
            except Exception as e:
                error = "BROKEN TEST DATA: There is no prospects lists with assign_to=None for this user, excepton: {0}".format(str(e))
                self.assertTrue(False, error)

            linkedin_credentials = None
            for cr in credentials:
                if cr.get('medium', '') == 'linkedin':
                    linkedin_credentials =cr
                    break

            if linkedin_credentials is None:
                self.assertTrue(False, "BROKEN TEST DATA: There is no linkedin credentials for this user")

            list_selected = lists[0]
        
        #now create
            req_dict = CAMPAIGN_LINKEDIN_ENRICHMENT_CREATE
            req_dict['title'] = req_dict['title'].format(random_num())
            req_dict['list_selected'] = list_selected
            req_dict['credentials'].append(linkedin_credentials)

            json_create_data = json.dumps(req_dict)
            form_data = {
                '_add_campaign' : json_create_data,
            }
            
            url = url_for('dashboard.create_linkedin_enrichment_campaign')
            r = post_with_token(user=user, client=client, url=url, data=form_data)

            response_data = json.loads(r.data)
            code = response_data['code']
            msg = response_data['msg']
            error_message = "msg: {0}".format(msg)
            self.assertTrue(code == 1, error_message)

        #check campaign type
            added = json.loads(response_data['added'])
            pprint(added)
            message = "Created wrong campaigntype {0}".format(added['campaign_type'])
            self.assertTrue(added['campaign_type'] == LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE, message)
            
        #check funnel
            message = "Created wrong funnel type {0}".format(added['funnel']['funnel_type'])
            self.assertTrue(added['funnel']['funnel_type'] == LINKEDIN_ENRICHMENT_FUNNEL_TYPE, message)

            LINKEDIN_ENRICH_CAMPAIGN_ID = added['_id']['$oid']

 #LIST LINKEDIN campaigns
            url = url_for('dashboard.list_linkedin_campaigns')
            r = post_with_token(user=user, client=client, url=url, data=None)

            response_data = json.loads(r.data)
            pprint(response_data)
            code = response_data['code']
            msg = response_data['msg']
            error_message = "msg: {0}".format(msg)
            self.assertTrue(code == 1, error_message)

        #check that campaigns are not GENERAL type
            campaigns = json.loads(response_data['campaigns'])
            for campaign in campaigns:
                if campaign['campaign_type'] == OUTREACH_CAMPAIGN_TYPE:
                    error = "ERROR list_linkedin_campaigns response: MUST show only Linkedin campaigns, but have OUTREACH campaign.id={0} campaign.title={1}".format(campaign.id, campaign.title)
                    self.assertTrue(False, message)
   

        #START
        #PAUSE
        #DELETE
    def test_1_check_campaigns_handlers(self):
        user = User.objects(email=TEST_USER_EMAIL).first()

        client = app.test_client()    
        with app.test_request_context():
 #LIST OUTREACH campaigns
            url = url_for('dashboard.list_campaigns')
            r = post_with_token(user=user, client=client, url=url, data=None)

            response_data = json.loads(r.data)
            pprint(response_data)
            code = response_data['code']
            msg = response_data['msg']
            error_message = "msg: {0}".format(msg)
            self.assertTrue(code == 1, error_message)

        #check that campaigns are GENERAL type ONLY
            campaigns = json.loads(response_data['campaigns'])
            for campaign in campaigns:
                if campaign['campaign_type'] != OUTREACH_CAMPAIGN_TYPE:
                    error = "ERROR list_campaigns response: MUST show only OUTREACH_CAMPAIGN_TYPE campaigns, but have LINKEDIN campaign.id={0} campaign.title={1}".format(campaign.id, campaign.title)
                    self.assertTrue(False, message)


def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

    #drop_database()
    #create_models()

if __name__ == '__main__':
    unittest.main()
        

