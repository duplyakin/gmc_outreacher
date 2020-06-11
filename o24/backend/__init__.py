# Import flask and template operators
from flask import Flask, request, g, session, redirect, url_for, render_template
from flask_mongoengine import MongoEngine
from flask import jsonify
import logging
import os
import o24.config as config
from celery import Celery
from flask_jwt_extended import JWTManager
from flask_cors import CORS

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
        },
        "enricher" : {
            "task": config.ENRICHER_HANDLER,
            "schedule": config.ENRICHER_HANDLER_PERIOD
        }
    }

    CORS(app)
    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        pass
        #return render_template('errors/404.html'), 404
    
    #ADD BEFORE request handlers
    #@app.before_request
    #def before_request():
    #    if env == "Test" and test_user:
    #        g.user = test_user
    #    else:
    #        g.user = None
    #        if 'user_id' in session:
    #            g.user = models.User.objects.get(id=session['user_id'])
    

    return app

app = create_app()
db = MongoEngine(app)
jwt = JWTManager(app)


# Import a module / component using its blueprint handler variable (mod_auth)
from o24.backend.dashboard import bp_dashboard
from o24.backend.scheduler import bp_scheduler

# Register blueprint(s)
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_scheduler)