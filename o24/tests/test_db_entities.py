USERS = [
    {'email' : '1@email.com',
     'password' : 'password1',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp', 'account' : 'ks.shilov@gmail.com'},
         'medium' : 'email'
         },
        {
         'data' : { 'sender' : 'api', 'account' : 'ks.shilov@howtotoken.com'},
         'medium' : 'email'
         },
         {
         'data' : { 'sender' : 'linkedin', 'account' : 'linkedin.com/ksshilov', 'password' : 'linkedin1-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]
    },
    {'email' : '2@email.com',
     'password' : 'password2',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
        {
         'data' : { 'sender' : 'api'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin2-email', 'password' : 'linkedin2-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]
    },
    {'email' : '3@email.com',
     'password' : 'password3',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin3-email', 'password' : 'linkedin3-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]

    },
    {'email' : '4@email.com',
     'password' : 'password4',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin4-email', 'password' : 'linkedin4-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    
    {'email' : '5@email.com',
     'password' : 'password5',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin5-email', 'password' : 'linkedin5-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    {'email' : '6@email.com',
     'password' : 'password6',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin6-email', 'password' : 'linkedin6-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '7@email.com',
     'password' : 'password7',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin7-email', 'password' : 'linkedin7-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '8@email.com',
     'password' : 'password8',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin8-email', 'password' : 'linkedin8-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    {'email' : '9@email.com',
     'password' : 'password9',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin9-email', 'password' : 'linkedin9-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '10@email.com',
     'password' : 'password10',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin10-email', 'password' : 'linkedin10-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },         
      ]

    },
    {
        'email' : '11@email.com',
        'password' : 'password11',
        'active' : True,
        'credentials' : []
    }
]

TEAMS = [
    {
        'admin' : '3@email.com',
        'title' : 'team1-3@email.com',
        'members' : ['4@email.com', '5@email.com', '6@email.com']
    },
    {
        'admin' : '7@email.com',
        'title' : 'team2-7@email.com',
        'members' : ['8@email.com', '9@email.com', '10@email.com']
    }
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

FUNNELS = [
    {
        'root' : {
            'key' : 'linkedin-connect',
            'root' : True,
            'if_true' : 'wait-1',
            'if_false' : 'wait-1',
        },

        'wait-1' : {
            'key' : 'delay-linkedin',
            'data' : { 'delay' : 10},
            'if_true' : 'check-connect-1',
            'if_false' : 'check-connect-1'
        },

        'check-connect-1' : {
            'key' : 'linkedin-check-accept',
            'if_true' : 'connect-approve-1',
            'if_false' : 'connect-deny-1'
        },

                'connect-approve-1' : {
                    'key' : 'linkedin-send-message',
                    'if_true' : 'wait-2',
                    'if_false' : 'wait-2'
                },

                'wait-2' : {
                    'key' : 'delay-linkedin',
                    'data' : { 'delay' : 10},
                    'if_true': 'check-reply-1',
                    'if_false': 'check-reply-1'
                },

                'check-reply-1' : {
                    'key' : 'linkedin-check-reply',
                    'if_true' : 'success',
                    'if_false' : 'connect-deny-1'
                },

        'connect-deny-1' : {
            'key' : 'email-send-message',
            'if_true' : 'wait-22',
            'if_false' : 'wait-22'
        },

                'wait-22' : {
                    'key' : 'delay-email',
                    'data' : { 'delay' : 10},
                    'if_true' : 'check-reply-intro',
                    'if_false' : 'check-reply-intro'
                },

                'check-reply-intro' : {
                    'key' : 'email-check-reply',
                    'if_true' : 'success',
                    'if_false' : 'email-followup-1'
                },

                'email-followup-1' :  {
                    'key' : 'email-send-message',
                    'if_true' : 'wait-3',
                    'if_false' : 'wait-3'
                },

                'wait-3' : {
                    'key' : 'delay-email',
                    'data' : { 'delay' : 10},
                    'if_true' : 'check-reply-followup-1',
                    'if_false' : 'check-reply-followup-1'
                },

                    'check-reply-followup-1' : {
                        'key' : 'email-check-reply',
                        'if_true' : 'success',
                        'if_false' : 'finished'
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
        'title' : 'campaign-1',
        'owner' : '1@email.com',
        'medium' : ['linkedin', 'email', 'special-medium']
    },

    {
        'title' : 'campaign-11',
        'owner' : '1@email.com',
        'medium' : ['linkedin', 'email', 'special-medium']
    },

    {
        'title' : 'campaign-2',
        'owner' : '3@email.com',
        'medium' : ['linkedin', 'email', 'special-medium']
    }   
]

LISTS = [
    {
        'owner' : '1@email.com',
        'title' : 'List-1 1@email.com'
    },
    {
        'owner' : '1@email.com',
        'title' : 'List-2 1@email.com'
    },
    {
        'owner' : '1@email.com',
        'title' : 'List-3 1@email.com'
    },
    {
        'owner' : '3@email.com',
        'title' : 'List-1 3@email.com'
    },
    {
        'owner' : '3@email.com',
        'title' : 'List-2 3@email.com'
    },
    {
        'owner' : '3@email.com',
        'title' : 'List-3 3@email.com'
    },
]

PROSPECTS = [
    {
        'owner' : '1@email.com',
        'amount' : 10,
        'assign_to' : 'campaign-1',
        'email_name' : 'ksshilov',
        'email_domain' : '@yandex.ru',
        'lists' : ['List-1 1@email.com']
    },
    {
        'owner' : '1@email.com',
        'amount' : 10,
        'assign_to' : 'campaign-11',
        'email_name' : 'ks.shilov',
        'email_domain' : '@gmail.ru',
        'lists' : ['List-2 1@email.com', 'List-3 1@email.com']
    },
    {
        'owner' : '3@email.com',
        'amount' : 10,
        'assign_to' : 'campaign-2',
        'email_name' : 'yana.shilov',
        'email_domain' : '@gmail.ru',
        'lists' : []
    },
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

import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel

from o24.backend.google.models import GoogleAppSetting

class TestUsersCampaignsProspects(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_create_users(self):
        users = USERS
        for user in users:
            new_user = User.create_user(user)
            self.assertEqual(new_user.email, user.get('email'), "Can't create user")

    def test_2_create_teams(self):
        teams = TEAMS
        for team in teams:
            members = []
            data = {}
            admin = User.get_user(team.get('admin'))
            for email in team.get('members'):
                user = User.get_user(email)
                self.assertEqual(user.email, email, "Wrong user's email")
                members.append(user)

            data['members'] = members
            data['title'] = team.get('title', '')
            data['admin'] = admin
            new_team = Team.create_team(data)
            self.assertEqual(new_team.title, team.get('title'), "Wrong team title after team creation")


    def test_3_create_credentials(self):
        users = USERS
        for user in users:
            db_user = User.get_user(user.get('email'))
            self.assertEqual(db_user.email, user.get('email'), "Wrong user email")
            
            credentials = user.get('credentials')
            for next_cred in credentials:
                owner = db_user

                new_credentials = Credentials.create_credentials(owner=owner, data=next_cred)
                self.assertTrue(new_credentials is not None, "new_credentials is None")

    def test_4_create_actions(self):
        actions = ACTIONS
        for action in actions:
            new_action = Action.create_action(action)
            self.assertEqual(new_action.key, action.get('key'), "Can't create action")

    def test_5_create_funnels(self):
        funnels = FUNNELS
        for funnel in funnels:
            success = construct_funnel(funnel)
            self.assertTrue(success, "construct_funnel failed")

    def test_6_create_campaigns(self):
        campaigns = CAMPAIGNS
        for campaign in campaigns:
            db_user = User.get_user(campaign.get('owner'))
            self.assertEqual(db_user.email, campaign.get('owner'), "Wrong user email")

            funnel = Funnel.get_random()
            self.assertTrue(funnel is not None, "can't get_random funnel")
            
            mediums = campaign.get('medium')
            credentials = []
            for medium in mediums:
                cred = Credentials.get_credentials(user_id=db_user.id,
                                                            medium=medium)
                self.assertTrue(cred is not None, "credentials is None")
                credentials.append(cred.id)
            
            data = {}
            data['funnel'] = funnel.id
            data['credentials'] = credentials
            data['title'] = campaign.get('title','')

            new_campaign = Campaign.create_campaign(data, owner=db_user.id)
            self.assertTrue(new_campaign is not None, "can't create campaign")

    def test_7_create_lists(self):
        lists = LISTS
        for lst in lists:
            owner = User.get_user(lst.get('owner'))
            self.assertTrue(owner is not None, "No such user")

            new_list = ProspectsList.create_list(owner_id=owner.id,
                                                    title=lst.get('title'))
            self.assertTrue(new_list is not None, "Can't create new_list")

    def test_8_create_prospects(self):
        
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
            
            lists = []
            for l in prospect.get('lists', []):
                next_list = ProspectsList.get_lists(owner=owner.id, title=l)
                self.assertTrue(next_list, "No such next_list")
                lists.append(next_list.id)
    

            count = 1
            for i in range(amount):
                linkedin = 'http://linkedin.com/u'+ email_name + str(count)
                data = {
                    'email' : email,
                    'assign_to' : campaign.title,
                    'lists' : lists,
                    'linkedin' : linkedin
                }
                new_prospect = Prospects.create_prospect(owner_id=owner.id,
                                                        campaign_id=campaign.id,
                                                        data=data,
                                                        lists=lists)
                self.assertTrue(new_prospect is not None, "Can't create prospect")

                email = email_name + '+' + str(count) + email_domain
                count = count + 1

    def test_9_create_google_app_settings(self):

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



def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

    with app.app_context():
        db.connection.drop_database(db_name)

if __name__ == '__main__':
    unittest.main()
        

