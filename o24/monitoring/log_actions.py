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
import argparse

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


def args_to_query(args):
    query = {}

    campaign_id = args.campaign_id
    if campaign_id:
        query['campaign_id'] = campaign_id
    
    status = args.status
    if status:
        query['status'] = int(status)

    prospect_id = args.prospect_id
    if prospect_id:
        query['prospect_id'] = prospect_id

    task_id = args.task_id
    if task_id:
        query['task_id'] = task_id

    return query

def log_actions(last_date, args):
    query = args_to_query(args)

    show_id = args.show_id

    logs = []
    if query:
        logs = scheduler_models.ActionLog.objects(**query, created__gt=last_date).order_by('created')
    else:
        logs = scheduler_models.ActionLog.objects(created__gt=last_date).order_by('created')

    for log in logs:
        prospect_data = log.input_data.get('prospect_data', {})
        linkedin = prospect_data.get('linkedin', 'None')
        email = prospect_data.get('email', 'None')
        if log.created > last_date:
            last_date = log.created

        if show_id:
            print("{log_id}  {id}--{status}--{action_key}--{step}--{description}--{linkedin}--{email}--{result_data}".format(
                                                                                                log_id=log.id,
                                                                                                id=log.task_id,
                                                                                                status=T_STATUSES[log.status],
                                                                                                action_key=log.action_key,
                                                                                                step=log.step,
                                                                                                description=log.description,
                                                                                                linkedin=linkedin,
                                                                                                email=email,
                                                                                                result_data=log.result_data))

        else:
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--show_id', dest='show_id', action='store', default=None, help='show log id')
    parser.add_argument('--once', dest='once', action='store', default=None, help='execute and exit only once')
    parser.add_argument('--campaign_id', dest='campaign_id', action='store', default=None, help='pass campaign_id to show logs for')
    parser.add_argument('--status', dest='status', action='store', default=None, help='show exact status')
    parser.add_argument('--prospect_id', dest='prospect_id', action='store', default=None, help='show only for prospect_id')
    parser.add_argument('--task_id', dest='task_id', action='store', default=None, help='show only task_id')

    args = parser.parse_args()
    
    campaign_id = args.campaign_id

    print("\n\n.......log_actions started for campaign_id={0}".format(campaign_id))
    print("id, status, action_key, step, description, linkedin, email, result_data")
    once = args.once
    if once is None:
        while True:
            last_date = log_actions(last_date=last_date, args=args)
            time.sleep(3)
    else:
        log_actions(last_date=last_date, args=args)

# python -m o24.monitoring.log_actions