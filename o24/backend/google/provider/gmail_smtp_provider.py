import base64
import email
import uuid
import o24.config as config
from o24.globals import *

import base64
import yagmail
from yagmail.headers import resolve_addresses
import email.encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import traceback
import o24.backend.google.provider.oauth_provider as oauth_provider
from o24.exceptions.exception_with_code import ErrorCodeException

class o24SMTP(yagmail.SMTP):
    @staticmethod
    def get_oauth_string(user, oauth2_info):
        #TODO implement refresh token
        access_token = oauth2_info.get('token')

        auth_string = 'user=%s\1auth=Bearer %s\1\1' % (user, access_token)
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
        return auth_string

    def prepare_send(
        self,
        to=None,
        subject=None,
        contents=None,
        attachments=None,
        cc=None,
        bcc=None,
        headers=None,
        newline_to_break=True,
    ):
        addresses = resolve_addresses(self.user, self.useralias, to, cc, bcc)

        msg = contents

        recipients = addresses["recipients"]
        msg_string = msg.as_string()
        return recipients, msg_string        
        

class GmailSmtpProvider():
    def __init__(self, email, credentials, credentials_id):
        self.credentials = credentials
        self.email = email
        self.credentials_id = credentials_id

        self._refresh_credentials()
    
    def _refresh_credentials(self):
        self.credentials = oauth_provider.GoogleOauthProvider.check_and_update_credentials(credentials_id=self.credentials_id)

        self.smtp_client = o24SMTP(user=self.email,
                                    host=config.GMAIL_SMTP_HOST,
                                    port=config.GMAIL_SMTP_PORT,
                                    smtp_starttls=True,
                                    smtp_ssl=False)

        self._hack_credentials()

    #this is workaround to set credentials manually as we don't need to load it from file
    def _hack_credentials(self):
        self.smtp_client.oauth2_file = True
        self.smtp_client.credentials = self._to_yagmail_format(self.email, self.credentials)

    def _to_yagmail_format(self, email, credentials):
        oauth2_info = {
            "email_address": email,
            "google_client_id": credentials.get('client_id'),
            "google_client_secret": credentials.get('client_secret'),
            "google_refresh_token": credentials.get('refresh_token'),
            "token" : credentials.get('token')
        }

        return oauth2_info


    def send_message(self, email_to, message):
        for i in range(2):
            try:
                res = self.smtp_client.send(to=email_to,
                                            contents=message)
                self.smtp_client.close()
                return res
            except Exception as e:
                print(e)
                traceback.print_exc()

                if (hasattr(e, 'smtp_code')):
                    if i <= 0 and e.smtp_code == SMTP_AUTH_ERROR:
                        self._refresh_credentials()
                        continue
                    else:
                        raise ErrorCodeException(error_code=e.smtp_code, message=str(e))
                
                raise