from o24.backend import db
from o24.backend import app
from o24.globals import *

import o24.backend.dashboard.models as models 
from mongoengine.queryset.visitor import Q
import datetime

class Action(db.Document):
    #shared field
    action_type = db.IntField(default=0)
    data = db.DictField()
    medium = db.StringField()
    key = db.StringField()

    @classmethod
    def create_action(cls, data):
        new_action = cls()

        new_action.action_type = data.get('action_type')
        new_action.data = data.get('data')
        new_action.medium = data.get('medium')
        new_action.key = data.get('key')


        new_action._commit()
        return new_action
    
    @classmethod
    def get_by_key(cls, key):
        action = cls.objects(key=key).first()
        return action

    def _commit(self):
        self.save()
    
    def is_true(self, result):
        if self.action_type == ACTION_NONE:
            pass
            #TODO: custom action checks can be implemented
        else:
            return result.get('if_true', False)


class Funnel(db.Document):
    action = db.ReferenceField(Action)
    paramters = db.DictField()

    root = db.BooleanField(default=False)

    if_true = db.ObjectIdField(default=None)
    if_false = db.ObjectIdField(default=None)

    template = db.DictField()

    @classmethod
    def next_node(cls, current_node, result):
        next_node = None
        
        action = current_node.action

        is_true = action.is_true(result)
        if is_true:
            next_node = Funnel.objects(id=current_node.if_true).get()
        else:
            next_node = Funnel.objects(id=current_node.if_false).get()

        return next_node
        

    @classmethod
    def get_random(cls):
        funnel = cls.objects(root=True).first()
        return funnel

    @classmethod
    def get_node(cls, node_id):
        node = cls.objects(id=node_id).first()
        return node

    @classmethod
    def create_node(cls, data):
        new_funnel = cls()

        new_funnel.update_data(data)

        return new_funnel

    def get_action_key(self):
        return self.action.key

    def update_data(self, data):

        if data.get('root', None):
            self.root = data.get('root')
        
        if data.get('action', None):
            self.action = data.get('action')

        if data.get('if_true', None):
            self.if_true = data.get('if_true')
        
        if data.get('if_false', None):
            self.if_false = data.get('if_false')

        self._commit()
        

    def _commit(self):
        self.save()

# How TaskQueue works
# When the new task created status = NEW
# When the task added to job queue status = IN_PROGRESS
class TaskQueue(db.Document):
    current_node = db.ReferenceField(Funnel)
    action_key = db.StringField()

    status = db.IntField(default=NEW)
    ack = db.IntField(default=0)

    credentials_dict = db.DictField()
    credentials_id = db.ObjectIdField()

    result_data = db.DictField()

    prospect_id = db.ObjectIdField(unique=True)
    campaign_id = db.ObjectIdField()
    
    record_type = db.IntField(default=0)
    followup_level = db.IntField(default=0)

    def switch_task(self, next_node):
        
        #init to 0
        self.current_node = next_node
        self.status = NEW
        self.ack = 0

        self.result_data = {}

        self.record_type = 0
        self.followup_level = 0

        self.credentials_dict = models.Campaign.get_credentials(self.campaign_id, next_node)
        self.credentials_id = self.credentials_dict.get('id', None)

        self.action_key = self.current_node.get_action_key()

    def acknowledge(self):
        self.ack = self.ack + 1
        return self.ack

    @classmethod
    def get_task(cls, task_id):
        return cls.objects(id=task_id).get()

    @classmethod
    def get_ready(cls):
        return TaskQueue.objects(status=READY).all()

    @classmethod
    def get_execute_tasks(cls):
        
        #TODO: filter only campaigns with now in schedule_period
        #campaign_ids = Campaign.for_schedule(datetime.datetime.now())

        credential_in_progress = [c.get('credentials_id') for c in TaskQueue.objects(status=IN_PROGRESS).only('credentials_id').all().as_pymongo()]
        credential_ready = models.Credentials.ready_now(datetime.datetime.now())

        #We received tasks that we can put to the JOB queue:
        # now() in campaigns_schedule_interval
        # now() >= credentials.next_action
        # credentials_id doesn't have another task with status = IN_PROGRESS (BECAUSE we can't execute more than 1 credential simulteniously)
        new_tasks = TaskQueue.objects(Q(status=NEW) & 
                                    Q(credentials_id__in=credential_ready) & 
                                    Q(credentials_id__nin=credential_in_progress)).all().distinct('credentials_id')

        return new_tasks


    @classmethod
    def pause_tasks(cls, campaign_id):
        TaskQueue.objects(Q(campaign_id=campaign_id) & Q(status__in=TASKS_CAN_BE_PAUSED)).update(status=PAUSED)

    @classmethod
    def resume_tasks(cls, campaign_id):
        TaskQueue.objects(Q(campaign_id=campaign_id) & Q(status__in=TASKS_CAN_BE_RESUMED)).update(status=IN_PROGRESS)

    @classmethod
    def create_task(cls, campaign, prospect):
        new_task = cls()
        new_task.current_node = campaign.funnel
        
        new_task.credentials_dict = models.Campaign.get_credentials(campaign.id, new_task.current_node)
        new_task.credentials_id = new_task.credentials_dict.get('id', None)

        new_task.prospect_id = prospect.id
        new_task.campaign_id = campaign.id

        new_task.action_key = new_task.current_node.get_action_key()

        return new_task

    @classmethod
    def update_tasks(cls, tasks):
        if not tasks:
            return None
        
        for task in tasks:
            task.save()

        #TaskQueue.objects.update(tasks, multi=True)

    @classmethod
    def insert_tasks(cls, tasks):
        if not tasks:
            return None
        
        return TaskQueue.objects.insert(tasks, load_bulk=True)
