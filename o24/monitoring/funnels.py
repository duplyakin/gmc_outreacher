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

MOSCOW = 'Europe/Moscow'

def show_funnels():
    print("\n\n.......show_funnels")
    pipeline = [
        {"$group" : {
            '_id': { "campaign_id" : "$campaign_id", "action_key" : "$action_key"},
            "num_of_prospects" : {"$sum" : 1},
            "campaign_title": { "$first": "$stat_campaign_title"}
        }},
        {"$group" :{
                "_id" : "$_id.campaign_id",
                "campaign_title" : {"$first" : "$campaign_title" },
                "actions" : { "$push" : {
                        "action_key" : "$_id.action_key",
                        "num_of_prospects" : "$num_of_prospects"
                    }
                }
            }
        }
    ]

    tasks_funnels = list(shared.TaskQueue.objects().aggregate(*pipeline))
    print("HELP: campaign.status: (0-created, 1-in progress, 2-paused)")
    print("c_status|campaign_title                          |funnel_title                          | actions")
    print("________|________________________________________|______________________________________|________________________________________________________________________________")

    for en in tasks_funnels:
        campaign_id = en.get('_id')
        campaign_title = en.get('campaign_title', 'None')
        campaign = models.Campaign.objects(id=campaign_id).first()
        if not campaign_id:
            print("..no such campaign:{0}".format(campaign_title))
            continue
        campaign_status = campaign.status
        funnel_title = campaign.funnel.title

        actions = ''
        steps = en.get('actions',[])
        for a in steps:
            actions = actions + '|' + a.get('action_key', 'None') + ':' + str(a.get('num_of_prospects', 'None'))

        print("{campaign_status:8}|{campaign_title:40}|{funnel_title:38}|{actions}|".format(campaign_status=campaign_status,
                                                                                campaign_title=campaign_title,
                                                                                funnel_title=funnel_title,
                                                                                actions=actions))
if __name__ == '__main__':
    show_funnels() 