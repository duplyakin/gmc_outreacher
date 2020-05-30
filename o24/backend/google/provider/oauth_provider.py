#import google.oauth2.credentials
import google_auth_oauthlib.flow

import o24.backend.dashboard.models as models
from o24.backend.google.models import GoogleAppSetting
from o24.backend.utils.data import credentials_to_dict

import o24.backend.google.provider.gmail_api_provider as gmail_api_provider   #remove then
from datetime import datetime

from google.auth.transport.requests import Request
import google.oauth2.credentials

class GoogleOauthProvider():
    def __init__(self):
        self.settings = GoogleAppSetting.settings()
    
    @classmethod
    def check_and_update_credentials(cls, credentials_id):
        credentials = models.Credentials.objects(id=credentials_id).first()
        if not credentials:
            message = "There is no such credentials for id={0}".format(credentials_id)
            raise Exception(message)

        raw_credentials, expiry = credentials.get_auth_credentials()
        if not raw_credentials:
            raise Exception('check_and_update_credentials ERROR: there is no raw_credentials , in get_auth_credentials')
        
        res = raw_credentials
        
        this = cls()
        updated_credentials, expiry = this.manual_refresh_credentials(credentials=raw_credentials, expiry=expiry)
        if updated_credentials:
            credentials.update_auth_credentials(new_credentials=updated_credentials, expiry=expiry)
            res = updated_credentials

        return res

    def get_gmail_auth_url(self, current_state):
        scopes = self.settings.gmail_scopes
        access_type = self.settings.gmail_access_type
        include_granted_scopes = self.settings.gmail_include_granted_scopes

        flow = self._get_flow(scopes, 
                                current_state)
        
        auth_url, state = flow.authorization_url(
                access_type=access_type,
                prompt='consent',
                include_granted_scopes=include_granted_scopes)
        
        return auth_url, state

    def set_gmail_auth_credentials(self, request_url, current_state):
        scopes = self.settings.gmail_scopes

        flow = self._get_flow(scopes, 
                                current_state)
        
        flow.fetch_token(authorization_response=request_url)

        if not flow.credentials:
            raise Exception("flow.fetch_token error")

        access_credentials = credentials_to_dict(flow.credentials)
        expiry = flow.credentials.expiry

        #receive user profile first
        api_provider = gmail_api_provider.GmailApiProvider(access_credentials)

        email = api_provider.get_user_email()
        if not email:
            raise Exception("Can't receive user's profile")


        return access_credentials, email, expiry
    
    def manual_refresh_credentials(self, credentials, expiry):
        credentials_obj = google.oauth2.credentials.Credentials(**credentials)

        #need to have naive datetime
        if expiry:
            expiry = expiry.replace(tzinfo=None)
            credentials_obj.expiry = expiry

        if (credentials_obj and credentials_obj.expired) or not expiry:
            credentials_obj.refresh(Request())
            access_credentials = credentials_to_dict(credentials_obj)
            return access_credentials, credentials_obj.expiry
        else:
            return None, None

    def valid_state(self, state, current_state):
        if state != current_state:
            return False
        
        return True


    def _get_flow(self, scopes, state):
        credentials = self.settings.credentials
        redirect_uri = self.settings.redirect_uri

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            credentials, 
            scopes=scopes, 
            state=state)

        flow.redirect_uri = redirect_uri

        return flow
