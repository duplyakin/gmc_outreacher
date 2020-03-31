from backend import db
from backend import app

from mongoengine.queryset.visitor import Q

class Action(db.Document):
    #shared field
    action_type = db.IntField(default=0)
    data = db.DictField()
    medium = db.StringField()
    key = db.StringField()

    @classmethod
    def create_action(cls, data):
        new_action = cls()

        new_action.action_type = data.get('action_type')
        new_action.data = data.get('data')
        new_action.medium = data.get('medium')
        new_action.key = data.get('key')


        new_action._commit()
    
    @classmethod
    def get_by_key(cls, key):
        action = cls.objects(key=key).first()
        return action

    def _commit(self):
        self.save()


class Funnel(db.Document):
    action = db.ReferenceField(Action)
    paramters = db.DictField()

    root = db.BooleanField(default=False)

    if_true = db.ReferenceField(Funnel, default=None)
    if_false = db.ReferenceField(Funnel, default=None)

    template = db.DictField()

    @classmethod
    def get_random(cls):
        funnel = cls.objects(root=True).first()
        return funnel

    @classmethod
    def get_node(cls, node_id):
        node = cls.objects(id=node_id).first()
        return node

    @classmethod
    def create_node(cls, data):
        new_funnel = cls()

        new_funnel.update_data(data)

        return new_funnel

    def update_data(self, data):

        if data.get('root', None):
            self.root = data.get('root')
        
        if data.get('action', None):
            self.action = data.get(action)

        if data.get('if_true', None):
            self.if_true = data.get('if_true')
        
        if data.get('if_false', None):
            self.if_false = data.get('if_false')

        self._commit()
        

    def _commit(self):
        self.save()

class ActionQueue(db.Document):
    current = db.ReferenceField(Funnel)
    
    #None - for root action
    parent = db.ReferenceField(ActionQueue)

    status = db.IntField(default=0)
    data = db.DictField()
    result = db.DictField()
    credentials = db.DictField()

    prospect_id = db.StringField()
    campaing_id = db.StringField()

    medium = db.StringField()
    
    record_type = db.IntField()
    followup_level = db.IntField(default=0)