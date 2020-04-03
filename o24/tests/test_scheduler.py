import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel


class TestScheduler(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_start_campaign(self):
        pass

    def test_2_pause_campaign(self):
        pass

    def test_3_resume_campaign(self):
        pass

    def test_4_add_new_prospect(self):
        pass

    def test_5_scheduler_plan(self):
        pass
    
    def test_6_scheduler_execute(self):
        pass

    def test_7_scheduler_celery_handler(self):
        pass

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()