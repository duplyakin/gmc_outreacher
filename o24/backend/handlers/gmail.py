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
from o24.backend.utils.templates import *

def construct_message(task, gmail_controller, mailbox):
    input_data = task.get_input_data()
    if not input_data:
        raise Exception("input_data error: can't construct message")

    template_data = input_data.get('template_data', None)
    if not template_data:
        raise Exception("template_data error: can't construct message")

    prospect_data = input_data.get('prospect_data', None)
    if not prospect_data:
        raise Exception("prospect_data error: can't construct message")

    subject = template_data.get('subject', None)
    if not subject:
        raise Exception("no subject: can't construct message")

    body_html = template_data.get('body', None)
    if not body_html:
        raise Exception("no body: can't construct message")
    
    plain = template_data.get('plain', None)
    if not plain:
        raise Exception("no plain version of email: can't construct message")
    
    body_plain = plain.get('body', None)
    if not body_plain:
        raise Exception("Plain body can't be empty")

    email_from = gmail_controller.current_email()
    if not email_from:
        raise Exception("email_from can't be empty")

    email_to = prospect_data.get('email', '')
    if not email_to:
        raise Exception("prospect doesn't have email: check your data")

    #INSERT TAGS
    subject = insert_tags(subject, prospect_data)
    body_html = insert_tags(body_html, prospect_data)
    body_plain = insert_tags(body_plain, prospect_data)


    message, trail = gmail_controller.create_multipart_message( 
                                                email_from=email_from,
                                                email_to=email_to,
                                                subject=subject,
                                                plain_version=body_plain,
                                                html_version=body_html,
                                                parent_mailbox=mailbox)

    return email_from, \
            email_to, \
            subject, \
            body_html, \
            body_plain, \
            message, \
            trail

def send_via_smtp(gmail_controller, 
                    task, 
                    prospect_id,
                    campaign_id,
                    parent_mailbox):
    result_data = {
        'code' : 0
    }

    email_from, \
    email_to, \
    subject, \
    body_html, \
    body_plain, \
    message, \
    trail = construct_message(task=task, 
                                        gmail_controller=gmail_controller, 
                                        mailbox=parent_mailbox)


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
        'mailbox_id' : mailbox.id
    }

    return result_data


def send_via_api(gmail_controller,
                    task, 
                    prospect_id,
                    campaign_id,
                    parent_mailbox):
    
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
                    prospect_id=prospect_id, 
                    campaign_id=campaign_id, 
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
        'mailbox_id' : mailbox.id
    }

    return result_data


def smtp_response_check(gmail_controller, 
                    task, 
                    prospect_id,
                    campaign_id,
                    parent_mailbox):
    return None

def api_response_check(gmail_controller,
                    task, 
                    prospect_id,
                    campaign_id,
                    parent_mailbox):
    return None


@celery.task
def gmail_check_reply(task_id):
    pass

@celery.task
def gmail_send_message(task_id):
    result_data = {
        'if_true' : False,
        'code' : -1,
        'error' : 'Unknown Error'
    }
    response = None

    try:
        task = shared.TaskQueue.get_task(task_id)
        if not task:
            raise Exception("No such task id:{0}".format(task_id))
        
        task.acknowledge()

        prospect_id = task.prospect_id
        campaign_id = task.campaign_id
        input_data = task.get_input_data()
        if not input_data:
            raise Exception("INPUT_DATA ERROR: No input_data for task_id:{0}".format(task_id))
        
        credentials_data = input_data.get('credentials_data', '')
        if not credentials_data:
            raise Exception("INPUT_DATA.CREDENTIALS_DATA ERROR: No credentials_data for task_id:{0}".format(task_id))
        
        email = credentials_data.get('email', '')
        if not email:
            raise Exception("Can't find email for credentials task_id:{0}".format(task_id))

        sender = credentials_data.get('sender', '')
        if not sender:
            raise Exception("Can't find sender for credentials task_id:{0}".format(task_id))
    
        smtp = False
        if sender == 'smtp':
            smtp = True

        access_credentials = credentials_data.get('credentials', '')
        if not access_credentials:
            raise Exception("Can't find access_credentials for credentials task_id:{0}".format(task_id))


        gmail_controller = GmailController(email=email,
                                            credentials=access_credentials,
                                            smtp=smtp)

        parent_mailbox = MailBox.get_parent(prospect_id=prospect_id, campaign_id=prospect_id)
        if not parent_mailbox:
            parent_mailbox = None


        if smtp:
            response = smtp_response_check(gmail_controller, 
                                        task, 
                                        prospect_id=prospect_id, 
                                        campaign_id=campaign_id, 
                                        parent_mailbox=parent_mailbox)
            if not response:
                result_data = send_via_smtp(gmail_controller, 
                                            task, 
                                            prospect_id=prospect_id, 
                                            campaign_id=campaign_id, 
                                            parent_mailbox=parent_mailbox)
        else:
            response = api_response_check(gmail_controller, 
                                        task,
                                        prospect_id=prospect_id,
                                        campaign_id=campaign_id, 
                                        parent_mailbox=parent_mailbox)
            if not response:
                result_data = send_via_api(gmail_controller, 
                                            task,
                                            prospect_id=prospect_id,
                                            campaign_id=campaign_id, 
                                            parent_mailbox=parent_mailbox)

    except Exception as e:
        print(e)
        traceback.print_exc()

        result_data = {
            'error' : str(e),
            'code' : -1
        }
        
        task.set_result(result_data)
        task.update_status(status=FAILED)
        return 
    
    if not response:
        task.set_result(result_data)
        if result_data.get('if_true', False):
            task.update_status(status=CARRYOUT)
        else:
            task.update_status(status=FAILED)
    else:
        result_data = {
            'code' : EMAIL_HAS_RESPONSE
        }
        task.set_result(result_data)
        task.update_status(status=CARRYOUT)

    return