from o24.backend.handlers.email_senders.utils import *
from o24.globals import *
import traceback
import time
import random
from o24.exceptions.exception_with_code import ErrorCodeException
from o24.backend.gmail.controller import GmailController
from o24.backend.models.inbox.mailbox import MailBox
from datetime import datetime

def check_reply(task, **kwargs):
    access_credentials = kwargs['credentials_data'].get('credentials', '')
    if not access_credentials:
        raise Exception("Can't find access_credentials for credentials task_id:{0}".format(task.id))

    
    gmail_controller = GmailController(email=kwargs['email_from'],
                                        credentials=access_credentials,
                                        credentials_id=kwargs['credentials_id'],
                                        smtp=False)
    
    start_time = MailBox.sequence_start_date(prospect_id=kwargs['prospect_id'], 
                                            campaign_id=kwargs['prospect_id'])
    
    prospect_email = kwargs['prospect_data'].get('email')
    messages = gmail_controller.check_reply(email_from=prospect_email, 
                                            after=start_time)
    result_data = {
        'if_true' : False,
        'code' : 0
    }
    if not messages:
        return result_data
    else:
        result_data['if_true'] = True
        result_data['reply_found_at'] = str(datetime.utcnow())


    #TODO - need to save reply to MailBox

    return result_data

    
def send_email(task, **kwargs):
    access_credentials = kwargs['credentials_data'].get('credentials', '')
    if not access_credentials:
        raise Exception("Can't find access_credentials for credentials task_id:{0}".format(task.id))

    
    gmail_controller = GmailController(email=kwargs['email_from'],
                                        credentials=access_credentials,
                                        credentials_id=kwargs['credentials_id'],
                                         smtp=False)
    
    parent_mailbox = kwargs['parent_mailbox']

    reply = check_reply(task, **kwargs)

    if type(reply) is dict:
        if_true = reply.get('if_true', None)
        if if_true:
            return reply


    email_from, 
    email_to,
    subject,
    body_html,
    body_plain,
    message,
    trail = construct_message(task=task, 
                                gmail_controller=gmail_controller, 
                                mailbox=parent_mailbox)

    raw_message = gmail_controller.add_gmail_api_meta(message=message,
                                                    parent_mailbox=parent_mailbox)
    
    api_res = gmail_controller.send_message(email_to=email_to, 
                                            message=raw_message)

    mailbox_reply_to_id = ''
    if parent_mailbox:
        mailbox_reply_to_id = parent_mailbox.id

    data = gmail_controller.construct_data(
                    message=message, 
                    prospect_id=kwargs['prospect_id'], 
                    campaign_id=kwargs['campaign_id'], 
                    msgId='',
                    plain_text=body_plain,
                    html_text=body_html,
                    trail = trail, 
                    api_res = api_res,
                    mailbox_reply_to_id=mailbox_reply_to_id)

    message_type = 1
    if parent_mailbox:
        message_type = 2
    
    mailbox = MailBox.add_message(data, message_type=message_type)

    msg_id = mailbox.get_api_msg_id()

    msgId = gmail_controller.get_msgId(msg_id=msg_id)

    mailbox.set_msgId(msgId=msgId)

    result_data = {
        'if_true' : True,
        'code' : 0,
        'mailbox_id' : mailbox.id
    }

    return result_data
