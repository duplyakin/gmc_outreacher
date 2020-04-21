import base64
import email
import uuid
import o24.config as config

import base64
import yagmail
from yagmail.headers import resolve_addresses
import email.encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class o24SMTP(yagmail.SMTP):
    @staticmethod
    def get_oauth_string(user, oauth2_info):
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
    def __init__(self, email, credentials):
        self.credentials = credentials
        self.email = email
        self.smtp_client = o24SMTP(user=email,
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
        res = self.smtp_client.send(to=email_to,
                                    contents=message)

        self.smtp_client.close()
        return res
