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
import json
from pprint import pprint
from o24.backend.utils.helpers import to_json_deep_dereference

class TestReferenceField(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_reference(self):
        lst = ProspectsList.objects().first()

        prospect = Prospects.objects().first()

        prospect.assign_to_list = lst.id
        prospect._commit()

        print(prospect.id)
        print(prospect.assign_to_list)

        for key, val in prospect._fields.items():
            print("{0} {1}".format(key,type(val)))
            if key == 'assign_to_list':
                print(prospect[key] == None)

        lst.delete()
        prospect.reload()

        print(prospect.assign_to_list)
        for key, val in prospect._fields.items():
            print("{0} {1}".format(key,type(val)))
            if key == 'assign_to_list':
                print(prospect[key] == None)

    


def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()