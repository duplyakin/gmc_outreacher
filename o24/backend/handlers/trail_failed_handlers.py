import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
from o24.globals import *
import datetime
from mongoengine.queryset.visitor import Q
import o24.backend.scheduler.models as scheduler_models

def system_error(task):
    if not task:
        print("system_error: task is None")
        return
  
    result_data = task.result_data
    
    code = result_data.get('code', None)
    
    #if code and code != -4080:
    #    task.update_status(status=NEW)
    #else:
    print("system_error trail_failed_handlers: can't fix for task.id={0} result_data={1}".format(task.id, result_data))

    task.update_status(status=FAILED_NEED_ACTION)
    
    #log task
    scheduler_models.ActionLog.log(task, step='failed_handler', description="system_error")
