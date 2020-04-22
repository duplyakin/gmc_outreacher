import os

class BaseConfig():
    TESTING = False
    DEBUG = False
    OAUTHLIB_INSECURE_TRANSPORT = 1
    OAUTHLIB_RELAX_TOKEN_SCOPE = 1
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'  # to not recieve Warning: Scope has changed

    # Flask-User settings
    USER_APP_NAME = "O24Mc"      # Shown in and email templates and page footers
    USER_ENABLE_USERNAME = False    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form

    USER_EMAIL_SENDER_EMAIL = 'hello@outreacher24.com'
    USER_ENABLE_CONFIRM_EMAIL = False
    USER_ENABLE_EMAIL = True      # Disable email authentication
    USER_SEND_REGISTERED_EMAIL = False


    #CELERY periodic tasks settings
    SCHEDULER_HANDLER_PERIOD = 10
    SCHEDULER_HANDLER = 'emit_scheduler'
    #WATCH_DOG_HANDLER = 'emit_test_watch_dog'
    broker_transport_options = {"max_retries": 3, "interval_start": 0, "interval_step": 0.2, "interval_max": 0.5}


    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED     = True

    # Use a secure, unique and absolutely secret key for
    # signing the data. 
    CSRF_SESSION_KEY = "secret"

    # Secret key for signing cookies
    SECRET_KEY = "secret"

    #UI specific settings
    PER_PAGE = 10
    USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ["pbkdf2_sha256"]

    PROSPECTS_PER_PAGE = 100
    #Flask-User customization
    #USER_LOGIN_TEMPLATE = 'login/login.html'
    #USER_REGISTER_TEMPLATE = 'login/register.html'

    GMAIL_SMTP_HOST = 'smtp.gmail.com'
    GMAIL_SMTP_PORT = 587

class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_BROKER = 'amqp://guest:guest@localhost:5672//'
    CELERY_BACKEND_RESULT_EXPIRES = 300
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    MONGODB_SETTINGS = {
        'db': 'O24Mc-dev',
        'host': '127.0.0.1',
        'port': 27017
    }

class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    CELERY_BROKER = 'amqp://guest:guest@localhost:5672//'
    CELERY_BACKEND_RESULT_EXPIRES = 300
    
    MONGODB_SETTINGS = {
        'db': 'O24Mc-prod',
        'host': '127.0.0.1',
        'port': 27017
    }

class TestConfig(BaseConfig):
    FLASK_ENV = 'test'
    DEBUG = True
    TESTING = True
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_BROKER = 'amqp://guest:guest@localhost:5672//'
    CELERY_BACKEND_RESULT_EXPIRES = 300
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED=False
    MONGODB_SETTINGS = {
        'db': 'O24Mc-test',
        'host': '127.0.0.1',
        'port': 27017
    }