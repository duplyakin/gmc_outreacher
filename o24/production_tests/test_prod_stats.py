import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend.scheduler.models import ActionLog
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
from datetime import datetime
from datetime import timedelta
import pytz

from o24.backend.google.models import GoogleAppSetting

from o24.production_tests.test_data import *
from o24.production_tests.campaigns_api import *

from o24.production_tests.utils import *
from o24.backend.utils.templates import *
from o24.backend.utils.decors import get_token

CAMPAIGN_TITLE = "Stats campaign title XX - {0}"

C_ID = '5edb71fc3bd934fb23ec3df'
P_ID = '5edd92fc3bd934fb23ec3df'

OWNER_ID = '9edd92fc3bd934fb23ec3df0'

CAMPAIGN_ID = '9adb71fc3bd934fb23ec3df0'
CAMPAIGN_TITLE = 'simple_campaign'

CAMPAIGN_ID_1 = '9adb71fc3bd934fb23ec3aa0'
CAMPAIGN_TITLE_1 = 'simple_campaign_1'
CAMPAIGN_ID_2 = '9adb71fc3bd934fb23ec3bb0'
CAMPAIGN_TITLE_2 = 'simple_campaign_2'


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

KEYS = [
    'linkedin-connect',
    'linkedin-check-accept',
    'linkedin-send-message',
    'linkedin-check-reply',
    'email-send-message',
    'email-check-reply',
    'email-send-message',
    'email-check-reply'
]

KEYS_1 = [
    'open',
    'close',
    'send',
    'reply',
    'connect'
]

KEYS_2 = [
    'open',
    'open',
    'open',
    'open',
    'open'
]


class StatsTest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects(email=TEST_USER_EMAIL).first()

    def test_show_total(self):
        ActionLog.log_open(owner_id=self.user.id, 
                            prospect_id=self.user.id, 
                            campaign_id=self.user.id)

        stats = ActionLog.get_stats_total(owner_id=self.user.id, from_date=1, to_date=2)

        pprint(stats)

    def test_show_campaign(self):
        stats = ActionLog.get_campaign_stats(owner_id=self.user.id, campaign_id=12, from_date=12, to_date=12)
        
        pprint(stats)

def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

