import os
import o24.config as config
from o24.backend import app
from o24.backend import db

import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
import o24.backend.scheduler.models as scheduler_models

from o24.globals import *
from datetime import datetime  
from datetime import timedelta  
from pytz import timezone
import pytz
import json
from pprint import pprint

def show_tasks():
    print("\n\n.......show_tasks")

    tasks_total = shared.TaskQueue.objects()
    
    ids_active_campaigns = models.Campaign.objects(status=IN_PROGRESS).distinct('id')
    tasks_for_active_campaigns = shared.TaskQueue.objects(campaign_id__in=ids_active_campaigns)

    pipeline = [
        {"$lookup" : {
            "from" : "campaign",
            "localField" : "campaign_id",
            "foreignField" : "_id",
            "as" : "campaigns"
        }},
        { "$unwind" : { "path" : "$campaigns", "preserveNullAndEmptyArrays": True }},
        {"$lookup" : {
            "from" : "credentials",
            "localField" : "credentials_id",
            "foreignField" : "_id",
            "as" : "credentials"
        }},
        { "$unwind" : { "path" : "$credentials", "preserveNullAndEmptyArrays": True }},
        {"$group" : {
            "_id": "$status",
            "status" : { "$first" : "$status" },
            "count" : {"$sum" : 1}
            }
        },
    ]

    tasks_group_by_status = list(shared.TaskQueue.objects().aggregate(*pipeline))

    pprint("1. Tasks total...............: *** {0}".format(len(tasks_total)))
    pprint("1. Tasks for active campaigns: *** {0}".format(len(tasks_for_active_campaigns)))
    pprint("1. Tasks grouped by status...: ")
    pprint(tasks_group_by_status)

if __name__ == '__main__':
    show_tasks()