import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
import o24.backend.scheduler.scheduler as scheduler

from o24.globals import *
import datetime
from mongoengine.queryset.visitor import Q
import o24.config as config
import o24.backend.handlers.enricher as enricher

def default_handler(task):
    if task.status != CARRYOUT:
        raise Exception("WRONG STATUS: default_handler should be called for CARRYOUT status. task.id={0} task.status={1}".format(task.id, task.status))
    
    result_data = task.get_result_data()
    if not result_data:
        raise Exception("default_handler ERROR: wrong result_data:{0}".format(result_data))

    code = result_data.get('code', 0)
    if code == SUCCESS_CODE:
        task.update_status(status=FINISHED)
        #TODO - save reply message
        return

    task.update_status(status=READY)
    return 


def start_linkedin_enrichment_campaign(task):
    #We have finixhed linkedin_search_action action and need to start enrichment campaign 
    if task.status != FINISHED:
        error = "WRONG STATUS: start_linkedin_enrichment_campaign should be called for FINISHED status. task.id={0} task.status={1}".format(task.id, task.status)
        raise Exception(error)

    campaign = task.get_campaign()
    if not campaign:
        error = "NO CAMPaIGN: start_linkedin_enrichment_campaign can't find campaign. task.id={0} task.status={1}".format(task.id, task.status)
        raise Exception(error)

    owner_id = campaign.get_owner_id()
    if not owner_id:
        raise Exception("start_linkedin_enrichment_campaign: There is no owner_id")

    list_id = campaign.get_list_id()
    if not list_id:
        raise Exception("start_linkedin_enrichment_campaign: list_id can't be null")
    
    prospects = models.Prospects.get_from_list(owner_id=owner_id, list_id=list_id)
    if not prospects or len(prospects) <= 0:
        raise Exception("start_linkedin_enrichment_campaign: no prospects for list_id={0}".format(list_id))


    new_campaign = campaign.fork_linkedin_enrichment_campaign()
    if not new_campaign:
        raise Exception("start_linkedin_enrichment_campaign: something went wrong after campaign.fork_linkedin_enrichment_campaign")
    
    ids = [p.id for p in prospects]
    scheduler.Scheduler.safe_assign_prospects(owner_id=owner_id, 
                                            campaign=new_campaign, 
                                            prospects_ids=ids)

    scheduler.Scheduler.safe_start_campaign(owner=owner_id, 
                                            campaign=new_campaign)
    
    return

def linkedin_search_action(task):
    #Special type of action
    # 1. Need to get prospects and create data from that
    # 2. Update campaign data with next_page 
    # 3. Update input_data
    # 4. If it's the last one then task.status=FINISHED  other way task.status=NEW
    if task.status != CARRYOUT:
        raise Exception("WRONG STATUS: linkedin_search_action should be called for CARRYOUT status. task.id={0} task.status={1}".format(task.id, task.status))

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
        campaign._safe_pause()
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
        campaign._safe_pause()
        return

    is_finished = campaign.parsing_switch(next_url=search_url)
    code = int(result_data.get('code', 0))

    if is_finished or code == CARRYOUT_SEARCH_ACTION_PAGES_FINISHED:
        task.update_status(status=FINISHED)
        campaign._safe_pause()
        start_linkedin_enrichment_campaign(task)
        return
    
    task.update_status(status=NEW)
    return

def linkedin_parse_profile_action(task):
    if task.status != CARRYOUT:
        raise Exception("WRONG STATUS: linkedin_parse_profile_action should be called for CARRYOUT status. task.id={0} task.status={1}".format(task.id, task.status))
    
    prospect = task.get_prospect()
    if not prospect:
        raise Exception("linkedin_parse_profile_action: no such prospect for task.id={0}".format(task.id))

    result_data = task.get_result_data()
    if not result_data:
        raise Exception("linkedin_parse_profile_action ERROR: wrong or empty result_data={0}".format(result_data))

    code = int(result_data.get('code', 0))
    if code < 0:
        task.update_status(status=FAILED)
        return
    
    data = result_data.get('data', '')
    if not data:
        raise Exception("linkedin_parse_profile_action: no data for task.id={0}".format(task.id))

    prospect.update_data_partly(new_data=data)

    task.update_status(status=READY)

    #TODO: need to be controlled by campaign
    if config.EMAIL_AUTO_ENRICHMENT:
        enricher.add_prospect_for_enrichment(prospect=prospect)

    return

    
def email_check_reply(task):
    if task.status != CARRYOUT:
        raise Exception("WRONG STATUS: email_check_reply should be called for CARRYOUT status. task.id={0} task.status={1}".format(task.id, task.status))
