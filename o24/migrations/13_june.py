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

def add_fork_from():
    parsing_campaign = models.Campaign.objects(campaign_type__in=[LINKEDIN_PARSING_CAMPAIGN_TYPE]).first()
    enrichment_campaign = models.Campaign.objects(campaign_type__in=[LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE]).first()

    if not enrichment_campaign or not parsing_campaign:
        raise Exception("Can't find parsing_campaign or enrichment_campaign")
    
    enrichment_campaign.fork_from = parsing_campaign.id
    enrichment_campaign.save()



if __name__ == '__main__':
    add_fork_from() 