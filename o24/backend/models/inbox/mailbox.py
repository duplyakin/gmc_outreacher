import o24.backend.dashboard.models as models 
from o24.globals import *
from o24.backend import db
from mongoengine.queryset.visitor import Q
import datetime
week_day_map = {
    0 : 'Mon',
    1 : 'Tue',
    2 : 'Wed',
    3 : 'Thu',
    4 : 'Fri',
    5 : 'Sat',
    6 : 'Sun'
}

month_map = {
    1 : 'Jan',
    2 : 'Feb',
    3 : 'Mar',
    4 : 'Apr',
    5 : 'May',
    6 : 'Jun',
    7 : 'Jul',
    8 : 'Aug',
    9 : 'Sep',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec'
}


class MailBox(db.Document):
    prospect_id = db.ReferenceField(models.Prospects)
    campaign_id = db.ReferenceField(models.Campaign)

    #it's incremented inside (prospect_id, campaign_id)
    sequence = db.IntField(default=0)

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

    created = db.DateTimeField(default=datetime.datetime.utcnow())

    @classmethod
    def add_message(cls, data, task_meta={}, tracker_token='', message_type=1):
        new_message = cls()

        new_message.prospect_id = data.get('prospect_id')
        new_message.campaign_id = data.get('campaign_id')

        has_parent = cls.get_parent(prospect_id=new_message.prospect_id,
                                            campaign_id=new_message.campaign_id)
        current_sequence = 0
        if has_parent:
            current_sequence = has_parent.sequence + 1

        new_message.sequence = current_sequence

        new_message.email_data = data.get('email_data')
        new_message.sender_meta = data.get('sender_meta')

        new_message.task_meta = task_meta
        new_message.tracker_token = tracker_token
        new_message.message_type = message_type
    

        new_message._commit()
        return new_message
    
    @classmethod
    def get_parent(cls, prospect_id, campaign_id):
        return cls.objects(Q(prospect_id=prospect_id) & Q(campaign_id=campaign_id)).order_by('-sequence').first()

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

    def get_trail(self):
        return self.email_data.get('trail', '')

    def get_wrote_on_data(self):
        data_dict = {
            'sender' : '',
            'week_day' : '',
            'date' : '',
            'month' : '',
            'year' : ''
        }

        data_dict['sender'] = self.email_data.get('sender', '')

        date = self.created

        data_dict['week_day'] = week_day_map[date.weekday()]
        data_dict['date'] = date.day
        data_dict['month'] = month_map[date.month]
        data_dict['year'] = date.year

        return data_dict

    def get_thread_id(self):
        thread_id = ''

        api_res = self.email_data.get('api_res', '')
        if api_res:
            thread_id = api_res.get('threadId','')

        return thread_id

    def get_api_msg_id(self):
        msg_id = ''
        
        api_res = self.email_data.get('api_res', '')
        if api_res:
            msg_id = api_res.get('id','')

        return msg_id

    def set_msgId(self, msgId):
        self.email_data['msgId'] = msgId
        self._commit()

        return True

    def _commit(self):
        self.save()
        self.reload()