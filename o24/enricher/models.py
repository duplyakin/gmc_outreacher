from o24.backend import db

from datetime import datetime  
from datetime import timedelta  
from pytz import timezone
import pytz
from dateutil.parser import parse
from o24.globals import *

class AuthData(db.Document):
    key = db.StringField()
    data = db.DictField() 
    posix_expires = db.IntField(default=0)

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )

    @classmethod
    def get_token(cls, key):
        res = cls.objects(key=key).first()
        if not res:
            return None, 0
        
        return res.data, res.posix_expires

    @classmethod
    def save_token(cls, key, data, posix_expires=0):
        exist = cls.objects(key=key).first()
        if not exist:
            exist = cls()
        
        exist.key = key
        exist.data = data
        exist.posix_expires = posix_expires

        exist._commit()
        return exist

    def _commit(self, _reload=False):        
        self.save()
        if _reload:
            self.reload()


class DataStorage(db.Document):
    data = db.DictField()

    @classmethod
    def add_data(cls, data):
        new_data = cls()
        new_data.data = data

        new_data._commit()
        return new_data

    def _commit(self):
        self.save()

class EnrichTaskQueueLock(db.Document):
    lock_key = db.StringField(unique=True, sparse=False)
    ack = db.IntField(default=0)

class EnrichTaskQueue(db.Document):
    # NEW(0) - didn't start enrich for this data
    # IN_PROGRESS(1) - enrich in progress
    # SUCCESS(2) - found data for this prospect
    # FAILED_TO_ENRICH(3) - didn't find data for this prospect (try to switch provider)
    status = db.IntField(default=ENRICH_NEW)
    ack = db.IntField(default=0)

    owner = db.ObjectIdField()
    prospect_id = db.ObjectIdField()

    input_data = db.DictField()
    result_data = db.DictField()

    total_spent = db.IntField(default=0)
    last_spent = db.IntField(default=0)

    actions_tried = db.ListField(db.StringField())
    can_search = db.StringField()

    #the current enricher to enrich this prospect
    current_enricher = db.IntField(default=0)

    #list of enrichers that prospect need to go through
    enricher_list = db.DictField()

    next_round = db.DateTimeField(default=parse("1980-05-25T16:31:37.436Z"))

    @classmethod
    def restart_task(cls, owner_id, prospect_id, input_data, providers):
        exist = cls.objects(owner=owner_id, prospect_id=prospect_id).first()
        if exist:
            exist.delete()

        return cls.create_task(owner_id=owner_id, 
                                prospect_id=prospect_id, 
                                input_data=input_data,
                                providers=providers)

    @classmethod
    def create_task(cls, owner_id, prospect_id, input_data, providers):
        exist = cls.objects(owner=owner_id, prospect_id=prospect_id).first()
        if exist:
            message = "Task exist for owner_id={0} prospect_id={1}".format(owner_id, prospect_id)
            raise Exception(message)

        new_task = cls()
        new_task.owner = owner_id
        new_task.prospect_id = prospect_id
        new_task.input_data = input_data
        new_task.enricher_list = providers

        start_with = providers.get('0', '')
        if start_with:
            new_task.current_enricher = start_with


        new_task._commit()
        return new_task

    @classmethod
    def get_enriched_tasks(cls):
        return cls.objects(status__in=[ENRICH_SUCCESS])

    @classmethod
    def get_execute_tasks(cls):
        now = pytz.utc.localize(datetime.utcnow())        
        return cls.objects(status__in=[ENRICH_NEW, ENRICH_IN_PROGRESS], next_round__lte=now)


    def delay(self, seconds, _commit=False):
        now = pytz.utc.localize(datetime.utcnow())
        self.next_round = now + timedelta(seconds=seconds)

        if _commit:
            self._commit()

        return self.next_round

    def update_status(self, status):
        self.status = status
        self._commit()

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()