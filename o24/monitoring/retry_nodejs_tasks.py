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


def retry_nodejs_tasks():

    tasks = shared.TaskQueue.objects(status=IN_PROGRESS, action_key__nin=NON_3RD_PARTY_ACTION_KEYS)
    if not tasks:
        print("nothing to retry")
        
    for task in tasks:
        task.next_round = parse("1980-05-25T16:31:37.436Z")
        task.is_queued = 0
        task.ack = 0

        task.update_status(status=NEW)
        task.reload()
        next_round = task.next_round.astimezone(pytz.timezone(MOSCOW)).strftime("%d-%b %H:%M")
        print("...retryed: {id} - {status} - {next_round} - {action_key} is_queued={is_queued} ack={ack}".format(id=task.id, 
                                                                                status=task.status, 
                                                                                next_round=next_round,
                                                                                action_key=task.action_key,
                                                                                is_queued=task.is_queued,
                                                                                ack=task.ack))


if __name__ == '__main__':
    print("\n\n.......retry_nodejs_tasks started")
    retry_nodejs_tasks()
# python -m o24.monitoring.retry_nodejs_tasks