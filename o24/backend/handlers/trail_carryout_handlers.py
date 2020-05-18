import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
from o24.globals import *
import datetime
from mongoengine.queryset.visitor import Q

def default_handler(task):
    if task.status != CARRYOUT:
        raise Exception("WRONG STATUS: default_handler should be called for CARRYOUT status. task.id={0} task.status={1}".format(task.id, task.status))
    
    task.update_status(status=READY)

def linkedin_search_action(task):
    #Special type of action
    # 1. Need to get prospects and create data from that
    # 2. Update campaign data with next_page 
    # 3. Update input_data
    # 4. If it's the last one then task.status=FINISHED  other way task.status=NEW

    result_data = task.get_result_data()
    if not result_data:
        raise Exception("linkedin_search_action ERROR: wrong or empty result_data={0}".format(result_data))
    
    campaign = task.get_campaign()
    if not campaign:
        task.update_status(status=FAILED)
        raise Exception("linkedin_search_action ERROR: There is no campaign for task.id={0}".format(task.id))
    
    owner_id = campaign.get_owner_id()
    list_id = campaign.get_list_id()
    update_existing = campaign.get_update_existing()

    data = result_data.get('data', '')
    if not data:
        print("linkedin_search_action WARNING: result_data.data is empty result_data={0}".format(result_data))
        task.update_status(status=FAILED)
        return 
    
    prospects_arr = data.get('arr', [])
    if prospects_arr:
        models.Prospects.upload_from_list(owner_id=owner_id, 
                                            prospects_arr=prospects_arr, 
                                            list_id=list_id, 
                                            update_existing=update_existing)
    search_url = data.get('link', '')
    if not search_url:
        print("linkedin_search_action WARNING: result_data.data.link is empty result_data={0}".format(result_data))
        task.update_status(status=FAILED)
        return

    is_finished = campaign.parsing_switch(next_url=search_url)
    if is_finished:
        task.update_status(status=FINISHED)
        linkedin_parsing_run_next_page(task)
        return


def linkedin_parse_profile_action(task):
    pass

def email_check_reply(task):
    pass