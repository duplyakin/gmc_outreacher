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

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()
    
    def is_true(self, result):
        return result.get('if_true', False)


class Funnel(db.Document):
    action = db.ReferenceField(Action, reverse_delete_rule=1)
    paramters = db.DictField()

    title = db.StringField()
    templates_required = db.DictField()
    template_key = db.StringField(default='')
    
    root = db.BooleanField(default=False)

    if_true = db.ObjectIdField(default=None)
    if_false = db.ObjectIdField(default=None)

    data = db.DictField() #any info here, like delay for DELAY action

    @classmethod
    def async_funnels(cls, owner=None):
        results = cls.objects(root=True).\
                only('id', 'title', 'template_key','templates_required', 'root')
        
        if results:
            return results.to_json()
        
        return []

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

    def get_template_key(self):
        return self.template_key

    def get_action_key(self):
        return self.action.key

    def check_true(self, result):
        return self.action.is_true(result)

    def update_data(self, data):
        
        json = data.get('json')
        root = data.get('root', None)
        if json:
            template_key = json.get('template_key', '')
            if template_key:
                self.template_key = template_key

            templates_required = json.get('templates_required', {})
            if root and not templates_required:
                raise Exception("ERROR: templates_required for root funnel can't be empty")
            
            if templates_required:
                self.templates_required = templates_required
        
            title = json.get('title', '')
            if root and not title:
                raise Exception("ERROR: title for root funnel can't be empty")
            
            if title:
                self.title = title


        if data.get('root', None):
            self.root = data.get('root')

        if data.get('action', None):
            self.action = data.get('action')

        if data.get('if_true', None):
            self.if_true = data.get('if_true')
        
        if data.get('if_false', None):
            self.if_false = data.get('if_false')
        
        if data.get('data', None):
            self.data = data.get('data')

        self._commit()
        

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()

