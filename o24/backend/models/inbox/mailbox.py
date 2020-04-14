import o24.backend.dashboard.models as models 
from o24.globals import *
from o24.backend import db
from mongoengine.queryset.visitor import Q
import datetime

class MailBox(db.Document):
    prospect_id = db.ReferenceField(models.Prospects)
    campaign_id = db.ReferenceField(models.Campaign)

    email_data = db.DictField()

    sender_meta = db.DictField()

    # 1 - Intro
    # 2 - Followup
    message_type = db.IntField(default=0)

    tracker_token = db.StringField()
    # we don't use it now BUT
    # if we will need to create complex email sequence (with several intro's and followups) then
    # we will use this field to store task meta that this email belongs to 
    task_meta = db.DictField()

    created = db.DateTimeField(default=datetime.datetime.now())

    @classmethod
    def add_message(cls, data, task_meta={}, tracker_token='', message_type=1):
        new_message = cls()

        new_message.prospect_id = data.get('prospect_id')
        new_message.campaign_id = data.get('campaign_id')

        new_message.email_data = data.get('email_data')
        new_message.sender_meta = data.get('sender_meta')

        new_message.task_meta = task_meta
        new_message.tracker_token = tracker_token
        new_message.message_type = message_type


        new_message._commit()
        return new_message
    
    @classmethod
    def get_parent(cls, prospect_id, campaign_id):
        return cls.objects(Q(prospect_id=prospect_id) and Q(campaign_id=campaign_id)).order_by('created').first()


    @classmethod
    #msgId - Global goole msgId 
    def get_mailbox(cls, mailbox_id=None, msgId=None):
        if mailbox_id:
            return cls.obcjects(id=mailbox_id).first()
        
        if msgId:
            return cls.obcjects(email_data__msgId=msgId).first()

        return None

    def get_references(self):
        return self.email_data.get('references', '')
    
    def get_text(self):
        return self.email_data.get('text', '')

    def get_html(self):
        return self.email_data.get('html', '')

    def get_msgId(self):
        return self.email_data.get('msgId', '')

    def _commit(self):
        self.save()