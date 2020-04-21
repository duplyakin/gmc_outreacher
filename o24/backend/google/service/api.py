from googleapiclient.discovery import build
import google.oauth2.credentials
from o24.backend.google.models import GoogleAppSetting

class GoogleApiService():
    def __init__(self):
        self.settings = GoogleAppSetting.settings()

    @classmethod
    def build_gmail_api_service(cls, credentials):
        this = GoogleApiService()
        gmail_api_settings = this.get_gmail_api_settings()

        credentials_obj = google.oauth2.credentials.Credentials(**credentials)

        this.check_credentials(credentials_obj)
        # need to check if credentials expired
        # like here: https://github.com/krishnakumar4a4/email-scrape/blob/master/scraper/service.py
        api_service = build(gmail_api_settings['api_name'], 
                            gmail_api_settings['api_version'], 
                            credentials=credentials_obj)
        
        return api_service

    @classmethod
    def build_spreadsheet_api_service(cls, credentials):
        this = GoogleApiService()

        credentials_obj = google.oauth2.credentials.Credentials(**credentials)

        this.check_credentials(credentials_obj)
        # need to check if credentials expired
        # like here: https://github.com/krishnakumar4a4/email-scrape/blob/master/scraper/service.py
        api_service = build('sheets', 
                            'v4', 
                            credentials=credentials_obj)
        
        return api_service

    def check_credentials(self, credentials_obj):
        pass

    def get_gmail_api_settings(self):
        api_name = self.settings.gmail_api_name
        api_version = self.settings.gmail_api_version

        return {
            "api_name" : api_name,
            "api_version" : api_version
        }
