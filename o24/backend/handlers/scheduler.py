from o24.backend import app
from o24.backend import db
from o24.backend.scheduler.scheduler import Scheduler
from celery import shared_task, group, chord

from . import celery
import traceback
import time


@shared_task
def emit_scheduler():
    try:
        #get all campaigns that are ready
        

        scheduler = Scheduler(db=db, app=app)

        scheduler.planning()

    except Exception as e:
        app.logger.error(".....emit_scheduler Exception:{0}".format(str(e)))
        traceback.print_exc()
        return {"status": False}


    return {"status": True}
