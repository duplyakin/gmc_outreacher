from backedn import app
from . import celery
import traceback
import time


@celery.task(bind=True)
def emit_send_email(self, action_id) :
    pass
