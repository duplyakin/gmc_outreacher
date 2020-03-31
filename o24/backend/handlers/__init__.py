from celery import Celery
import config

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
