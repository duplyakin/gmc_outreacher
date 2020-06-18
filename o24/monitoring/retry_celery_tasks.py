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
from dateutil.parser import parse

MOSCOW = 'Europe/Moscow'

DONOT_SHOW = []

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


def retry_tasks():

    tasks = shared.TaskQueue.objects(status=IN_PROGRESS, action_key__in=NON_3RD_PARTY_ACTION_KEYS)
    if not tasks:
        print("nothing to retry")
        
    for task in tasks:
        task.next_round = parse("1980-05-25T16:31:37.436Z")
        task.update_status(status=NEW)
        task.reload()
        next_round = task.next_round.astimezone(pytz.timezone(MOSCOW)).strftime("%d-%b %H:%M")
        print("...retryed: {id} - {status} - {next_round} - {action_key}".format(id=task.id, 
                                                                                status=task.status, 
                                                                                next_round=next_round,
                                                                                action_key=task.action_key))


if __name__ == '__main__':
    print("\n\n.......retry_celery_tasks started")
    retry_tasks()
# python -m o24.monitoring.retry_celery_tasks