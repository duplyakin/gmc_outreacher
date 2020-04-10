import o24.backend.google.provider.gmail_api_provider as gmail_api_provider
import o24.backend.models.inbox.mailbox as mailbox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
import html
import uuid

class GmailController():
    def __init__(self, mailbox, credentials):
        self.mailbox = mailbox
        self.credentials = credentials
        self.provider = gmail_api_provider.GmailApiProvider(credentials)
    
    #TODO: use prospect_id and campaign_id to get msg_id data
    def get_msgId_for_followup(self, msg_id):
        msg = self.provider.get_mime_message(msg_id=msg_id)
        msgId = format(msg['Message-ID'])
        return msgId

    #msgId - is the global ID from gmail, example: <CAAfG+wAyJgc8uZVpbh78LzEENnQJWkru6VWtHZSyJOYnyZ8w5g@mail.gmail.com>
    def create_multipart_message(self, email_from, email_to, 
                                subject, 
                                html_version, 
                                plain_version,
                                thread_id=None,
                                msgId=None,
                                image_data=None):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['subject'] = subject
        msgRoot['from'] = email_from
        msgRoot['to'] = email_to
        if msgId:
            msgRoot.add_header('Reference', msgId)
            msgRoot.add_header('In-Reply-To', msgId)


        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText(plain_version, 'plain', 'utf-8')
        msgAlternative.attach(msgText)

        msg_html = None
        if image_data:
            msg_html = MIMEText(html_version.format(alt=html.escape(image_data['title'], quote=True), 
                                                cid=image_data['cid']), 'html', 'utf-8')
        else:
            msg_html = MIMEText(html_version, 'html', 'utf-8')

        msgAlternative.attach(msg_html)
        
        if image_data:
            msg_image = MIMEImage(image_data.get('raw'))
            msg_image.add_header('Content-ID', '<{}>'.format(image_data['cid']))
            msgRoot.attach(msg_image)

        raw_message = {'raw': base64.urlsafe_b64encode(msgRoot.as_string().encode()).decode()}
        if thread_id:
            raw_message['threadId'] = thread_id
        
        return raw_message

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

