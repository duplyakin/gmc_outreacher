from o24.backend import app
from o24.backend import db
from celery import shared_task, group, chord
from o24.backend import celery
from o24.backend.scheduler.scheduler import Scheduler
from flask import current_app

import traceback
import time

from o24.backend.models.shared import TaskQueue


@celery.task(name='emit_scheduler')
def emit_scheduler():
    
    scheduler = None
    try:
        scheduler = Scheduler.lock()
        if not scheduler:
            print("emit_scheduler concurrence attempt")
            return {"status": False}
        
        #handle FAILED and CARRYOUT tasks
        scheduler.trail()

        #Switch READY tasks to the next stage
        scheduler.plan()

        #Create jobs for all NEW tasks that are ready
        jobs = scheduler.execute()
        print("...emit_scheduler: scheduler.execute() returned {0} jobs".format(len(jobs)))

        group_jobs = group(jobs)

        group_jobs.apply_async()
        return {"status": True}
    except Exception as e:
        app.logger.error(".....emit_scheduler Exception:{0}".format(str(e)))
        traceback.print_exc()
        return {"status": False}
        
    finally:
        if scheduler:
            scheduler.unlock()

    return {"status": True}
