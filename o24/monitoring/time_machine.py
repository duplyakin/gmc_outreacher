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
from o24.enricher.models import EnrichTaskQueue

MOSCOW = 'Europe/Moscow'

def check_enrich_finished(task):
    prospect_id = task.prospect_id

    enrich_task = EnrichTaskQueue.objects(prospect_id=prospect_id).first()
    if not enrich_task:
        return False

    if enrich_task.status == ENRICH_OUT_OF_CREDITS:
        print("Enrich out of credits for task.id={0}".format(task.id))
        return False

    if enrich_task.status in [ENRICH_SUCCESS, ENRICH_FAILED_TO_FOUND]:
        print("check_enrich_finished True for task.id={0} with status={1}".format(task.id, enrich_task.status))
        return True

    prospect = models.Prospects.objects(id=prospect_id).first()
    if prospect:
        email = prospect.data.get('email', '')
        if email:
            return True

    return False

def inc_limits():
    CAMPAIGN_ID = None
    if len(sys.argv) < 2:
        print("Time machine started for ALL tasks in TaskQueue - for all campaigns")
    else:
        CAMPAIGN_ID = sys.argv[1]
        print("time machine started for CAMPAIGN_ID={0}".format(CAMPAIGN_ID))

    tasks = []

    while True:
        if CAMPAIGN_ID:
            tasks = shared.TaskQueue.objects(campaign_id=CAMPAIGN_ID)
        else:
            tasks = shared.TaskQueue.objects()

        if not tasks:
            print("...Waiting for tasks appeared")
            print("Can't find tasks for campaign_id={0}".format(CAMPAIGN_ID))
            time.sleep(2)
        else:
            break
    
    print("...Found tasks - starting the next round")
    for task in tasks:
        if task.action_key == ENRICH_DELAY_ACTION:
            enrich_finished = check_enrich_finished(task)
            if enrich_finished:
                task.status = READY
                task.next_round = parse("1980-05-25T16:31:37.436Z")
                task._commit()
            continue

        if task.action_key == 'delay':
            task.status = READY
            task.next_round = parse("1980-05-25T16:31:37.436Z")
            task._commit()
            continue


        task.next_round = parse("1980-05-25T16:31:37.436Z")
        task._commit()

        credentials = models.Credentials.objects(id=task.credentials_id).first()
        if not credentials:
            print("Can't find credentials for task_id={0}".format(task.id))
            exit(0)
        
        credentials.next_action = parse("1980-05-25T16:31:37.436Z")
        credentials._commit()

    

if __name__ == '__main__':
    print("\n\n.......time_machine started")
    while True:
        inc_limits()
        time.sleep(3)

# python -m o24.monitoring.time_machine