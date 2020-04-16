import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects
from o24.backend.scheduler.models import Priority
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel, TaskQueue
from o24.backend.utils.funnel import construct_funnel
import o24.backend.scheduler.scheduler as SCHEDULER
from mongoengine.queryset.visitor import Q
from o24.globals import *
from o24.exceptions.exception_with_code import ErrorCodeException
from o24.exceptions.error_codes import *
import time
from celery import shared_task, group, chord
import datetime
from o24.backend.gmail.controller import GmailController
from o24.backend.models.inbox.mailbox import MailBox
import smtplib
import base64
from o24.tests.email_messages import * 
import uuid
from o24.backend.google.provider.gmail_smtp_provider import GmailSmtpProvider
from o24.backend.google.models import GoogleAppSetting
from flask_security.utils import login_user
from flask import current_app

from flask_user import login_required, current_user
from flask_login import login_user, logout_user
from flask import url_for

USERS = [
    {'email' : 'test@email.com',
     'password' : 'password',
     'active' : True,
     'credentials' : [
        {
        'data' : {'sender' : 'smtp'},
        'medium' : 'email'
        },
        {
         'data' : { 'sender' : 'api'},
         'medium' : 'email'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]
    }
]


FUNNELS = [
    {
        'root' : {
            'key' : 'email-send-message',
            'root' : True,
            'if_true' : 'wait-1',
            'if_false' : 'finished',
            'template' : INTRO_TEMPALTE
        },

        'wait-1' : {
            'key' : 'delay-email',
            'data' : { 'delay' : 10},
            'if_true' : 'send-followup-1',
            'if_false' : 'finished'
        },

        'send-followup-1' :  {
            'key' : 'email-send-message',
            'if_true' : 'wait-2',
            'if_false' : 'finished',
            'template' : FOLLOW_UP_1
        },

        'wait-2' : {
            'key' : 'delay-email',
            'data' : { 'delay' : 10},
            'if_true' : 'send-followup-2',
            'if_false' : 'finished'
        },

        'send-followup-2' :  {
            'key' : 'email-send-message',
            'if_true' : 'finished',
            'if_false' : 'finished',
            'template' : FOLLOW_UP_2
        },

        'finished' : {
            'key' : 'finished'
        },

        'success' : {
            'key' : 'success'
        }

    }
]

CAMPAIGNS = [
    {
        'title' : 'campaign-1-smtp',
        'owner' : 'test@email.com',
        'senders' : ['smtp', 'special-medium']
    },

    {
        'title' : 'campaign-2-api',
        'owner' : 'test@email.com',
        'senders' : ['api', 'special-medium']
    }   
]

CAMPAIGNS_TO_START = [
    {
        'title' : 'campaign-1-smtp'
    },
    {
        'title' : 'campaign-2-api'
    },
]


PROSPECTS = [
    {
        'owner' : 'test@email.com',
        'amount' : 3,
        'email_name' : 'ksshilov',
        'email_domain' : '@yandex.ru',
        'assign_to' : 'campaign-1-smtp'
    },
    {
        'owner' : 'test@email.com',
        'email_name' : 'ks.shilov',
        'email_domain' : '@gmail.com',
        'amount' : 3,
        'assign_to' : 'campaign-2-api'
    },
]

# 0 - Actions with limit
# 1 - Delays
# 2 - Sync Events
# 3 - Async Events
# 4 - FINISHED
# 5 - SUCCESS
ACTIONS = [
    {
        'action_type' : 0,
        'data' : {
            'what' : 'visit-profile'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-visit-profile'
    },
    {
        'action_type' : 0,
        'data' : {
            'what' : 'connect'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-connect'
    },
    {
        'action_type' : 0,
        'data' : {
            'what' : 'send-message'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-send-message'
    },
    

    {
        'action_type' : 0,
        'data' : {
            'what' : 'send-message'
        },
        'medium' : 'email',
        'key' : 'email-send-message'
    },


    {
        'action_type' : 1,
        'data' : {
            'what' : 'delay'
        },
        'medium' : 'special-medium',
        'key' : 'delay-linkedin'
    },

     {
        'action_type' : 1,
        'data' : {
            'what' : 'delay'
        },
        'medium' : 'special-medium',
        'key' : 'delay-email'
    },

    {
        'action_type' : 4,
        'data' : {
            'what' : 'FINISHED'
        },
        'medium' : 'special-medium',
        'key' : 'finished'
    },
    
    {
        'action_type' : 5,
        'data' : {
            'what' : 'SUCCESS'
        },
        'medium' : 'special-medium',
        'key' : 'success'
    },

    {
        'action_type' : 2,
        'data' : {
            'what' : 'check-accept'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-check-accept'
    },

    {
        'action_type' : 2,
        'data' : {
            'what' : 'check-reply'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-check-reply'
    },

    {
        'action_type' : 2,
        'data' : {
            'what' : 'check-reply'
        },
        'medium' : 'email',
        'key' : 'email-check-reply'
    }
]

GOOGLE_APP_SETTINGS = [{
    'title': 'Outreacher24 - web app credentials - development local',
    'credentials': {"web":{"client_id":"606646624276-qcedt5p3vdad7h6aie2l5s75mg59at7t.apps.googleusercontent.com","project_id":"outreacher24","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"Gn-M_96r8PTML9SQaLxAqqWD","redirect_uris":["http://127.0.0.1:5000/oauth/callback"],"javascript_origins":["http://127.0.0.1:5000"]}},
    'redirect_uri': 'http://127.0.0.1:5000/oauth/callback',

    'gmail_scopes': ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.metadata'],
    'gmail_access_type': 'offline',
    'gmail_include_granted_scopes': 'true',

    'gmail_api_name': 'gmail',
    'gmail_api_version': 'v1',

    'active' : True
}]



class TestGmailHandlers(unittest.TestCase):
    def test_1_drop_all_data(self):
        return
        settings = config.MONGODB_SETTINGS
        db_name = settings.get('db', None)
        assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

        with app.app_context():
            db.connection.drop_database(db_name)

        print("STEP 1: ......Data dropped success")
 
    def test_2_create_data(self):
        return
        users = USERS

        #CREATE USERS
        for user in users:
            new_user = User.create_user(user)
            self.assertEqual(new_user.email, user.get('email'), "Can't create user")

        #CREATE CREDENTIALS
        for user in users:
            db_user = User.get_user(user.get('email'))
            self.assertEqual(db_user.email, user.get('email'), "Wrong user email")
            
            credentials = user.get('credentials')
            for next_cred in credentials:
                owner = db_user

                new_credentials = Credentials.create_credentials(owner=owner, data=next_cred)
                self.assertTrue(new_credentials is not None, "new_credentials is None")

        #CREATE ACTIONS
        actions = ACTIONS
        for action in actions:
            new_action = Action.create_action(action)
            self.assertEqual(new_action.key, action.get('key'), "Can't create action")

        #CREATE FUNNELS
        funnels = FUNNELS
        for funnel in funnels:
            success = construct_funnel(funnel)
            self.assertTrue(success, "construct_funnel failed")

        #CREATE CAMPAIGNS
        campaigns = CAMPAIGNS
        for campaign in campaigns:
            db_user = User.get_user(campaign.get('owner'))
            self.assertEqual(db_user.email, campaign.get('owner'), "Wrong user email")

            funnel = Funnel.get_random()
            self.assertTrue(funnel is not None, "can't get_random funnel")
            
            senders = campaign.get('senders')
            
            credentials = []
            for sender in senders:
                cred = Credentials.get_credentials(user_id=db_user.id,
                                                            sender=sender)
                self.assertTrue(cred is not None, "credentials is None")
                credentials.append(cred.id)
            
            data = {}
            data['funnel'] = funnel.id
            data['credentials'] = credentials
            data['title'] = campaign.get('title','')

            new_campaign = Campaign.create_campaign(data)
            self.assertTrue(new_campaign is not None, "can't create campaign")

        #CREATE PROSPECTS
        prospects = PROSPECTS
        for prospect in prospects:
            owner = User.get_user(prospect.get('owner'))
            self.assertTrue(owner is not None, "No such user")

            campaign = Campaign.get_campaign(title=prospect.get('assign_to'))
            self.assertTrue(campaign is not None, "No such campaign")

            amount = prospect.get('amount')
            email_name = prospect.get('email_name')
            email_domain = prospect.get('email_domain')
            email = email_name + email_domain
            
            count = 1
            for i in range(amount):
                data = {
                    'email' : email
                }
                new_prospect = Prospects.create_prospect(owner_id=owner.id,
                                                        campaign_id=campaign.id,
                                                        data=data)
                self.assertTrue(new_prospect is not None, "Can't create prospect")

                email = email_name + '+' + str(count) + email_domain
                count = count + 1
        
        
        #CREATE GOOGLE_APP_SETTINGS
        for setting in GOOGLE_APP_SETTINGS:
            s = GoogleAppSetting()

            s.title = setting.get('title')
            s.credentials = setting.get('credentials')
            s.redirect_uri = setting.get('redirect_uri')

            s.gmail_scopes = setting.get('gmail_scopes')
            s.gmail_access_type = setting.get('gmail_access_type')
            s.gmail_include_granted_scopes = setting.get('gmail_include_granted_scopes')

            s.gmail_api_name = setting.get('gmail_api_name')
            s.gmail_api_version = setting.get('gmail_api_version')

            s.active = setting.get('active')

            s.save()

        print("STEP 2: ......Testing data created success")

    def test_3_get_google_credentials(self):

        user = USERS[0]
        email = user.get('email')
        password = user.get('password')

        db_user =  User.get_user(email)
        self.assertTrue(db_user, "User doesn't exist:{0}".format(email))
    
        client = app.test_client()    
        with app.test_request_context():
            is_loged = login_user(db_user, remember=True)
            self.assertTrue(is_loged, "Can't login user:{0}".format(email))

            #LOGING VIA form
            login_url = url_for('user.login')
            response = client.post(login_url, data={'email' : email, 'password' : password}, follow_redirects=False)
            
            url = url_for('dashboard.dashboard_main')
            r = client.get(url, follow_redirects=False)
            self.assertTrue(r.data == b'Hello world', "Login Error")

            

        print("STEP 3: ......Google Credentials received success")


    def test_4_start_campaigns(self):
        return
        campaigns_to_start = CAMPAIGNS_TO_START

        campaigns = []
        for c in campaigns_to_start:
            title = c.get('title')

            campaign = Campaign.get_campaign(title=title)
            self.assertTrue(campaign is not None, "There is no such campaign title:{0}".format(title))
            campaigns.append(campaign)
        
        scheduler = SCHEDULER.Scheduler()

        # campaign changed status to IN_PROGRESS
        # prospects changed status to IN_PROGRESS
        # all prospects changed status
        # All ids appeared in TaskQueue with status NEW
        for campaign in campaigns:
            prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
            ids_before = [prospect.id for prospect in prospects]
            count_before = len(prospects)
            self.assertTrue(count_before > 0, "There is no prospects for campaign_title:{0} count_before={1}".format(campaign.title, count_before))

            scheduler.start_campaign(campaign)

            prospects = Prospects.get_prospects(status=IN_PROGRESS, campaign_id=campaign.id)
            count_after = len(prospects)
            ids_after = [prospect.id for prospect in prospects]

            self.assertTrue(set(ids_before) == set(ids_after), "not all prospects updates campaign_title:{0} count_before={1} count_after={2}".format(campaign.title, count_before, count_after))

            campaign.reload()
            self.assertTrue(campaign.status == IN_PROGRESS, "campaing status change error campaign_title:{0}".format(campaign.title))
            
            ids_in_queue = TaskQueue.objects(Q(status=NEW) & Q(prospect_id__in=ids_after)).distinct('prospect_id')
            count_queue = len(ids_in_queue)
            self.assertTrue(set(ids_in_queue) == set(ids_before), "not all prospects appeared in TaskQueue campaign_title:{0} count_before={1} count_queue={2}".format(campaign.title, count_before, count_queue))

        print("STEP 4: ......Campaigns started success")



def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()