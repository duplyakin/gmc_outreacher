from o24.backend import db
from o24.backend import app
import datetime
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

class TaskLog(db.Document):
    owner_id = db.ObjectIdField()

    prospect_id = db.ObjectIdField()
    campaign_id = db.ObjectIdField()

    campaign_title = db.StringField()

    actions = db.DictField()

    log = db.ListField(db.DictField())

    #STATS THAT WE SHOW
    email_sent = db.IntField(default=0)
    email_open = db.IntField(default=0)
    email_bounced = db.IntField(default=0)
    email_replied = db.IntField(default=0)

    ln_visit = db.IntField(default=0)
    ln_messages_sent = db.IntField(default=0)
    ln_messages_failed = db.IntField(default=0)
    ln_connect_accepted = db.IntField(default=0)
    ln_connect_sent = db.IntField(default=0)
    ln_replied = db.IntField(default=0)

    meta = {
        'indexes': [
            {
                'fields' : ('prospect_id', 'campaign_id'),
                'unique': True
            }
        ]
    }

    @classmethod
    def track_email_open(cls, prospect_id, campaign_id):
        exist = cls.objects(prospect_id=prospect_id, campaign_id=campaign_id).first()
        if not exist:
            raise Exception("TaskLog.track_email_open ERROR: no such log for prospect_id={0} campaign_id={1}".format(prospect_id, campaign_id))
        
        exist.email_open = exist.email_open + 1
        exist._commit()

    @classmethod
    #TODO: uncomment
    #def list_stats(cls, owner_id, page=1, per_page=config.STATS_PER_PAGE):
    def list_stats(cls, page=1, per_page=config.STATS_PER_PAGE):
        if page <= 1:
            page = 1
        
        #db_query = cls.objects(owner_id=owner_id)
        db_query = cls.objects()
        total = db_query.count()

        pipeline = [
            {"$group" : {
                '_id':"$campaign_id",
                "campaign_title": { "$first": "$campaign_title"},

                'prospects_contacted_total': { '$sum': 1 },
                'prospects_email_opens_total': {'$sum': '$email_open'},
                'email_bounced_total' : {'$sum' : '$email_bounced'},
                'linkedin_messages_failed_total' : {'$sum' : '$ln_messages_failed'},
                'prospects_accepted_linkedin_total' : {'$sum' : '$ln_connect_accepted'},
                'emails_sent' : {'$sum' : '$email_sent'},
                'emails_opened' : {'$sum' : '$email_open'},
                'emails_replies_total' : {'$sum' : '$email_replied'},
                'connect_request_total' : {'$sum' : '$ln_connect_sent'},
                'connect_request_approved_total' : {'$sum' : '$ln_connect_accepted'},
                'linkedin_messages_sent_total' : {'$sum' : '$ln_connect_sent'},
                'linkedin_replies_received' : {'$sum' : '$ln_replied'}
            }}
        ]

        stats = list(db_query.skip(per_page * (page-1)).limit(per_page).order_by('campaign_title').aggregate(*pipeline))

        pprint(stats)
        if stats:
            results = json.dumps(stats)

            return (total, results)
        else:
            return None, None
    
    def _log_stats(self, action_key, res):
        if action_key == LINKEDIN_VISIT_PROFILE_ACTION:
            if res:
                self.ln_visit = self.ln_visit + 1
        elif action_key == LINKEDIN_CONNECT_ACTION:
            if res:
                self.ln_connect_sent = self.ln_connect_sent + 1
        elif action_key == LINKEDIN_SEND_MESSAGE_ACTION:
            if res:
                self.ln_messages_sent = self.ln_messages_sent + 1
            else:
                self.ln_messages_failed = self.ln_messages_failed + 1
        elif action_key == LINKEDIN_CHECK_ACCEPT_ACTION:
            if res:
                self.ln_connect_accepted = self.ln_connect_accepted + 1
        elif action_key == LINKEDIN_CHECK_REPLY_ACTION:
            if res:
                self.ln_replied = self.ln_replied + 1


        elif action_key == EMAIL_SEND_MESSAGE_ACTION:
            if res:
                self.email_sent = self.email_sent + 1
        elif action_key == EMAIL_CHECK_REPLY_ACTION:
            if res:
                self.email_replied = self.email_replied + 1


    @classmethod
    def create_log(cls, task):
        exist = TaskLog.objects(prospect_id=task.prospect_id, campaign_id=task.campaign_id).first()
        if not exist:
            exist = cls()
            exist.owner_id = task.owner_id
            exist.prospect_id = task.prospect_id
            exist.campaign_id = task.campaign_id

        exist.campaign_title = task.stat_campaign_title

        action_key = task.action_key
        if action_key not in DONT_LOG:            
            res = False
            if task.result_data:
                res = task.result_data.get('if_true', False)
            
            exist.actions[action_key] = res
        
        exist.log.append(task.to_mongo())
        return exist


    @classmethod
    def update_logs(cls, logs):
        if not logs:
            return None

        for log in logs:
            log._commit()
            
        #TaskLog.objects.update(logs, multi=True)

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()