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
from bson import ObjectId
from o24.backend.utils.filter_data import *

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
    owner = db.ReferenceField(User)
    status = db.BooleanField(default=False)
    
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
        ids = cls.objects(next_action__lte=utc_now).distinct('id')
        return ids

    @classmethod
    def create_credentials(cls, owner, data):
        exist = None
        new_data = data.get('data')

        account = new_data.get('account', '')
        if account:
            exist = Credentials.objects(Q(owner=owner) & Q(data__account=account) ).first()

        if not exist:
            exist = cls()

        exist.owner = owner
        exist.medium = data.get('medium')
        exist.data = new_data
        
        exist._commit()

        return exist
    
    @classmethod
    def delete_credentials(cls, owner_id, credentials_ids):
        if not owner_id or not credentials_ids:
            return 0
        
        active_campaign = Campaign.objects(owner=owner_id, credentials__in=credentials_ids, status=1).first()
        if active_campaign:
            raise Exception("Can't delete - you have active campaigns on this account")
        
        return Credentials.objects(owner=owner_id, id__in=credentials_ids).delete()


    @classmethod
    def get_credentials(cls, user_id, medium=None, sender=None):
        if medium:
            return cls.objects(Q(owner=user_id) & Q(medium=medium)).first()

        if sender:
            return cls.objects(Q(owner=user_id) & Q(data__sender=sender)).first()

        return credentials

    @classmethod
    def async_credentials(cls, owner, page=None, per_page=config.CREDENTIALS_PER_PAGE):
        if page and page <= 1:
            page = 1

        query = {
            'owner' : owner
        }

        db_query = cls.objects(__raw__=query). \
                    only('id', 'data', 'status', 'medium', 'limit_per_day', 'last_action', 'next_action')
        
        total = db_query.count()
        results = []
        if page:
            results = db_query.skip(per_page * (page-1)).limit(per_page).order_by('status').all()
        else:
            results = db_query.order_by('status').all()
            
        return (total, results)


    @classmethod
    def list_credentials(cls, credential_ids):
        return cls.objects(Q(id__in=credential_ids)).all()

    @classmethod
    def update_credentials(cls, arr):
        if not arr:
            return None

        for e in arr:
            e.save()
        #cls.objects.update(arr)

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

    def update_data(self, data, allow_update=['limit_per_day', 'li_at']):
        new_limit_per_day = int(data.get('limit_per_day', 0))
        if new_limit_per_day > 0:
            self.limit_per_day = new_limit_per_day

        data_prop = data.get('data', '')
        if data_prop:
            li_at = data_prop.get('li_at', None)
            if li_at is not None:
                self.data['li_at'] = li_at
        
        self._commit()
    
    def warmup(self):
        self.limit_per_day = round(self.limit_per_day * 1.3)

    def _commit(self):
        self.save()

#### Menu: Teams ####
#### Manage teams
class Team(db.Document):
    admin = db.ReferenceField(User)
    
    title = db.StringField()
    members = db.ListField(db.ReferenceField(User))

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

class Campaign(db.Document):
    owner = db.ReferenceField(User)
    title = db.StringField()
    credentials = db.ListField(db.ReferenceField(Credentials))

    # 0 - created
    # 1 - in progress
    # 2 - paused
    # 11 - archived (deleted)
    status = db.IntField(default=0)

    funnel = db.ReferenceField(shared.Funnel)
    
    sending_days = db.DictField(default=DEFAULT_SENDING_DAYS)
    from_hour = db.IntField(default=DEFAULT_FROM_HOUR)
    to_hour = db.IntField(default=DEFAULT_TO_HOUR)

    last_action = db.DateTimeField(default=datetime.now())
    next_action = db.DateTimeField(default=datetime.now())

    data = db.DictField()
    
    #not used now
    priorities = db.IntField(default=0)

    templates = db.DictField()

    created = db.DateTimeField( default=datetime.now() )

    @classmethod
    def list_campaigns(cls, owner):
        return cls.objects(owner=owner).all()

    @classmethod
    def async_campaigns(cls, owner, page=None, per_page=config.CAMPAIGNS_PER_PAGE):
        if page and page <= 1:
            page = 1

        query = {
            'owner' : owner
        }

        db_query = cls.objects(__raw__=query). \
                    only('id', 'title', 'status', 'templates', 'data', 'created', 'credentials')
        
        total = db_query.count()
        results = []

        if page:
            results = db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').all()
        else:
            results = db_query.order_by('-created').all()
        
        return (total, results)

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
            c.save()
   
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

    #can delete only if:
    # not in progress
    # no prospects assigned
    def safe_delete(self):
        if self.status == IN_PROGRESS:
            raise Exception("DELETE ERROR: campaign in progress, stop it first")
        


    def inprogress(self):
        if self.status == 1:
            return True
        
        return False

    def update_status(self, status):
        self.status = status
        self._commit()

    def _commit(self):
        self.save()


