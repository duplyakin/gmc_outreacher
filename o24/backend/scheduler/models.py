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

class ActionStats(db.Document):
    owner_id = db.ObjectIdField()

    prospect_id = db.ObjectIdField()
    campaign_id = db.ObjectIdField()

    campaign_title = db.StringField()

    action_key = db.StringField()
    medium = db.StringField()

    result = db.IntField()

    created = db.DateTimeField()

    @classmethod
    def log_email_open(cls, owner_id, prospect_id, campaign_id):
        medium = 'email'
        action_key = 'email-opened'

        created = pytz.utc.localize(datetime.utcnow())

        stat = cls(owner_id=owner_id,
                    campaign_id=campaign_id,
                    prospect_id=prospect_id,
                    action_key=action_key,
                    result=1,
                    created=created,
                    medium=medium)
        
        stat.save()


    @classmethod
    def log_stats(cls, owner_id, prospect_id, campaign_id, campaign_title, action_key, result, test_date=None):
        medium = 'unknown'
        if action_key in SPECIAL_ACTIONS:
            medium = 'special-medium'
        elif 'email' in action_key:
            medium = 'email'
        elif 'linkedin' in action_key:
            medium = 'linkedin'

        created = pytz.utc.localize(datetime.utcnow())
        if test_date:
            created = test_date

        stat = cls(owner_id=owner_id,
                    campaign_id=campaign_id,
                    campaign_title=campaign_title,
                    prospect_id=prospect_id,
                    action_key=action_key,
                    result=result,
                    created=created,
                    medium=medium)
        
        stat.save()

    @classmethod
    def stats_total(cls, owner_id, page=1, per_page=config.STATS_PER_PAGE):
        if page <= 1:
            page = 1
        
        db_query = cls.objects(owner_id=owner_id, result=1)
        total = db_query.count()

        pipeline = [
            {"$group" : {
                '_id': { "campaign_id" : "$campaign_id", "action_key" : "$action_key"},
                "campaign_title": { "$first": "$campaign_title"}
            }},
            {"$group" : {
                "_id" : "$_id.campaign_id",
                "campaign_title" : {"$first" : "$campaign_title" },
                "aggregated" : { "$push" : {
                        "action_key" : "$_id.action_key",
                        "count" : "$total"
                    }
                }
                }
            }
        ]

        stats = list(db_query.skip(per_page * (page-1)).limit(per_page).order_by('campaign_title').aggregate(*pipeline))

        results = bson_dumps(stats)
        
        return total, results

    
    @classmethod
    def stats_campaign(cls, owner_id, campaign_id, last_days=config.STATS_SHOW_LAST_DAYS):
        
        end_date = pytz.utc.localize(datetime.utcnow())
        start_date = end_date - timedelta(days=last_days)

        db_query = cls.objects(owner_id=owner_id, 
                                campaign_id=campaign_id, 
                                created__gte=start_date,
                                created__lte=end_date,
                                result=1)

        pipeline = [
            {"$group" : {
                '_id': { 
                    "year": { "$year": "$created" },
                    "month" : {"$month" : "$created" },
                    "day": { "$dayOfMonth": "$created"},
                    "action_key" : "$action_key"
                    },
                "medium" : {"$first" : "$medium" },
                "campaign_id" : {"$first" : "$campaign_id"},
                "campaign_title" : {"$first" : "$campaign_title" }
            }},
            {"$group" : {
                "_id" : "$prospect_id",
                "prospects_total" : {"$sum" : 1 },
                }
            },
            {"$group" : {
                "_id" : {
                    "medium" : "$medium",
                    "year": "$_id.year",
                    "month" : "$_id.month",
                    "day": "$_id.day",
                },
                "campaign_title" : {"$first" : "$campaign_title" },
                "prospects_contacted" : {"$first" : "$prospects_total" },
                "campaign_id" : {"$first" : "$campaign_id"},
                "medium" : {"$first" : "$medium"},
                "aggregated" : { "$push" : {
                        "action_key" : "$_id.action_key",
                        "count" : "$total"
                    }
                }
                }
            }

        ]


        stats = list(db_query.order_by('created').aggregate(*pipeline))

        results = bson_dumps(stats)

        return results

class TaskLog(db.Document):
    owner_id = db.ObjectIdField()

    prospect_id = db.ObjectIdField()
    campaign_id = db.ObjectIdField()

    campaign_title = db.StringField()

    log = db.ListField(db.DictField())

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )

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
        exist = TaskLog.objects(prospect_id=task.prospect_id, campaign_id=task.campaign_id).first()
        if not exist:
            exist = cls()
            exist.owner_id = task.owner_id
            exist.prospect_id = task.prospect_id
            exist.campaign_id = task.campaign_id

        exist.campaign_title = task.stat_campaign_title

        action_key = task.action_key
        if action_key not in DONT_LOG:            
            if task.result_data:
                res = task.result_data.get('if_true', False)
                if res == True:
                    res = 1
                else:
                    res = 0

                ActionStats.log_stats(owner_id=exist.owner_id, 
                                        prospect_id=exist.prospect_id, 
                                        campaign_id=exist.campaign_id, 
                                        campaign_title=exist.campaign_title, 
                                        action_key=action_key, 
                                        result=res)
            
            
        
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