import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
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
from flask import jsonify
import json
from o24.backend.google.provider.gmail_smtp_provider import GmailSmtpProvider

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user


class TestMongoJson(unittest.TestCase):
    def test_1_doc_to_json(self):
        current_user = get_current_user()

        lists = ProspectsList.objects(owner=current_user.id).all()
        l1 = lists.to_json()

        js = json.loads(l1)
        for j in js:
            q = ProspectsList(**j)
            print(q)
        #campaigns = Campaign.list_campaigns(owner=current_user.id)
        #if campaigns:
        #    result['campaigns'] = jsonify(campaigns)

        #prospects = Prospects.list_prospects(owner=current_user.id,
        #                                list_filter=list_filter,
        #                                page=page)
        

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()