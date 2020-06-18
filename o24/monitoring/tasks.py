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


def show_tasks():
    CAMPAIGN_ID = sys.argv[1]

    tasks = shared.TaskQueue.objects(campaign_id=CAMPAIGN_ID)
    if not tasks:
        print("Can't find tasks for campaign_id={0}".format(CAMPAIGN_ID))
        exit(0)
    
    print("...tasks for campaign_id={0}".format(CAMPAIGN_ID))
    for task in tasks:
        next_round = 'None'
        next_action = 'None'
        if task.next_round:
            next_round = task.next_round.astimezone(pytz.timezone(MOSCOW)).strftime("%d-%b %H:%M")
        credentials = models.Credentials.objects(id=task.credentials_id).first()
        if credentials:
            next_action = credentials.next_action.astimezone(pytz.timezone(MOSCOW)).strftime("%d-%b %H:%M")

        print("{id} - {status:12}-{action_key:25}-next_round={next_round:15}-cr_next_action={next_action:15} {result_data}".format(id=task.id,
                                                                                                status=T_STATUSES[task.status],
                                                                                                action_key=task.action_key,
                                                                                                result_data=task.result_data,
                                                                                                next_round=next_round,
                                                                                                next_action=next_action))

    


if __name__ == '__main__':
    print("\n\n.......tasks started")
    show_tasks()

# python -m o24.monitoring.tasks <campaign_id>