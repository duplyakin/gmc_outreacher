# Import flask and template operators
from flask import Flask, render_template, url_for
from flask_mongoengine import MongoEngine
from flask import jsonify
import logging
import os
import o24.config as config
from celery import Celery

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()

celery = Celery(__name__, broker=config.CELERY_BROKER)


def create_app():
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object('o24.config')

    celery.conf.update(app.config)
    
    #Setup celery scheduler
    celery.conf.beat_schedule = {
        "scheduler": {
            "task": config.SCHEDULER_HANDLER,
            "schedule": config.SCHEDULER_HANDLER_PERIOD
        }
    }

    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    return app

app = create_app()
db = MongoEngine(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from o24.backend.dashboard import bp_dashboard
from o24.backend.scheduler import bp_scheduler

# Register blueprint(s)
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_scheduler)
