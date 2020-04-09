import o24.backend.google.provider.gmail_api_provider as gmail_api_provider
import o24.backend.models.inbox.mailbox as mailbox
from email.mime.text import MIMEText
import base64

class GmailController():
    def __init__(self, mailbox, credentials):
        self.mailbox = mailbox
        self.credentials = credentials
        self.provider = gmail_api_provider.GmailApiProvider(credentials)
    
    def create_message(self, email_from, email_to, subject, body):
        message = MIMEText(body)
        message['to'] = email_to
        message['from'] = email_from
        message['subject'] = subject
        
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_email(self, message):
        return self.provider.send_message(message=message)
    
    def send_email_as_reply(self, body):
        pass
    
    def receive_reply(self):
        pass

