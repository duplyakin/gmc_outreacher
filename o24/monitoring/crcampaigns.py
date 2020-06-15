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

def show_campaigns():
    print("\n\n.......show_campaigns")
    campaigns = models.Campaign.objects().order_by('status')

    print("HELP status: (0-Created, 1-Inprogress, 2-paused, -1-Failed) | next_action | title ")
    print("status|next_action  |title ")
    print("______|_____________|_________________________")
    for c in campaigns:
        moscow_format = c.next_action.astimezone(pytz.timezone(MOSCOW)).strftime("%d-%b %H:%M")
        print("{status:6}|{next_action:13}|{title}|".format(status=c.status, 
                                                        next_action=moscow_format, 
                                                        title=c.title))

def show_credentials():
    print("\n\n.......show_credentials")
    pipeline = [
        {"$lookup" : {
            "from" : "accounts",
            "localField" : "_id",
            "foreignField" : "_id",
            "as" : "accounts"
        }},
        { "$unwind" : { "path" : "$accounts", "preserveNullAndEmptyArrays": True }},
        { "$project" : { 
            'status' : 1,
            'medium' : 1,
            'limit_per_day' : 1,
            'limit_interval' : 1,
            'current_daily_counter' : 1,
            'next_action' : 1,
            'accounts' : 1
        }}
    ]

    credentials = list(models.Credentials.objects().aggregate(*pipeline))
    print("HELP: status1: 0-New, 1-Active, -1-Failed")
    print("HELP: status2: 0-Available, 1-In_progress, 2-Blocked, 3-Solving_Captcha, 4-BROKEN_CREDENTIALS, -1-Failed")
    print("status1|medium         |limit_per_day|limit_interval|current_daily_counter|next_action  |status2|li_at |expired    |blocking_data|login |password|task_id|")
    print("_______|_______________|_____________|______________|_____________________|_____________|_______|______|___________|_____________|______|________|_______|")

    for cr in  credentials:
        status1 = cr.get('status', 'None')
        moscow_format = 'None'
        if cr.get('next_action', None):
            moscow_format = cr.get('next_action').astimezone(pytz.timezone(MOSCOW)).strftime("%d-%b %H:%M")

        medium = cr.get('medium', 'None')
        limit_per_day = cr.get('limit_per_day', 'None')
        limit_interval = cr.get('limit_interval', 'None')
        current_daily_counter = cr.get('current_daily_counter', 'None')

        accounts = cr.get('accounts', {})
        login = 'True' if accounts.get('login', '') else 'False'
        password = 'True' if accounts.get('password', '') else 'False'
        task_id = 'True' if accounts.get('task_id', '') else 'False'
        blocking_data = 'True' if accounts.get('blocking_data', '') else 'False'
        status2 = accounts.get('status', 'None')

        li_at_cookie = 'False'
        expired = 'None'
        
        cookies = accounts.get('cookies', [])

        li_at = None
        for n in cookies:
            if n.get('name', '') == 'li_at':
                li_at = n
                break
            
        if li_at:
            li_at_cookie = 'True'
            expired = li_at.get('expires', 'None')
            if expired != 'None':
                expired = time.strftime('%Y-%m-%d', time.localtime(int(expired)))
        
        print("{status1:7}|{medium:15}|{limit_per_day:13}|{limit_interval:14}|\
{current_daily_counter:21}|{next_action:13}|{status2:7}|{li_at_cookie:6}|\
{expired:11}|{blocking_data:13}|{login:6}|{password:8}|{task_id:8}".format(status1=status1,
                                                                                medium=medium,
                                                                                limit_per_day=limit_per_day,
                                                                                limit_interval=limit_interval,
                                                                                current_daily_counter=current_daily_counter,
                                                                                next_action=moscow_format,
                                                                                status2=status2,
                                                                                li_at_cookie=li_at_cookie,
                                                                                expired=expired,
                                                                                blocking_data=blocking_data,
                                                                                login=login,
                                                                                password=password,
                                                                                task_id=task_id))
if __name__ == '__main__':
    show_campaigns()
    show_credentials()