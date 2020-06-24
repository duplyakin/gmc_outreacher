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
import argparse

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


def fix_task_deadlock(task_id):
    task = shared.TaskQueue.objects(id=task_id).get()
    if not task:
        print("Can't task task_id={0}".format(task_id))
        exit(0)

    task.ack = 0
    task.celery_ack = 0
    task.is_queued = 0
    task.update_status(status=NEW)

    print("Has fixed task_id {0}".format(task_id))



def fix_campaign_deadlocks(campaign_id):
    tasks = shared.TaskQueue.objects(campaign_id=campaign_id, ack=1)
    if not tasks:
        print("Can't find ack=1 tasks for campaign_id={0}".format(campaign_id))
        exit(0)

    counter = 0    
    for task in tasks:
        task.ack = 0
        task.is_queued = 0
        task.update_status(status=NEW)
        counter = counter + 1
    
    print("Has fixed deadlocks {0} tasks".format(counter))
    

if __name__ == '__main__':
    print("\n\n.......fix_deadlocks started")
    parser = argparse.ArgumentParser()
    parser.add_argument('--campaign_id', dest='campaign_id', action='store', default=None, help='pass campaign_id to show logs for')
    parser.add_argument('--task_id', dest='task_id', action='store', default=None, help='task_id')
        
    args = parser.parse_args()

    campaign_id = args.campaign_id
    task_id = args.task_id
    if campaign_id:
        fix_campaign_deadlocks(campaign_id)
    elif task_id:
        fix_task_deadlock(task_id)

# python -m o24.monitoring.fix_deadlocks <campaign_id>