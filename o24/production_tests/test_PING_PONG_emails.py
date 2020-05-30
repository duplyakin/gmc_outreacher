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
import time

from o24.backend.google.models import GoogleAppSetting

from o24.production_tests.test_data import *
from o24.production_tests.campaigns_api import *

from o24.production_tests.utils import *
from o24.backend.utils.templates import *
from o24.backend.utils.decors import get_token
import o24.backend.scheduler.scheduler as scheduler
import o24.backend.handlers.email as gmail_handlers
import re
import o24.backend.handlers.email as gmail_handlers


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


CAMPAIGN_GSUITE_DATA = {
    'title' : 'test_gsuite_handler_campaign',
    'templates': {
        'email': [
            {
                'title' : 'Intro email',
                'template_key' : 'intro_email',
                'order' : 0,
                'subject': '❓ Question to GMAIL from gsuite - ' + str(datetime.utcnow()),
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


CAMPAIGN_GMAIL_DATA = {
    'title' : 'test_email_handler_campaign',
    'templates': {
        'email': [
            {
                'title' : 'Intro email',
                'template_key' : 'intro_email',
                'order' : 0,
                'subject': '❓ Question to GSUITE from gmail - ' + str(datetime.utcnow()),
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




class PingPongEmailsTest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects(email=TEST_USER_EMAIL).first()

    def _create_task(self):
        user = User.objects(email=TEST_USER_EMAIL).first()
        campaign = Campaign.objects(title='test_email_handler_campaign').first()
        if not campaign:
            raise Exception("BROKEN TEST data - can't find campaign.title=test_email_handler_campaign")

        client = app.test_client()    
        with app.test_request_context():
            try:                                
                api_campaigns_pause(user=user, client=client, campaign_id=str(campaign.id))
            except:
                print(".....Campaign already paused")
                pass


            api_campaigns_edit(user=user, 
                                client=client,
                                campaign_id=str(campaign.id),
                                template=CAMPAIGN_GMAIL_DATA)

            try:                                
                api_campaigns_start(user=user, client=client, campaign_id=str(campaign.id))
            except:
                print(".....Campaign already started")
                pass

        return campaign

    def _get_email_from(self, gmail):
        #if gmail true - then we are looking for *@gmail.com email, else other
        email_from = None

        credentials = Credentials.objects(test_title='test_email_handlers').first()
        email_from = credentials.data.get('email')

        if not gmail:
            credentials = Credentials.objects(test_title='test_gsuite_handlers').first()
            email_from = credentials.data.get('email')

        if not email_from:
            raise Exception("BROKEN TEST DATA: can't find email_from")

        return email_from

    def _find_gsuite_thread_id(self, task, email_from):
        #answer from gsuite
        gsuite_credentials = Credentials.objects(test_title='test_gsuite_handlers').first()
        if not gsuite_credentials:
            raise Exception("Can't find gsuite_credentials")
            
        prospect_id = task.prospect_id
        campaign_id = task.campaign_id

        start_date = MailBox.sequence_start_date(prospect_id=prospect_id, campaign_id=campaign_id)

        res = api_find_message(email_from=email_from, credentials_id=gsuite_credentials.id, after=start_date)
        if not res:
            raise Exception("Can't find thread_id")
        
        thread_id = None
        for r in res:
            thread_id = r.get('threadId', None)
            if thread_id:
                break

        if not thread_id:
            message = "Can't find thread_id seems broken res:{0}".format(res)
            raise Exception(message)

        return thread_id
        

    def test_gmail_to_gsuite(self):

        campaign = self._create_task()

        #Call handler to send emails:
        task = TaskQueue.objects(campaign_id=campaign.id).first()
        if not task:
            raise Exception("BROKEN DATA: can't find task for campaign id")
        
        #send 2 emails
        for i in range(2):
            gmail_handlers.email_send_message(str(task.id))
            print("sent {0} email to gsuite".format(i))
            time.sleep(5)
        
        #answer from gsuite
        gsuite_credentials = Credentials.objects(test_title='test_gsuite_handlers').first()
        if not gsuite_credentials:
            raise Exception("Can't find gsuite_credentials")
        
        sent_from = self._get_email_from(gmail=True)
        
        #FIND THREAD_ID
        thread_id = self._find_gsuite_thread_id(task=task, email_from=sent_from)

        api_reply_to(task=task, 
                thread_id=thread_id,
                subject="",
                message_text="It's just a reply for test",
                email_to=sent_from,
                credentials_id=gsuite_credentials.id, 
                smtp=False)

        time.sleep(5)

        #send 3rd email - should check reply
        result_data = gmail_handlers.email_send_message(str(task.id))
        print("sent 3rd email to gsuite result_data={0}".format(result_data))
        if_true = result_data.get('if_true', None)
        assert if_true == True, "CHECK REPLY not detected"

        return

    def test_gsuite_to_gmail(self):
        pass

    def test_check_reply(self):
        campaign = self._create_task()

        #answer from gsuite
        gsuite_credentials = Credentials.objects(test_title='test_gsuite_handlers').first()
        if not gsuite_credentials:
            raise Exception("Can't find gsuite_credentials")
        
        task = TaskQueue.objects(campaign_id=campaign.id).first()
        if not task:
            raise Exception("BROKEN DATA: can't find task for campaign id")
    
        prospect_id = task.prospect_id
        campaign_id = task.campaign_id

        start_date = MailBox.sequence_start_date(prospect_id=prospect_id, campaign_id=campaign_id)
        print(".......POSIX start_date={0}".format(start_date))

        res = api_find_message(email_from='ks.shilov@gmail.com', credentials_id=gsuite_credentials.id, after=start_date)
        print(res)

def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

