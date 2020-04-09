import o24.backend.dashboard.models as models 
from o24.globals import *
from o24.backend import db


class MailBox(db.Document):
    prospect_id = db.ReferenceField(models.Prospects)
    campaign_id = db.ReferenceField(models.Campaign)


    email_meta = db.DictField()
    email_body = db.DictField()

    sender_meta = db.DictField()

