import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
from o24.globals import *
import datetime
from mongoengine.queryset.visitor import Q

def banned(task):
    if not task:
        print("banned: task is None")
        return
    
    cr_id = task.credentials_id
    credentials = models.Credentials.objects().get(id=cr_id)
    if not credentials:
        print("banned: Can't find credentials for task.id".format(task.id))
        return

    campaign_id = task.campaign_id
    campaign = models.Campaign.objects().get(id=campaign_id)
    if not campaign:
        print("banned: Can't find campaign for task.id".format(task.id))
        return

    #If credentials refreshed then update it
    if credentials.is_refreshed():
        credentials.resume()
        try:
            campaign._safe_start()
        except Exception as e:
            print("banned: Can't resume campaign from credentials_error:{0}".format(str(e)))
        
        task._resume()
        return True
    
    #We need user action
    #Set Credentials status = -1
    #Pause campaign
    credentials.error(error="Seems Linkedin ban us - check your account. We've set 1 day pause", delay=1)
    campaign._safe_pause()
    return True


def credentials_error(task):
    if not task:
        print("credentials_error: task is None")
        return
    
    cr_id = task.credentials_id
    credentials = models.Credentials.objects().get(id=cr_id)
    if not credentials:
        print("credentials_error: Can't find credentials for task.id".format(task.id))
        return

    campaign_id = task.campaign_id
    campaign = models.Campaign.objects().get(id=campaign_id)
    if not campaign:
        print("credentials_error: Can't find campaign for task.id".format(task.id))
        return

    #If credentials refreshed then update it
    if credentials.is_refreshed():
        credentials.resume()
        try:
            campaign._safe_start()
        except Exception as e:
            print("credentials_error: Can't resume campaign from credentials_error:{0}".format(str(e)))
        
        task._resume()
        return True
    
    #We need user action
    #Set Credentials status = -1
    #Pause campaign
    credentials.error(error="Can't login - check your credentials or Ban")
    campaign._safe_pause()
    return True

def system_error(task):
    if not task:
        print("system_error: task is None")
        return
  
    result_data = task.result_data
    print("system_error: can't fix for task.id={0} result_data={1}".format(task.id, result_data))

