from googleapiclient.discovery import build
import google.oauth2.credentials
from o24.backend.google.models import GoogleAppSetting

class GoogleApiService():
    def __init__(self):
        self.settings = GoogleAppSetting.settings()

    #!!! YOU NEED to check credentials expired before using this method
    # See how GmailController example
    @classmethod
    def build_gmail_api_service(cls, credentials):
        this = GoogleApiService()
        gmail_api_settings = this.get_gmail_api_settings()

        credentials_obj = google.oauth2.credentials.Credentials(**credentials)

        api_service = build(gmail_api_settings['api_name'], 
                            gmail_api_settings['api_version'], 
                            credentials=credentials_obj,
                            cache_discovery=False)
        
        return api_service
        
    #!!! YOU NEED to check credentials expired before using this method
    # See how GmailController example
    @classmethod
    def build_spreadsheet_api_service(cls, credentials):
        this = GoogleApiService()

        credentials_obj = google.oauth2.credentials.Credentials(**credentials)

        api_service = build('sheets', 
                            'v4', 
                            credentials=credentials_obj)
        
        return api_service

    def get_gmail_api_settings(self):
        api_name = self.settings.gmail_api_name
        api_version = self.settings.gmail_api_version

        return {
            "api_name" : api_name,
            "api_version" : api_version
        }
