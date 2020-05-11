from o24.backend import db
from o24.backend import app

from datetime import datetime  
from datetime import timedelta  

from flask_user import UserManager, UserMixin
import uuid
from mongoengine.queryset.visitor import Q
import json
import traceback

from werkzeug.security import check_password_hash, generate_password_hash
from o24.globals import *
import o24.config as config

from passlib.context import CryptContext

import o24.backend.models.shared as shared
import o24.backend.scheduler.scheduler as scheduler

from bson import ObjectId
from bson.json_util import dumps as bson_dumps
from o24.backend.utils.filter_data import *
from o24.backend.utils.helpers import template_key_dict 
from o24.backend.dashboard.serializers import JSCampaignData
from o24.backend.utils.aes_encode import *

class User(db.Document, UserMixin):
    email = db.EmailField(unique=True)
    password = db.StringField()

    active = db.BooleanField(default=True)
    current_oauth_state = db.StringField()

    # Relationships
    roles = db.ListField(db.StringField(), default=[])

    created = db.DateTimeField( default=datetime.now() )

    @classmethod
    def create_user(cls, data):
        new_user = cls()

        password_crypt_context = CryptContext(
            schemes=["pbkdf2_sha256"])

        new_user.email = data.get('email')
        new_user.password = password_crypt_context.hash(data.get('password'))
        new_user.active = data.get('active')

        new_user._commit()
        return new_user
    
    @classmethod
    def get_user(cls, email):
        user = cls.objects(email=email).first()
        return user


    def get_oauth_state(self):
        if not self.current_oauth_state or self.current_oauth_state == '':
            self.current_oauth_state = self._generate_ouath_state()
            self._commit()
        
        return self.current_oauth_state

    def _generate_ouath_state(self):
        state = uuid.uuid4().hex

        return state


    def _commit(self):
        self.save()
        self.reload()

    def __repr__(self):
        return '<User %r>' % (self.email)

# Customize Flask-User
class CustomUserManager(UserManager):

    def customize(self, app):
        pass
        # Configure customized forms
        #self.RegisterFormClass = CustomRegisterForm
        #self.LoginFormClass = CustomLoginForm

    # Override the default password validator
    def captcha_validator(form, field):
        pass

    # Override the default password validator
    def invite_validator(form, field):
        pass

user_manager = CustomUserManager(app, db, User)



