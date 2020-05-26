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
import o24.backend.handlers.gmail as gmail_handlers
import re


class OauthTest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects(email=TEST_USER_EMAIL).first()
        
        """Setup the test driver and create test users"""
        self.driver = webdriver.Firefox()
        self.driver.get(self.get_server_url())
    
    def test_0_gmail_token(self):
        response = urllib.urlopen(self.get_server_url())
        #client = app.test_client()    
        #with app.test_request_context():
        #    self._credentials_get(user=self.user, client=client)
        

    def _credentials_get(self, user, client):
        url = url_for('dashboard.dashboard_oauth_button')
        r = post_with_token(user=user, client=client, url=url, data=None, follow_redirects=True)

        response_data = json.loads(r.data)



def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()