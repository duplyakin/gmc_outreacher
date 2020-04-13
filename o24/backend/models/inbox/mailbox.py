import o24.backend.dashboard.models as models 
from o24.globals import *
from o24.backend import db


class MailBox(db.Document):
    prospect_id = db.ReferenceField(models.Prospects)
    campaign_id = db.ReferenceField(models.Campaign)

    email_meta = db.DictField()
    email_body = db.DictField()

    sender_meta = db.DictField()
    message_type = db.IntField()

    tracker_token = db.StringField()
    # we don't use it now BUT
    # if we will need to create complex email sequence (with several intro's and followups) then
    # we will use this field to store task meta that this email belongs to 
    task_meta = db.DictField()

    @classmethod
    def add_message(cls, data):
        new_message = cls()

        new_message.prospect_id = data.get('prospect_id')
        new_message.campaign_id = data.get('campaign_id')

        new_message.email_meta = data.get('email_meta')
        new_message.email_body = data.get('email_body')
        
        new_message.sender_meta = data.get('sender_meta')


        new_message._commit()
        return new_message
    
    @classmethod
    def get_mailbox(cls, mailbox_id=None, msg_id=None):
        if mailbox_id:
            return cls.obcjects(id=mailbox_id).first()
        
        if msg_id:
            return cls.obcjects(email_meta__id=msg_id).first()

        return None

    def _commit(self):
        self.save()