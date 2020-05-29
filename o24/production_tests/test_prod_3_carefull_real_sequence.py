import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel, TaskQueue
from o24.backend.utils.funnel import construct_funnel
import random
import string
from flask import url_for
import json
from pprint import pprint
from bson.objectid import ObjectId
import traceback

from o24.backend.google.models import GoogleAppSetting

from o24.production_tests.test_data import *
from o24.production_tests.utils import *
from o24.backend.utils.templates import *
from o24.backend.utils.decors import get_token
import o24.backend.scheduler.scheduler as scheduler
import o24.backend.handlers.email as gmail_handlers
import re

CAMPAIGN_MODIFIED_FIELDS = {
    'title' : True,
    'templates' : True,
    'time_table' : True,
    'funnel' : False,
    'credentials' : False,
    'lists' : False,
    'from_hour' : True,
    'to_hour' : True,
    'from_minutes' : True,
    'to_minutes' : True,
    'sending_days' : True,
    'time_zone' : True
}

CAMPAIGN_LINKEDIN_DATA_TEST = {
    'title' : 'test_linkedin_handler_campaign',
    'templates': {
        'linkedin': [
            {
                'title' : 'Intro linkedin message',
                'template_key' : 'intro_linkedin',
                'order' : 0,
                'message' : '''
                Hi {first_name}!

                Just wanted to follow up here and ask.

                Could you send your e_mail please?
                '''
            }
        ]
    },
    'from_hour': "00:00",
    'to_hour': "23:59",
    'time_zone': {
        'label': "(GMT+03:00) Moscow Standard Time - Moscow",
        'value' : "Europe/Moscow",
        'offset' : 180
    },
    'sending_days': {
        "0": True,
        "1": True,
        "2": True,
        "3": True,
        "4": True,
        "5": True,
        "6": True
    }
}

CAMPAIGN_DATA_TEST = {
    'title' : 'test_email_handler_campaign',
    'templates': {
        'email': [
            {
                'title' : 'Intro email',
                'template_key' : 'intro_email',
                'order' : 0,
                'subject': '❓ Question to {first_name} from {company}',
                'body' : '''
<!DOCTYPE html>
<html>
<head>
</head>
<body>
Hi {first_name}<br /><br />My name is Kirill - I'm a blockchain developer and writer. Since early 2017 I’ve worked hard to become the top blockchain contributor for Hacker Noon - you can check my signature for published topics and my Linkedin and Hacker Noon profiles.<br /><br />I'm writing a Roundup <span style="color: #e74c3c;">topic for NewsBtc</span> that I’m planning to publish in the beginning of March.<br /><br /><br /><strong>The idea:</strong><br />Make a roundup with quotes from blockchain project founders, and ask them:<br /><span style="color: #e74c3c;"><em>What will be the share (in %) of crypto payments for online services at the end of 2020? Which services will be paid with crypto the most and why? (Excluding dark-net)</em></span><br /><br /><br />It's good PR for projects and interesting to the community at large:<br />- Quote from the founder<br />- Dofollow link from NewsBtc<br />The price to be mentioned: $50 (Small managing fee: proofreading, editing, distribution)<br /><br /><br />I've done such a Roundup recently and it got a lot of hype - you could find a link in a signature.<br /><br />Is this interesting to you?<br /><br /><br />P.S.<br />If you’re not interested, just let me know.<br />For a quicker response, message me on telegram: ksshilov<br /><br />Thanks,<br />Kirill Shilov,<br /><br />Telegram: @ksshilov<br />Linkedin: https://www.linkedin.com/in/kirill-shilov-25aa8630/
</body>
</html>
'''
            }
        ]
    },
    'from_hour': "00:00",
    'to_hour': "23:59",
    'time_zone': {
        'label': "(GMT+03:00) Moscow Standard Time - Moscow",
        'value' : "Europe/Moscow",
        'offset' : 180
    },
    'sending_days': {
        "0": True,
        "1": True,
        "2": True,
        "3": True,
        "4": True,
        "5": True,
        "6": True
    }
}


