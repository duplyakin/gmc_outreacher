from o24.backend.handlers.email_senders.utils import *
from o24.globals import *
import traceback
import time
import random
from o24.exceptions.exception_with_code import ErrorCodeException
from o24.backend.gmail.controller import GmailController
from o24.backend.models.inbox.mailbox import MailBox
import o24.backend.handlers.email_senders.gmail_api as gmail_api

def check_reply(task, **kwargs):
    return gmail_api.check_reply(task, **kwargs)

def send_email(task, **kwargs):
    access_credentials = kwargs['credentials_data'].get('credentials', '')
    if not access_credentials:
        raise Exception("Can't find access_credentials for credentials task_id:{0}".format(task.id))

    
    gmail_controller = GmailController(email=kwargs['email_from'],
                                        credentials=access_credentials,
                                        credentials_id=kwargs['credentials_id'],
                                        smtp=True)
    parent_mailbox = kwargs['parent_mailbox']

    reply = check_reply(task, **kwargs)

    if type(reply) is dict:
        if_true = reply.get('if_true', None)
        if if_true:
            return reply


    email_from, \
    email_to, \
    subject, \
    body_html, \
    body_plain, \
    message, \
    trail = construct_message(task=task, 
                            mail_controller=gmail_controller, 
                            mailbox=parent_mailbox)
    
    msgId, message = gmail_controller.add_header_msgId(message)

    gmail_controller.send_message(email_to=email_to,
                                        message=message)
    
    mailbox_reply_to_id = ''
    if parent_mailbox:
        mailbox_reply_to_id = parent_mailbox.id

    data = gmail_controller.construct_data(
                message, 
                kwargs['prospect_id'], 
                kwargs['campaign_id'], 
                msgId,
                plain_text=body_plain,
                html_text=body_html,
                trail=trail,
                mailbox_reply_to_id=mailbox_reply_to_id)

    message_type = 1
    if parent_mailbox:
        message_type = 2
    
    mailbox = MailBox.add_message(data, message_type=message_type)

    result_data = {
        'if_true' : True,
        'code' : 0,
        'mailbox_id' : mailbox.id
    }

    return result_data