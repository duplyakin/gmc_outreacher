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

import o24.backend.models.shared as shared

class User(db.Document, UserMixin):
    email = db.EmailField(unique=True)
    password = db.StringField()

    active = db.BooleanField(default=True)

    # Relationships
    roles = db.ListField(db.StringField(), default=[])

    created = db.DateTimeField( default=datetime.now() )

    @classmethod
    def create_user(cls, data):
        new_user = cls()

        new_user.email = data.get('email')
        new_user.password = generate_password_hash(data.get('password'))
        new_user.active = data.get('active')

        new_user._commit()
        return new_user
    
    @classmethod
    def get_user(cls, email):
        user = cls.objects(email=email).first()
        return user

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

    #current_day = db.DateTimeField(default=datetime.datetime(1970, 1, 1))
    #current_hour = db.DateTimeField(default=datetime.datetime(1970, 1, 1))
    #daily_counter = db.IntField(default=0)
    #hourly_counter = db.IntField(default=0)

    @classmethod
    def ready_ids(cls, utc_now):
        #ids = [p.get('_id') for p in cls.objects(next_action__lte=utc_now).only('id').all().as_pymongo()]
        ids = cls.objects(next_action__lte=utc_now).distinct('id')
        return ids

    @classmethod
    def create_credentials(cls, owner, data):
        new_credentials = cls()

        new_credentials.owner = owner
        new_credentials.medium = data.get('medium')
        new_credentials.data = data.get('data')

        #defaults
        new_credentials.limits = {}
        
        new_credentials._commit()

        return new_credentials
    
    @classmethod
    def get_credentials(cls, user_id, medium):
        credentials = cls.objects(Q(owner=user_id) & Q(medium=medium)).first()

        return credentials

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

    
    #not used now
    priorities = db.IntField(default=0)
    templates = db.DictField()

    @classmethod
    def get_campaign(cls, id=None, title=None):
        
        campaign = None
        if title:
            campaign = cls.objects(title=title).first()
        elif id:
            campaign = cls.objects(id=id).first()

        return campaign

    @classmethod
    def create_campaign(cls, data):
        new_campaign = cls()
        
        new_campaign.title = data.get('title', '')
        new_campaign.credentials = data.get('credentials')
        new_campaign.funnel = data.get('funnel')
        
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
        
        return credentials_dict
                
    @classmethod
    def update_campaigns(cls, campaigns):
        if not campaigns:
            return None

        for c in campaigns:
            c.save()
   
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


    def inprogress(self):
        if self.status == 1:
            return True
        
        return False

    def update_status(self, status):
        self.status = status
        self._commit()

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

    @classmethod
    def create_prospect(cls, owner_id, campaign_id, data={}):
        new_prospect = cls()

        new_prospect.owner = owner_id
        new_prospect.assign_to = campaign_id
        new_prospect.data = data

        new_prospect._commit()

        return new_prospect

    @classmethod
    def get_prospects(cls, status, campaign_id):
        return cls.objects(Q(status=status) & Q(assign_to=campaign_id)).all()

    @classmethod
    def update_prospects(cls, ids, status):
        return cls.objects(Q(id__in=ids)).update(status=status)

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
