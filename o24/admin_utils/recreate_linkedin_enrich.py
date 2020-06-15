import os
import o24.config as config
from o24.backend import app
from o24.backend import db

import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
import o24.backend.scheduler.models as scheduler_models

from o24.globals import *
from datetime import datetime  
from datetime import timedelta  
from pytz import timezone
import pytz
import json
from pprint import pprint
import time 
import sys
from o24.backend.handlers.trail_carryout_handlers import start_linkedin_enrichment_campaign

def restart_linkedin_enrich():
    task_id = sys.argv[1]

    task = shared.TaskQueue.objects(id=task_id).first()
    if not task:
        raise Exception("Can't find task_id:{0}".format(task_id))
    
    start_linkedin_enrichment_campaign(task)

if __name__ == '__main__':
    restart_linkedin_enrich() 

#python -m o24.admin_utils.recreate_linkedin_enrich <task_id>