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
    r = client.post(url, data=data, content_type='multipart/form-data', headers=headers, follow_redirects=False)
    
    return r

class ProdTestScenaries(unittest.TestCase):
    def setUp(self):
        pass

    def test_0_check_linkedin_campaigns_handlers(self):
        user = User.objects(email=TEST_USER_EMAIL).first()
        linkedin_credentials = Credentials.get_credentials(user_id=user.id, medium='linkedin')

        #CREATE parse LINKEDIN campaign
        req_dict = CAMPAIGN_LINKEDIN_PARSING_CREATE
        req_dict['title'] = req_dict['title'].format(random_num())
        req_dict['list_title'] = req_dict['list_title'].format(random_num())
        
        credentials_dict = json.loads(linkedin_credentials.to_json())
        req_dict['credentials'].append(credentials_dict)

        client = app.test_client()    
        with app.test_request_context():
            json_create_data = json.dumps(req_dict)
            form_data = {
                '_add_campaign' : json_create_data
            }
            
            url = url_for('dashboard.create_linkedin_parsing_campaign')
            r = post_with_token(user=user, client=client, url=url, data=form_data)

            response_data = json.loads(r.data)
            code = response_data['code']
            msg = response_data['msg']
            self.assertTrue(code == 0, msg)

            added = response_data['added']
            self.assertTrue(added['campaign_type'] == 1, "Created wrong campaigntype {0}".format(added['campaign_type']))

        #EDIT parse LINKEDIN campaign

        #CREATE enrichment LINKEDIN campaign

        #EDIT enrichment LINKEDIN campaign

        #GET data 
        #GET list

        #START
        #PAUSE
        #DELETE

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
        