CAMPAIGN_LINKEDIN_PARSING_TEST_DATA = {
    'title': 'Linkedin parse test campaign - XX-{0}',
    'list_title' : 'Linkedin parse test list title - XX-{0}',
    'data' : {
        'search_url': 'https://www.linkedin.com/search/results/people/?keywords=Head%20of%20sales%20in%20germany&origin=SWITCH_SEARCH_VERTICAL',
        'total_pages': 100,
        'interval_pages': 10,
    },
    'credentials': [],
    'from_hour': '00:00',
    'to_hour': '23:59',
    'time_zone': {
        'label': "(GMT+00:00) United Kingdom Time",
        'value': "Europe/London",
        'offset': 0
    },
    'sending_days': {
        "0": True,
        "1": True,
        "2": True,
        "3": True,
        "4": True,
        "5": True,
        "6": True
    }
}


class RealSequenceTest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects(email=TEST_USER_EMAIL).first()

    def test_0_utils(self):
        subject = 'To {first_name} from {company} - carefull {first_name}'
        body_html = '<p><strong> Hi {first_name} </strong>, I found your {company} via {url}. {first_name} please forward</p>'
        body_plain = 'Hi {first_name}, I found your {company} via {url}. {first_name} please forward'

        prospect_data = {
            'first_name' : 'Kirill',
            'last_name' : 'Shilov',
            'company' : 'Outreacher'
        }

        subject = insert_tags(subject, prospect_data)
        body_html = insert_tags(body_html, prospect_data)
        body_plain = insert_tags(body_plain, prospect_data)

        subs = [subject, body_html, body_plain]

        print(subject)
        print(body_html)
        print(body_plain)

        for s in subs:
            q = [m.start() for m in re.finditer('{|}', s)]
            if len(q) > 0:
                message = "insert_tags error: {0}".format(s)
                self.assertTrue(False, message)
    
    def test_get_gmail_token(self):
        return
        client = app.test_client()    
        with app.test_request_context():
            self._credentials_get(user=self.user, client=client)
        

    def test_1_email_handlers(self):
        #GET ID of campaign by title:
        campaign = Campaign.objects(title='test_email_handler_campaign').first()
        if not campaign:
            self.assertTrue(False, "BAD TEST DATA: there is not campaign with title: test_email_handler_campaign")

        #stop campaign
        try:
            current_user = get_current_user()
            scheduler.Scheduler.safe_pause_campaign(campaign=campaign)
        except Exception as e:
            print(e)
            traceback.print_exc()

        client = app.test_client()    
        with app.test_request_context():
            updated_campaign = self._campaigns_edit(user=self.user, 
                                                    client=client, 
                                                    campaign_id=str(campaign.id),
                                                    TEMPLATE=CAMPAIGN_DATA_TEST)

        #start campaign if not started
        try:
            current_user = get_current_user()
            scheduler.Scheduler.safe_start_campaign(owner=current_user.id, campaign=campaign)
        except Exception as e:
            print(e)
            traceback.print_exc()


        #Get the task and call handler
        task = TaskQueue.objects(campaign_id=campaign.id).first()
        if not task:
            message = "Can't find task for campaign_id={0}".format(campaign.id)
            self.assertTrue(False, message)

        gmail_handlers.email_send_message(task_id=str(task.id))



    def test_1_linkedin_handlers(self):
        #GET ID of campaign by title:
        campaign = Campaign.objects(title='test_linkedin_handler_campaign').first()
        if not campaign:
            self.assertTrue(False, "BAD TEST DATA: there is not campaign with title: test_linkedin_handler_campaign")

        #stop campaign
        try:
            current_user = get_current_user()
            scheduler.Scheduler.safe_pause_campaign(campaign=campaign)
        except Exception as e:
            print(e)
            traceback.print_exc()

        client = app.test_client()    
        with app.test_request_context():
            updated_campaign = self._campaigns_edit(user=self.user, 
                                                    client=client, 
                                                    campaign_id=str(campaign.id),
                                                    TEMPLATE=CAMPAIGN_LINKEDIN_DATA_TEST)

        #start campaign if not started
        try:
            current_user = get_current_user()
            scheduler.Scheduler.safe_start_campaign(owner=current_user.id, campaign=campaign)
        except Exception as e:
            print(e)
            traceback.print_exc()


        #SWITCH tasks until we have the right one:
        #Get the task and call handler
        tasks = TaskQueue.objects(campaign_id=campaign.id)
        if not tasks:
            message = "Can't find task for campaign_id={0}".format(campaign.id)
            self.assertTrue(False, message)
        
        test_actions = Prospects.objects(assign_to=campaign.id).distinct("data.test_action")
        if not test_actions:
            self.assertTrue("TEST DATA BROKEN: can't find distinct(data.test_action)")
        print("******** FOUND test_actions:")
        print(test_actions)
        for t_a in test_actions:
            pr = Prospects.objects(data__test_action=t_a).first()
            task = TaskQueue.objects(prospect_id=pr.id).first()
            if not task:
                message = "TEST DATA BROKEN: can't find task for test_action = {0}".format(t_a)
                self.assertTrue(False, message)

            never_found = True
            while True:
                if task.action_key == t_a:
                    task.status = IN_PROGRESS
                    task._commit()
                    
                    never_found = False
                    break
                
                current_node = task.current_node
                next_node = Funnel.next_node(current_node, {'if_true' : True})
                task.switch_task(next_node, _commit=True)
                task.reload
            
            if never_found:
                self.assertTrue(False, "BROKEN TEST DATA: can't find test_action node")

        #START SEARCH PARSING CAMPAIGN
        credentials = campaign.credentials
        linkedin_credentials = None
        for cr in credentials:
            if cr.medium == 'linkedin':
                linkedin_credentials = cr
                break
        
        if not linkedin_credentials:
            message = "Can't find linkedin credentials for campaign_id:{0}".format(campaign.id)

        current_user = get_current_user()

        client = app.test_client()    
        with app.test_request_context():
            #CREATE parse LINKEDIN campaign
            LINKEDIN_PARSE_CAMPAIGN_ID = self._create_linkedin_parsing_campaign(user=current_user, 
                                                                credentials=linkedin_credentials, 
                                                                client=client)
            if not LINKEDIN_PARSE_CAMPAIGN_ID:
                self.assertTrue(False, "Can't create _create_linkedin_parsing_campaign")

            #stop campaign
            try:
                current_user = get_current_user()
                to_pause = Campaign.objects(id=LINKEDIN_PARSE_CAMPAIGN_ID).first()
                scheduler.Scheduler.safe_pause_campaign(campaign=to_pause)
            except Exception as e:
                print(e)
                traceback.print_exc()


            #START parse LINKEDIN campaign
            self._start_linkedin_campaign(user=current_user, client=client, campaign_id=LINKEDIN_PARSE_CAMPAIGN_ID)
            task = TaskQueue.objects(campaign_id=LINKEDIN_PARSE_CAMPAIGN_ID).first()
            task.status = IN_PROGRESS
            task._commit()

    def test_2_campaign_sequence(self):
        pass

    def _credentials_get(self, user, client):
        url = url_for('dashboard.dashboard_oauth_button')
        r = post_with_token(user=user, client=client, url=url, data=None, follow_redirects=True)

        response_data = json.loads(r.data)



    def _campaigns_edit(self, user, client, campaign_id, TEMPLATE):
        modified_fields = json.dumps(CAMPAIGN_MODIFIED_FIELDS)

        _req_dict = TEMPLATE
        
        json_create_data = json.dumps(_req_dict)
        form_data = {
            '_campaign_id' : campaign_id,
            '_add_campaign' : json_create_data,
            '_modified_fields' : modified_fields
        }
        
        url = url_for('dashboard.edit_campaign')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

        updated_campaign = json.loads(response_data['updated'])
        pprint(updated_campaign)
        self.assertTrue(updated_campaign['_id']['$oid'] == campaign_id, "Updated campaign ID not equal get campaign ID")
                
        return updated_campaign



    def _create_linkedin_parsing_campaign(self, user, credentials, client, req_dict=None):
        _req_dict = None

        if req_dict:
            _req_dict = req_dict
        else:
            _req_dict = CAMPAIGN_LINKEDIN_PARSING_TEST_DATA
            _req_dict['title'] = _req_dict['title'].format(random_num())
            _req_dict['list_title'] = _req_dict['list_title'].format(random_num())
            
            credentials_dict = json.loads(credentials.to_json())
            _req_dict['credentials'].append(credentials_dict)


        json_create_data = json.dumps(_req_dict)
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

        return added['_id']['$oid']


    def _start_linkedin_campaign(self, user, client, campaign_id):
        form_data = {
            '_campaign_id' : campaign_id,
        }

        url = url_for('dashboard.start_linkedin_campaign')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        pprint(response_data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

        started = json.loads(response_data['started'])
        error = "Wrong campaign started  need id:{0}  has id:{1}".format(campaign_id, started['_id']['$oid'])
        self.assertTrue(started['_id']['$oid'] == campaign_id, error)

        error = "Campaign didn't started status={0}".format(started['status'])
        self.assertTrue(started['status'] == IN_PROGRESS, error)

        return started



def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

