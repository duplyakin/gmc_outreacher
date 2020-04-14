import o24.backend.google.provider.gmail_api_provider as gmail_api_provider
import o24.backend.google.provider.gmail_smtp_provider as gmail_smtp_provider

import o24.backend.models.inbox.mailbox as mailbox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid
from email import charset

import base64
import html
import uuid
from bs4 import BeautifulSoup

class GmailController():
    def __init__(self, email, credentials, smtp=False):
        self.credentials = credentials
        self.email = email

        self.provider = gmail_api_provider.GmailApiProvider(credentials)

        self.smtp = smtp   
        if self.smtp:
            self.smtp_provider = gmail_smtp_provider.GmailSmtpProvider(email, credentials)

    #TODO: use prospect_id and campaign_id to get msg_id data
    def get_msgId(self, msg_id):
        msg = self.provider.get_mime_message(msg_id=msg_id)
        msgId = format(msg['Message-ID'])
        return msgId

    #msgId - is the global ID from gmail, example: <CAAfG+wAyJgc8uZVpbh78LzEENnQJWkru6VWtHZSyJOYnyZ8w5g@mail.gmail.com>
    def create_multipart_message(self, 
                                email_from, 
                                email_to, 
                                subject,  
                                plain_version,
                                html_version=None,
                                parent_mailbox=None):
        
        charset.add_charset('utf-8', charset.QP, charset.QP, 'utf-8')

        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = email_from
        msgRoot['To'] = email_to

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        if plain_version:
            msgText = MIMEText(plain_version.encode('utf-8'), 'plain', 'UTF-8')
            msgAlternative.attach(msgText)

        if html_version:
            if parent_mailbox:
                trail = self._construct_trail(parent_mailbox)
                html_version = html_version + trail

            msg_html = MIMEText(html_version.encode('utf-8'), 'html', 'UTF-8')
            msgAlternative.attach(msg_html)

        #Need to construct reply email body in Gmail format
        if parent_mailbox:
            msgRoot.add_header('References', parent_mailbox.get_references())
            msgRoot.add_header('In-Reply-To', parent_mailbox.get_msgId())

            if 'Re:' not in subject:
                msgRoot['Subject'] = 'Re: '+ subject

        return msgRoot

    def _construct_trail(self, parent_mailbox):
        trail = parent_mailbox.get_html()
        if not trail:
            return ''

        soup = BeautifulSoup(trail, "html.parser")
        if '<html>' in trail:
            soup.html.unwrap()
        
        if '<body>' in trail:
            soup.body.unwrap()

        if '<head>' in trail:
            soup.head.unwrap()


        start = '''<div style="margin-left: 1em; color: #500050; padding-top: 20px;"><div>On Mon, 03 Feb 2020, Kirill Shilov &lt;ks.shilov@gmail.com&gt; wrote:</div><div style="border-left: 1px solid black; padding-left: 1em;">'''
        end = '''</div></div>'''

        trail = start + str(soup) + end

        return trail

    def add_header_msgId(self, message, mailbox_id=None, mailer='o24 (outreacher24.com)', domain='outreacher24.com'):
        msg_id = make_msgid(domain=domain)
        if not msg_id:
            raise Exception('Can not generate msg_id')

        message.add_header('Message-Id', msg_id)
        if mailbox_id:
            message.add_header('X-o24-Message-Id', mailbox_id)
        
        if mailer:
            message.add_header('X-Mailer', mailer)

        return msg_id, message

    def _get_payload(self, message):
        text = ''
        html = ''
        references = message.get(name='references', failobj='')

        for part in message.walk():
            content_type = part.get(name='content-type')
            if 'text/plain' in content_type:
                text = part.get_payload()
            elif 'text/html' in content_type:
                html = part.get_payload()
            
            if text and html:
                break 

        return text, html, references

    def construct_data(self,
                        message, 
                        prospect_id, 
                        campaign_id, 
                        msgId,  
                        mailbox_reply_to_id='', 
                        sender_meta={}):

        text, html, references = self._get_payload(message)

        email_data = {
            'msgId' : msgId,
            'mailbox_parent_id' : mailbox_reply_to_id,
            'message' : message,
            'references' : references.strip(),
            'text' : text,
            'html' : html
        }

        data = {}

        data['prospect_id'] = prospect_id
        data['campaign_id'] = campaign_id

        data['email_data'] = email_data

        data['sender_meta'] = sender_meta

        return data

    def send_message(self, email_to, message):
        if self.smtp:
            return self.smtp_provider.send_message(email_to=email_to,
                                                    message=message)
        else:
            pass

        return {'Error' : 'Something went wrong'}
    
    def parse_tags(self, message):
        pass
    
    def parse_images(self, message, images):
        pass

