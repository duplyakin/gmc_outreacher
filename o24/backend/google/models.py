from o24.backend import db
from o24.backend import app
import datetime


class GoogleAppSetting(db.Document):
    title = db.StringField()

    credentials = db.DictField()
    redirect_uri = db.StringField()

    gmail_scopes = db.ListField(db.StringField())
    gmail_access_type = db.StringField()
    gmail_include_granted_scopes = db.StringField()

    gmail_api_name = db.StringField()
    gmail_api_version = db.StringField()

    active = db.BooleanField(default=False)

    created = db.DateTimeField( default=datetime.datetime.utcnow )

    PASS_ON_CREATE = ['created']
    BOOLEAN_FIELDS = ['active']
    TO_STR = ['gmail_include_granted_scopes']

    @classmethod
    def get_create_fields(cls):
        return cls._fields.keys()

    @classmethod
    def settings(cls):
        settings = GoogleAppSetting.objects(active=True).first()
        if not settings:
            raise Exception("There is no active config created for gogole app service")
        
        return settings
    
    @classmethod
    def create_settings(cls, from_data):
        if not from_data:
            return None

        new_settings = cls()

        new_settings.update_data(from_data=from_data)

        return new_settings

    def update_data(self, from_data):
        if not from_data:
            return
        
        create_fields = GoogleAppSetting.get_create_fields()

        for field in create_fields:
            if field in self.PASS_ON_CREATE:
                continue
            
            val = from_data.get_field(field)
            if val == '' or val is None:
                continue 

            if field in self.BOOLEAN_FIELDS:
                if val in ['true', 'True', '1']:
                    val = True
                else:
                    val = False
            elif field in self.TO_STR:
                val = str(val)
                
            setattr(self, field, val)
        
        self._commit()

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()
