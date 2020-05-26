#import google.oauth2.credentials
import google_auth_oauthlib.flow

from o24.backend.google.models import GoogleAppSetting
from o24.backend.utils.data import credentials_to_dict

import o24.backend.google.provider.gmail_api_provider as gmail_api_provider   #remove then

from google.auth.transport.requests import Request
import google.oauth2.credentials

class GoogleOauthProvider():
    def __init__(self):
        self.settings = GoogleAppSetting.settings()

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

        #receive user profile first
        api_provider = gmail_api_provider.GmailApiProvider(access_credentials)

        email = api_provider.get_user_email()
        if not email:
            raise Exception("Can't receive user's profile")


        return access_credentials, email
    
    def manual_refresh_credentials(self, credentials):
        credentials_obj = google.oauth2.credentials.Credentials(**credentials)

        credentials_obj.refresh(Request())

        access_credentials = credentials_to_dict(credentials_obj)

        return access_credentials

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
