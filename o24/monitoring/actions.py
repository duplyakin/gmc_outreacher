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

def linkedin_parse_metrics(en):
    metrics = ''

    total_profiles_parsed = 0
    by_num_of_fields = ''

    all_result_data = en.get('all_result_data', [])
    uniqueue_profiles = {}
    num_fields = {}
    for r in all_result_data:
        result_data = r.get('data', None)
        input_data = r.get('input_data', {})
        if result_data:
            raw_data = result_data.get('data', '')
            linkedin_profile = ''
            prospect_data = input_data.get('prospect_data', '')
            if prospect_data:
                linkedin_profile = prospect_data.get('linkedin', '')
            if raw_data:
                json_data = json.loads(raw_data)
                if json_data:
                    total_profiles_parsed = total_profiles_parsed + 1
                    has_keys = len(list(json_data.keys()))
                    if num_fields.get(str(has_keys), None) is None:
                        num_fields[str(has_keys)] = 1
                    else:
                        num_fields[str(has_keys)] = num_fields[str(has_keys)] + 1
                    if linkedin_profile:
                        uniqueue_profiles[linkedin_profile] = True
    
    for k, v in num_fields.items():
        by_num_of_fields = by_num_of_fields + '-Col(' + str(k) + '):num(' + str(v) + ')'
    
    total_uniqueue_profiles = len(list(uniqueue_profiles.keys()))
    metrics = 'total_profiles_parsed:{total_profiles_parsed}**uniqueue_profiles:{total_uniqueue_profiles}**\
by_num_of_fields:{by_num_of_fields}'.format(total_profiles_parsed=total_profiles_parsed,
                                            by_num_of_fields=by_num_of_fields,
                                            total_uniqueue_profiles=total_uniqueue_profiles)
    return metrics

def count_search_total(json_data, uniqueue_profiles):
    count = 0
    arr = json_data.get('arr', [])
    if not arr:
        return 0
    
    for profile in arr:
        linkedin = profile.get('linkedin', None)
        if linkedin:
            count = count + 1
            uniqueue_profiles[linkedin] = True

    return count

def linkedin_search_metrics(en):
    metrics = ''
    campaign_data = en.get('campaign_data')
    total_pages = campaign_data.get('total_pages', 0)
    pages_done = campaign_data.get('pages_done', 0)

    total_profiles_parsed = 0
    total_uniqueue_profiles_parsed = 0

    all_result_data = en.get('all_result_data', [])
    uniqueue_profiles = {}
    for r in all_result_data:
        result_data = r.get('data', None)
        if result_data:
            raw_data = result_data.get('data', '')
            if raw_data:
                json_data = json.loads(raw_data)
                total = count_search_total(json_data, uniqueue_profiles)
                total_profiles_parsed = total_profiles_parsed + total
    
    total_uniqueue_profiles_parsed = len(list(uniqueue_profiles.keys()))

    metrics = 'total_pages:{total_pages}*pages_done:{pages_done}*\
total_profiles_parsed:{total_profiles_parsed}*\
total_uniqueue_profiles_parsed:{total_uniqueue_profiles_parsed}'.format(total_pages=total_pages,
                                                                        pages_done=pages_done,
                                                                        total_profiles_parsed=total_profiles_parsed,
                                                                        total_uniqueue_profiles_parsed=total_uniqueue_profiles_parsed)
    return metrics

def show_actions():
    print("\n\n.......show_actions")
    pipeline = [
        {"$lookup" : {
            "from" : "campaign",
            "localField" : "campaign_id",
            "foreignField" : "_id",
            "as" : "campaign"
        }},
        { "$unwind" : { "path" : "$campaign", "preserveNullAndEmptyArrays": True }},
        {"$group" :{
                "_id" : "$campaign_id",
                "action_key" : {"$first" : "$action_key"},
                "campaign_title" : {"$first" : "$campaign.title" },
                "campaign_data" : {"$first" : "$campaign.data"},
                "all_input_data" : { "$push" : {
                        "data" : "$input_data"
                    }
                },
                "all_result_data" : { "$push" : {
                        "data" : "$result_data",
                        "input_data" : "$input_data"
                    }
                }
            }
        }
    ]

    linkedin_search_actions = list(scheduler_models.ResultDataLog.objects(action_key=LINKEDIN_SEARCH_ACTION).aggregate(*pipeline))

    print("campaign_title                                              |action                   | metrics")
    print("____________________________________________________________|_________________________|________________________________________________________________________________")

    for en in linkedin_search_actions:
        campaign_title = en.get('campaign_title')
        action = en.get('action_key')
        metrics = linkedin_search_metrics(en)
        print("{campaign_title:60}|{action:25}|{metrics}".format(campaign_title=campaign_title,
                                                            action=action,
                                                            metrics=metrics))

    linkedin_parse_profile = list(scheduler_models.ResultDataLog.objects(action_key=LINKEDIN_PARSE_PROFILE_ACTION).aggregate(*pipeline))

    for en in linkedin_parse_profile:
        campaign_title = en.get('campaign_title')
        action = en.get('action_key')
        metrics = linkedin_parse_metrics(en)
        print("{campaign_title:60}|{action:25}|{metrics}".format(campaign_title=campaign_title,
                                                            action=action,
                                                            metrics=metrics))



if __name__ == '__main__':
    show_actions() 