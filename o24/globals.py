FAILED = -1
FAILED_NEED_ACTION = -2

#scheduler statuses
NEW = 0 #this status can be get by execution stage
IN_PROGRESS = 1 #execution
PAUSED = 2 #Not used
FINISHED = 3
READY = 4
CARRYOUT = 5
BLOCK_HAPPENED = 6
NEED_USER_ACTION = 7
NEED_USER_ACTION_PROGRESS = 8
NEED_USER_ACTION_RESOLVED = 9


TASKS_CAN_BE_PAUSED = [IN_PROGRESS]
TASKS_CAN_BE_RESUMED = [PAUSED]
TRAIL_STATUSES = [FAILED, CARRYOUT, BLOCK_HAPPENED, NEED_USER_ACTION_RESOLVED]

ACTION_NONE = -1

INTRO=0
FOLLOWUP=1

#ENRICH controller statuses
ENRICH_NEW = 0
ENRICH_IN_PROGRESS = 1
ENRICH_SUCCESS = 2
ENRICH_FAILED_TO_FOUND = 3
ENRICH_TRIED_ALL = 4
ENRICH_OUT_OF_CREDITS = 5
ENRICH_MOVED = 6

#ENRICH Providers
SNOVIO_PROVIDER = 1

# this is the secs that you need to substruct to receive correct time in POSIX
MAGIC_TIME_DIFF_SEC = 3015

#15 hours
NEXT_DAY_SECONDS = 15 * 60 * 60
DAY_TO_SECONDS = 24 * 60 * 60

FINISHED_KEYS = ['finished', 'success']

#Activated mediums
ACTIVATED_MEDIUMS = ['special-medium', 'email']

#defaults
DEFAULT_PER_DAY_LIMIT=500
DEFAULT_INTERVAL=20

SM_DEFAULT_PER_DAY_LIMIT=100000
SM_DEFAULT_INTERVAL=0

