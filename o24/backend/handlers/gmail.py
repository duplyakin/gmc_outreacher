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

def send_via_smtp(gmail_controller, 
                    task, 
                    propspect_id,
                    campaign_id,
                    parent_mailbox):
    result_data = {}

    email_from = gmail_controller.current_email()
    
    send_to_data = task.get_send_data()

    email_to = send_to_data.get('email_to')
    subject = send_to_data.get('subject')
    plain_version = send_to_data.get('plain')
    html_version = send_to_data.get('html')

    message, trail = gmail_controller.create_multipart_message( 
                                                email_from=email_from,
                                                email_to=email_to,
                                                subject=subject,
                                                plain_version=plain_version,
                                                html_version=html_version,
                                                parent_mailbox=parent_mailbox)

    msgId, message = gmail_controller.add_header_msgId(message)

    res = gmail_controller.send_message(email_to=email_to,
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
                plain_text=plain_version,
                html_text=html_version,
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
    
    send_to_data = task.get_send_data()

    email_to = send_to_data.get('email_to')
    subject = send_to_data.get('subject')
    plain_version = send_to_data.get('plain')
    html_version = send_to_data.get('html')

    message, trail = gmail_controller.create_multipart_message( 
                                    email_from=email_from,
                                    email_to=email_to,
                                    subject=subject,
                                    plain_version=plain_version,
                                    html_version=html_version,
                                    parent_mailbox=parent_mailbox)

    raw_message = gmail_controller.add_gmail_api_meta(message=message,
                                                    parent_mailbox=parent_mailbox)
    api_res = gmail_controller.send_message(email_to=email_to, 
                                            message=raw_message)

    mailbox_reply_to_id = ''
    if parent_mailbox:
        mailbox_reply_to_id = parent_mailbox.id

    data = gmail_controller.construct_data(
                    message=message, 
                    prospect_id=prospect_id, 
                    campaign_id=campaign_id, 
                    msgId='',
                    plain_text=plain_version,
                    html_text=html_version,
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
    credentials = task.credentials_dict.get('credentials', '')
    if not credentials:
        raise Exception("No credentials for task_id:{0}".format(task_id))

    email = task.credentials_dict.get('email', '')
    if not email:
        raise Exception("Can't find email for credentials task_id:{0}".format(task_id))

    credentials_type = task.credentials_dict.get('credentials_type', '')
    smtp = False
    if credentials_type == 'smtp':
        smtp = True

    gmail_controller = GmailController(email=email,
                                        credentials=credentials,
                                        smtp=smtp)

    is_followup = task.is_followup()
    parent_mailbox = None

    if is_followup:
        parent_mailbox = Mailbox.get_parent(prospect_id=propspect_id, campaign_id=propspect_id)
        if not parent_mailbox:
            raise Exception('There is no previous email found task_id:{0}'.format(task_id))

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