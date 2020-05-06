import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel

from o24.backend.google.models import GoogleAppSetting
from o24.production_tests.test_data import *
from o24.production_tests.create_data import *


class TestUsersCampaignsProspects(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_create_models(self):
        print("*** test_1_create_models")
        users = USERS
        for user in users:
            new_user = User.create_user(user)
            self.assertEqual(new_user.email, user.get('email'), "Can't create user")

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


        users = USERS
        for user in users:
            db_user = User.get_user(user.get('email'))
            self.assertEqual(db_user.email, user.get('email'), "Wrong user email")
            
            credentials = user.get('credentials')
            for next_cred in credentials:
                owner = db_user

                new_credentials = Credentials.create_credentials(owner=owner, data=next_cred)
                self.assertTrue(new_credentials is not None, "new_credentials is None")

        actions = ACTIONS
        for action in actions:
            new_action = Action.create_action(action)
            self.assertEqual(new_action.key, action.get('key'), "Can't create action")

        funnels = FUNNELS
        for funnel in funnels:
            success = construct_funnel(funnel)
            self.assertTrue(success, "construct_funnel failed")

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
            data['data'] = {
                'funnel_title': funnel.title,
                'prospects_list' : '',
                'account' : ''
            }

            new_campaign = Campaign.create_campaign(data, owner=db_user.id)
            self.assertTrue(new_campaign is not None, "can't create campaign")

        lists = LISTS
        for lst in lists:
            owner = User.get_user(lst.get('owner'))
            self.assertTrue(owner is not None, "No such user")

            new_list = ProspectsList.create_list(owner_id=owner.id,
                                                    title=lst.get('title'))
            self.assertTrue(new_list is not None, "Can't create new_list")

        
        prospects = PROSPECTS
        for prospect in prospects:
            owner = User.get_user(prospect.get('owner'))
            self.assertTrue(owner is not None, "No such user")

            campaign = Campaign.get_campaign(title=prospect.get('assign_to'))
            self.assertTrue(campaign is not None, "No such campaign title: {0}".format(prospect.get('assign_to')))

            amount = prospect.get('amount')
            email_name = prospect.get('email_name')
            email_domain = prospect.get('email_domain')
            email = email_name + email_domain
            
            l = prospect.get('assign_to_list', '')
            prospects_list = ProspectsList.objects(owner=owner.id, title=l).first()


            list_id = None
            if prospects_list:
                list_id = prospects_list.id
            count = 1
            for i in range(amount):
                linkedin = 'http://linkedin.com/u'+ email_name + str(count)
                data = {
                    'email' : email,
                    'linkedin' : linkedin
                }
                
                new_prospect = Prospects.create_prospect(owner_id=owner.id,
                                                        campaign_id=campaign.id,
                                                        list_id=list_id,
                                                        data=data)
                self.assertTrue(new_prospect is not None, "Can't create prospect")

                email = email_name + '+' + str(count) + email_domain
                count = count + 1


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
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

    drop_database()

if __name__ == '__main__':
    unittest.main()
        

