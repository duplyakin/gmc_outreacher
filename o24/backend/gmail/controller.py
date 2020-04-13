import o24.backend.google.provider.gmail_api_provider as gmail_api_provider
import o24.backend.google.provider.gmail_smtp_provider as gmail_smtp_provider

import o24.backend.models.inbox.mailbox as mailbox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
import html
import uuid

class GmailController():
    def __init__(self, email, credentials, smtp=False):
        self.credentials = credentials
        self.email = email

        self.provider = gmail_api_provider.GmailApiProvider(credentials)

        self.smtp = smtp   
        if self.smtp:
            self.smtp_provider = gmail_smtp_provider.GmailSmtpProvider(email, credentials)

    #TODO: use prospect_id and campaign_id to get msg_id data
    def get_msgId_for_followup(self, msg_id):
        msg = self.provider.get_mime_message(msg_id=msg_id)
        msgId = format(msg['Message-ID'])
        return msgId

    def parse_tags(self, message):
        pass
    
    def parse_images(self, message, images):
        pass

    #msgId - is the global ID from gmail, example: <CAAfG+wAyJgc8uZVpbh78LzEENnQJWkru6VWtHZSyJOYnyZ8w5g@mail.gmail.com>
    def create_multipart_message(self, 
                                email_from, 
                                email_to, 
                                subject,  
                                plain_version,
                                html_version=None,
                                msgId=None):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = email_from
        msgRoot['To'] = email_to
        if msgId:
            msgRoot.add_header('Reference', msgId)
            msgRoot.add_header('In-Reply-To', msgId)

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        if plain_version:
            msgText = MIMEText(plain_version, 'plain', 'utf-8')
            msgAlternative.attach(msgText)

        if html_version:
            msg_html = MIMEText(html_version, 'html', 'utf-8')
            msgAlternative.attach(msg_html)
        
        return msgRoot

    def send_message(self, email_to, message):
        if self.smtp:
            return self.smtp_provider.send_message(email_to=email_to,
                                                    message=message)

        return None