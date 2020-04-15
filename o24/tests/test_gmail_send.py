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

def is_ascii(s):            
    return all(ord(c) < 128 for c in s)

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
    
    def test_3_GMAIL_GSUITE_EMAIL(self):
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

        subject = "GSUITE-8 тест привет Invite to roundup - for howtotoken.com"
        email_to = 'ksshilov@yandex.ru'

        gmail_controller = GmailController(email=gmail,
                                            credentials=access_credentials)

        message, trail = gmail_controller.create_multipart_message( 
                                            email_from=gmail,
                                            email_to=email_to,
                                            subject=subject,
                                            plain_version=EMAIL_TEXT_1_PLAIN,
                                            html_version=EMAIL_TEXT_1_HTML)
        
        raw_message = gmail_controller.add_gmail_api_meta(message=message)
        self.assertTrue(raw_message, "gmail_controller.add_gmail_api_meta empty:{0}".format(raw_message))

        api_res = gmail_controller.send_message(email_to=email_to, 
                                                message=raw_message)
        
        self.assertTrue(api_res, "gmail_controller.send_message error:{0}".format(api_res))

        mailbox_id = None
        prospect_id = Prospects.objects().first().id
        campaign_id = Campaign.objects().first().id

        data = gmail_controller.construct_data(
                        message=message, 
                        prospect_id=prospect_id, 
                        campaign_id=campaign_id, 
                        msgId='',
                        plain_text=EMAIL_TEXT_1_PLAIN,
                        html_text=EMAIL_TEXT_1_HTML,
                        trail = trail, 
                        api_res = api_res)

        mailbox = MailBox.add_message(data)
        self.assertTrue(mailbox, "Error: can't create mailbox:{0}".format(mailbox))

        mailbox_id = mailbox.id
        
        msg_id = mailbox.get_api_msg_id()
        self.assertTrue(msg_id, "Error: get_api_msg_id msg_id:{0}".format(msg_id))

        msgId = gmail_controller.get_msgId(msg_id=msg_id)
        self.assertTrue(msgId, "Error: gmail_controller.get_msgId:{0}".format(msgId))

        mailbox.set_msgId(msgId=msgId)

        time.sleep(4)
        # Send 3 follow ups to the previous one

        for followup in EMAIL_FOLLOWUPS:
            message, trail = gmail_controller.create_multipart_message( 
                                            email_from=gmail,
                                            email_to=email_to,
                                            subject=subject,
                                            plain_version=EMAIL_TEXT_1_PLAIN,
                                            html_version=followup,
                                            parent_mailbox=mailbox)

            self.assertTrue(message, "Can't construct followup message error:{0}".format(message))
            
            raw_message = gmail_controller.add_gmail_api_meta(message=message,
                                                            parent_mailbox=mailbox)
            self.assertTrue(raw_message, "gmail_controller.add_gmail_api_meta empty:{0}".format(raw_message))

            api_res = gmail_controller.send_message(email_to=email_to, 
                                                    message=raw_message)
            
            self.assertTrue(api_res, "gmail_controller.send_message error:{0}".format(api_res))

            data = gmail_controller.construct_data(
                            message=message, 
                            prospect_id=prospect_id, 
                            campaign_id=campaign_id, 
                            msgId='',
                            plain_text=EMAIL_TEXT_1_PLAIN,
                            html_text=followup,
                            trail = trail, 
                            api_res = api_res,
                            mailbox_reply_to_id=mailbox.id)

            mailbox = MailBox.add_message(data, message_type=2)

            msg_id = mailbox.get_api_msg_id()
            self.assertTrue(msg_id, "Error: get_api_msg_id msg_id:{0}".format(msg_id))

            msgId = gmail_controller.get_msgId(msg_id=msg_id)
            self.assertTrue(msgId, "Error: gmail_controller.get_msgId:{0}".format(msgId))

            mailbox.set_msgId(msgId=msgId)

            time.sleep(4)


    def test_2_send_SMTP_email(self):
        return
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

    def test_3_GMAIL_SMTP_EMAIL_WORKS(self):
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

        subject = "ХАХА-3 с blockquote Кирилл апрель Invite to roundup - for howtotoken.com"
        email_to = 'ksshilov@yandex.ru'

        gmail_controller = GmailController(email=gmail,
                                            credentials=access_credentials,
                                            smtp=True)

        message, trail = gmail_controller.create_multipart_message( 
                                            email_from=gmail,
                                            email_to=email_to,
                                            subject=subject,
                                            plain_version=EMAIL_TEXT_1_PLAIN,
                                            html_version=EMAIL_TEXT_1_HTML)
        
        msgId, message = gmail_controller.add_header_msgId(message)
        self.assertTrue(msgId, "msgId generation error:{0}".format(msgId))

        res = gmail_controller.send_message(email_to=email_to,
                                            message=message)
        
        self.assertTrue(not res, "gmail_controller.send_message error:{0}".format(res))

        mailbox_id = None
        prospect_id = Prospects.objects().first().id
        campaign_id = Campaign.objects().first().id

        data = gmail_controller.construct_data(
                        message, 
                        prospect_id, 
                        campaign_id, 
                        msgId,
                        plain_text=EMAIL_TEXT_1_PLAIN,
                        html_text=EMAIL_TEXT_1_HTML,
                        trail=trail)

        mailbox = MailBox.add_message(data)
        self.assertTrue(mailbox, "Error: can't create mailbox:{0}".format(mailbox))

        mailbox_id = mailbox.id
        
        time.sleep(10)
        # Send 3 follow ups to the previous one

        for followup in EMAIL_FOLLOWUPS:
            message, trail = gmail_controller.create_multipart_message( 
                                                        email_from=gmail,
                                                        email_to=email_to,
                                                        subject=subject,
                                                        plain_version=EMAIL_TEXT_1_PLAIN,
                                                        html_version=followup,
                                                        parent_mailbox=mailbox)

            self.assertTrue(message, "Can't construct followup message error:{0}".format(message))
            
            msgId, message = gmail_controller.add_header_msgId(message)
            self.assertTrue(msgId, "msgId generation error:{0}".format(msgId))

            res = gmail_controller.send_message(email_to=email_to,
                                                message=message)
            
            self.assertTrue(not res, "gmail_controller.send_message error:{0}".format(res))
            data = gmail_controller.construct_data(
                        message, 
                        prospect_id, 
                        campaign_id, 
                        msgId,
                        plain_text=EMAIL_TEXT_1_PLAIN,
                        html_text=followup,
                        trail=trail,
                        mailbox_reply_to_id=mailbox.id)

            mailbox = MailBox.add_message(data, message_type=2)

            get_last = MailBox.get_parent(prospect_id=prospect_id, campaign_id=campaign_id)
            
            #self.assertTrue(mailbox.id == get_last.id, "MailBox.get_parent error:{0}".format(get_last))

            time.sleep(10)

    def test_4_trail_construction(self):
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

        subject = "999 Invite to Hacker Noon roundup - for howtotoken.com"
        email_to = 'ksshilov@yandex.ru'

        gmail_controller = GmailController(email=gmail,
                                            credentials=access_credentials,
                                            smtp=True)

        message, trail = gmail_controller.create_multipart_message( 
                                            email_from=gmail,
                                            email_to=email_to,
                                            subject=subject,
                                            plain_version=EMAIL_TEXT_1_PLAIN,
                                            html_version=EMAIL_TEXT_1_HTML)
        
        msgId, message = gmail_controller.add_header_msgId(message)
        self.assertTrue(msgId, "msgId generation error:{0}".format(msgId))

        prospect_id = Prospects.objects().first().id
        campaign_id = Campaign.objects().first().id

        data = gmail_controller.construct_data(
                        message, 
                        prospect_id, 
                        campaign_id, 
                        msgId,
                        plain_text=EMAIL_TEXT_1_PLAIN,
                        html_text=EMAIL_TEXT_1_HTML,
                        trail=trail)

        mailbox = MailBox.add_message(data)
        self.assertTrue(mailbox, "Error: can't create mailbox:{0}".format(mailbox))
        print("******** Created mailbox.id:{0}".format(mailbox.id))
        
        print("####################### Message Intro:")
        print(message.as_string())

        mailbox_id = mailbox.id
        for followup in EMAIL_FOLLOWUPS:
            message, trail = gmail_controller.create_multipart_message( 
                                                        email_from=gmail,
                                                        email_to=email_to,
                                                        subject=subject,
                                                        plain_version=EMAIL_TEXT_1_PLAIN,
                                                        html_version=followup,
                                                        parent_mailbox=mailbox)

            self.assertTrue(message, "Can't construct followup message error:{0}".format(message))
            
            msgId, message = gmail_controller.add_header_msgId(message)
            self.assertTrue(msgId, "msgId generation error:{0}".format(msgId))

            data = gmail_controller.construct_data(
                        message, 
                        prospect_id, 
                        campaign_id, 
                        msgId,
                        plain_text=EMAIL_TEXT_1_PLAIN,
                        html_text=followup,
                        trail=trail,
                        mailbox_reply_to_id=mailbox.id)

            mailbox = MailBox.add_message(data, message_type=2)

            print("####################### Message Followup:")
            print(message.as_string())


       

    def test_5_send_unicode_data(self): 
        return
        #GET DATA for constructor
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

        subject = "000 Invite to Hacker Noon roundup - for howtotoken.com"
        email_to = 'ks.shilov@howtotoken.com'

        gmail_controller = GmailController(email=gmail,
                                            credentials=access_credentials,
                                            smtp=True)

        mailbox = MailBox.objects(email_data__msgId='<158688645769.12500.11841317466977919490@outreacher24.com>').first()

        trail = gmail_controller._construct_trail(mailbox)

        text = mailbox.get_text()
        html = trail

        message = gmail_controller.create_multipart_message( 
                                            email_from='ks.shilov@gmail.com',
                                            email_to='ks.shilov@howtotoken.com',
                                            subject='Encoding test',
                                            plain_version=text,
                                            html_version=html)
        
        msgId, message = gmail_controller.add_header_msgId(message)
        self.assertTrue(msgId, "msgId generation error:{0}".format(msgId))

        print("************************** GOING TO SEND*************")
        print(message)

        res = gmail_controller.send_message(email_to=email_to,
                                            message=message)
        
        print("************************** RESULT *************")
        print(res)
    

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()