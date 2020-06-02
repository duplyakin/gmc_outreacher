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

from o24.backend.google.models import GoogleAppSetting

from o24.production_tests.test_data import *
from o24.production_tests.utils import *
from o24.backend.utils.templates import *
from o24.backend.utils.decors import get_token
import o24.backend.scheduler.scheduler as scheduler
import o24.backend.handlers.email as gmail_handlers
import re
import o24.backend.handlers.enricher as enrich_handler

import o24.enricher.controller as enrich_controller
import o24.enricher.models as enrich_models
import o24.enricher.providers.snovio as snovio_provider


#THIS IS THE prospect we test for:
Example = {
        'owner' : '1@email.com',
        'data' : {
            'linkedin' : 'https://www.linkedin.com/in/barry-magennis-768a0a1aa/',
            'company_url' : 'Boostlabs.com',
            'first_name' : 'Barry',
            'prospect_test' : 'enrich_test'
        },
        'assign_to_list' : 'enrich_test_list'
}


class EnricherTest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects(email=TEST_USER_EMAIL).first()

    def test_tasks_restore_progress(self):
        prospect = Prospects.objects(data__prospect_test='enrich_test').first()
        if not prospect:
            raise Exception("BROKEN TEST DATA: can't find 'prospect_test' : 'enrich_test'")

        #check Queue
        task = enrich_models.EnrichTaskQueue.objects(prospect_id=prospect.id).first()
        if not task:
            raise Exception("Task didn't created for prospect_id={0}".format(prospect.id))
        
        task.status = 1
        task._commit()
        
    def test_snovio_restart_prospect(self):
        prospect = Prospects.objects(data__prospect_test='enrich_test').first()
        if not prospect:
            raise Exception("BROKEN TEST DATA: can't find 'prospect_test' : 'enrich_test'")
        
        #ADD prospect to queue
        enrich_handler.restart_prospect_enrichment(prospect=prospect)

        #check Queue
        task = enrich_models.EnrichTaskQueue.objects(prospect_id=prospect.id).first()
        if not task:
            raise Exception("Task didn't created for prospect_id={0}".format(prospect.id))

    def test_snovio_emit_enricher(self):
        prospect = Prospects.objects(data__prospect_test='enrich_test').first()
        if not prospect:
            raise Exception("BROKEN TEST DATA: can't find 'prospect_test' : 'enrich_test'")
                
        res = enrich_handler.emit_enricher()
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
        

