from o24.backend import celery
import o24.backend.scheduler.scheduler as scheduler
from flask import current_app
from o24.globals import *
import traceback
import time

import o24.backend.models.shared as shared

result_data = {
    'if_true' : True
}

@celery.task
def dummy_linkedin_check_reply(task_id):
    #app = current_app._get_current_object()
    print("dummy_linkedin_visit_profile")
 
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
    print("dummy_linkedin_visit_profile")
    
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
    print("dummy_linkedin_connect")

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
    print("dummy_linkedin_send_message")

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
    print("dummy_email_send_message")

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
    print("dummy_linkedin_check_accept")

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
    print("dummy_email_check_reply")

    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()
    
    if task.last_action():
        task.finish_task()
    else:
        task.set_result(result_data)
        task.update_status(status=READY)
