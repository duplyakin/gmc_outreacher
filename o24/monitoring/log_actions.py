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
import sys

MOSCOW = 'Europe/Moscow'

DONOT_SHOW = []

T_STATUSES = {
    FAILED: 'failed',
    FAILED_NEED_ACTION : 'failed_need_action',
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


def log_actions(last_date, campaign_id=None):
    logs = []
    if campaign_id:
        logs = scheduler_models.ActionLog.objects(campaign_id=campaign_id, created__gt=last_date).order_by('created')
    else:
        logs = scheduler_models.ActionLog.objects(created__gt=last_date).order_by('created')

    for log in logs:
        prospect_data = log.input_data.get('prospect_data', {})
        linkedin = prospect_data.get('linkedin', 'None')
        email = prospect_data.get('email', 'None')
        if log.created > last_date:
            last_date = log.created

        print("{id}--{status}--{action_key}--{step}--{description}--{linkedin}--{email}--{result_data}".format(id=log.task_id,
                                                                                                status=T_STATUSES[log.status],
                                                                                                action_key=log.action_key,
                                                                                                step=log.step,
                                                                                                description=log.description,
                                                                                                linkedin=linkedin,
                                                                                                email=email,
                                                                                                result_data=log.result_data))

    return last_date

if __name__ == '__main__':
    last_date = parse("1980-05-25T16:31:37.436Z")

    campaign_id = None
    try:
        campaign_id = sys.argv[1]
    except:
        pass
    print("\n\n.......log_actions started for campaign_id={0}".format(campaign_id))
    print("id, status, action_key, step, description, linkedin, email, result_data")

    while True:
        last_date = log_actions(last_date=last_date, campaign_id=campaign_id)
        time.sleep(3)

# python -m o24.monitoring.log_actions