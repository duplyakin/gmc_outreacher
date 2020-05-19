from o24.backend import app
from o24.backend import db
from celery import shared_task, group, chord
from o24.backend import celery
from o24.backend.scheduler.scheduler import Scheduler
from flask import current_app

import traceback
import time

from o24.backend.models.shared import TaskQueue


@celery.task
def emit_scheduler():
    try:
        scheduler = Scheduler()
        
        #handle FAILED and CARRYOUT tasks
        scheduler.trail()

        #Switch READY tasks to the next stage
        scheduler.plan()

        #Create jobs for all NEW tasks that are ready
        jobs = scheduler.execute()

        group_jobs = group(jobs)

        return group_jobs.apply_async()
    except Exception as e:
        app.logger.error(".....emit_scheduler Exception:{0}".format(str(e)))
        traceback.print_exc()
        return {"status": False}


    return {"status": True}