# How TaskQueue works
# When the new task created status = NEW
# When the task added to job queue status = IN_PROGRESS
class TaskQueue(db.Document):
    current_node = db.ReferenceField(Funnel, reverse_delete_rule=1)
    action_key = db.StringField()

    status = db.IntField(default=NEW)
    ack = db.IntField(default=0)

    input_data = db.DictField()
    result_data = db.DictField()

    credentials_id = db.ObjectIdField()
    prospect_id = db.ObjectIdField(unique=True)
    campaign_id = db.ObjectIdField()
    
    record_type = db.IntField(default=0)
    followup_level = db.IntField(default=0)

    def decrypt_password(self, credentials_dict):
        data = credentials_dict.get('data', '')
        if not data:
            return
        
        password = data.get('password', '')
        if not password:
            return
        
        credentials_dict['password'] = decode_password(password)

    def _fill_input_data(self, campaign_id=None, prospect_id=None, credentials_id=None, template_key=''):
        self.input_data = {}

        #Input data format:
        #	credentials_data : {
        #        email : ‘dsafadsf’
        #        password: ‘dasfadadsf’	
        #    }
        #
        #    campaign_data: {
        #        start_url: “,...” // Ты это НЕ используешь,
        #            pages_total: 100
        #
        #        next_url: ‘linkedin.com/search?u=...’  // Тот search URL который надо использовать,
        #        page_count: 10,
        #    }
        #    template_data: {
        #        title: 'Hello from {company_url}'    
        #        body: ‘Hi {first_name}! I found your {linkedin} and follow up’’
        #    }
        #    prospect_data: {
        #        first_name: ‘Kirill’
        #        last_name: ‘Shilov’
        #        linkedin: ‘linkedin.com/shilov’,
        #        company_title: ‘howtotoken.com’
        #        ....
        #    }

        medium=''
        if credentials_id:
            credentials = models.Credentials.objects().get(id=credentials_id)
            if not credentials:
                raise Exception("_fill_input_data ERROR: can't find credentials_id={0}".format(credentials_id))
            
            self.input_data['credentials_data'] = credentials.get_data() 
            medium = credentials.get_medium()

        if campaign_id:
            campaign = models.Campaign.objects().get(id=campaign_id)
            if not campaign:
                raise Exception("_fill_input_data ERROR: can't find campaign_id={0}".format(campaign_id))
            
            self.input_data['campaign_data'] = campaign.get_data()
            
            if template_key:
                template_data = campaign.get_template_data(template_key=template_key, medium=medium)
                self.input_data['template_data'] = template_data

        if prospect_id:
            prospect =  models.Prospects.objects().get(id=prospect_id)
            if not prospect:
                raise Exception("_fill_input_data ERROR: can't find prospect_id={0}".format(prospect_id))

            self.input_data['prospect_data'] = prospect.get_data() 

        return self.input_data

    def switch_task(self, next_node, _commit=False):
        if not next_node:
            raise Exception("switch_task ERROR: next_node={0} can't be None".format(next_node))
        
        #Switch algo:
        #1 - Init states
        #2 - switch current_node pointer
        #3 - update credentials
        #4 - _fill_input_data

        #init sta
        self.status = NEW
        self.ack = 0

        self.result_data = {}

        self.record_type = FOLLOWUP
        self.followup_level = 0

        self.current_node = next_node
        self.action_key = next_node.get_action_key()

        self.credentials_id = models.Campaign.get_credentials_id(self.campaign_id, next_node)
        if not self.credentials_id:
            raise Exception("Can't find credentials for task.id={0} node_id={1}".format(self.id, next_node.id))

        template_key = next_node.get_template_key()
        self._fill_input_data(campaign_id=self.campaign_di, 
                                prospect_id=self.prospect_id, 
                                credentials_id=self.credentials_id, 
                                template_key=template_key)

        if _commit:
            self._commit()

    def acknowledge(self):
        self.ack = self.ack + 1
        return self.ack

    def update_status(self, status):
        self.status = status
        self._commit()
    
    def set_result(self, result):
        self.result_data = result
        self._commit()

    def last_action(self):
        if self.current_node.action.key in FINISHED_KEYS:
            return True
        
        return False

    def finish_task(self):
        self.status = FINISHED
        self._commit()

    def get_email_data(self):
        result = {}
        prospect = models.Prospects.objects(id=self.prospect_id).get()
        campaign = models.Campaign.objects(id=self.campaign_id).get()

        result['template'] = campaign.get_node_template(template_key=self.current_node.template_key,
                                                        medium='email')
        result['email_to'] = prospect.get_email()
        
        return result

    def get_code(self):
        return self.result_data.get('code', None)

    def get_campaign(self):
        if not self.campaign_id:
            return None
        
        return models.Campaign.objects(id=self.campaign_id).get()

    def get_result_data(self):
        return self.result_data

    def _resume(self):
        self.status = NEW
        self._commit()

    @classmethod
    def get_task(cls, task_id):
        return cls.objects(id=task_id).get()

    @classmethod
    def get_ready(cls):
        return TaskQueue.objects(status=READY)

    @classmethod
    def get_trail_tasks(cls):
        return TaskQueue.objects(Q(status=FAILED) | Q(status=CARRYOUT))

    @classmethod
    def get_execute_tasks(cls, do_next, followup_level, now):
        
        # Which tasks are ready for execution:
        # OUTPUT: list of UNIQUE(credentials_id)
        # REMOVE:
        # **** remove credentials_id tasks.status == IN_PROGRESS
        # **** remove tasks.id where campaign.status == PAUSE
        # ADD:
        # now >= crededentials.next_action
        # now >= campaign.next_action
        # tasks.record_type == Priority.do_next
        # if tasks.followup_level == 1 then check tasks.followup_level == Priority.followup_level
        credentials_ids_in_progress = TaskQueue.objects(status=IN_PROGRESS).distinct('credentials_id')
        
        query = {"$match": {"record_type" : {"$eq" : INTRO} }}
        if (do_next == 1):
            query = {"$match" : {"record_type" : {"$eq" : FOLLOWUP}, "followup_level" : {"$eq" : followup_level}}}
        
        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "campaign_id",
                "foreignField" : "_id",
                "as" : "campaign_docs"
            }},
            { "$unwind" : "$campaign_docs" },
            {"$match" : { 
                "campaign_docs.status" : {"$eq" : IN_PROGRESS}, 
                'campaign_docs.next_action' : {'$lte' : now}
            }},
            {"$lookup" : {
                "from" : "credentials",
                "localField" : "credentials_id",
                "foreignField" : "_id",
                "as" : "cr_docs"
            }},
            { "$unwind" : "$cr_docs" },
            {"$match" : { "cr_docs.next_action" : { "$lte" : now},
                "cr_docs._id" : { "$nin" : credentials_ids_in_progress}
             } },
             query,
            {"$group" : {"_id": "$credentials_id", "task_id" : { "$first" : "$_id" }}},
        ]

        new_tasks = list(TaskQueue.objects(status=NEW).aggregate(*pipeline))
        tasks_ids = [x.get('task_id') for x in new_tasks]

        execute_tasks = TaskQueue.objects(Q(id__in=tasks_ids))
        return execute_tasks


    @classmethod
    def safe_unassign_prospects(cls, prospects_ids):
        return cls.objects(prospect_id__in=prospects_ids).delete()

    @classmethod
    def delete_campaign(cls, campaign_id):
        return cls.objects(campaign_id=campaign_id).delete()

    @classmethod
    def create_task(cls, campaign, prospect, test_crededentials_dict=None, _commit=False):
        new_task = cls()

        _node = campaign.funnel

        new_task.current_node = _node

        new_task.action_key = _node.get_action_key()
        new_task.credentials_id = models.Campaign.get_credentials_id(campaign.id, _node)
        if not new_task.credentials_id:
            raise Exception("create_task ERROR: Can't find credentials for node_id={0}".format(_node.id))

        if test_crededentials_dict:
            new_task.credentials_id = test_crededentials_dict.get('credentials_id')
            new_task.action_key = test_crededentials_dict.get('action_key')

        prospect_id = None
        if prospect:
            new_task.prospect_id = prospect.id
            prospect_id = new_task.prospect_id

        new_task.campaign_id = campaign.id
        new_task.status = NEW

        template_key = _node.get_template_key()
        new_task._fill_input_data(campaign_id=campaign.id, 
                                prospect_id=prospect_id, 
                                credentials_id=new_task.credentials_id, 
                                template_key=template_key)

        if _commit:
            new_task._commit(_reload=True)

        return new_task

    @classmethod
    def update_tasks(cls, tasks):
        if not tasks:
            return None
        
        for task in tasks:
            task._commit()

        #TaskQueue.objects.update(tasks, multi=True)

    @classmethod
    def insert_tasks(cls, tasks):
        if not tasks:
            return None
        
        return TaskQueue.objects.insert(tasks, load_bulk=True)

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()

#We put async tasks here. 
class AsyncTaskQueue(db.Document):
    campaign_id = db.ObjectIdField(unique=True)

    input_data = db.DictField()
    result_data = db.DictField()

    def put_result_data(self, result_data):
        self.result_data = result_data
        self._commit()

    @classmethod
    def get_async_task(cls, campaign_id):
        return cls.objects(campaign_id=campaign_id).first()

    @classmethod
    def create_async_task(cls, campaign_id, input_data=None):
        if not campaign_id:
            raise Exception("Can't create async task for campaign_id:{0}".format(campaign_id))

        exist = cls.objects(campaign_id=campaign_id).first()
        if exist:
            return exist

        new_task = cls()
        if input_data:
            new_task.input_data = input_data
        
        new_task.campaign_id = campaign_id
        
        new_task._commit()
        return new_task

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()

class OpenTracker(db.Document):
    #open, reply
    action_type = db.IntField()
    
    count = db.IntField()    
    
    #email, linkedin, twitter
    medium = db.StringField()

    #based on medium, check different tables: Mailbox, Linkedin, Twitter
    ref = db.ObjectIdField()

    action_meta = db.DictField()

    created = db.DateTimeField( default=datetime.datetime.now() )

