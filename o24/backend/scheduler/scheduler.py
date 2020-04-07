from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Campaign, Prospects, Credentials
from o24.backend.models.shared import TaskQueue, Funnel, Action
from o24.globals import *
from .models import Priority, TaskLog
import o24.backend.handlers.jobs_map as jobs_map
import datetime
from mongoengine.queryset.visitor import Q

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
        # follow up level = 0(reserve the current followups) 1(execute followup_level=1 until finished)
        
        current_priority = Priority.get_priority()
        follow_ups = TaskQueue.objects(Q(record_type=FOLLOWUP) and Q(status__ne=FINISHED))
    
        #if we don't have followups then we need to execute INTRO
        if follow_ups.count() <= 0:
            print("follow_ups.count() <= 0")
            current_priority.do_next = INTRO
            current_priority.save()
            return

        #switch to INTRO if we did followups on the last round
        if current_priority.do_next == FOLLOWUP:
            print("current_priority.do_next == FOLLOWUP")
            current_priority.do_next = INTRO
            current_priority.save()
            return

        #switch to followup if we did INTRO on the last round
        if current_priority.do_next == INTRO:
            current_priority.do_next = FOLLOWUP
            print("current_priority.do_next == INTRO")

            # we need to check followup_level
            if current_priority.followup_level == 0:
                print("current_priority.followup_level == 0")
                follow_ups.update(followup_level=FOLLOWUP)
                current_priority.followup_level = 1
                current_priority.save()
                return

            if follow_ups.filter(followup_level=FOLLOWUP).count() <= 0:
                print("follow_ups.filter(followup_level=FOLLOWUP).count() <= 0")
                current_priority.followup_level = 0
                current_priority.save()
                return
            current_priority.save()
            return    
    
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
    
    
    def execute(self, now):
        current_priority = Priority.get_priority()
        do_next = current_priority.do_next
        followup_level = current_priority.followup_level

        tasks = TaskQueue.get_execute_tasks(do_next=do_next, followup_level=followup_level, now=now)
        
        task_update = []
        credential_update = []
        jobs = []
    
        #TODO: for each task based on type create job and send it to the queue
        for task in tasks:
            handler = jobs_map.JOBS_MAP.get(task.action_key, None)
            if not handler:
                raise Exception("There is no handler for key:{0}".format(task.action_key))
            
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
    
    #Inc counters for each credential (It will change next_action)
    #Refresh next_action for campaigns
    def refresh_limits(self, credential_ids):
        credentials = Credentials.list_credentials(credential_ids)
        now = datetime.datetime.now()

        updated = []
        for c in credentials:
            c.change_limits(now)
            updated.append(c)

        Credentials.update_credentials(updated)

        campaigns = Campaign.objects(status=IN_PROGRESS).all()
        campaigns_updated = []
        for campaign in campaigns:
            campaign.change_limits(now)
            campaigns_updated.append(campaign)
        
        Campaign.update_campaigns(campaigns_updated)

    def _switch(self, task):
        if task.status != READY:
            return None
        
        next_node = Funnel.next_node(task.current_node, 
                                    task.result_data)
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
        Priority.get_priority()

