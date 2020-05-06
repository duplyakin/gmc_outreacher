import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel, TaskQueue
from o24.backend.utils.funnel import construct_funnel
from o24.globals import *
from mongoengine.queryset.visitor import Q
from pprint import pprint

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user


class TestFilter(unittest.TestCase):
    def test_1_bulk_update(self):
        return
        follow_ups = TaskQueue.objects(record_type=FOLLOWUP)

    def test_2_distinct(self):
        return 
        pipeline = [
            {"$group" : {
                "_id" : {
                    'email' : '$data.email',
                    'linkedin' : '$data.linkedin' 
                },
                "prospect_id" : {"$first" : { "$toString" : "$_id" }}
            }}        
        ]

        prospects = list(Prospects.objects().aggregate(*pipeline))

        duplicates = {
            'email' : [],
            'linkedin' : [],
            'ids' : []
        }

        def spl(val, dp):
            element = val.get('_id', '')
            if not element:
                return 
            
            if not val:
                return

            email = element.get('email','')
            if email:
                dp['email'].append(email)

            linkedin = element.get('linkedin', '')
            if linkedin:
                dp['linkedin'].append(linkedin)
        
            prospect_id = val.get('prospect_id', '')
            if prospect_id:
                dp['ids'].append(prospect_id)

        q = [spl(p, duplicates) for p in prospects]

        print(duplicates)
        print(prospects)

    def test_3_or_query(self):
        current_user = get_current_user()
        p = Prospects.objects(id='5eb2b667fa795f404d2b9ce0').first()

        print(p.id)

        query = {
            'owner' : current_user.id,
            '_id' : {'$ne' : p.id}
        }

        or_array = []
        or_array.append({
            'data.email' : 'helghardt@rehive.com'
        })

        query['$or'] = or_array
        prospects = Prospects.objects(__raw__=query).first()
        pprint(prospects.id)

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

