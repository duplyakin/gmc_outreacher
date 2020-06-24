import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
from o24.globals import *
import datetime
from mongoengine.queryset.visitor import Q
import o24.backend.scheduler.models as scheduler_models
import o24.backend.handlers.trail_carryout_handlers as carryout_handlers

def system_error(task):
    if not task:
        print("system_error: task is None")
        return
    
    if task.action_key == LINKEDIN_SEARCH_ACTION:
        campaign = task.get_campaign()
        if campaign:
            carryout_handlers._save_search_data(task=task, campaign=campaign)
            campaign._safe_pause(message='Finished parsing')

    result_data = task.result_data
    
    task.update_status(status=FAILED_NEED_ACTION)
    
    #log task
    scheduler_models.ActionLog.log(task, step='failed_handler', description="system_error")
