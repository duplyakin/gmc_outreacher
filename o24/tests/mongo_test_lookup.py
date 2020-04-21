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
import datetime
from datetime import timedelta

CAMPAIGNS = [
    {
        'title' : 'IN_PROGRESS-1',
        'owner' : '1@email.com',
        'credentials' : ['IN_PROGRESS-1-LIMITED', 'IN_PROGRESS-1-OK'],
        'next_action' : True
    },

    {
        'title' : 'IN_PROGRESS-2',
        'owner' : '3@email.com',
        'credentials' : ['IN_PROGRESS-2-OK', 'IN_PROGRESS-2-LIMITED'],
        'next_action' : True
    },

    {
        'title' : 'PAUSED',
        'owner' : '4@email.com',
        'credentials' : ['PAUSED-1-OK', 'PAUSED-2-LIMITED'],
        'next_action' : True
    }
]

TASKS = [
    {
        'campaign_id' : 'IN_PROGRESS-1',
        'credentials_id' : 'IN_PROGRESS-1-LIMITED',
        'prospect_id' : 1,

        'status' : NEW,
        'record_type' : INTRO,
        'followup_level' : INTRO,
    },
    {
        'campaign_id' : 'IN_PROGRESS-1',
        'credentials_id' : 'IN_PROGRESS-1-OK',
        'prospect_id' : 2,

        'status' : NEW,
        'record_type' : FOLLOWUP,
        'followup_level' : 0,
       
    },
    {
        'campaign_id' : 'IN_PROGRESS-1',
        'credentials_id' : 'IN_PROGRESS-1-OK',
        'prospect_id' : 3,

        'status' : NEW,
        'record_type' : FOLLOWUP,
        'followup_level' : 1,
    },



    {
        'campaign_id' : 'IN_PROGRESS-2',
        'credentials_id' : 'IN_PROGRESS-1-LIMITED',
        'prospect_id' : 4,

        'status' : NEW,
        'record_type' : INTRO,
        'followup_level' : 0,
    },
    {
        'campaign_id' : 'IN_PROGRESS-2',
        'credentials_id' : 'IN_PROGRESS-1-LIMITED',
        'prospect_id' : 5,

        'status' : NEW,
        'record_type' : INTRO,
        'followup_level' : 0,
    },
    {
        'campaign_id' : 'IN_PROGRESS-2',
        'credentials_id' : 'IN_PROGRESS-2-OK',
        'prospect_id' : 6,

        'status' : NEW,
        'record_type' : INTRO,
        'followup_level' : 0,
    },



    {
        'campaign_id' : 'PAUSED',
        'credentials_id' : 'PAUSED-1-OK',
        'prospect_id' : 7,

        'status' : NEW,
        'record_type' : INTRO,
        'followup_level' : 0,
    },
    {
        'campaign_id' : 'PAUSED',
        'credentials_id' : 'PAUSED-1-OK',
        'prospect_id' : 8,

        'status' : NEW,
        'record_type' : INTRO,
        'followup_level' : 0,
    },
    {
        'campaign_id' : 'PAUSED',
        'credentials_id' : 'PAUSED-2-LIMITED',
        'prospect_id' : 9,

        'status' : NEW,
        'record_type' : INTRO,
        'followup_level' : 0,
    },
]

TITLES = ['IN_PROGRESS-1', 'IN_PROGRESS-2', 'PAUSED']

