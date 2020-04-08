USERS = [
    {'email' : '1@email.com',
     'password' : 'password1',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail1-token'},
         'medium' : 'email'
         },
        {
         'data' : { 'oauth-token' : 'gsuite1-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin1-email', 'password' : 'linkedin1-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]
    },
    {'email' : '2@email.com',
     'password' : 'password2',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail2-token'},
         'medium' : 'email'
         },
        {
         'data' : { 'oauth-token' : 'gsuite2-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin2-email', 'password' : 'linkedin2-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]
    },
    {'email' : '3@email.com',
     'password' : 'password3',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail3-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin3-email', 'password' : 'linkedin3-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]

    },
    {'email' : '4@email.com',
     'password' : 'password4',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail4-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin4-email', 'password' : 'linkedin4-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    
    {'email' : '5@email.com',
     'password' : 'password5',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail5-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin5-email', 'password' : 'linkedin5-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    {'email' : '6@email.com',
     'password' : 'password6',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail6-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin6-email', 'password' : 'linkedin6-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '7@email.com',
     'password' : 'password7',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail7-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin7-email', 'password' : 'linkedin7-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '8@email.com',
     'password' : 'password8',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail8-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin8-email', 'password' : 'linkedin8-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    {'email' : '9@email.com',
     'password' : 'password9',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail9-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin9-email', 'password' : 'linkedin9-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '10@email.com',
     'password' : 'password10',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'oauth-token' : 'gmail10-token'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin10-email', 'password' : 'linkedin10-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'special-medium' : 'special-medium'},
         'medium' : 'special-medium'
         },         
      ]

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
            'data' : 10,
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
                    'data' : 'Hello on Linkedin',
                    'if_true' : 'wait-2',
                    'if_false' : 'wait-2'
                },

                'wait-2' : {
                    'key' : 'delay-linkedin',
                    'data' : 10,
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
            'data' : 'hello on email',
            'if_true' : 'wait-22',
            'if_false' : 'wait-22'
        },

                'wait-22' : {
                    'key' : 'delay-email',
                    'data' : 10,
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
                    'data' : 'hello on email - follow up 1',
                    'if_true' : 'wait-3',
                    'if_false' : 'wait-3'
                },

                'wait-3' : {
                    'key' : 'delay-email',
                    'data' : 10,
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
        'title' : 'campaign-2',
        'owner' : '3@email.com',
        'medium' : ['linkedin', 'email', 'special-medium']
    }   
]

PROSPECTS = [
    {
        'owner' : '1@email.com',
        'amount' : 5,
        'assign_to' : 'campaign-1'
    },
    {
        'owner' : '3@email.com',
        'amount' : 5,
        'assign_to' : 'campaign-2'
    },
]

import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel


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

            new_campaign = Campaign.create_campaign(data)
            self.assertTrue(new_campaign is not None, "can't create campaign")

    def test_7_create_prospects(self):
        prospects = PROSPECTS
        for prospect in prospects:
            owner = User.get_user(prospect.get('owner'))
            self.assertTrue(owner is not None, "No such user")

            campaign = Campaign.get_campaign(title=prospect.get('assign_to'))
            self.assertTrue(campaign is not None, "No such campaign")

            amount = prospect.get('amount')
            for p in range(amount):
                new_prospect = Prospects.create_prospect(owner_id=owner.id,
                                                        campaign_id=campaign.id)
                self.assertTrue(new_prospect is not None, "Can't create prospect")

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
        

