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
from o24.production_tests.stats_api import *

from o24.production_tests.utils import *
from o24.backend.utils.templates import *
from o24.backend.utils.decors import get_token


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

    def test_request_handlers(self):
        campaign = Campaign.objects().first()
        client = app.test_client()
        with app.test_request_context():
            try:
                res = api_get_stats_total(user=self.user, 
                                    client=client)
                print(".....Recive stats total")
                print(res)
            except Exception as e:
                print(e)

            try:
                now = pytz.utc.localize(datetime.utcnow())
                from_date = now - timedelta(days=TOTAL_STATS_DAYS_DEFAULT)
                res = api_get_stats_campaign(user=self.user, 
                                    client=client, 
                                    campaign_id=str(campaign.id),
                                    from_date=from_date,
                                    to_date=now)

                print(".....Recive campaign stats")
                print(res)
            except Exception as e:
                print(e)


        return True


def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

