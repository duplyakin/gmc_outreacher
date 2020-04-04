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

class TestBulkUpdates(unittest.TestCase):
    def test_1_bulk_update(self):
        return 

        Prospects.objects().update(status=NEW)

        new = Prospects.objects(status=NEW).all()
        print("*** Before update:{0}".format(len(new)))

        ids = Prospects.objects(status=NEW).update(status=IN_PROGRESS, full_result=True)
        print(dir(ids))
        print(ids.upserted_id)
        new = Prospects.objects(status=NEW).all()
        print("*** After update:{0} ids:{1}".format(len(new), ids))

    def test_2_unique_index(self):
        return 

    def test_3_modify(self):
        return
        prospect = Prospects.objects().first()
        print("***** Before status:{0}".format(prospect.status))

        status=prospect.status + 1
        ids = [prospect.id]
        Prospects.update_prospects(ids, status=status)
        
        prospect = Prospects.objects().first()
        print("***** After status:{0}".format(prospect.status))


    def test_4_only(self):
        ids = [p.get('prospect_id') for p in TaskQueue.objects(Q(status=NEW)).only('prospect_id').all().as_pymongo()]
        print(ids)

    def test_5_taskqueue_methods(self):

        #Need to select random tasks, but the final credentials_id should be unique
        
        Campaign.objects(title="campaign-1").update(status=PAUSED)

        #1. выбрать все tasks для которых есть кампании и показать campaign.title
        #2. выбрать все tasks кампании которых активны и показать campaign.title
        #3
        tasks_q = TaskQueue.objects()
        print(tasks_q.count())
        print(tasks_q.filter(status=1).all())
        return
        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "campaign_id",
                "foreignField" : "_id",
                "as" : "campaign_docs"
            }},
            {"$match": {"campaign_docs.status" : {"$ne" : PAUSED} }},
            {"$group" : {"_id": "$credentials_id", "task_id" : { "$first" : "$_id" }}},
        ]
        

        tasks = list(TaskQueue.objects().aggregate(*pipeline))
        print(tasks)
        for task in tasks:
            o = TaskQueue.objects(id=task.get('task_id')).first()
            pprint(o.credentials_id)
        #for task in tasks:
        #    pprint(task)


def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

