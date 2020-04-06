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

        # Which tasks are ready for execution:
        # OUTPUT: list of UNIQUE(credentials_id)
        # REMOVE:
        # **** remove credentials_id tasks.status == IN_PROGRESS : DONE
        # **** remove tasks.id where campaign.status == PAUSE  (DONE)
        # ADD:
        # now >= crededentials.next_action
        # now >= campaign.next_action DONE
        # tasks.record_type == Priority.do_next DONE
        # if tasks.followup_level == 1 then check tasks.followup_level == Priority.followup_level DONE

        do_next = 0
        followup_level = 0

        query = {"$match": {"record_type" : {"$eq" : INTRO} }}
        if (do_next == 1):
            query = {"$match" : {"record_type" : {"$eq" : FOLLOWUP}, "followup_level" : {"$eq" : followup_level}}}
        
        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "campaign_id",
                "foreignField" : "_id",
                "as" : "campaign_docs"
            }},
            {"$lookup" : {
                "from" : "credentials",
                "localField" : "campaign_id",
                "foreignField" : "_id",
                "as" : "campaign_docs"
            }},


            *query,
            {"$match" : {"campaign_docs.status" : {"$eq" : IN_PROGRESS}, "campaign_docs.next_action" : {"$le": now}}},
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
        

