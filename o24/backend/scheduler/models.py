from o24.backend import db
from o24.backend import app
from datetime import datetime
from datetime import timedelta
import pytz
import uuid
from mongoengine.queryset.visitor import Q
import json
import traceback
import o24.backend.dashboard.models as models
from bson.json_util import dumps as bson_dumps
from pprint import pprint
from pymongo.errors import DuplicateKeyError
from o24.backend.models.shared import TaskQueue
import o24.config as config
from o24.globals import *

class Priority(db.Document):
    #campaign = db.ReferenceField(Campaign, unique=True)

    # 0 - Intro, 1 - Follow up
    do_next = db.IntField(default=0)

    #0 - Init phase, 1 - While all 1 are empty
    followup_level = db.IntField(default=0)

    @classmethod
    def get_priority(cls):
        exist = Priority.objects().first()
        if exist:
            return exist

        new_priority = cls()

        new_priority._commit()
        return new_priority

    def update_priority(self, do_next, followup_level):
        self.do_next = do_next
        self.followup_level = followup_level
        self._commit()

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()

class ActionLog(db.Document):
    owner_id = db.ObjectIdField()
    task_id = db.ObjectIdField()
    
    status = db.IntField()
    description = db.StringField()
    step = db.StringField()

    prospect_id = db.ObjectIdField()
    campaign_id = db.ObjectIdField()

    action_key = db.StringField()
    input_data = db.DictField()
    result_data = db.DictField()

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )

    @classmethod
    def log(cls, task, step, description):
        now = pytz.utc.localize(datetime.utcnow())
        new_log = cls(
            owner_id = task.owner_id,
            task_id = task.id,
            status = task.status,
            step=step,
            description = description,
            prospect_id = task.prospect_id,
            campaign_id = task.campaign_id,
            action_key = task.action_key,
            input_data = task.input_data,
            result_data = task.result_data,
            created = now
        )

        new_log._commit()
    
    def _commit(self):
        self.save()