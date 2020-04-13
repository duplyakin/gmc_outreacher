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

def GenerateOAuth2String(username, access_token, base64_encode=True):
    """Generates an IMAP OAuth2 authentication string.
    See https://developers.google.com/google-apps/gmail/oauth2_overview
    Args:
    username: the username (email address) of the account to authenticate
    access_token: An OAuth2 access token.
    base64_encode: Whether to base64-encode the output.
    Returns:
    The SASL argument for the OAuth2 mechanism.
    """
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if base64_encode:
        auth_string = base64.b64encode(auth_string)
    return auth_string


class TestGmailSend(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_1_send_GSUITE_email(self):
        return
        email = USER_EMAIL

        user = User.get_user(email=email)
        self.assertTrue(user, "user not found email:{0}".format(email))

        credentials = Credentials.get_credentials(user_id=user.id, medium='email')
        self.assertTrue(credentials, "credentials not found email:{0}".format(email))

        data = credentials.get_data()
        access_credentials = data.get('credentials')
        self.assertTrue(access_credentials, "access_credentials not found gmail:{0}".format(data.get('email', None)))

        access_token = access_credentials.get('token')

        gsuite = data.get('email')
        self.assertTrue(gsuite == EMAIL_FROM, "wrong from emails data gsuite:{0}  EMAIL_FROM:{1}".format(gsuite, EMAIL_FROM))

        mailbox = MailBox()
        mailbox.save()

        gmail_controller = GmailController(mailbox=mailbox,
                                           credentials=access_credentials)
        
        image_data = {}                           
        fp = open(IMAGE_PATH, 'rb')
        raw = fp.read()
        fp.close()

        image_data = {
            'path' : IMAGE_PATH,
            'raw' : raw,
            'title' : 'image_insert1',
            'cid' : uuid.uuid4()
        }
        
        msg_id= '171646a693777b08'
        msgId = gmail_controller.get_msgId_for_followup(msg_id=msg_id)
        print("Received msgId:{0}".format(msgId))
        thread_id= '171645c9f9d69d72'

        subject = 'Re:Test email - 345 for howtotoken.com'
        message_data = gmail_controller.create_multipart_message(email_from=gsuite, 
                                                                email_to=EMAIL_TO, 
                                                                subject=subject, 
                                                                html_version=EMAIL_TEXT_2_HTML, 
                                                                plain_version=EMAIL_TEXT_1_PLAIN, 
                                                                image_data=image_data,
                                                                msgId=msgId,
                                                                thread_id=thread_id)

        res = gmail_controller.send_email(message=message_data)
        print(res)

    def test_2_send_SMTP_email(self):
        email = USER_EMAIL

        user = User.get_user(email=email)
        self.assertTrue(user, "user not found email:{0}".format(email))

        credentials = Credentials.get_credentials(user_id=user.id, medium='email')
        self.assertTrue(credentials, "credentials not found email:{0}".format(email))

        data = credentials.get_data()
        access_credentials = data.get('credentials')
        access_token = access_credentials.get('token')

        gmail = data.get('email')
        self.assertTrue(access_credentials, "access_credentials not found gmail:{0}".format(data.get('email', None)))
        self.assertTrue(gmail, "email from data empty:{0}".format(gmail))

        user_email = 'ks.shilov@gmail.com'
        auth_string = GenerateOAuth2String(user_email, access_token, base64_encode=False)

        print
        smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_conn.set_debuglevel(True)
        smtp_conn.ehlo('test')
        smtp_conn.starttls()

        q = base64.b64encode(str.encode(auth_string))
        smtp_conn.docmd('AUTH', 'XOAUTH2 ' + q.decode())
        
        header = 'To:ks.shilov@howtotoken.com\n' + 'From: ks.shilov@gmail.com\n' + 'Subject:testing \n'
        msg = header + '\n this is test msg from me \n\n'
        smtp_conn.sendmail('ks.shilov@gmail.com', ['ks.shilov@howtotoken.com', 'ks.shilov@gmail.com','ks.shilov@outreacher24.com'], msg)

        print(smtp_conn.data)
        #gmail_controller = GmailController(mailbox=mailbox,
        #                                   credentials=access_credentials)
                                    
        #subject = 'Hello Kirill'
        #body = 'Follow up 1'
        
        #message_data = gmail_controller.create_message(email_from='ks.shilov@howtotoken.com', 
        #                                email_to=EMAIL_TO, 
        #                                subject=subject, 
        #                                body=body)
        #print(message_data)
        #res = gmail_controller.send_email(message=message_data)
        #print(res)

    def test_3_send_YAG_email(self):
        return
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

        subject = "1111 Invite to Hacker Noon roundup - for howtotoken.com"
        email_to = 'ksshilov@yandex.ru'

        gmail_controller = GmailController(email=gmail,
                                            credentials=access_credentials,
                                            smtp=True)

        message = gmail_controller.create_multipart_message( 
                                            email_from=gmail,
                                            email_to=email_to,
                                            subject=subject,
                                            plain_version=EMAIL_TEXT_1_PLAIN,
                                            html_version=EMAIL_TEXT_1_HTML)

        self.assertTrue(message, "Empty message:{0}".format(message))

        res = gmail_controller.send_message(email_to=email_to,
                                            message=message)

        print(res)

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()