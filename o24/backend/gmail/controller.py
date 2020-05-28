import o24.backend.google.provider.gmail_api_provider as gmail_api_provider
import o24.backend.google.provider.gmail_smtp_provider as gmail_smtp_provider
import o24.backend.google.provider.oauth_provider as oauth_provider

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
    def __init__(self, email, credentials, credentials_id, smtp=False):
        self.credentials = credentials
        self.credentials_id = credentials_id
        self.email = email
        self.smtp = smtp

        self.provider = gmail_api_provider.GmailApiProvider(credentials, credentials_id=credentials_id)

        if self.smtp:
            self.smtp_provider = gmail_smtp_provider.GmailSmtpProvider(self.email, credentials, credentials_id=credentials_id)


    def current_email(self):
        return self.email
       
    #message - is a MIMEMultipart object
    def add_gmail_api_meta(self, message, parent_mailbox=None):
        raw_message = {
            'raw' : base64.urlsafe_b64encode(message.as_string().encode()).decode()
        }

        if parent_mailbox:
            thread_id = parent_mailbox.get_thread_id()        
            if thread_id:
                raw_message['threadId'] = thread_id

        return raw_message

    #msgId - is the global ID from gmail, example: <CAAfG+wAyJgc8uZVpbh78LzEENnQJWkru6VWtHZSyJOYnyZ8w5g@mail.gmail.com>
    def create_multipart_message(self, 
                                email_from, 
                                email_to, 
                                subject,  
                                plain_version,
                                html_version='',
                                parent_mailbox=None):
        
        charset.add_charset('utf-8', charset.QP, charset.QP, 'utf-8')

        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        
        if parent_mailbox:
            if 'Re:' not in subject:
                msgRoot['Subject'] = 'Re: '+ subject
            else:
                msgRoot['Subject'] = subject
        else:
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

        trail = html_version

        #Need to construct reply email body in Gmail format
        if parent_mailbox:
            in_reply_to = parent_mailbox.get_msgId()
            references = parent_mailbox.get_references()
            if not references:
                references = in_reply_to
            else:
                references = references + ' ' + in_reply_to

            msgRoot.add_header('References', references)
            msgRoot.add_header('In-Reply-To', in_reply_to)


        return msgRoot, trail

    def _construct_trail(self, parent_mailbox):
        trail = parent_mailbox.get_trail()
        if not trail:
            return ''

        soup = BeautifulSoup(trail, "html.parser")
        if '<html>' in trail:
            soup.html.unwrap()
        
        if '<body>' in trail:
            soup.body.unwrap()

        if '<head>' in trail:
            soup.head.unwrap()

        data_dict = parent_mailbox.get_wrote_on_data()

        wrote_on = "On {week_day}, {date} {month} {year}, {sender} wrote:".format(**data_dict)
        start = '''<br><div class="gmail_quote"><div dir="ltr" class="gmail_attr">''' + wrote_on + '''<br></div><blockquote class="gmail_quote" style="margin:0px 0px 0px 0.8ex;border-left:1px solid rgb(204,204,204);padding-left:1ex"><u></u><div>'''
        end = '''</div></blockquote></div>'''

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

    def construct_data(self,
                        message, 
                        prospect_id, 
                        campaign_id, 
                        msgId,
                        plain_text='',
                        html_text='',
                        trail = '', 
                        mailbox_reply_to_id='',
                        api_res = {},
                        sender_meta={}):

        references = message.get(name='References', failobj='')
        sender = message.get(name='From', failobj=self.email)

        email_data = {
            'msgId' : msgId,
            'mailbox_parent_id' : mailbox_reply_to_id,
            'message' : message,
            'references' : references.strip(),
            'text' : plain_text,
            'html' : html_text,
            'trail' : trail,
            'sender' : sender,
            'api_res' : api_res
        }

        
        if not sender_meta:
            sender_meta = {
                'credentials' : self.credentials
            }
            if self.smtp:
                sender_meta['type'] = 'smtp'
            else:
                sender_meta['type'] = 'api'

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
            return self.provider.send_message(message=message)

        return -1

    def get_msgId(self, msg_id):
        msgId = ''
        msg = self.provider.get_message_data(msg_id=msg_id, metadataHeaders=['Message-Id'])
        payload = msg.get('payload', '')
        if payload:
            headers = payload.get('headers', '')
            if headers:
                for header in headers:
                    if header.get('name', '') == 'Message-Id':
                        msgId = header.get('value', '')
                        break
        return msgId
