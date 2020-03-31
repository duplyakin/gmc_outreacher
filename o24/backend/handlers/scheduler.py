from backend import app
from backend import db
from backend.scheduler.scheduler import Scheduler

from . import celery
import traceback
import time


@celery.task(bind=True, name='emit_scheduler')
def emit_scheduler(self):
    try:
        scheduler = Scheduler(db=db, app=app)
   
    except Exception as e:
        app.logger.error(".....emit_scheduler Exception:{0}".format(str(e)))
        traceback.print_exc()
        return {"status": False}


    return {"status": True}
