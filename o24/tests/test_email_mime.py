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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid

USER_EMAIL = '11@email.com'
EMAIL_FROM = 'ks.shilov@howtotoken.com'
EMAIL_TO = 'ks.shilov@gmail.com'
IMAGE_PATH = './i1.png'



class TestMimeEmail(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_1_show_mime(self):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = 'Test subject'
        msgRoot['From'] = 'ks.shilov@gmail.com'
        msgRoot['To'] = 'ks.shilov@howtotoken.com'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText('Text for plain version', 'plain', 'utf-8')
        msgAlternative.attach(msgText)


        msg_html = MIMEText(EMAIL_TEXT_1_HTML, 'html', 'utf-8')
        msgAlternative.attach(msg_html)

        msgRoot.add_header('References', '<adfadsf> <adfadfds>')
        msgRoot.add_header('In-Reply-To', '<adfadsfasdfdsfasdfsdfsdf>')

        print(type(msgRoot))
        print(dir(msgRoot))
        print(msgRoot.get(name='referencesss', failobj=''))

        print("******************************* FOR LOOP HERE *****************************************")
        
        text_plain = None
        text_html = None
        for i in msgRoot.walk():
            content_type = i.get(name='content-type')
            if 'text/plain' in content_type:
                text_plain = i.get_payload()
            elif 'text/html' in content_type:
                text_html = i.get_payload()
            
            if text_plain and text_html:
                break
        
        print(text_plain)
        print(text_html)

    

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()