from o24.backend import celery
import o24.backend.scheduler.scheduler as scheduler
from flask import current_app
from o24.globals import *
import traceback
import time
import random
import o24.backend.models.shared as shared
from datetime import datetime
from datetime import timedelta

@celery.task
def finished_handler(task_id):
    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("finished_handler ERROR: No such task id:{0}".format(task_id))

    task.update_status(status=FINSIHED)
    return

@celery.task
def success_handler(task_id):
    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("success_handler ERROR: No such task id:{0}".format(task_id))

    task.update_status(status=FINSIHED)
    return


@celery.task
def delay_handler(task_id):
    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("delay_handler ERROR: No such task id:{0}".format(task_id))
    
    task.acknowledge()

    input_data = task.get_input_data()
    if not input_data:
        raise Exception("delay_handler ERROR: wrong input_data:{0}".format(input_data))

    delay_data = input_data.get('delay', {})
    if not delay_data:
        raise Exception("delay_handler ERROR: wrong delay_data:{0}".format(input_data))
 
    start = delay_data.get('start')
    delay_sec = delay_data.get('delay_sec')
    next_round = start + timedelta(seconds=delay_sec)

    now = pytz.utc.localize(datetime.utcnow())

    if now >= next_round:
        result_data = {
            'code' : DELAY_FINISHED_CODE,
            'if_true' : True
        }
        task.set_result(result_data=result_data)
        task.update_status(status=CARRYOUT)
        return
     
    task.next_round = next_round
    result_data = {
        'code' : 0
    }
    task.set_result(result_data=result_data)

    task.update_status(status=NEW)
    return