class ProspectsList(db.Document):
    owner = db.ReferenceField(User)
    
    title = db.StringField()

    created = db.DateTimeField( default=datetime.now() )
    
    # 0 - just created
    # 1 - in progress
    # 2 - paused
    # 3 - finished

    @classmethod
    def async_lists(cls, owner):
        return cls.objects(owner=owner).only('id', 'title').all()

    @classmethod
    def get_lists(cls, owner, title=None, id=None):
        if title:
            return cls.objects(owner=owner, title=title).first()
        elif id:
            return cls.objects(owner=owner, id=id).first()
        else:
            return cls.objects(owner=owner).all()

    @classmethod
    def create_list(cls, owner_id, title):
        new_list = cls()
        
        new_list.owner = owner_id
        new_list.title = title

        new_list._commit()
        return new_list

    def _commit(self):
        self.save()


class Prospects(db.Document):
    owner = db.ReferenceField(User)
    
    team = db.ListField(db.ReferenceField(Team))
    data = db.DictField()

    assign_to = db.ReferenceField(Campaign)
    
    # 0 - just created
    # 1 - in progress
    # 2 - paused
    # 3 - finished
    status = db.IntField(default=0)
    
    tags = db.ListField(db.StringField())
    lists = db.ListField(db.ReferenceField(ProspectsList))

    created = db.DateTimeField( default=datetime.now() )

    @classmethod
    def create_prospect(cls, owner_id, campaign_id=None, data={}, lists=[], commit=True):
        new_prospect = cls()

        new_prospect.owner = owner_id
        new_prospect.data = data

        if campaign_id:
            new_prospect.assign_to = campaign_id

        if lists:
            new_prospect.lists = lists

        if commit:
            new_prospect._commit()

        return new_prospect


    @classmethod
    def delete_prospects(cls, owner_id, prospects_ids):
        if not prospects_ids:
            return 0

        return Prospects.objects(owner=owner_id, id__in=prospects_ids).delete()

    @classmethod
    def upload(cls, owner_id, csv_with_header, map_to, add_to_list):

        prospects_list = []
        
        i = 0
        for row in csv_with_header:
            i = i + 1

            #pass header
            if i == 1:
                continue

            data = {}
            if add_to_list:
                data['lists'] = [add_to_list.title]

            for m_t in map_to.keys():
                row_data = row[m_t]
                field_name = map_to[m_t]

                data[field_name] = row_data

            next_prospect = cls.create_prospect(owner_id=owner_id,
                                                data=data, 
                                                lists=add_to_list, 
                                                commit=False)
            prospects_list.append(next_prospect)

        if not prospects_list:
            return 0

        ids = cls.objects.insert(prospects_list, load_bulk=False)
        return len(ids)

    @classmethod
    def assign_prospects(cls, owner_id, prospects_ids, campaign_id):
        if not prospects_ids or not campaign_id:
            return 0
        
        return Prospects.objects(owner=owner_id, id__in=prospects_ids).update(data__assign_to=campaign_id)


    @classmethod
    def unassign_prospects(cls, owner_id, prospects_ids):
        if not prospects_ids:
            return 0
        
        return Prospects.objects(owner=owner_id, id__in=prospects_ids).update(data__assign_to='')

    @classmethod
    def async_prospects(cls, owner, list_filter, page, per_page=config.PROSPECTS_PER_PAGE):
        if page <= 1:
            page = 1

        filter_fields = ['assign_to', 'list', 'column', 'contains']     

        #remove denied values
        list_filter.pop('owner', '')
        list_filter.pop('_id', '')

        #construct list_filter
        #list_filter = {'field_name' : {'operator' : 'value'}}
        query = {
            'owner' : owner
        }

        q = construct_prospect_filter(filter_data=list_filter, 
                                        filter_fields=filter_fields)
        if q:
            query.update(q)

        db_query = cls.objects(__raw__=query). \
                    only('id', 'data', 'assign_to', 'status', 'lists')
        
        total = db_query.count()
        results = db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').all()

        return (total, results)

    @classmethod
    def get_prospects(cls, status, campaign_id):
        return cls.objects(Q(status=status) & Q(assign_to=campaign_id)).order_by('-created').all()

    @classmethod
    def update_prospects(cls, ids, status):
        return cls.objects(Q(id__in=ids)).update(status=status)

    def get_email(self):
        return self.data.get('email', '')

    def update_data(self, data):
        #TEST ONLY:
        data['lists'] = 'Updated list - FIX IT'
        self.data = data
        self._commit()

    def update_status(self, status):
        self.status = status

        self._commit()

    def _commit(self):
        self.save()


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
