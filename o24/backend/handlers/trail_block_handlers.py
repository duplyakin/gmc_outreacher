import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
import o24.backend.scheduler.scheduler as scheduler

from o24.globals import *
import datetime
from mongoengine.queryset.visitor import Q
import o24.config as config

def block_happend(task):
    credentials_id = task.credentials_id
    credentials = models.Credentials.objects(id=credentials_id).first()
    if not credentials:
        raise Exception("There is no credentials for task.id={0}".format(task.id))

    if credentials.status == -1:
        print("Should happened rare: block_happend, repeat call for credentials.id={0}".format(credentials_id))
        return 

    credentials.error(error='Need to relogin')

    task.status = NEED_USER_ACTION
    task._commit()
    return

def block_resolved(task):
    credentials_id = task.credentials_id
    credentials = models.Credentials.objects(id=credentials_id).first()
    if not credentials:
        raise Exception("There is no credentials for task.id={0}".format(task.id))

    if credentials.status != -1:
        print("Should never happened: block_resolved, repeat call for credentials.id={0}".format(credentials_id))
        return 
    
    credentials.resolved()

    shared.TaskQueue.objects(credentials_id=credentials.id).update(status=NEW)
    return
    

def block_default(task):
    print("MUST NEVER HAPPENED: block_default for task.id={0}".format(task.id))