class TestLookupQuery(unittest.TestCase):
    def test_1_create_fake_data(self):
        return
        fake_campaigns = CAMPAIGNS
        
        propspects = []
        for c in fake_campaigns:
            user = User.get_user(c.get('owner'))
            self.assertTrue(user, "user")
            
            credentials = c.get('credentials')
            
            credentials_lst = []
            for cr in credentials:
                data = {
                    'medium' : cr,
                    'data' : {}
                }
                new_cr = Credentials.create_credentials(owner=user, data=data)
                if 'LIMITED' in cr:
                    new_cr.next_action = datetime.datetime.now() + timedelta(days=1)
                    new_cr.save()
                self.assertTrue(new_cr, "credentials")
                credentials_lst.append(new_cr.id)

            funnel = Funnel.objects().first()
            data = {
                'title': c.get('title'),
                'credentials' : credentials_lst,
                'funnel' : funnel.id
            }
            new_campaign = Campaign.create_campaign(data)
            self.assertTrue(new_campaign, "campaign")
            if 'PAUSED' in c.get('title'):
                new_campaign.status = PAUSED
                new_campaign.save()
            elif 'PROGRESS' in c.get('title'):
                new_campaign.status = IN_PROGRESS
                new_campaign.save()

            if c.get('next_action') == False:
                new_campaign.next_action =  datetime.datetime.now() + timedelta(days=1)
                new_campaign.save()
            
            for i in range(5):
                new_prospect = Prospects.create_prospect(owner_id=user.id, campaign_id=new_campaign.id)
                self.assertTrue(new_prospect, "new_prospect")
                propspects.append(new_prospect.id)

        fake_tasks = TASKS
        p_nin = []
        for task in fake_tasks:
            campaign = Campaign.get_campaign(title=task.get('campaign_id'))
            self.assertTrue(campaign, "campaign not found")

            credentials = Credentials.objects(medium=task.get('credentials_id')).first()
            self.assertTrue(credentials, "credentials not found, medium:{0}".format(task.get('credentials_id')))

            next_prospect = Prospects.objects(Q(id__in=propspects) & Q(assign_to=campaign.id)).filter(Q(id__nin=p_nin)).first()
            self.assertTrue(next_prospect, "next_prospect not found")

            p_nin.append(next_prospect.id)
            test_crededentials_dict = {
                'credentials_dict' : {},
                'credentials_id' : credentials.id,
                'action_key' : task.get('credentials_id')
            }

            new_task = TaskQueue.create_task(campaign, next_prospect, test_crededentials_dict)
            new_task.save()
            self.assertTrue(new_task, "can't create new_task")
            
            saved_task = TaskQueue.objects(id=new_task.id).first()
            self.assertTrue(saved_task, "saved_task not found")

            saved_task.status = task.get('status')
            saved_task.record_type = task.get('record_type')
            saved_task.followup_level = task.get('followup_level')
            saved_task.save()




    def test_2_lookup_3_tables(self):
        do_next = 1
        followup_level = 1
        
        now = datetime.datetime.now()
        print ("***** now:{0}".format(now))

        query = {"$match": {"record_type" : {"$eq" : INTRO} }}
        if (do_next == 1):
            query = {"$match" : {"record_type" : {"$eq" : FOLLOWUP}, "followup_level" : {"$eq" : followup_level}}}
        
        credentials_ids_in_progress = TaskQueue.objects(status=IN_PROGRESS).distinct('credentials_id')

        #r_obj = Credentials.objects(id='5e8b3533836677a843ae0712').first()
        #credentials_ids_in_progress.append(r_obj.id)

        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "campaign_id",
                "foreignField" : "_id",
                "as" : "campaign_docs"
            }},
            { "$unwind" : "$campaign_docs" },
            {"$match" : { "campaign_docs.title" : { "$in" : TITLES}, 
                "campaign_docs.status" : {"$eq" : IN_PROGRESS}, 
                'campaign_docs.next_action' : {'$lte' : now}
            }},
            {"$lookup" : {
                "from" : "credentials",
                "localField" : "credentials_id",
                "foreignField" : "_id",
                "as" : "cr_docs"
            }},
            { "$unwind" : "$cr_docs" },
            {"$match" : { "cr_docs.next_action" : { "$lte" : now},
                "cr_docs._id" : { "$nin" : credentials_ids_in_progress}
             } },
             query,
            {"$group" : {"_id": "$credentials_id", "task_id" : { "$first" : "$_id" }}},
        ]
        

        tasks = list(TaskQueue.objects().aggregate(*pipeline))
        tasks_ids = [x.get('task_id') for x in tasks]

        final_tasks = TaskQueue.objects(Q(id__in=tasks_ids)).all()
        print("****** {0}".format(len(tasks)))
        pprint(tasks)
        print(tasks_ids)
        print(final_tasks)

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()