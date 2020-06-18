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


def log_actions():

    tasks = shared.TaskQueue.objects(status__ne=NEW, id__nin=DONOT_SHOW)

    for task in tasks:
        prospect_data = task.input_data.get('prospect_data', {})
        next_round = 'None'
        next_action = 'None'
        if task.next_round:
            next_round = task.next_round.astimezone(pytz.timezone(MOSCOW)).strftime("%d-%b %H:%M")
        credentials = models.Credentials.objects(id=task.credentials_id).first()
        if credentials:
            next_action = credentials.next_action.astimezone(pytz.timezone(MOSCOW)).strftime("%d-%b %H:%M")

        print("id:{id} status={status} action_key={action_key} result_data={result_data} next_round={next_round} cr_next_action={next_action}".format(id=task.id,
                                                                                                status=T_STATUSES[task.status],
                                                                                                action_key=task.action_key,
                                                                                                result_data=task.result_data,
                                                                                                next_round=next_round,
                                                                                                next_action=next_action))
        print("id:{id} prospect_data={prospect_data}".format(id=task.id, prospect_data=prospect_data))
        if task.status == FINISHED:
            DONOT_SHOW.append(task.id)


if __name__ == '__main__':
    print("\n\n.......log_actions started")
    while True:
        log_actions()
        time.sleep(3)

# python -m o24.monitoring.log_actions