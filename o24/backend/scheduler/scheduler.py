from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Campaign, Prospects, Credentials
from o24.backend.models.shared import TaskQueue
from o24.globals import *
from .models import Priority, TaskLog
import o24.backend.handlers.jobs_map as jobs_map
import datetime
    
from o24.exceptions.exception_with_code import ErrorCodeException
from o24.exceptions.error_codes import *
    
    
class Scheduler():
    def __init__(self):
        pass
    
    ###################################### SCHEDULER CYCLE tasks  ##################################
    #################################################################################################
    
    def switch_priority(self):
        # We need to equally select tasks from TaskQueue
        # do_next = intro(0) or follow up(1)
        # follow up level = 0(update level=1)
        # The algo:
        # if do_next == intro(0):
        # **** execute all intro tasks (record_type=0)
        
        current_priority = Priority.get_priority()
        follow_ups = TaskQueue.objects(Q(record_type=FOLLOWUP))
    
        if follow_ups.count() <= 0:
            current_priority.do_next = INTRO
        else:
            follow_level = follow_ups.filter(followup_level=FOLLOWUP)
        current_priority.save()
    
        #Check if followup queue finished
        if current_priority.do_next == FOLLOWUP:
            if follow_ups.count() <=0:
                current_priority.do_next = INTRO
                
    
            left = TaskQueue.objects(Q(record_type=FOLLOWUP) and Q(followup_level=FOLLOWUP)).all()
            if len(left) <= 0:
                current_priority.do_next = INTRO
            return
         
        
        current_priority.save()
    
    
    def plan(self):
        #All tasks
    
        self.switch_priority()
    
        tasks = TaskQueue.get_ready()
        for_update = []
        logs = []
    
        for task in tasks:
            log = self._switch(task)
            
            for_update.append(task)
            if log:
                logs.append(log)
    
        if logs:
            TaskLog.update_logs(logs)
        
        if for_update:
            TaskQueue.update_tasks(for_update)
    
    
    def execute(self):
        tasks = TaskQueue.get_execute_tasks()
        
        task_update = []
        credential_update = []
        jobs = []
    
        #TODO: for each task based on type create job and send it to the queue
        for task in tasks:
            handler = jobs_map.JOBS_MAP.get(task.action_key, None)
            if not handler:
                continue
            
            job = handler.s(str(task.id))
            jobs.append(job)
    
            task.status = IN_PROGRESS
            task_update.append(task)

            credential_update.append(task.credentials_id)
        
        if task_update:
            TaskQueue.update_tasks(task_update)
        
        if credential_update:
            self.refresh_limits(credential_update)
    
        return jobs
    
    
    def refresh_limits(self, credential_ids):
        credentials = Credentials.list_credentials(credential_ids)
    
        updated = []
        for c in credentials:
            c.inc_limits(datetime.datetime.utcnow())
            c.warmup(datetime.datetime.utcnow())
            updated.append(c)

        Credentials.update_credentials(updated)


    def _switch(self, task):
        if task.status != READY:
            return None
        
        next_node = Funnel.next_node(task.current_node)
        log = TaskLog.create_log(task)
        if next_node:
            task.switch_task(next_node) 

        return log
    ###################################### CAMPAIGN START/PAUSE/RESUME ##################################
    #####################################################################################################
    def start_campaign(self, campaign):
        if campaign.status != NEW:
            raise ErrorCodeException(START_CAMPAIGN_ERROR, "You can start only NEW campaign, title={0} status={1}".format(campaign.title, campaign.status))

        prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
        
        prospect_ids = self._load_prospects(campaign, prospects)
        if not prospect_ids:
            raise Exception("Can't load_prospects campaign_title={0} prospect_ids={1}".format(campaign.title, prospect_ids))

        self._update_prospects(prospect_ids, status=IN_PROGRESS)    
        
        self._setup_scheduler_data(campaign)

        campaign.update_status(status=IN_PROGRESS)

    def pause_campaign(self, campaign):
        if not campaign.inprogress():
            raise Exception("Campaign already paused, title={0}".format(campaign.title))

        # TaskQueue.pause_tasks(campaign_id=campaign.id)

        campaign.update_status(status=PAUSED)

    def resume_campaign(self, campaign):
        if campaign.inprogress():
            raise Exception("Campaign already resumed, title={0}".format(campaign.title))

        # TaskQueue.resume_tasks(campaign_id=campaign.id)

        self._check_new_prospects(campaign)

        campaign.update_status(status=IN_PROGRESS)


    def add_prospects(self, campaign, prospects):
        ids = self._load_prospects(campaign, prospects)
        if not ids:
            raise Exception("Can't load_prospects campaign_title={0} ids={1}".format(campaign.title, ids))

        self._update_prospects(ids, status=IN_PROGRESS)


    def _check_new_prospects(self, campaign):
        prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
        if prospects:
            self.add_prospects(campaign, prospects)

    def _load_prospects(self, campaign, prospects):
        tasks = []

        for prospect in prospects:
            task = TaskQueue.create_task(campaign, prospect)
            tasks.append(task)

        inserted_tasks = TaskQueue.insert_tasks(tasks)
        prospect_ids = [t.prospect_id for t in inserted_tasks]
        
        return prospect_ids

    def _update_prospects(self, ids, status):
        Prospects.update_prospects(ids, status)

    def _setup_scheduler_data(self, campaign):
        Priority.create_priority(campaign)

