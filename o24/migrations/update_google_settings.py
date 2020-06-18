import os
import o24.config as config
from o24.backend import app
from o24.backend import db

import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
import o24.backend.scheduler.models as scheduler_models

from o24.globals import *
from datetime import datetime  
from datetime import timedelta  
from pytz import timezone
import pytz
import json
from pprint import pprint
import time 
from o24.production_tests.test_data_production import GOOGLE_APP_SETTINGS_PRODUCTION, GOOGLE_APP_SETTINGS
from o24.backend.google.models import GoogleAppSetting
import sys
from pprint import pprint

def _update_settings(instance, new_settings):
    instance.title = new_settings.get('title')
    instance.credentials = new_settings.get('credentials')
    instance.redirect_uri = new_settings.get('redirect_uri')

    instance.gmail_scopes = new_settings.get('gmail_scopes')
    instance.gmail_access_type = new_settings.get('gmail_access_type')
    instance.gmail_include_granted_scopes = new_settings.get('gmail_include_granted_scopes')

    instance.gmail_api_name = new_settings.get('gmail_api_name')
    instance.gmail_api_version = new_settings.get('gmail_api_version')

    instance.active = new_settings.get('active')

    instance._commit()



def update_google_apps_settings():
    IS_TEST = sys.argv[1]

    settings = None
    if IS_TEST == 'test':
        settings = GOOGLE_APP_SETTINGS[0]
    elif IS_TEST == 'prod':
        settings = GOOGLE_APP_SETTINGS_PRODUCTION[0]
    else:
        raise Exception("Unknown argument (should be test or prod) has:{0}".format(IS_TEST))
    
    if not settings:
        raise Exception("Can't find google apps settings for {0}".format(IS_TEST))

    active_settings = GoogleAppSetting.objects(active=True).first()
    if not active_settings:
        raise Exception("There is no active google settings for {0}".format(IS_TEST))
    
    _update_settings(instance=active_settings, new_settings=settings)

    active_settings.reload()
    pprint(active_settings.to_json())

if __name__ == '__main__':
    update_google_apps_settings() 

# python -m o24.migrations.update_google_settings <test>