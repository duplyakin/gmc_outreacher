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
from bson.objectid import ObjectId

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

#enricher statuses
E_STATUSES = {
    ENRICH_NEW: 'new', 
    ENRICH_IN_PROGRESS: 'in_progress',
    ENRICH_SUCCESS: 'enrich_success',
    ENRICH_FAILED_TO_FOUND: 'enrich_failed_to_found',
    ENRICH_TRIED_ALL: 'tried_all',
    ENRICH_OUT_OF_CREDITS: 'out_of_credits',
    ENRICH_MOVED: 'enrich_moved'
}

def show_enrich_log(log, last_date, show_id):
    input_data = log.task.get('input_data', {})
    linkedin = input_data.get('linkedin', 'None')
    email = input_data.get('email', 'None')
    actions_tried = str(log.task.get('actions_tried', 'no_actions_tried'))
    if log.created > last_date:
        last_date = log.created

    moscow_format = log.created.astimezone(pytz.timezone(MOSCOW)).strftime("%y-%d-%b %H:%M:%S")
    if show_id:
        print("{created} {log_id}  {id}--{status}---{step}--{description}--{linkedin}--{email}--{actions_tried}".format(
                                                                                            created=moscow_format,
                                                                                            log_id=log.id,
                                                                                            id=log.task.get('_id'),
                                                                                            status=E_STATUSES[log.task.get('status')],
                                                                                            step=log.step,
                                                                                            description=log.description,
                                                                                            linkedin=linkedin,
                                                                                            email=email,
                                                                                            actions_tried=actions_tried))

    else:
        print("{created} {id}--{status}--{step}--{description}--{linkedin}--{email}--{actions_tried}".format(
                                                                                            created=moscow_format,
                                                                                            id=log.task.get('_id'),
                                                                                            status=E_STATUSES[log.task.get('status')],
                                                                                            step=log.step,
                                                                                            description=log.description,
                                                                                            linkedin=linkedin,
                                                                                            email=email,
                                                                                            actions_tried=actions_tried))
    return last_date

def args_to_query(args):
    query = {}
    raw = {}

    campaign_id = args.campaign_id
    if campaign_id:
        query['task__campaign_id'] = ObjectId(campaign_id)

    credentials_id = args.credentials_id
    if credentials_id:
        query['task__credentials_id'] = ObjectId(credentials_id)

    status = args.status
    if status:
        query['task__status'] = int(status)

    prospect_id = args.prospect_id
    if prospect_id:
        query['task__prospect_id'] = ObjectId(prospect_id)

    task_id = args.task_id
    if task_id:
        raw['task._id'] = ObjectId(task_id)

    return query, raw

def log_actions(last_date, args):
    query, raw = args_to_query(args)

    show_id = args.show_id
    no_result_data = args.no_result_data

    logs = []
    if query or raw:
        logs = scheduler_models.ActionLog.objects(__raw__=raw, **query, created__gt=last_date).order_by('created')
    else:
        logs = scheduler_models.ActionLog.objects(created__gt=last_date).order_by('created')

    for log in logs:
        log_type = log.log_type
        if not log_type:
            print('Unknown log_type for log.id={0}'.format(log.id))
            continue

        if log_type == 'enricher-log':
            last_date = show_enrich_log(log, last_date, show_id)
            continue

        prospect_data = log.task.get('input_data').get('prospect_data', {})
        linkedin = prospect_data.get('linkedin', 'None')
        email = prospect_data.get('email', 'None')
        if log.created > last_date:
            last_date = log.created

        moscow_format = log.created.astimezone(pytz.timezone(MOSCOW)).strftime("%y-%d-%b %H:%M:%S")
        if no_result_data:
            if show_id:
                print("{created} {log_id}  {id}--{status}--{action_key}--{step}--{description}--{linkedin}--{email}".format(
                                                                                                    created=moscow_format,
                                                                                                    log_id=log.id,
                                                                                                    id=log.task.get('_id'),
                                                                                                    status=T_STATUSES[log.task.get('status')],
                                                                                                    action_key=log.task.get('action_key'),
                                                                                                    step=log.step,
                                                                                                    description=log.description,
                                                                                                    linkedin=linkedin,
                                                                                                    email=email))

            else:
                print("{created} {id}--{status}--{action_key}--{step}--{description}--{linkedin}--{email}".format(
                                                                                                    created=moscow_format,
                                                                                                    id=log.task.get('_id'),
                                                                                                    status=T_STATUSES[log.task.get('status')],
                                                                                                    action_key=log.task.get('action_key'),
                                                                                                    step=log.step,
                                                                                                    description=log.description,
                                                                                                    linkedin=linkedin,
                                                                                                    email=email))

        else:
            if show_id:
                print("{created} {log_id}  {id}--{status}--{action_key}--{step}--{description}--{linkedin}--{email}--{result_data}".format(
                                                                                                    created=moscow_format,
                                                                                                    log_id=log.id,
                                                                                                    id=log.task.get('_id'),
                                                                                                    status=T_STATUSES[log.task.get('status')],
                                                                                                    action_key=log.task.get('action_key'),
                                                                                                    step=log.step,
                                                                                                    description=log.description,
                                                                                                    linkedin=linkedin,
                                                                                                    email=email,
                                                                                                    result_data=log.task.get('result_data')))

            else:
                print("{created} {id}--{status}--{action_key}--{step}--{description}--{linkedin}--{email}--{result_data}".format(
                                                                                                    created=moscow_format,
                                                                                                    id=log.task.get('_id'),
                                                                                                    status=T_STATUSES[log.task.get('status')],
                                                                                                    action_key=log.task.get('action_key'),
                                                                                                    step=log.step,
                                                                                                    description=log.description,
                                                                                                    linkedin=linkedin,
                                                                                                    email=email,
                                                                                                    result_data=log.task.get('result_data')))

    return last_date

if __name__ == '__main__':
    last_date = parse("1980-05-25T16:31:37.436Z")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--last_date', dest='last_date', action='store', default=None, help='last_date')
    parser.add_argument('--show_id', dest='show_id', action='store', default=None, help='show log id')
    parser.add_argument('--once', dest='once', action='store', default=None, help='execute and exit only once')
    parser.add_argument('--campaign_id', dest='campaign_id', action='store', default=None, help='pass campaign_id to show logs for')
    parser.add_argument('--status', dest='status', action='store', default=None, help='show exact status')
    parser.add_argument('--prospect_id', dest='prospect_id', action='store', default=None, help='show only for prospect_id')
    parser.add_argument('--task_id', dest='task_id', action='store', default=None, help='show only task_id')
    parser.add_argument('--credentials_id', dest='credentials_id', action='store', default=None, help='show only credentials_id')
    parser.add_argument('--no_result_data', dest='no_result_data', action='store', default=None, help='no_result_data')
        
    args = parser.parse_args()

    if args.last_date:
        moscow_time = parse(args.last_date)
        last_date = moscow_time.replace(tzinfo=pytz.timezone(MOSCOW))
        print("...starting from  last_date={0}".format(last_date)) 
    
    campaign_id = args.campaign_id

    print("\n\n.......log_actions started for campaign_id={0}".format(campaign_id))
    print("log_id, id, status, action_key, step, description, linkedin, email, result_data")
    once = args.once
    if once is None:
        while True:
            last_date = log_actions(last_date=last_date, args=args)
            time.sleep(3)
    else:
        log_actions(last_date=last_date, args=args)

# python -m o24.monitoring.log_actions --last_date=2020-06-24T12:00