DEFAULT_FROM_HOUR=7
DEFAULT_TO_HOUR=21
DEFAULT_SENDING_DAYS = {
        '0' : True,
        '1' : True,
        '2' : True, 
        '3' : True,
        '4' : True,
        '5' : False,
        '6' : False
}
DEAFULT_TRACKING_EVENTS = {
        'open' : True,
        'click' : False
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

GENERAL_FUNNEL_TYPE = 0 
LINKEDIN_PARSING_FUNNEL_TYPE = 1
LINKEDIN_ENRICHMENT_FUNNEL_TYPE = 2



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
EMAIL_CHECK_REPLY_ACTION = 'email-check-reply' #potential BUG: what if we will add this action to SPECIAL_ACTIONS ?
EMAIL_CHECK_BOUNCED_ACTION = 'email-check-bounced'

EMAIL_ENRICH = 'email-enrich'
EMAIL_CHECK_ENRICHED = 'email-check-enriched'


DELAY_ACTION = 'delay'
ENRICH_DELAY_ACTION = 'delay-enrich' #helpfull for logs and test
FINISHED_ACTION = 'finished'
SUCCESS_ACTION = 'success'

#actions that we can execute parallel on 1 account
SPECIAL_ACTIONS = [EMAIL_CHECK_REPLY_ACTION,
                        EMAIL_CHECK_BOUNCED_ACTION,
                        EMAIL_ENRICH,
                        ENRICH_DELAY_ACTION,
                        EMAIL_CHECK_ENRICHED,
                        DELAY_ACTION,
                        FINISHED_ACTION,
                        SUCCESS_ACTION]


DEFAULT_SEARCH_DELAY = 605
DEFAULT_PROFILE_ENRICH_DELAY = 705


NON_3RD_PARTY_ACTION_KEYS = [EMAIL_SEND_MESSAGE_ACTION,
                                EMAIL_CHECK_REPLY_ACTION,
                                DELAY_ACTION,
                                ENRICH_DELAY_ACTION,
                                EMAIL_CHECK_BOUNCED_ACTION,
                                EMAIL_ENRICH,
                                EMAIL_CHECK_ENRICHED,
                                FINISHED_ACTION,
                                SUCCESS_ACTION]


#CARRYOUT CODES
CARRYOUT_DEFAULT_HANDLER = 'carryout_default_handler'
BLOCK_DEFAULT_HANDLER = -666

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
EMAIL_HAS_RESPONSE = 10000


#EMAIL/SMTP error
SMTP_AUTH_ERROR = 530
SMTP_RECEIPENT_REJECTED = 541
SMTP_NON_EXISTENT_EMAIL = 550

SMTP_UNKNOWN_ERROR = -1


#LIMITS:

EMAIL_LIMITS_DAILY = {
        'smtp' : {
                'limits' : {
                        'account_maximum' : 250,
                        EMAIL_SEND_MESSAGE_ACTION: 250,
                },
                'warmup' : {
                        'account_maximum' : 25,
                        EMAIL_SEND_MESSAGE_ACTION: 25,

                        'interval_sec' : 60,
                        'increase' : 1.33,
                        'days_inactivity' : 5
                }
        },
        'api' : {
                'limits' : {
                        'account_maximum' : 500,
                        EMAIL_SEND_MESSAGE_ACTION: 500,
                },
                'warmup' : {
                        'account_maximum' : 40,
                        EMAIL_SEND_MESSAGE_ACTION: 40,

                        'interval_sec' : 60,
                        'increase' : 1.33,
                        'days_inactivity' : 5   
                }
        }
}

LINKEDIN_LIMITS_DAILY = {
        'basic' : {
                'limits' : {
                        'account_maximum' : 240,
                        LINKEDIN_SEARCH_ACTION: 100,
                        LINKEDIN_PARSE_PROFILE_ACTION: 120,
                        LINKEDIN_VISIT_PROFILE_ACTION: 500,
                        LINKEDIN_CONNECT_ACTION: 100,
                        LINKEDIN_SEND_MESSAGE_ACTION: 100
                },
                'warmup' : {
                        'account_maximum' : 80,
                        LINKEDIN_SEARCH_ACTION: 10,
                        LINKEDIN_PARSE_PROFILE_ACTION: 20,
                        LINKEDIN_VISIT_PROFILE_ACTION: 100,
                        LINKEDIN_CONNECT_ACTION: 20,
                        LINKEDIN_SEND_MESSAGE_ACTION: 10,

                        'interval_sec' : 60,
                        'increase' : 1.33,
                        'days_inactivity' : 5
                }
        },
        'premium' : {
                'limits' : {
                        'account_maximum' : 250,
                        LINKEDIN_SEARCH_ACTION: 200,
                        LINKEDIN_PARSE_PROFILE_ACTION: 300,
                        LINKEDIN_VISIT_PROFILE_ACTION: 500,
                        LINKEDIN_CONNECT_ACTION: 300,
                        LINKEDIN_SEND_MESSAGE_ACTION: 300
                },
                'warmup' : {
                        'account_maximum' : 100,
                        LINKEDIN_SEARCH_ACTION: 20,
                        LINKEDIN_PARSE_PROFILE_ACTION: 40,
                        LINKEDIN_VISIT_PROFILE_ACTION: 150,
                        LINKEDIN_CONNECT_ACTION: 30,
                        LINKEDIN_SEND_MESSAGE_ACTION: 20,

                        'interval_sec' : 60,
                        'increase' : 1.33,
                        'days_inactivity' : 5
                }
        }
}

WORKAROUND_PASS = ['account_maximum', 'interval_sec', 'increase', 'days_inactivity']

BOUNCED_DAEMONS = {
        'api' : 'mailer-daemon@googlemail.com',
        'smtp' : 'mailer-daemon@googlemail.com'
}

LIMITS_BASED_ON_MEDIUM = {
        'email' : EMAIL_LIMITS_DAILY,
        'linkedin' : LINKEDIN_LIMITS_DAILY
}

NO_LIMITS_MEDIUMS = ['special-medium']
LIMITS_24_PERIOD_SECS = 86500  #24 hours period in seconds
RANDOM_INTERVAL_MAX = 5 # will calculate interval = randrange(interval_sec, interval_sec * RANDOM_INTERVAL_MAX)


TASK_QUEUE_LOCK = 'taskqueue_lock'
ENRICH_TASK_QUEUE_LOCK = 'enrich_taskqueue_lock'

CSV_EXPORT_HEADERS = {
        'campaign' : 'assign_to#title',
        'leads list' : 'assign_to_list#title',
        'first_name' : 'data#first_name',
        'last_name' : 'data#last_name',
        'email' : 'data#email',
        'linkedin' : 'data#linkedin',
        'company url' : 'data#company_url',
        'company linkedin page' : 'data#company_linkedin_page',
        'country' : 'data#country',
        'education' : 'data#education',
        'job title' : 'data#job_title',
        'twitter' : 'data#twitter'
}

CAMPAIGN_STATUSES_CSV = {
        0 : 'New',
        1 : 'In progress',
        2 : 'Paused',
        3 : 'Finished',
        -1 : 'Failed',
        -2 : 'Failed need action'
}

#STATISTICS
TOTAL_STATS_DAYS_DEFAULT = 7