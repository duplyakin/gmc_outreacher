import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel
from o24.backend.utils.filter_data import *
from o24.backend.google.models import GoogleAppSetting

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user


class TestFilterData(unittest.TestCase):
    def test_1_filter(self):
        user = get_current_user()
        self.assertTrue(user, "No such user")

        filter_data = {
          'campaign' : '',
          'list' : '',
          'column' : 'email',
          'contains': '\\.shilov\\+.*',
        }
        filter_fields = ['campaign', 'list', 'column', 'contains']     

        query = {
        }
        q = construct_prospect_filter(filter_data=filter_data, 
                                        filter_fields=filter_fields)
        query.update(q)

        print(query)
        res = Prospects.objects(__raw__=query).only('id', 'data', 'assign_to', 'status', 'lists').all()
        print(res)
        for r in res:
            print("email: {0}  linkedin: {1}".format(r.data['email'], r.data['linkedin']))

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

