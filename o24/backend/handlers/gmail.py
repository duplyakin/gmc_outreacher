from o24.backend import celery
import o24.backend.scheduler.scheduler as scheduler
from flask import current_app
from o24.globals import *
import traceback
import time
import random
import o24.backend.models.shared as shared

from o24.backend.gmail.controller import GmailController
from o24.backend.models.inbox.mailbox import MailBox

def email_data_extract(gmail_controller, task):
    data = {
        'email_to' : '',
        'subject' : '',
        'plain_version' : '',
        'html_version' : ''
    }

    send_to_data = task.get_email_data()

    email_to = send_to_data.get('email_to')
    template = send_to_data.get('template')

    subject = gmail_controller.inser_tags(template.get('subject'))
    plain_version = gmail_controller.inser_tags(template.get('plain'))
    
    html_version = gmail_controller.inser_tags(template.get('html'))
    html_version = gmail_controller.insert_images(html_version)

    data['email_to'] = email_to
    data['subject'] = subject
    data['plain_version'] = plain_version
    data['html_version'] = html_version

    return data

def send_via_smtp(gmail_controller, 
                    task, 
                    propspect_id,
                    campaign_id,
                    parent_mailbox):
    result_data = {}
    email_from = gmail_controller.current_email()

    send_to_data = email_data_extract(gmail_controller, task)

    message, trail = gmail_controller.create_multipart_message( 
                                                email_from=email_from,
                                                email_to=send_to_data.get('email_to'),
                                                subject=send_to_data.get('subject'),
                                                plain_version=send_to_data.get('plain_version'),
                                                html_version=send_to_data.get('html_version'),
                                                parent_mailbox=parent_mailbox)

    msgId, message = gmail_controller.add_header_msgId(message)

    res = gmail_controller.send_message(email_to=send_to_data.get('email_to'),
                                        message=message)

    if res:
        result_data['if_true'] = False
        result_data['res'] = res
        return result_data
    
    mailbox_reply_to_id = ''
    if parent_mailbox:
        mailbox_reply_to_id = parent_mailbox.id

    data = gmail_controller.construct_data(
                message, 
                prospect_id, 
                campaign_id, 
                msgId,
                plain_text=send_to_data.get('plain_version'),
                html_text=send_to_data.get('html_version'),
                trail=trail,
                mailbox_reply_to_id=mailbox_reply_to_id)

    message_type = 1
    if parent_mailbox:
        message_type = 2
    
    mailbox = MailBox.add_message(data, message_type=message_type)

    result_data = {
        'if_true' : True,
        'mailbox_id' : mailbox.id
    }

    return result_data


def send_via_api(gmail_controller,
                    task, 
                    propspect_id,
                    campaign_id,
                    parent_mailbox):
    
    email_from = gmail_controller.current_email()

    send_to_data = email_data_extract(gmail_controller, task)
    

    message, trail = gmail_controller.create_multipart_message( 
                                    email_from=email_from,
                                    email_to=send_to_data.get('email_to'),
                                    subject=send_to_data.get('subject'),
                                    plain_version=send_to_data.get('plain_version'),
                                    html_version=send_to_data.get('html_version'),
                                    parent_mailbox=parent_mailbox)

    raw_message = gmail_controller.add_gmail_api_meta(message=message,
                                                    parent_mailbox=parent_mailbox)
    
    api_res = gmail_controller.send_message(email_to=send_to_data.get('email_to'), 
                                            message=raw_message)

    mailbox_reply_to_id = ''
    if parent_mailbox:
        mailbox_reply_to_id = parent_mailbox.id

    data = gmail_controller.construct_data(
                    message=message, 
                    prospect_id=prospect_id, 
                    campaign_id=campaign_id, 
                    msgId='',
                    plain_text=send_to_data.get('plain_version'),
                    html_text=send_to_data.get('html_version'),
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
        'mailbox_id' : mailbox.id
    }

    return result_data


@celery.task
def gmail_send_message(task_id):
    
    task = shared.TaskQueue.get_task(task_id)
    if not task:
        raise Exception("No such task id:{0}".format(task_id))
    
    task.acknowledge()

    propspect_id = task.propspect_id
    campaign_id = task.campaign_id
    data = task.credentials_dict.get('data', '')
    if not data:
        raise Exception("No data for task_id:{0}".format(task_id))

    credentials = data.get('credentials', '')
    email = data.get('email', '')
    if not email:
        raise Exception("Can't find email for credentials task_id:{0}".format(task_id))

    sender = data.get('sender', '')
    smtp = False
    if sender == 'smtp':
        smtp = True

    gmail_controller = GmailController(email=email,
                                        credentials=credentials,
                                        smtp=smtp)

    parent_mailbox = Mailbox.get_parent(prospect_id=propspect_id, campaign_id=propspect_id)
    if not parent_mailbox:
        parent_mailbox = None


    result_data = {
        'if_true' : False,
        'error' : 'Unknown Error'
    }
    try:
        if smtp:
            result_data = send_via_smtp(gmail_controller, 
                                        task, 
                                        propspect_id=propspect_id, 
                                        campaign_id=campaign_id, 
                                        parent_mailbox=parent_mailbox)
        else:
            result_data = send_via_api(gmail_controller, 
                                        task,
                                        propspect_id=propspect_id,
                                        campaign_id=campaign_id, 
                                        parent_mailbox=parent_mailbox)

    except Exception as e:
        result_data = {
            'error' : str(e)
        }
        
        task.set_result(result_data)
        task.update_status(status=FAILED)
        return 
    
    
    task.set_result(result_data)
    if result_data.get('if_true', False):
        task.update_status(status=READY)
    else:
        task.update_status(status=FAILED)

    return