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
from o24.backend.models.shared import TaskQueue, TaskQueueLock, Funnel, Action
from pymongo.errors import DuplicateKeyError
from mongoengine.errors import NotUniqueError

class TestLock(unittest.TestCase):
    def setUp(self):
        pass

    def test_lock(self):
        try:
            locked = TaskQueueLock.objects(key='scheduler_lock', ack=0).update_one(upsert=True, ack=1)
            print(locked)
            if not locked:
                return None
        except Exception as e:
            print(type(e))
            if type(e) == NotUniqueError:
                print("Attempt to lock")

    def test_unlock(self):
        TaskQueueLock.objects(key='scheduler_lock').update_one(upsert=False, ack=0)


def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()