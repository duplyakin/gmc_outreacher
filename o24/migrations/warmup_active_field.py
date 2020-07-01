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

if __name__ == '__main__':
    pass

# Execute below requests on mongodb manually

#
# db.credentials.update({}, {$unset: {limit_per_day:1}}, false, true)  -remove limit_per_day field
# db.credentials.update({}, {"$set": {"warmup_active": true}}, false, true)          - add warmup_active field to true

# criteria – query which selects the record to update;
# objNew – updated object or $ operators (e.g., $inc) which manipulate the object
# upsert – if this should be an “upsert” operation; that is, if the record(s) do not exist, insert one. Upsert only inserts a single document.
# multi – indicates if all documents matching criteria should be updated rather than just one. Can be useful with the $ operators below.
