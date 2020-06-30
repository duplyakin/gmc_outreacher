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
from bson import ObjectId

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
    prospect_id = db.ObjectIdField()
    campaign_id = db.ObjectIdField()

    task = db.DictField()

    description = db.StringField()
    step = db.StringField()

    log_type = db.StringField()

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )

    @classmethod
    def log(cls, task, step, description):
        try:
            task.reload()
            now = pytz.utc.localize(datetime.utcnow())
            new_log = cls(
                owner_id=task.owner_id,
                prospect_id=task.prospect_id,
                campaign_id=task.campaign_id,
                step=step,
                description=description,
                created = now,
                task=task.to_mongo(),
                log_type='general'
            )

            new_log._commit()
        except Exception as e:
            print("LOG ERROR: .....")
            print(str(e))
            traceback.print_exc()

    @classmethod
    def log_open(cls, owner_id, prospect_id, campaign_id):
        try:
            now = pytz.utc.localize(datetime.utcnow())
            new_log = cls(
                owner_id = owner_id,
                prospect_id=prospect_id,
                campaign_id=campaign_id,
                step='email-open-log',
                created = now,
                log_type='email-open'
            )

            new_log._commit()
        except Exception as e:
            print("OPEN LOG ERROR: .....")
            print(str(e))
            traceback.print_exc()

    @classmethod
    def log_enricher(cls, task, step, description):
        try:
            now = pytz.utc.localize(datetime.utcnow())
            task.reload()
            new_log = cls(
                owner_id=task.owner,
                step=step,
                description=description,
                created = now,
                task=task.to_mongo(),
                log_type='enricher-log'
            )

            new_log._commit()
        except Exception as e:
            print("OPEN LOG ERROR: .....")
            print(str(e))
            traceback.print_exc()

    @classmethod
    def get_stats_total(cls, owner_id, from_date, to_date):
        db_query = cls.objects(owner_id=owner_id, 
                                created__gte=from_date,
                                created__lte=to_date)

        stats = []

        #we use it for join and showing objects as it is
        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq" :["$step", 'carryout_handler'] },
                            { "$eq": ["$task.status",  READY ] },
                            { "$eq": ["$task.result_data.if_true",  True ] },
                        ]
                    }
                }
            },
            {"$group" : {
                '_id':"$task.action_key",
                'total' : {'$sum' : 1},
                }
            }  
        ]

        events = list(db_query.aggregate(*pipeline))
        if events:
            stats.extend(events)

        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq" :["$step", 'carryout_handler'] },
                            { "$eq": ["$task.status",  READY ] },
                            { "$eq": ["$task.result_data.if_true",  True ] },
                        ]
                    }
                }
            },
            {"$group" : {
                '_id': "$task.prospect_id",
            }},
            {"$group" : {
                '_id' : 'prospects_total',
                'total' : {"$sum" : 1}
            }}
        ]

        prospects = list(db_query.aggregate(*pipeline))
        if prospects:
            stats.extend(prospects)


        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq": ["$step", 'email-open-log' ] },
                        ]
                    }
                }
            },
            {"$group" : {
                '_id' : 'email_opens',
                'total' : {"$sum" : 1}
            }}
        ]

        email_opens = list(db_query.aggregate(*pipeline))
        if email_opens:
            stats.extend(email_opens)

        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq": ["$step", 'enrich-controller-enrich' ] },
                            { "$eq": ["$task.status", ENRICH_SUCCESS ] },
                        ]
                    }
                }
            },
            {"$group" : {
                '_id' : '$task.prospect_id',
            }},
            {"$group" : {
                '_id' : 'emails-enriched-success',
                'total' : {"$sum" : 1}
            }}

        ]

        emails_enriched = list(db_query.aggregate(*pipeline))
        if emails_enriched:
            stats.extend(emails_enriched)


        #need to add Amount of credits for this user
        user = models.User.objects(id=owner_id).first()
        if user:
            credits_left = user.get_credits()
            credits_stats = [{
                '_id' : 'credits-left',
                'total' : credits_left
            }]
            stats.extend(credits_stats)

        results = bson_dumps(stats)
        return results

    @classmethod
    def get_campaign_stats(cls, owner_id, campaign_id, from_date, to_date):
        db_query = cls.objects(owner_id=owner_id,
                                campaign_id=campaign_id,
                                created__gte=from_date,
                                created__lte=to_date)

        stats = []

        #we use it for join and showing objects as it is
        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq" :["$step", 'carryout_handler'] },
                            { "$eq": ["$task.status",  READY ] },
                            { "$eq": ["$task.result_data.if_true",  True ] },
                        ]
                    }
                }
            },
            {"$group" : {
                '_id': {
                    'action_key' : "$task.action_key",
                    'month_day' : { '$dateToString' : { 'format' : "%m-%d", 'date' : "$created" }  }
                },
                'total' : {'$sum' : 1},
                }
            }  
        ]

        events = list(db_query.aggregate(*pipeline))
        if events:
            stats.extend(events)

        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq" :["$step", 'carryout_handler'] },
                            { "$eq": ["$task.status",  READY ] },
                            { "$eq": ["$task.result_data.if_true",  True ] },
                        ]
                    }
                }
            },
            {"$group" : {
                '_id': {
                    "prospect_id" : "$task.prospect_id",
                    'month_day' : { '$dateToString' : { 'format' : "%m-%d", 'date' : "$created" }  }
                },
            }},
            {"$group" : {
                '_id' : {
                    'month_day' : "$_id.month_day",
                    "action_key" : "prospects_total"
                },
                'total' : {"$sum" : 1}
            }}
        ]

        prospects = list(db_query.aggregate(*pipeline))
        if prospects:
            stats.extend(prospects)

        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq": ["$step", 'email-open-log' ] },
                        ]
                    }
                }
            },
            {"$group" : {
                '_id' : {
                    'action_key' : 'email_opens',
                    'month_day' : { '$dateToString' : { 'format' : "%m-%d", 'date' : "$created" }  } 
                },
                'total' : {"$sum" : 1}
            }}
        ]

        email_opens = list(db_query.aggregate(*pipeline))
        if email_opens:
            stats.extend(email_opens)

        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq": ["$task.status", FAILED ] },
                        ]
                    }
                }
            },
            {"$group" : {
                '_id': {
                    "a_key" : "$task.action_key",
                    'month_day' : { '$dateToString' : { 'format' : "%m-%d", 'date' : "$created" }  }
                },
            }},
            {"$group" : {
                '_id' : {
                    'month_day' : "$_id.month_day",
                    "action_key" : "errors"
                },
                'total' : {"$sum" : 1}
            }}
        ]

        errors = list(db_query.aggregate(*pipeline))
        if errors:
            stats.extend(errors)

        pipeline = [
            { "$match":
                { "$expr":
                    { "$and":
                        [
                            { "$eq": ["$step", 'enrich-controller-enrich' ] },
                            { "$eq": ["$task.status", ENRICH_SUCCESS ] },
                        ]
                    }
                }
            },

            {"$group" : {
                '_id': {
                    "prospect_id" : "$task.prospect_id",
                    'month_day' : { '$dateToString' : { 'format' : "%m-%d", 'date' : "$created" }  }
                },
            }},

            {"$group" : {
                '_id' : {
                    'month_day' : "$_id.month_day",
                    "action_key" : "emails-enriched-success"
                },
                'total' : {"$sum" : 1}
            }}
        ]

        emails_enriched = list(db_query.aggregate(*pipeline))
        if emails_enriched:
            stats.extend(emails_enriched)


        #need to add Amount of credits for this user
        user = models.User.objects(id=owner_id).first()
        if user:
            credits_left = user.get_credits()
            credits_stats = [{
                '_id' : 'credits-left',
                'total' : credits_left
            }]
            stats.extend(credits_stats)


        results = bson_dumps(stats)
        return results

    def _commit(self):
        self.save()