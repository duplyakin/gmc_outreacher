import os

class BaseConfig():
    TESTING = False
    DEBUG = False
    OAUTHLIB_INSECURE_TRANSPORT = 1
    OAUTHLIB_RELAX_TOKEN_SCOPE = 1
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'  # to not recieve Warning: Scope has changed

    #JWT token
    JWT_ACCESS_TOKEN_EXPIRES = False

    # Flask-User settings
    USER_APP_NAME = "O24Mc"      # Shown in and email templates and page footers
    USER_ENABLE_USERNAME = False    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form

    USER_EMAIL_SENDER_EMAIL = 'hello@outreacher24.com'
    USER_ENABLE_CONFIRM_EMAIL = False
    USER_ENABLE_EMAIL = True      # Disable email authentication
    USER_SEND_REGISTERED_EMAIL = False

    #CELERY periodic tasks settings for Enricher
    task_acks_late = True
    ENRICHER_HANDLER_PERIOD = 120
    ENRICHER_HANDLER = 'emit_enricher'

    #CELERY periodic tasks settings for Scheduler
    SCHEDULER_HANDLER_PERIOD = 60
    SCHEDULER_HANDLER = 'emit_scheduler'
    broker_transport_options = {"max_retries": 3, "interval_start": 0, "interval_step": 0.2, "interval_max": 0.5}


    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 4

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED     = True

    # Use a secure, unique and absolutely secret key for
    # signing the data. 
    CSRF_SESSION_KEY = "super-never-appatit-nomand-key-log-forget"

    # Secret key for signing cookies
    SECRET_KEY = "repus-reven-appatit90-dnamon-yek-gol-tegrof"
    AES_SECRET = b'1234567890123456'

    #UI specific settings
    PER_PAGE = 10
    USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ["pbkdf2_sha256"]

    STATS_PER_PAGE = 100
    STATS_SHOW_LAST_DAYS = 14

    PROSPECTS_PER_PAGE = 100
    CREDENTIALS_PER_PAGE = 100
    CAMPAIGNS_PER_PAGE = 100
    #Flask-User customization
    #USER_LOGIN_TEMPLATE = 'login/login.html'
    #USER_REGISTER_TEMPLATE = 'login/register.html'

    GMAIL_SMTP_HOST = 'smtp.gmail.com'
    GMAIL_SMTP_PORT = 587

    EMAIL_AUTO_ENRICHMENT = False
    #Enrich providers
    SNOVIO_CREDENTIALS = {
        'grant_type':'client_credentials',
        'client_id':'5c543104ff5fc8cb5e12e3432883f42e',
        'client_secret': '1a87f87d6ec80e754046a1d6aa2c05c3'
    }
    SNOVIO_API_URL = 'https://api.snov.io/v1'
    DEFAULT_ENRICH_PROVIDERS = {
        '0' : 1 #snovio provider
    }

    DEFAULT_SUBDOMAIN_PREFIX = 'https://email.'
    DEAFULT_TRACKING_DOMAIN = 'https://via.outreacher24.com'
    DEFAULT_CODE_LENGTH = 13

class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    CELERY_TASK_ALWAYS_EAGER = True
    TEST_USER_EMAIL = '1@email.com'

    CELERY_BROKER = 'amqp://guest:guest@localhost:5672//'
    CELERY_BACKEND_RESULT_EXPIRES = 300
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    MONGODB_SETTINGS = {
        'db': 'O24Mc-dev',
        'host': '127.0.0.1',
        'port': 27017,
        'tz_aware':True
    }

class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    CELERY_BROKER = 'amqp://guest:guest@localhost:5672//'
    CELERY_BACKEND_RESULT_EXPIRES = 300
    CELERY_TASK_ALWAYS_EAGER = False
    
    MONGODB_SETTINGS = {
        'db': 'O24Mc-prod',
        'host': '127.0.0.1',
        'port': 27017,
        'tz_aware':True
    }

class TestConfig(BaseConfig):
    FLASK_ENV = 'test'
    DEBUG = True
    TESTING = True
    CELERY_TASK_ALWAYS_EAGER = False #change to True if you need sync execution
    CELERY_BROKER = 'amqp://guest:guest@localhost:5672//'
    CELERY_BACKEND_RESULT_EXPIRES = 300
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    ENRICHER_HANDLER_PERIOD = 10
    SCHEDULER_HANDLER_PERIOD = 10

    TEST_USER_EMAIL = '1@email.com'
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = False
    MONGODB_SETTINGS = {
        'db': 'O24Mc-test',
        'host': '127.0.0.1',
        'port': 27017,
        'tz_aware':True
    }