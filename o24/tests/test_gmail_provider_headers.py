import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects
from o24.backend.scheduler.models import Priority
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel, TaskQueue
from o24.backend.utils.funnel import construct_funnel
import o24.backend.scheduler.scheduler as SCHEDULER
from mongoengine.queryset.visitor import Q
from o24.globals import *
from o24.exceptions.exception_with_code import ErrorCodeException
from o24.exceptions.error_codes import *
import time
from celery import shared_task, group, chord
import datetime
from o24.backend.gmail.controller import GmailController
from o24.backend.models.inbox.mailbox import MailBox
import smtplib
import base64
from o24.tests.email_messages import * 
import uuid
from o24.backend.google.provider.gmail_smtp_provider import GmailSmtpProvider

USER_EMAIL = '11@email.com'
EMAIL_FROM = 'ks.shilov@howtotoken.com'
EMAIL_TO = 'ks.shilov@gmail.com'
IMAGE_PATH = './i1.png'

class TestGmailProvider(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_1_MSGID(self):
        email = USER_EMAIL

        user = User.get_user(email=email)
        self.assertTrue(user, "user not found email:{0}".format(email))

        credentials = Credentials.get_credentials(user_id=user.id, medium='email')
        self.assertTrue(credentials, "credentials not found email:{0}".format(email))

        data = credentials.get_data()
        access_credentials = data.get('credentials')

        gmail = data.get('email')
        self.assertTrue(access_credentials, "access_credentials not found gmail:{0}".format(data.get('email', None)))
        self.assertTrue(gmail, "email from data empty:{0}".format(gmail))

        subject = "GSUITE-4 тест привет Invite to roundup - for howtotoken.com"
        email_to = 'ks.shilov@gmail.com'

        gmail_controller = GmailController(email=gmail,
                                            credentials=access_credentials)

        msg_id='1717e1e8c71b60ca'
        msgId = gmail_controller.get_msgId(msg_id=msg_id)

        print(msgId)
        return


    

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()