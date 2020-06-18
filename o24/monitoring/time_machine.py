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


def inc_limits():
    CAMPAIGN_ID = sys.argv[1]

    tasks = shared.TaskQueue.objects(campaign_id=CAMPAIGN_ID)
    if not tasks:
        print("Can't find tasks for campaign_id={0}".format(CAMPAIGN_ID))
        exit(0)
    
    for task in tasks:
        if task.action_key == 'delay':
            task.status = READY
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