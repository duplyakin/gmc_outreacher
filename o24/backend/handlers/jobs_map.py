import o24.backend.handlers.dummy as dummy
import os

JOBS_MAP = None

JOBS_MAP_TEST = {
    'linkedin-check-reply' : dummy.dummy_linkedin_check_reply, 
    'linkedin-visit-profile' : dummy.dummy_linkedin_visit_profile,
    'linkedin-connect' : dummy.dummy_linkedin_connect,
    'linkedin-send-message' : dummy.dummy_linkedin_send_message,
    'email-send-message' : dummy.dummy_email_send_message,
    'delay' : dummy.dummy_delay,
    'finished' : dummy.dummy_finished,
    'success' : dummy.dummy_success,
    'linkedin-check-accept' : dummy.dummy_linkedin_check_accept,
    'email-check-reply' : dummy.dummy_email_check_reply,
}

JOBS_MAP_PROD = {}

env = os.environ.get('APP_ENV', None)
if env == "Test":
    JOBS_MAP = JOBS_MAP_TEST
else:
    JOBS_MAP = JOBS_MAP_PROD
