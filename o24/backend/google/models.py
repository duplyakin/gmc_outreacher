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

    @classmethod
    def settings(cls):
        settings = GoogleAppSetting.objects(active=True).first()
        if not settings:
            raise Exception("There is no active config created for gogole app service")
        
        return settings


    def list_fields(self):
        return {
            'Id' : self.id,
            'Title' : self.title,
            'Created at' : self.created,
            'Active' : self.active
        }

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()