#### Menu: Outreach Accounts ####
#### Store data to access external accounts
class Credentials(db.Document):
    SHOWED_MEDIUM = ['linkedin', 'email']

    owner = db.ReferenceField(User, reverse_delete_rule=1)
    
    # 0 - Fresh or just created
    # 1 - Refreshed (need to update all tasks)
    # -1 - Failed
    status = db.IntField(default=0)
    
    medium = db.StringField()

    data = db.DictField()
    
    last_action = db.DateTimeField(default=datetime.now())
    next_action = db.DateTimeField(default=datetime.now())

    #limits and schedule
    limit_per_day = db.IntField(default=DEFAULT_PER_DAY_LIMIT)

    limit_per_hour = db.IntField(default=0) #NOT USED
    limit_interval = db.IntField(default=DEFAULT_INTERVAL) #in seconds

    current_daily_counter = db.IntField(default=0)
    current_hourly_counter = db.IntField(default=0) #NOT USED

    @classmethod
    def ready_ids(cls, utc_now):
        #ids = [p.get('_id') for p in cls.objects(next_action__lte=utc_now).only('id').all().as_pymongo()]
        ids = cls.objects(next_action__lte=utc_now, status=0).distinct('id')
        return ids

    @classmethod
    def create_credentials(cls, owner, new_data, medium, limit_per_day=None):
        exist = None

        #hash password
        #password = new_data.get('password', '')
        #if password:
        #    new_data['password'] = encode_passowrd(password)

        account = new_data.get('account', '')
        if account:
            exist = Credentials.objects(owner=owner, data__account=account).first()

        if not exist:
            exist = cls()

        if (limit_per_day is not None) and (limit_per_day > 0):
            exist.limit_per_day = limit_per_day

        exist.owner = owner
        exist.medium = medium
        exist.data = new_data
        
        exist.status = 0
        
        exist._commit()

        return exist
     

    def safe_delete_credentials(self):
        campaign_assigned = Campaign.objects(owner=self.owner, credentials__in=[self.id]).first()
        if campaign_assigned:
            account = self.data.get('account', '')
            error = "Can't delete credentials for account:{0} - you have campaign assigned, delete campaign first".format(account)
            raise Exception(error)
        
        return self.delete()


    @classmethod
    def get_credentials(cls, user_id, medium=None, sender=None):
        if medium is not None:
            return cls.objects(owner=user_id, medium=medium).first()

        if sender is not None:
            return cls.objects(owner=user_id, data__sender=sender).first()

        return None

    @classmethod
    def async_credentials(cls, owner, page=None, per_page=config.CREDENTIALS_PER_PAGE):
        if page and page <= 1:
            page = 1

        query = {
            'owner' : owner
        }

        db_query = cls.objects(__raw__=query, medium__in=cls.SHOWED_MEDIUM). \
                    only('id', 'data', 'status', 'medium', 'limit_per_day', 'last_action', 'next_action', 'current_daily_counter')
        
        total = db_query.count()
        results = []
        if page is not None:
            results = db_query.skip(per_page * (page-1)).limit(per_page).order_by('status')
        else:
            results = db_query.order_by('status')
        
        if results:
            results = results.to_json()

        return (total, results)


    @classmethod
    def list_credentials(cls, credential_ids):
        return cls.objects(Q(id__in=credential_ids))

    @classmethod
    def update_credentials(cls, arr):
        if not arr:
            return None

        for e in arr:
            e._commit()
        #cls.objects.update(arr)

    def get_account(self):
        return self.data['account']

    def get_data(self):
        return self.data


    def change_limits(self, now):
        self.current_daily_counter = self.current_daily_counter + 1

        self.last_action = self.next_action
        if self.current_daily_counter >= self.limit_per_day:
            #switch action to the next day
            self.next_action = now + timedelta(seconds=NEXT_DAY_SECONDS)
            self.current_daily_counter = 0
            self.warmup()
        else:
            self.next_action = now + timedelta(seconds=self.limit_interval)        

    def _check_for_duplicates(self, data):
        #check duplicates:
        account = data.get('account', '')
        if account:
            exist = Credentials.objects(owner=self.owner, data__account=account, id__ne=self.id).first()
            if exist:
                error = "Credentials duplicate error for account: {0}".format(account)
                raise Exception(error)

    def safe_update_credentials(self, credentials_data):
        limit_per_day = credentials_data.get_limit_per_day()
        if limit_per_day:
            self.limit_per_day = limit_per_day
        
        data = credentials_data.get_data()
        if data:
            self.update_data(new_data=data, _commit=False)
        
        self._commit()

    def update_data(self, new_data, _commit=True):
        if not isinstance(new_data, dict):
            raise Exception("Can't update_data, new_data is not dict object")
        
        if not new_data:
            return 0

        self._check_for_duplicates(new_data)
        for key, val in new_data.items():
            if val is not None:
                self.data[key] = val
        
        #refreshed data
        self.status = 1

        if _commit:
            self._commit()
    
    def change_status(self, status):
        self.status = status
        self._commit()

    def warmup(self):
        self.limit_per_day = round(self.limit_per_day * 1.3)

    def _commit(self):
        self.save()
        self.reload()

#### Menu: Teams ####
#### Manage teams
class Team(db.Document):
    admin = db.ReferenceField(User, reverse_delete_rule=1)
    
    title = db.StringField()
    members = db.ListField(db.ReferenceField(User, reverse_delete_rule=1))

    @classmethod
    def create_team(cls, data):
        new_team = cls()

        new_team.admin = data.get('admin')
        new_team.title = data.get('title')
        new_team.members = data.get('members')

        new_team._commit()

        return new_team

    def _commit(self):
        self.save()
        self.reload()

