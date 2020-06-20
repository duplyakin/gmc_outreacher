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
import pytz
from datetime import datetime
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
from o24.backend.models.inbox.mailbox import MailBox, BouncedMessages
import o24.backend.handlers.email_senders.gmail_api as gmail_api



def check_bounced(email_from, bounced_email):
    access_credentials = Credentials.objects(data__email=email_from).first()
    if not access_credentials:
        raise Exception("Can't find credentials for modification=smtp email_from={0}".format(email_from))

    owner_id = access_credentials.owner.id


    start_time = pytz.utc.localize(datetime(year=2020, month=3, day=17))
    start_time_posix = int(start_time.timestamp())


    bounced_exist = BouncedMessages.check_bounced(owner_id=owner_id, 
                                                email=bounced_email, 
                                                after=start_time)
    if bounced_exist:
        print("Found bounced_exist for email={0}".format(bounced_email))
        exit(0)


    access_credentials_data = access_credentials.data.get('credentials')

    gmail_controller = GmailController(email=email_from,
                                        credentials=access_credentials_data,
                                        credentials_id=access_credentials.id,
                                        smtp=True)


    bounce_daemon = BOUNCED_DAEMONS['smtp']
    messages = gmail_controller.check_reply(email_from=bounce_daemon, 
                                            after=start_time_posix)
    
    ids = [m.get('id') for m in messages]

    full_messages = []
    if ids:
        print("ids before substract={0}".format(ids))
        has_ids = BouncedMessages.has_messages(owner_id=owner_id, msg_ids=ids)
        if has_ids:
            print("Found has_messages has_ids={0}".format(has_ids))
            ids = [not_exist for not_exist in ids if not_exist not in has_ids]
            print("ids after substract={0}".format(ids))
        
        if ids:
            full_messages = gmail_controller.get_full_messages(msg_ids=ids)
    
    res = BouncedMessages.parse_messages(owner_id=owner_id,
                                        messages=full_messages, 
                                        search_email=bounced_email)
    print("....parse_messages res={0}".format(res))


check_bounced(email_from='ks.shilov@gmail.com', bounced_email='k1@howtotoken.com')