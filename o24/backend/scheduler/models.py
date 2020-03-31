from backend import db
from backend import app
import datetime
from flask_user import UserManager, UserMixin
import uuid
from mongoengine.queryset.visitor import Q
import json
import traceback
from backend.dashboard.models import Credentials, Campaign

class Schedule(db.Document):
    credentials = db.ReferenceField(Credentials)
    current_day = db.DateTimeField()
    current_hour = db.DateTimeField()
    
    daily_counter = db.IntField()
    hourly_counter = db.IntField()

class Priority(db.Document):
    campaign = db.ReferenceField(Campaign)

    # 0 - Intro, 1 - Follow up
    do_next = db.IntField(default=0)

    #0 - Init phase, 1 - While all 1 are empty
    followup_level = db.IntField(default=0)