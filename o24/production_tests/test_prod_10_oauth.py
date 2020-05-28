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
from selenium import webdriver
import urllib

from o24.backend.google.models import GoogleAppSetting

from o24.production_tests.test_data import *
from o24.production_tests.utils import *
from o24.backend.utils.templates import *
from o24.backend.utils.decors import get_token
import o24.backend.scheduler.scheduler as scheduler
import o24.backend.handlers.email as gmail_handlers
import re


class OauthTest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects(email=TEST_USER_EMAIL).first()
            
    def test_0_ack(self):
        try:
            task = TaskQueue.lock(task_id="5eccfa492e7ba73109dd9a5a")
            if not task:
                print("Return here")
                return 

            print("Found task: {0}".format(task))

        except Exception as e:
            print(str(e))
        finally:
            task = TaskQueue.unlock(task_id="5eccfa492e7ba73109dd9a5a", result_data={}, status=1)
            #print("Free task: {0}".format(task))


def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()