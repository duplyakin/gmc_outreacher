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

from o24.backend.google.models import GoogleAppSetting
from o24.production_tests.create_data import *


CREATE_CAMPAIGN = {
    'credentials' : '',
    'funnel' : '',
    'prospects_list' : '',
    'title' : '',
    'from_hour' : '10:23',
    'to_hour' : '19:43',
    'sending_days' : {
        '0' : False,
        '1' : True,
        '2' : False,
        '3' : True,
        '4' : True,
        '5' : True,
        '6' : False
    },
    'time_zone' : 'asdfasdf',
    'templates' : {
        'email' : [],
        'linkedin' : []
    }
}


class ProdTestCampaigns(unittest.TestCase):
    def setUp(self):
        pass

    def test_0_assign_prospects(self):
        return 
        random_list = ProspectsList.objects(id='5eac99a6cb371cc2df4b9f20').first()
        random_campaign = Campaign.objects(id='5eac9d618c7bdc3f8fe96969').first()

        random_prospects = Prospects.objects().update(assign_to_list=random_list.id, assign_to=random_campaign.id)
        print(random_prospects)

    def test_1_create_campaign(self):
        return
        print("....Testing campaigns creation")
        create_data = CREATE_CAMPAIGN
        create_data['title'] = '--test title new campaign ' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))


        client = app.test_client()    
        with app.test_request_context():            
            url = url_for('dashboard.data_campaigns')
            r = client.post(url, follow_redirects=False)

            json_data = json.loads(r.data)

            #select funnel with both email and linkedin templates
            json_funnels = json.loads(json_data['funnels'])
            funnel_obj = {}
            for funnel in json_funnels:
                templates_required = funnel.get('templates_required')
                if 'email' in templates_required.keys():
                    if 'linkedin' in templates_required.keys():
                        funnel_obj = funnel
                        break
            self.assertTrue(funnel_obj, "Can't find templates_required with email and linkedin")

            #select credentials for email and linkedin medium
            json_credentials = json.loads(json_data['credentials'])
            credentials = []
            required = ['email', 'linkedin']
            for cr in json_credentials:
                if cr['medium'] in required:
                    credentials.append(cr)
                    required.remove(cr['medium'])
                    if len(required) <= 0:
                        break
            self.assertTrue(len(credentials) >= 2, "Can't find credentials for both email and linkedin")

            #select prospects_list 
            json_prospects_list = json.loads(json_data['prospects_list'])
            prospects_list = json_prospects_list[1]

            #construct templates
            email_templates = funnel_obj['templates_required']['email']
            for required in email_templates.values():
                create_data['templates']['email'].append(
                    {
                        'template_key' : required['template_key'],
                        'subject' : 'This is test subject',
                        'body' : 'This is test body'
                    }
                )
            
            linkedin_templates = funnel_obj['templates_required']['linkedin']
            for required in linkedin_templates.values():
                create_data['templates']['linkedin'].append(
                    {
                        'template_key' : required['template_key'],
                        'Message' : 'This is test linkedin message'
                    }
                )
            
            create_data['funnel'] = funnel_obj
            create_data['credentials'] = credentials
            create_data['prospects_list'] = prospects_list


            #pprint(create_data)
            json_create_data = json.dumps(create_data)
            form_data = {
                '_add_campaign' : json_create_data
            }
            
            url = url_for('dashboard.create_campaign')
            r = client.post(url, data=form_data, content_type='multipart/form-data', follow_redirects=False)
            
            json_data = json.loads(r.data)
            pprint(json_data)

    def test_2_list_campaign(self):
        return 
        print("....Testing campaigns list")
        client = app.test_client()    
        with app.test_request_context():            
            url = url_for('dashboard.list_campaigns')
            form_data = {
                '_init' : 1
            }

            r = client.post(url, data=form_data, content_type='multipart/form-data', follow_redirects=False)

            json_data = json.loads(r.data)
            pprint(json_data)


    def test_3_edit_campaign(self):
        return
        print("....Testing campaigns edit")
        cm = Campaign.objects(id='5eac98010c71c60b37fb6b88').first()

        client = app.test_client()    
        with app.test_request_context():
            #recieve campaign first:
            url = url_for('dashboard.get_campaign_by_id')
            form_data = {
                '_campaign_id' : cm.id
            }
            r = client.post(url, data=form_data, content_type='multipart/form-data', follow_redirects=False)
            
            json_data = json.loads(r.data)
            
            modified_fields = json.loads(json_data['modified_fields'])
            pprint(modified_fields)

            
            prospects_list = ProspectsList.objects(id='5eac8d7181b6dd5589c2cea8').first()
            
            edit_campaign = {
                'title' : 'Fucking new title - 3',
                'prospects_list' : prospects_list.to_json()
            }

            url = url_for('dashboard.edit_campaign')
            form_data = {
                '_campaign_id' : cm.id,
                '_modified_fields' : json_data['modified_fields'],
                '_edit_campaign_data' : json.dumps(edit_campaign)
            }

            r = client.post(url, data=form_data, content_type='multipart/form-data', follow_redirects=False)

            json_data = json.loads(r.data)
            pprint(json_data)


    def test_4_delete_campaign(self):
        return
        print("....Testing campaigns delete")
        cm = Campaign.objects().first()
        
        client = app.test_client()    
        with app.test_request_context():            
            url = url_for('dashboard.delete_campaign')
            form_data = {
                '_campaign_id' : cm.id
            }

            r = client.post(url, data=form_data, content_type='multipart/form-data', follow_redirects=False)

            json_data = json.loads(r.data)
            pprint(json_data)
        


    def test_5_start_pause_campaign(self):
        print("....Testing campaigns start and pause")
        
        cm = Campaign.objects(id="5eac9d618c7bdc3f8fe96969").first()

        client = app.test_client()    
        with app.test_request_context():            
            url = url_for('dashboard.start_campaign')
            form_data = {
                '_campaign_id' : cm.id
            }

            r = client.post(url, data=form_data, content_type='multipart/form-data', follow_redirects=False)

            json_data = json.loads(r.data)
            pprint(json_data)


            url = url_for('dashboard.pause_campaign')
            form_data = {
                '_campaign_id' : cm.id
            }

            r = client.post(url, data=form_data, content_type='multipart/form-data', follow_redirects=False)

            json_data = json.loads(r.data)
            pprint(json_data)



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
        

