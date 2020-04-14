NEW = 0
IN_PROGRESS = 1
PAUSED = 2
FINISHED = 3
READY = 4
FAILED = -1

TASKS_CAN_BE_PAUSED = [IN_PROGRESS]
TASKS_CAN_BE_RESUMED = [PAUSED]

ACTION_NONE = -1

INTRO=0
FOLLOWUP=1

#15 hours
NEXT_DAY_SECONDS = 15 * 60 * 60

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


#MEDIUMS
GMAIL_TYPE = 'gmail'

