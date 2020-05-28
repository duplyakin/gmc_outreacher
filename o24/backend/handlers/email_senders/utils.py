from o24.backend.utils.templates import *

def construct_message(task, mail_controller, mailbox):
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

    email_from = mail_controller.current_email()
    if not email_from:
        raise Exception("email_from can't be empty")

    email_to = prospect_data.get('email', '')
    if not email_to:
        raise Exception("prospect doesn't have email: check your data")

    #INSERT TAGS
    subject = insert_tags(subject, prospect_data)
    body_html = insert_tags(body_html, prospect_data)
    body_plain = insert_tags(body_plain, prospect_data)


    message, trail = mail_controller.create_multipart_message( 
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