class Campaign(db.Document):
    RESTRICTED_SET_FIELDS = [
        'owner',
        'id',
        '_id',
        'status',
        'last_action',
        'next_action',
        'data',
        'created'
    ]

    CAN_BE_NULL = ['from_hour', 'to_hour', 'from_minutes', 'to_minutes', 'status']

    @classmethod
    def get_create_fields(cls):
        return cls._fields.keys()

    owner = db.ReferenceField(User, reverse_delete_rule=1, required=True)
    # 0 - created
    # 1 - in progress
    # 2 - paused
    # 11 - archived (deleted)
    status = db.IntField(default=0)

    title = db.StringField(required=True)

    credentials = db.ListField(db.ReferenceField(Credentials, reverse_delete_rule=1))

    funnel = db.ReferenceField(shared.Funnel, reverse_delete_rule=1)
    
    #get from timeTable
    sending_days = db.DictField(default=DEFAULT_SENDING_DAYS)
    from_hour = db.IntField(default=DEFAULT_FROM_HOUR)
    from_minutes = db.IntField(default=0)
    to_hour = db.IntField(default=DEFAULT_TO_HOUR)
    to_minutes = db.IntField(default=0)
    time_zone = db.StringField(default='')

    templates = db.DictField()

    data = db.DictField()

    last_action = db.DateTimeField(default=datetime.now())
    next_action = db.DateTimeField(default=datetime.now())

    created = db.DateTimeField( default=datetime.now() )


    @classmethod
    def async_campaigns_list(cls, owner, page=None, per_page=config.CAMPAIGNS_PER_PAGE):
        if page and page <= 1:
            page = 1

        db_query = cls.objects(owner=owner)
                
        total = db_query.count()

        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "credentials",
                "localField" : "credentials",
                "foreignField" : "_id",
                "as" : "credentials"
            }},
            {"$lookup" : {
                "from" : "funnel",
                "localField" : "funnel",
                "foreignField" : "_id",
                "as" : "funnel"
            }},
            { "$unwind" : { "path" : "$funnel", "preserveNullAndEmptyArrays": True }},
            { "$project" : { 
                'status' : 1,
                'data' : 1,
                'title' : 1,
                'credentials' : 1,
                'funnel' : 1
            }}
        ]

        campaigns = []
        if page is not None:
            campaigns = list(db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').aggregate(*pipeline))
        else:
            campaigns = list(db_query.order_by('-created').aggregate(*pipeline))

        results = bson_dumps(campaigns)

        return (total, results)

    @classmethod
    def get_campaign_for_list(cls, owner_id, list_id):
        return cls.objects(owner=owner_id, prospects_list=list_id).first()

    @classmethod
    def get_campaign(cls, owner=None, id=None, title=None):
        
        campaign = None
        if owner:
            campaign = cls.objects(owner=owner, id=id).first()
        if title:
            campaign = cls.objects(title=title).first()
        elif id:
            campaign = cls.objects(id=id).first()

        return campaign

    @classmethod
    def create_campaign(cls, data, owner):
        new_campaign = cls()

        new_campaign.owner = owner

        new_campaign.title = data.get('title', '')
        new_campaign.credentials = data.get('credentials')
        new_campaign.funnel = data.get('funnel')

        if data.get('templates', ''):
            new_campaign.templates = data.get('templates')
        
        if data.get('time_table', ''):
            timeTable = data.get('time_table')
            new_campaign.sending_days = timeTable.get('sending_days')
            new_campaign.from_hour = timeTable.get('from_hour')
            new_campaign.to_hour = timeTable.get('to_hour')
            new_campaign.time_zone = timeTable.get('time_zone')


        new_campaign.data = data.get('data')

        new_campaign.status = NEW

        new_campaign._commit()
        return new_campaign
    
    @classmethod
    def get_credentials(cls, campaign_id, funnel_node):
        campaign = cls.objects(id=campaign_id).get()

        medium = funnel_node.action.medium

        credentials_dict = {}
        for c in campaign.credentials:
            if c.medium == medium:
                credentials_dict['id'] = c.id
                credentials_dict['data'] = c.data
                credentials_dict['medium'] = medium
                break
        
        return credentials_dict
                
    @classmethod
    def update_campaigns(cls, campaigns):
        if not campaigns:
            return None

        for c in campaigns:
            c._commit()

    def valid_funnel(self):
        if self.funnel == None:
            return False
        
        return True

    def get_node_template(self, template_key, medium):
        if not template_key:
            return ''
        
        if not medium:
            raise Exception("ERROR: get_node_template, medium can't be empty")
        
        templates_for_medium = self.templates.get(medium, '')
        if not templates_for_medium:
            return ''
        
        template = templates_for_medium.get(template_key, '')
        return template

    def change_limits(self, now):
        current_hour = now.hour
        current_day = now.day

        if current_hour >= self.to_hour:
            self.last_action = self.next_action

            days_delta = self.days_delta(current_day)

            next_t = now + timedelta(days=days_delta)
            self.next_action = next_t.replace(hour=self.from_hour, minutes=0)
    

    def days_delta(self, current_day):
        delta = 1
        next_day = current_day + 1
        a = self.sending_days

        for i in range(6):
            if next_day > 6:
                next_day = 0

            if a.get(str(next_day)):
                break

            delta = delta + 1
            next_day = next_day + 1

        return delta

    def _safe_pause(self):
        self.update_status(status=PAUSED)

    def _safe_start(self):
        if self.inprogress():
            raise Exception("Starting error: campaign already in progress")
        
        if not self.funnel:
            raise Exception("Starting error: there is not selected funnel for campaign_id:{0}".format(self.id))
        
        has_prospects = Prospects.get_prospects(campaign_id=self.id)
        if not has_prospects:
            raise Exception("Starting error: There is no assigned prospects for this campaign")

        self.update_status(status=IN_PROGRESS)


    def _validate_campaign_data(self, owner, campaign_data, changed_fields):

        if 'title' in changed_fields:
            title = campaign_data.title()
            if not title:
                raise Exception("Title can't be empty")
            
            exist = None
            if self.id is not None:
                exist = Campaign.objects(owner=owner, id__ne=self.id, title=title).first()
            else:
                exist = Campaign.objects(owner=owner, title=title).first()

            if exist:
                raise Exception("Campaign with this title already exist")


    def _async_set_field(self, field_name, val):
        if field_name == 'title':
            if not val:
                raise Exception("Campaign title can't be empty")

            self.title = val
        else:
            setattr(self, field_name, val)

    def async_edit(self, owner, campaign_data, edit_fields, restricted_fields=None):
        if not restricted_fields:
            restricted_fields = self.RESTRICTED_SET_FIELDS

        self._validate_campaign_data(owner=owner, campaign_data=campaign_data, changed_fields=edit_fields)

        for field in edit_fields:
            if field in restricted_fields:
                continue

            val = campaign_data.get_field(field)
            if val:
                self._async_set_field(field_name=field, val=val)
            elif field in self.CAN_BE_NULL:
                self._async_set_field(field_name=field, val=val)
        
        self._commit()
        return True

    @classmethod
    def async_create(cls, owner, campaign_data, create_fields, restricted_fields=None):
        if not restricted_fields:
            restricted_fields = cls.RESTRICTED_SET_FIELDS

        new_campaign = cls()
        new_campaign.owner = owner

        new_campaign._validate_campaign_data(owner=owner, campaign_data=campaign_data, changed_fields=create_fields)

        for field in create_fields:
            if field in restricted_fields:
                continue
    
            val = campaign_data.get_field(field)
            if val:
                new_campaign._async_set_field(field_name=field, val=val)
            elif field in cls.CAN_BE_NULL:
                new_campaign._async_set_field(field_name=field, val=val)

        new_campaign._commit()
        return new_campaign


    def inprogress(self):
        if self.status == 1:
            return True
        
        return False

    def update_status(self, status):
        self.status = status
        self._commit()

    def _commit(self):
        self.save()
        self.reload()




class ProspectsList(db.Document):
    owner = db.ReferenceField(User, reverse_delete_rule=1)
    
    title = db.StringField()

    created = db.DateTimeField( default=datetime.now() )
    
    # 0 - just created
    # 1 - in progress
    # 2 - paused
    # 3 - finished

    @classmethod
    def async_aggreagte_lists(cls, owner_id):
        pipeline = [
            {"$lookup" : {
                "from" : "prospects",
                "let" : { "list_id": "$_id"},
                "pipeline" : [
                        {"$match": { "owner": owner_id } },
                        {"$group" : {
                            '_id':"$assign_to_list", 
                            'count' : {'$sum' : 1},
                            "owner": { "$first": "$owner"},
                            }
                        },
                        { "$match":
                            { "$expr":
                                { "$and":
                                    [
                                        { "$ne" :["$_id", None] },
                                        { "$eq": [ "$_id",  "$$list_id" ] },
                                    ]
                                }
                            }
                        },
                ],
                "as" : "grouped_prospects"
            }},
            {
                "$project" : {
                    "_id" : 1,
                    "title" : 1,
                    "grouped_prospects" : 1,
                    "total" : {
                        "$map" : {
                                "input" : "$grouped_prospects",
                                "as": "g",
                                "in" : { "$cond": {
                                            "if": {"$ne": ["$$g.count", None]},
                                            "then": "$$g.count",
                                            "else": 0
                                                }
                                        }
                        }
                    }
                }
            }
        ]


        lists = list(ProspectsList.objects(owner=owner_id).aggregate(*pipeline))

        sz = bson_dumps(lists)
        return sz


    @classmethod
    def async_lists(cls, owner_id, page=1):
        db_query = cls.objects(owner=owner_id). \
                    only('id', 'title')
        
        total = db_query.count()
        prospects_list = db_query.order_by('-created')

        results = prospects_list.to_json()
        return (total, results)

    @classmethod
    def get_lists(cls, owner, title=None, id=None):
        if title:
            return cls.objects(owner=owner, title=title).first()
        elif id is not None:
            return cls.objects(owner=owner, id=id).first()
        else:
            return cls.objects(owner=owner)

    @classmethod
    def create_list(cls, owner_id, title):
        new_list = cls()
        
        new_list.owner = owner_id
        new_list.title = title

        new_list._commit()
        return new_list
    
    def serialize(self):
        return 0

    def update_data(self, title=None):
        if title:
            self.title = title
            self._commit()

    def safe_delete(self):
        has_prospects = Prospects.objects(assign_to_list=self.id).count()
        if has_prospects > 0:
            raise Exception("LIST DELETE ERROR: Remove prospects from the list, before delete")

        return self.delete()

    def _commit(self):
        self.save()
        self.reload()


class Prospects(db.Document):
    RESTRICTED_SET_FIELDS = [
        'owner',
        'id',
        '_id',
        'status',
        'created',
        'assign_to'
    ]

    MEDIUM = ['email', 'linkedin', 'Email', 'Linkedin']
    
    @classmethod
    def get_create_fields(cls):
        return cls._fields.keys()

    owner = db.ReferenceField(User, reverse_delete_rule=1)
    
    team = db.ListField(db.ReferenceField(Team, reverse_delete_rule=1))
    
    data = db.DictField()

    assign_to = db.ReferenceField(Campaign, reverse_delete_rule=1)
    
    # 0 - just created
    # 1 - in progress
    # 2 - paused
    # 3 - finished
    status = db.IntField(default=0)
    
    # DO_NOTHING (0) - don’t do anything (default).
    # NULLIFY (1) - Updates the reference to null.
    # CASCADE (2) - Deletes the documents associated with the reference.
    # DENY (3) - Prevent the deletion of the reference object.
    # PULL (4) - Pull the reference from a ListField of references
    assign_to_list = db.ReferenceField('ProspectsList')

    created = db.DateTimeField( default=datetime.now() )

    def serialize(self):
        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "assign_to",
                "foreignField" : "_id",
                "as" : "assign_to"
            }},
            { "$unwind" : { "path" : "$assign_to", "preserveNullAndEmptyArrays": True }},

            {"$lookup" : {
                "from" : "prospects_list",
                "localField" : "assign_to_list",
                "foreignField" : "_id",
                "as" : "assign_to_list"
            }},
            { "$unwind" : { "path" : "$assign_to_list", "preserveNullAndEmptyArrays": True }}
        ]

        prospect = list(Prospects.objects(id=self.id).aggregate(*pipeline))

        if len(prospect) > 0:
            prospect = prospect[0]

        sz = bson_dumps(prospect)

        return sz

    def _async_set_field(self, field_name, val):
        setattr(self, field_name, val)

    def _chek_for_duplicates(self, owner_id, data):
        if not data:
            return False
        
        query = {
            'owner' : owner_id,
            '_id' : { '$ne' : self.id }
        }

        check_duplicate = False
        or_array = []

        email = data.get('email','')
        if email:
            or_array.append(
                {
                    'data.email' : email
                }
            )
            check_duplicate = True

        linkedin = data.get('linkedin','')
        if linkedin:
            or_array.append(
                {
                    'data.linkedin' : linkedin
                }
            )
            check_duplicate = True

        if check_duplicate:
            query['$or'] = or_array
            duplicates = Prospects.objects(__raw__=query)
            if duplicates:
                error = "Duplicate found ERROR: email:{0} or linkedin:{1} exists".format(email, linkedin)
                raise Exception(error)


    def _validate_prospect_data(self, owner_id, prospect_data):
        
        assign_to_list = prospect_data.assign_to_list()
        if assign_to_list:
            exist = ProspectsList.objects(owner=owner_id, id=assign_to_list).first()
            if not exist:
                raise Exception("Prospect List doesn't exist")
        
        #check for email duplicate
        data = prospect_data.data()
        self._chek_for_duplicates(owner_id=owner_id, data=data)

        return True

    @classmethod
    def async_create(cls, owner_id, prospect_data, create_fields, restricted_fields=None):
        if not restricted_fields:
            restricted_fields = cls.RESTRICTED_SET_FIELDS

        new_prospect = cls()
        new_prospect.owner = owner_id

        new_prospect._validate_prospect_data(owner_id=owner_id, prospect_data=prospect_data)

        for field in create_fields:
            if field in restricted_fields:
                continue
    
            val = prospect_data.get_field(field)
            if val:
                new_prospect._async_set_field(field_name=field, val=val)

        new_prospect._commit()
        return new_prospect



    #we use this for test only
    @classmethod
    def create_prospect(cls, owner_id, data={}, list_id=None, campaign_id=None, commit=True):
        new_prospect = cls()

        new_prospect.owner = owner_id

        if data:
            new_prospect.data = data

        if list_id:
            new_prospect.assign_to_list = list_id

        obj_fields = cls.get_create_fields()

        prod_data = {}
        for key, val in data.items():
            if not data[key]:
                continue

            if key in obj_fields:
                setattr(new_prospect, key, data[key])
            else:
                prod_data[key] = val
        
        new_prospect.data = prod_data

        #DEPRECATED FIELDS USED BY TEST - need to remove
        if campaign_id:
            new_prospect.assign_to = campaign_id

        if commit:
            new_prospect._commit()

        return new_prospect

    @classmethod
    def filter_no_campaign(cls, owner_id, prospects_ids):
        return Prospects.objects(owner=owner_id, id__in=prospects_ids, assign_to=None)

    @classmethod
    def _unassign_campaign(cls, owner_id, prospects_ids):
        if not prospects_ids:
            return 0

        return Prospects.objects(owner=owner_id, 
                                id__in=prospects_ids).update(assign_to=None, status=NEW)

    @classmethod
    def _assign_campaign_on_create(cls, owner_id, campaign_id, prospects_ids):
        if not prospects_ids or not campaign_id:
            return 0

        return Prospects.objects(owner=owner_id,
                                assign_to=None, 
                                id__in=prospects_ids).update(status=NEW, assign_to=campaign_id)


    @classmethod
    def _assign_campaign(cls, owner_id, prospects_ids, campaign_id):
        if not prospects_ids or not campaign_id:
            return 0

        return Prospects.objects(owner=owner_id, 
                                id__in=prospects_ids).update(assign_to=campaign_id)


    #Only prospects that are not assigned to any campaign will be remove
    @classmethod
    def delete_prospects(cls, owner_id, prospects_ids):
        if not prospects_ids:
            return 0

        return Prospects.objects(owner=owner_id, id__in=prospects_ids, assign_to=None).delete()
    
    @classmethod
    def duplicates(cls, owner_id):
        def split_helper(obj, duplicates_dict):
            if not obj:
                return

            element = obj.get('_id', '')
            if not element:
                return 
            
            email = element.get('email','')
            if email:
                duplicates_dict['email'].append(email)

            linkedin = element.get('linkedin', '')
            if linkedin:
                duplicates_dict['linkedin'].append(linkedin)
        
            prospect_id = obj.get('prospect_id', '')
            if prospect_id:
                duplicates_dict['ids'].append(prospect_id)

        pipeline = [
            {"$group" : {
                "_id" : {
                    'email' : '$data.email',
                    'linkedin' : '$data.linkedin' 
                },
                "prospect_id" : {"$first" : { "$toString" : "$_id" }}
            }}        
        ]

        prospects = list(Prospects.objects(owner=owner_id).aggregate(*pipeline))

        duplicates = {
            'email' : [],
            'linkedin' : [],
            'ids' : []
        }

        q = [split_helper(p, duplicates) for p in prospects]

        return duplicates

    @classmethod
    def update_duplicates(cls, owner_id, new_data, values=[], list_id=None):
        duplicates = Prospects.objects(Q(owner=owner_id) & (Q(data__email__in=values) | Q(data__linkedin__in=values)))
        if not duplicates:
            return

        for prospect in duplicates:
            email = prospect.data.get('email', '')
            linkedin = prospect.data.get('linkedin', '')
            for data in new_data:
                if (data.get('email', '') and email == data['email']) or (data.get('linkedin', '') and linkedin == data['linkedin']):
                    prospect.data = data
                    if list_id:
                        prospect.assign_to_list = list_id
                    prospect._commit()
                    del data
                    break

    @classmethod
    def upload(cls, owner_id, csv_with_header, map_to, list_id, update_existing=0):

        prospects_list = []
        need_update = []
        duplicate_values = []

        #dict with
        # 'email' : [] (All current emails)
        # 'linkedin' : [] (All current linkedins)
        # 'ids' : [] (All ids)
        duplicates = cls.duplicates(owner_id=owner_id)

        i = 0
        for row in csv_with_header:
            i = i + 1

            #pass header
            if i == 1:
                continue

            data = {}
            found_duplicate = False
            just_pass = False
            for m_t in map_to.keys():
                row_data = row[m_t]
                field_name = map_to[m_t]

                data[field_name] = row_data
                if field_name in cls.MEDIUM:
                    #check if it exists in database
                    if row_data in duplicates['email'] or row_data in duplicates['linkedin']:
                        #check if we already seen this one (there could be duplicates in the CSV too)
                        if row_data not in duplicate_values:
                            found_duplicate = True
                            duplicate_values.append(row_data)
                        else:
                            just_pass = True
                            break

            if just_pass:
                continue
            elif found_duplicate:
                need_update.append(data)
            else:
                next_prospect = cls.create_prospect(owner_id=owner_id,
                                                    data=data, 
                                                    list_id=list_id, 
                                                    commit=False)
                prospects_list.append(next_prospect)

        # create the new prospects first
        ids = []
        if prospects_list:
            ids = cls.objects.insert(prospects_list, load_bulk=False)
        
        #then update existing ones
        if update_existing:
            cls.update_duplicates(owner_id=owner_id, new_data=need_update, values=duplicate_values, list_id=list_id)

        return len(ids)

    @classmethod
    def count_prospects_in_a_list(cls, list_id):
        return Prospects.objects(assign_to_list=list_id).count()

    @classmethod
    def add_to_list(cls, owner_id, prospects_ids, list_id):
        if not prospects_ids or not list_id:
            return 0
        
        list_exist = ProspectsList.objects(id=list_id).first()
        if not list_exist:
            raise Exception("List doesn't exist")
        
        res = Prospects.objects(owner=owner_id, id__in=prospects_ids).update(assign_to_list=list_id)

        return res
    
    @classmethod
    def remove_from_list(cls, owner_id, prospects_ids):
        if not owner_id or not prospects_ids:
            return 0
        
        res = Prospects.objects(owner=owner_id, id__in=prospects_ids).update(assign_to_list=None)

        return res


    @classmethod
    def async_prospects_list(cls, owner, list_filter, page, per_page=config.PROSPECTS_PER_PAGE):
        if page <= 1:
            page = 1

        filter_fields = ['assign_to', 'assign_to_list', 'column', 'contains']     

        #remove denied values
        list_filter.pop('owner', '')
        list_filter.pop('_id', '')

        #construct list_filter
        #list_filter = {'field_name' : {'operator' : 'value'}}
        query = {
            'owner' : owner
        }
        without_prefix = cls.get_create_fields()
        q = construct_prospect_filter(filter_data=list_filter,
                                        without_prefix = without_prefix,
                                        filter_fields=filter_fields)
        if q:
            query.update(q)

        db_query = cls.objects(**query)
        
        total = db_query.count()

        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "assign_to",
                "foreignField" : "_id",
                "as" : "assign_to"
            }},
            { "$unwind" : { "path" : "$assign_to", "preserveNullAndEmptyArrays": True }},
            {"$lookup" : {
                "from" : "prospects_list",
                "localField" : "assign_to_list",
                "foreignField" : "_id",
                "as" : "assign_to_list"
            }},
            { "$unwind" : { "path" : "$assign_to_list", "preserveNullAndEmptyArrays": True }},
            { "$project" : { 
                "team" : 1,
                "data" : 1,
                "assign_to" : 1,
                "status" : 1,
                "assign_to_list" : 1
            }}
        ]

        prospects = db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').aggregate(*pipeline)

        results = bson_dumps(prospects)

        return (total, results)

    @classmethod
    def get_prospects(cls, status=None, campaign_id=None):
        if status is None and campaign_id is None:
            raise Exception("Status and campaign_id can't be None")
        
        if status is not None:
            return cls.objects(Q(status=status) & Q(assign_to=campaign_id)).order_by('-created')
        else:
            return cls.objects(assign_to=campaign_id)


    @classmethod
    def update_prospects(cls, ids, status):
        return cls.objects(id__in=ids).update(status=status)

    def get_email(self):
        return self.data.get('email', '')

    def update_data(self, data):
        self._chek_for_duplicates(owner_id=self.owner.id, data=data)

        self.data = data
        self._commit()

    def update_status(self, status):
        self.status = status

        self._commit()

    def _commit(self):
        self.save()
        self.reload()


class MediumSettings(db.Document):
    # which medium
    medium = db.StringField()

    per_day = db.IntField()
    per_hour = db.IntField()

    interval = db.IntField()

class Templates(db.Document):
    label = db.StringField()
    data = db.DictField()
    status = db.IntField()

class MergeTags(db.Document):
    tag_name = db.StringField()
    tag_value = db.DictField()


#Register delete rules for '' ReferenceFields as described here: https://github.com/MongoEngine/mongoengine/issues/1707

ProspectsList.register_delete_rule(Prospects, "assign_to_list", 1)
