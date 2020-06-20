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
import o24.backend.scheduler.models as scheduler_models
import pytz

@celery.task
def finished_handler(task_id):
    result_data = {
        'if_true' : False,
        'code' : -1,
        'error' : 'Unknown Error'
    }
    status = FAILED

    task = None
    try:
        task = shared.TaskQueue.lock(task_id)
        if not task:
            print("CONCURRENCY in finished_handler attempt")
            return result_data

        status = FINISHED
        result_data = {
            'if_true' : True,
            'code' : 0,
            'raw' : 'finished_handler'
        }
    except Exception as e:
        print(e)
        traceback.print_exc()

        status = FAILED
        code = -1
        raw = ''

        result_data = {
            'error' : str(e),
            'code' : code,
            'raw' : raw
        }
            
    finally:
        if task:
            unlocked = shared.TaskQueue.unlock(task_id=task_id, result_data=result_data, status=status)
            if not unlocked:
                raise Exception("Can't unlock finished_handler")

            #log task
            scheduler_models.ActionLog.log(task, step='handler', description="finished_handler")
        return result_data

    return result_data

@celery.task
def success_handler(task_id):
    result_data = {
        'if_true' : False,
        'code' : -1,
        'error' : 'Unknown Error'
    }
    status = FAILED

    task = None
    try:
        task = shared.TaskQueue.lock(task_id)
        if not task:
            print("CONCURRENCY in success_handler attempt")
            return result_data

        status = FINISHED
        result_data = {
            'if_true' : True,
            'code' : 0,
            'raw' : 'success_handler'
        }
    except Exception as e:
        print(e)
        traceback.print_exc()

        status = FAILED
        code = -1
        raw = ''

        result_data = {
            'error' : str(e),
            'code' : code,
            'raw' : raw
        }
            
    finally:
        if task:
            unlocked = shared.TaskQueue.unlock(task_id=task_id, result_data=result_data, status=status)
            if not unlocked:
                raise Exception("Can't unlock success_handler")

            #log task
            scheduler_models.ActionLog.log(task, step='handler', description="success_handler")
        return result_data

    return result_data

@celery.task
def delay_handler(task_id):

    result_data = {
        'if_true' : False,
        'code' : -1,
        'error' : 'Unknown Error'
    }
    status = FAILED

    task = None
    try:
        task = shared.TaskQueue.lock(task_id)
        if not task:
            print("CONCURRENCY in delay_handler attempt")
            return result_data

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
            status = READY

            task.set_result(result_data=result_data)
            task.update_status(status=READY)
            return result_data
        
        task.next_round = next_round
        task._commit()

        result_data = {
            'code' : 0
        }
        status = NEW
    except Exception as e:
        print(e)
        traceback.print_exc()

        status = FAILED
        code = -1
        raw = ''

        result_data = {
            'error' : str(e),
            'code' : code,
            'raw' : raw
        }
            
    finally:
        if task:
            unlocked = shared.TaskQueue.unlock(task_id=task_id, result_data=result_data, status=status)
            if not unlocked:
                raise Exception("Can't unlock delay_handler")

            #log task
            scheduler_models.ActionLog.log(task, step='handler', description="delay_handler")
        return result_data

    return result_data