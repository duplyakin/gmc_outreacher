from o24.backend import celery
import o24.backend.scheduler.scheduler as scheduler
from flask import current_app
from o24.globals import *
import traceback
import time
import random
import o24.backend.models.shared as shared

from o24.backend.gmail.controller import GmailController

@celery.task
def gmail_send_message(task_id):
    
    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    propspect_id = task.propspect_id
    campaign_id = task.campaign_id
    
    mailbox = 