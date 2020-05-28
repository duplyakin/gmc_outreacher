from o24.globals import *
import o24.backend.handlers.dummy as dummy
import o24.backend.handlers.general as general
import o24.backend.handlers.email as email

import os

JOBS_MAP = None

JOBS_MAP_TEST = {
    'linkedin-check-reply' : dummy.dummy_linkedin_check_reply, 
    'linkedin-visit-profile' : dummy.dummy_linkedin_visit_profile,
    'linkedin-connect' : dummy.dummy_linkedin_connect,
    'linkedin-send-message' : dummy.dummy_linkedin_send_message,
    'email-send-message' : dummy.dummy_email_send_message,
    'delay-linkedin' : dummy.dummy_delay,
    'delay-email' : dummy.dummy_delay,
    'finished' : dummy.dummy_finished,
    'success' : dummy.dummy_success,
    'linkedin-check-accept' : dummy.dummy_linkedin_check_accept,
    'email-check-reply' : dummy.dummy_email_check_reply,
    DELAY_ACTION: dummy.dummy_delay
}

JOBS_MAP_PROD = {
    EMAIL_SEND_MESSAGE_ACTION: email.email_send_message,
    EMAIL_CHECK_REPLY_ACTION: email.email_check_reply,
    DELAY_ACTION: general.delay_handler,
    FINISHED_ACTION: general.finished_handler,
    SUCCESS_ACTION: general.success_handler
}

env = os.environ.get('APP_ENV', None)
if env == "Test":
    JOBS_MAP = JOBS_MAP_TEST
else:
    JOBS_MAP = JOBS_MAP_PROD
