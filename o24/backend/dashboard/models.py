from o24.backend import db
from o24.backend import app
import datetime
from flask_user import UserManager, UserMixin
import uuid
from mongoengine.queryset.visitor import Q
import json
import traceback
from o24.backend.models.shared import Funnel
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Document, UserMixin):
    email = db.EmailField(unique=True)
    password = db.StringField()

    active = db.BooleanField(default=True)

    # Relationships
    roles = db.ListField(db.StringField(), default=[])

    created = db.DateTimeField( default=datetime.datetime.utcnow )

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
    
    last_action = db.DateTimeField(default=datetime.datetime(1970, 1, 1))
    next_action = db.DateTimeField(default=datetime.datetime(1970, 1, 1))

    limits = db.DictField()

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

    status = db.IntField(default=0)

    funnel = db.ReferenceField(Funnel)
    
    sending_schedule = db.DictField()
    
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
        
        new_campaign.status = 1

        new_campaign._commit()
        return new_campaign
    
    def _commit(self):
        self.save()

class Prospects(db.Document):
    owner = db.ReferenceField(User)
    
    team = db.ListField(db.ReferenceField(Team))
    data = db.DictField()

    assign_to = db.ReferenceField(Campaign)
    status = db.IntField()

    @classmethod
    def create_prospect(cls, owner_id, campaign_id, data={}):
        new_prospect = cls()

        new_prospect.owner = owner_id
        new_prospect.assign_to = campaign_id
        new_prospect.data = data

        new_prospect._commit()

        return new_prospect

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