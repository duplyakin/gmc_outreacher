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

from o24.backend.google.models import GoogleAppSetting

from o24.production_tests.test_data import *
from o24.production_tests.campaigns_api import *

from o24.production_tests.utils import *
from o24.backend.utils.templates import *
from o24.backend.utils.decors import get_token
import o24.backend.scheduler.scheduler as scheduler
import o24.backend.handlers.email as gmail_handlers
import re
import o24.backend.handlers.email as gmail_handlers

from o24.backend.handlers.email_senders.utils import *
from o24.globals import *
import traceback
import time
from o24.exceptions.exception_with_code import ErrorCodeException
from o24.backend.gmail.controller import GmailController
from o24.backend.models.inbox.mailbox import MailBox
import o24.backend.handlers.email_senders.gmail_api as gmail_api




SUBJECT = '❓ Question to GMAIL from gsuite'
BODY_HTML = '''
<!DOCTYPE html>
<html>
<head>
</head>
<body>
Hi {first_name}<br /><br />My name is Kirill - I'm a blockchain developer and writer. Since early 2017 I’ve worked hard to become the top blockchain contributor for Hacker Noon - you can check my signature for published topics and my Linkedin and Hacker Noon profiles.<br /><br />I'm writing a Roundup <span style="color: #e74c3c;">topic for NewsBtc</span> that I’m planning to publish in the beginning of March.<br /><br /><br /><strong>The idea:</strong><br />Make a roundup with quotes from blockchain project founders, and ask them:<br /><span style="color: #e74c3c;"><em>What will be the share (in %) of crypto payments for online services at the end of 2020? Which services will be paid with crypto the most and why? (Excluding dark-net)</em></span><br /><br /><br />It's good PR for projects and interesting to the community at large:<br />- Quote from the founder<br />- Dofollow link from NewsBtc<br />The price to be mentioned: $50 (Small managing fee: proofreading, editing, distribution)<br /><br /><br />I've done such a Roundup recently and it got a lot of hype - you could find a link in a signature.<br /><br />Is this interesting to you?<br /><br /><br />P.S.<br />If you’re not interested, just let me know.<br />For a quicker response, message me on telegram: ksshilov<br /><br />Thanks,<br />Kirill Shilov,<br /><br />Telegram: @ksshilov<br />Linkedin: https://www.linkedin.com/in/kirill-shilov-25aa8630/
</body>
</html>
'''
BODY_PLAIN = 'Hello world from plain'


def send_email_from_smtp(email_from, email_to):
    access_credentials = Credentials.objects(modification='smtp', data__email=email_from).first()
    if not access_credentials:
        raise Exception("Can't find credentials for modification=smtp email_from={0}".format(email_from))

    access_credentials_data = access_credentials.data.get('credentials')

    gmail_controller = GmailController(email=email_from,
                                        credentials=access_credentials_data,
                                        credentials_id=access_credentials.id,
                                        smtp=True)

    random_prospect = Prospects.objects().first()
    random_campaign = Campaign.objects().first()

    mailbox = MailBox.create_draft(prospect_id=random_prospect.id, campaign_id=random_campaign.id)
    
    owner_id = mailbox.get_owner_id()

    subject = SUBJECT
    body_html = BODY_HTML
    body_plain = BODY_PLAIN

    message, trail = gmail_controller.create_multipart_message( 
                                                email_from=email_from,
                                                email_to=email_to,
                                                subject=subject,
                                                plain_version=body_plain,
                                                html_version=body_html,
                                                parent_mailbox=mailbox)

    
    msgId, message = gmail_controller.add_header_msgId(message)

    res = gmail_controller.send_message(email_to=email_to,
                                        message=message)
    
    print(res)

    return 


send_email_from_smtp(email_from='ks.shilov@gmail.com', email_to='k@howtotoken.com')