from celery import Celery
from celery.schedules import crontab
import o24.config as config

#Init celery instance
def make_celery():
    celery = Celery(__name__, broker=config.CELERY_BROKER)
    celery.conf.update(config.as_dict())
    return celery

celery = make_celery()

#Setup celery scheduler
celery.conf.beat_schedule = {
    "scheduler": {
        "task": config.SCHEDULER_HANDLER,
        "schedule": config.SCHEDULER_HANDLER_PERIOD
    }
}


#celery.conf.beat_schedule = {
#    'scheduler': {
#        'task': 'celery_uncovered.toyex.tasks.produce_hot_repo_report_task',
#        'schedule': crontab(minute=0, hour=0)  # midnight,
#        'args': ('today',)
#    },
#}

