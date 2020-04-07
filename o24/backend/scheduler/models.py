from o24.backend import db
from o24.backend import app
import datetime
from flask_user import UserManager, UserMixin
import uuid
from mongoengine.queryset.visitor import Q
import json
import traceback
from o24.backend.dashboard.models import Credentials, Campaign
from pymongo.errors import DuplicateKeyError
from o24.backend.models.shared import TaskQueue


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

    def _commit(self):
        self.save()

class TaskLog(db.Document):
    prospect_id = db.ObjectIdField()
    campaign_id = db.ObjectIdField()

    log = db.ListField(db.DictField())

    meta = {
        'indexes': [
            {
                'fields' : ('prospect_id', 'campaign_id'),
                'unique': True
            }
        ]
    }

    @classmethod
    def create_log(cls, task):
        exist = TaskLog.objects(Q(prospect_id=task.prospect_id) & Q(campaign_id=task.campaign_id)).first()
        if not exist:
            exist = cls()
            exist.prospect_id = task.prospect_id
            exist.campaign_id = task.campaign_id

        exist.log.append(task.to_mongo())
        return exist


    @classmethod
    def update_logs(cls, logs):
        if not logs:
            return None

        for log in logs:
            log.save()
            
        #TaskLog.objects.update(logs, multi=True)
