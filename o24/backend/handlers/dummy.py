from o24.backend import celery
import o24.backend.scheduler.scheduler as scheduler
from flask import current_app
from o24.globals import *
import traceback
import time
import random

import o24.backend.models.shared as shared

result_data = {
    'if_true' : False
}

@celery.task
def dummy_linkedin_check_reply(task_id):
    #app = current_app._get_current_object()
    #print("dummy_linkedin_visit_profile")
    
    result_data.update({
        'if_true' : random.choice([True,False])
    })
    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)

@celery.task
def dummy_linkedin_visit_profile(task_id):
    #print("dummy_linkedin_visit_profile")

    result_data.update({
        'if_true' : random.choice([True,False])
    })    
    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)


@celery.task
def dummy_linkedin_connect(task_id):
    #print("dummy_linkedin_connect")
    result_data.update({
        'if_true' : random.choice([True,False])
    })

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)

@celery.task
def dummy_linkedin_send_message(task_id):
    #print("dummy_linkedin_send_message")
    result_data.update({
        'if_true' : random.choice([True,False])
    })

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)


@celery.task
def dummy_email_send_message(task_id):
    #print("dummy_email_send_message")
    result_data.update({
        'if_true' : random.choice([True,False])
    })

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)


@celery.task
def dummy_delay(task_id):
    print("dummy_delay")
    result_data.update({
        'if_true' : random.choice([True,False])
    })

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)


@celery.task
def dummy_finished(task_id):
    print("dummy_finished")
    result_data.update({
        'if_true' : random.choice([True,False])
    })

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)


@celery.task
def dummy_success(task_id):
    print("dummy_success")
    result_data.update({
        'if_true' : random.choice([True,False])
    })

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)


@celery.task
def dummy_linkedin_check_accept(task_id):
    #print("dummy_linkedin_check_accept")
    result_data.update({
        'if_true' : random.choice([True,False])
    })

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)


@celery.task
def dummy_email_check_reply(task_id):
    #print("dummy_email_check_reply")
    result_data.update({
        'if_true' : random.choice([True,False])
    })

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)
