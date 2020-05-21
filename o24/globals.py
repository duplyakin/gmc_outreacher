NEW = 0 #this status can be get by execution stage
IN_PROGRESS = 1 #execution
PAUSED = 2 #Not used
FINISHED = 3
READY = 4
CARRYOUT = 5
FAILED = -1

TASKS_CAN_BE_PAUSED = [IN_PROGRESS]
TASKS_CAN_BE_RESUMED = [PAUSED]

ACTION_NONE = -1

INTRO=0
FOLLOWUP=1

#15 hours
NEXT_DAY_SECONDS = 15 * 60 * 60
DAY_TO_SECONDS = 24 * 60 * 60

FINISHED_KEYS = ['finished', 'success']


#defaults
DEFAULT_PER_DAY_LIMIT=10000
DEFAULT_INTERVAL=0

DEFAULT_FROM_HOUR=7
DEFAULT_TO_HOUR=21
DEFAULT_SENDING_DAYS={
        '0' : True,
        '1' : True,
        '2' : True, 
        '3' : True,
        '4' : True,
        '5' : False,
        '6' : False
}

DEFAULT_TIME_ZONE = {
        'label': "(GMT+00:00) United Kingdom Time",
        'value': "Europe/London",
        'offset': 0
}

#CAMPAIGN TYPES
OUTREACH_CAMPAIGN_TYPE = 0
LINKEDIN_PARSING_CAMPAIGN_TYPE = 1
LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE = 2


#MEDIUMS
GMAIL_TYPE = 'gmail'


#Current actions
LINKEDIN_SEARCH_ACTION = 'linkedin-search'
LINKEDIN_PARSE_PROFILE_ACTION = 'linkedin-parse-profile'
LINKEDIN_VISIT_PROFILE_ACTION = 'linkedin-visit-profile'
LINKEDIN_CONNECT_ACTION = 'linkedin-connect'
LINKEDIN_SEND_MESSAGE_ACTION = 'linkedin-send-message'
LINKEDIN_CHECK_ACCEPT_ACTION = 'linkedin-check-accept'
LINKEDIN_CHECK_REPLY_ACTION = 'linkedin-check-reply'

EMAIL_SEND_MESSAGE_ACTION = 'email-send-message'
EMAIL_CHECK_REPLY_ACTION = 'email-check-reply'

DELAY_ACTION = 'delay'
FINISHED_ACTION = 'finished'
SUCCESS_ACTION = 'success'

NON_3RD_PARTY_ACTION_KEYS = [EMAIL_SEND_MESSAGE_ACTION,
                                EMAIL_CHECK_REPLY_ACTION,
                                DELAY_ACTION,
                                FINISHED_ACTION,
                                SUCCESS_ACTION]


#CARRYOUT CODES
CARRYOUT_DEFAULT_HANDLER = 'carryout_default_handler'

#ERROR_CODES
TRAIL_UNKNOWN_ERROR = -2000

HANDLER_ERROR = -2010
WORKER_ERROR = -2020
ACTION_ERROR = -2030
MONGODB_ERROR = -3000

LOGIN_WORKER_ERROR = -4010
CONNECT_WORKER_ERROR = -4020
CONNECT_CHECK_WORKER_ERROR = -4030
MESSAGE_WORKER_ERROR = -4040
MESSAGE_CHECK_WORKER_ERROR = -4050
SCRIBE_WORKER_ERROR = -4060
SEARCH_WORKER_ERROR = -4070

BAN_ERROR = -1 #Seems we are banned

LOGIN_ACTION_ERROR = -1010 #On our sid
LOGIN_ERROR = -1011 #Check credentials
LOGIN_PAGE_ERROR = -1012 #login page is not available Linkedin blocked us
CONNECT_ACTION_ERROR = -1020 #Not used
CONNECT_CHECK_ACTION_ERROR = -1030 #Not used
MESSAGE_ACTION_ERROR = -1040 #Not used
MESSAGE_CHECK_ACTION_ERROR = -1050 #Not used
SCRIBE_ACTION_ERROR = -1060 #Not used
SEARCH_ACTION_ERROR = -1070 #Can't open the next page, need to wait maybe because of limit


CARRYOUT_SEARCH_ACTION_PAGES_FINISHED = 1000 #we have reached the last page for this search
SUCCESS_CODE = 2000
DELAY_FINISHED_CODE = 1001