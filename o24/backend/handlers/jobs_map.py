import o24.backend.handlers.dummy as dummy

JOBS_MAP = {
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