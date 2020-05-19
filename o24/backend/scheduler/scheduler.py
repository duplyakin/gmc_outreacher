from o24.backend import db
from o24.backend import app
import o24.backend.dashboard.models as models

from o24.backend.models.shared import TaskQueue, Funnel, Action, AsyncTaskQueue
from o24.globals import *
from .models import Priority, TaskLog
import o24.backend.handlers.jobs_map as jobs_map
import o24.backend.handlers.trail_handlers as trail_handlers

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
        follow_ups = TaskQueue.objects(Q(record_type=FOLLOWUP) & Q(status__ne=FINISHED))
    
        #if we don't have followups then we need to execute INTRO
        if follow_ups.count() <= 0:
            print("follow_ups.count() <= 0")
            current_priority.do_next = INTRO
            current_priority._commit()
            return

        #switch to INTRO if we did followups on the last round
        if current_priority.do_next == FOLLOWUP:
            print("current_priority.do_next == FOLLOWUP")
            current_priority.do_next = INTRO
            current_priority._commit()
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
                current_priority._commit()
                return

            if follow_ups.filter(followup_level=FOLLOWUP).count() <= 0:
                print("follow_ups.filter(followup_level=FOLLOWUP).count() <= 0")
                current_priority.followup_level = 0
                current_priority._commit()
                return
            current_priority._commit()
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
            if task.action_key in NON_3RD_PARTY_ACTION_KEYS:
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
        credentials = models.Credentials.list_credentials(credential_ids)
        now = datetime.datetime.now()

        updated = []
        for c in credentials:
            c.change_limits(now)
            updated.append(c)

        models.Credentials.update_credentials(updated)

        campaigns = Campaign.objects(status=IN_PROGRESS)
        campaigns_updated = []
        for campaign in campaigns:
            campaign.change_limits(now)
            campaigns_updated.append(campaign)
        
        models.Campaign.update_campaigns(campaigns_updated)

    def trail(self):
        tasks = TaskQueue.get_trail_tasks()
        for task in tasks:
            if task.status == FAILED:
                error_code = task.get_code()
                handler = trail_handlers.FAILED_HANDLERS.get(error_code, None)
                if handler is None:
                    handler = trail_handlers.FAILED_HANDLERS[TRAIL_UNKNOWN_ERROR]
                
                handler(task)
                continue

            elif task.status == CARRYOUT:
                action_key = task.action_key
                handler = trail_handlers.CARRYOUT_HANDLERS.get(action_key, None)
                if handler is None:
                    handler = trail_handlers.CARRYOUT_HANDLERS[CARRYOUT_DEFAULT_HANDLER]
                
                handler(task)
                continue
            else:
                print("Trail unknown status task.id={0} task.status={1} task.action_key={2}".format(task.id, task.status, task.action_key))
                continue
            

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
    def start_campaign(self, owner, campaign, input_data=None):
        if campaign.status != NEW:
            return self.resume_campaign(owner=owner, campaign=campaign)

        prospects = models.Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
        if not prospects:
            raise Exception("There is no prospects assigned to campaign")

        campaign._safe_start()

        prospect_ids = self._load_prospects(campaign, prospects)
        if not prospect_ids:
            campaign._safe_pause()
            raise Exception("Can't load_prospects campaign_title={0} prospect_ids={1}".format(campaign.title, prospect_ids))

        self._update_prospects(prospect_ids, status=IN_PROGRESS)    
        
        self._setup_scheduler_data(campaign)

        #campaign.update_status(status=IN_PROGRESS)
        #create async action for campaign
        AsyncTaskQueue.create_async_task(campaign_id=campaign.id, input_data=input_data)

    def pause_campaign(self, campaign):
        if not campaign.inprogress():
            return 
            
        # TaskQueue.pause_tasks(campaign_id=campaign.id)

        campaign._safe_pause()
        #campaign.update_status(status=PAUSED)

    def resume_campaign(self, owner, campaign):
        if campaign.inprogress():
            raise Exception("Campaign already resumed, title={0}".format(campaign.title))

        # TaskQueue.resume_tasks(campaign_id=campaign.id)

        self._check_new_prospects(owner=owner, campaign=campaign)

        campaign._safe_start()

        #campaign.update_status(status=IN_PROGRESS)
    @classmethod
    def safe_unassign_prospects(cls, owner_id, prospects_ids):
        if not owner_id or not prospects_ids:
            return 0

        scheduler = cls()
        #To unassign we need:
        # 1. Pause all campaigns prospects belongs to
        # 2. Remove all tasks from task_queue
        # 3. Update prospects assign_to=None

        campaigns_refs = models.Prospects.objects(owner=owner_id, id__in=prospects_ids).distinct('assign_to')
        if campaigns_refs:
            campaigns_ids = [c.id for c in campaigns_refs]
            campaigns = models.Campaign.objects(owner=owner_id, id__in=campaigns_ids)
            for campaign in campaigns:
                scheduler.pause_campaign(campaign)
        
        tasks_deleted = TaskQueue.safe_unassign_prospects(prospects_ids=prospects_ids)

        prospects_unassigned = models.Prospects._unassign_campaign(owner_id=owner_id, prospects_ids=prospects_ids)    

        return prospects_unassigned

    @classmethod
    def safe_assign_prospects(cls, owner_id, campaign, prospects_ids):
        if not campaign or not prospects_ids:
            return 0

        prospects_without_campaign = models.Prospects.filter_no_campaign(owner_id=owner_id, prospects_ids=prospects_ids)
        if not prospects_without_campaign:
            return 0
        
        scheduler = cls()

        res = scheduler.add_prospects(owner=owner_id, campaign=campaign, prospects=prospects_without_campaign)

        if type(res) != list:
            return 0

        return len(res)

    @classmethod
    def safe_start_campaign(cls, owner, campaign):
        if not campaign:
            raise Exception("No such campaign")

        scheduler = cls()
        scheduler.start_campaign(owner=owner, campaign=campaign)

    @classmethod
    def safe_pause_campaign(cls, campaign):
        if not campaign:
            raise Exception("No such campaign")

        scheduler = cls()
        scheduler.pause_campaign(campaign=campaign)


    @classmethod
    def safe_delete_campaign(cls, campaign):
        if not campaign:
            raise Exception("DELETE ERROR: No such campaign")

        if campaign.inprogress():
            raise Exception("DELETE ERROR: campaign in progress, stop it first")
        
        assigned_prospects = models.Prospects.get_prospects(campaign_id=campaign.id)
        if assigned_prospects:
            raise Exception("DELETE ERROR: campaign has prospects, unassign all prospects before delete")
        
        TaskQueue.delete_campaign(campaign_id=campaign.id)

        return campaign.delete()


    def add_prospects(self, owner, campaign, prospects):
        ids = self._load_prospects(campaign, prospects)
        if not ids:
            raise Exception("Can't load_prospects campaign_title={0} ids={1}".format(campaign.title, ids))
        
        self._update_prospects(ids=ids, status=IN_PROGRESS)

        models.Prospects._assign_campaign(owner_id=owner, prospects_ids=ids, campaign_id=campaign.id)

        return ids


    def _check_new_prospects(self, owner, campaign):
        prospects = models.Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
        if prospects:
            self.add_prospects(owner=owner, campaign=campaign, prospects=prospects)

    def _load_prospects(self, campaign, prospects):
        tasks = []

        for prospect in prospects:
            task = TaskQueue.create_task(campaign, prospect)
            tasks.append(task)

        inserted_tasks = TaskQueue.insert_tasks(tasks)
        prospect_ids = [t.prospect_id for t in inserted_tasks]
        
        return prospect_ids

    def _update_prospects(self, ids, status):
        models.Prospects.update_prospects(ids, status)

    def _setup_scheduler_data(self, campaign):
        Priority.get_priority()

