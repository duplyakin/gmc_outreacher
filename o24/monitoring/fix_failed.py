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
import time 
import sys
from dateutil.parser import parse

MOSCOW = 'Europe/Moscow'

T_STATUSES = {
    FAILED: 'failed',
    NEW: 'new',
    IN_PROGRESS: 'in_progress',
    PAUSED: 'paused',
    FINISHED: 'finished',
    READY: 'ready',
    CARRYOUT: 'carryout',
    BLOCK_HAPPENED: 'block_happened',
    NEED_USER_ACTION: 'need_user_action',
    NEED_USER_ACTION_PROGRESS: 'need_user_action_progress',
    NEED_USER_ACTION_RESOLVED: 'need_user_action_resolved'
}


def fix_failed():
    CAMPAIGN_ID = sys.argv[1]

    tasks = shared.TaskQueue.objects(campaign_id=CAMPAIGN_ID, status__in=[-1, -2])
    if not tasks:
        print("Can't find FAILED tasks for campaign_id={0}".format(CAMPAIGN_ID))
        exit(0)

    counter = 0    
    for task in tasks:
        task.result_data = {}
        task.update_status(status=NEW)
        counter = counter + 1
    
    print("Has fixed {0} tasks".format(counter))
    


if __name__ == '__main__':
    print("\n\n.......fix_failed started")
    fix_failed()

# python -m o24.monitoring.fix_failed <campaign_id>