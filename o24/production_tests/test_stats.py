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
import time

from o24.backend.google.models import GoogleAppSetting

from o24.production_tests.test_data import *
from o24.production_tests.campaigns_api import *

from o24.production_tests.utils import *
from o24.backend.utils.templates import *
from o24.backend.utils.decors import get_token
from o24.backend.scheduler.models import TaskLog

CAMPAIGN_TITLE = "Stats campaign title XX - {0}"

C_ID = '5edb71fc3bd934fb23ec3df'
P_ID = '5edd92fc3bd934fb23ec3df'

P_ID2 = '5edd99fc3bd934fb23ec3df'

ACTIONS = {
    'email_sent' : 1,
    'email_open' : 2,
    'email_bounced': 3,
    'email_replied': 4,

    'ln_visit' : 5,
    'ln_messages_sent': 6,
    'ln_messages_failed': 7,
    'ln_connect_accepted': 8,
    'ln_connect_sent': 9,
    'ln_replied': 10
}

class StatsTest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects(email=TEST_USER_EMAIL).first()

    def test_create_random_stats_data(self):
        TaskLog.objects().delete()

        for i in range(5):
            campaign_id = C_ID + str(i)
            prospect_id = P_ID + str(i)

            new_log = TaskLog(**ACTIONS)
            new_log.campaign_id = campaign_id
            new_log.prospect_id = prospect_id

            new_log._commit()

        for i in range(5):
            campaign_id = C_ID + str(i)
            prospect_id = P_ID2 + str(i)

            new_log = TaskLog(**ACTIONS)
            new_log.campaign_id = campaign_id
            new_log.prospect_id = prospect_id

            new_log._commit()


    def test_list_stats(self):
        res = TaskLog.list_stats()
        pprint(res)

    def test_campaign_stats(self):
        pass

def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

