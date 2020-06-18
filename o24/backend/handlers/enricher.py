from o24.backend import app
from o24.backend import db
from celery import shared_task, group, chord
from o24.backend import celery
from o24.enricher.controller import EnrichController
from flask import current_app
from o24.globals import *

import o24.config as config
import traceback
import time
import o24.backend.dashboard.models as models
import o24.backend.models.shared as shared
from o24.enricher.models import EnrichTaskQueue

def restart_prospect_enrichment(prospect, providers=None):
    if not providers:
        providers = config.DEFAULT_ENRICH_PROVIDERS

    try:
        user = prospect.owner
        if not user:
            raise Exception("No user for prospect.id={0}".format(prospect.id))

        credits_amount = user.get_credits()
        if credits_amount <= 0:
            raise Exception("NOT ENOUGH CREDITS: Can't launch enrich for user.id={0} credits_amount={1}".format(user.id, credits_amount))

        EnrichController.restart_prospect(owner_id=user.id,
                                        prospect_id=prospect.id,
                                        input_data=prospect.get_data(),
                                        providers=providers)
    except Exception as e:
        app.logger.error(".....restart_prospect_enrichment Exception:{0}".format(str(e)))
        traceback.print_exc()
        return False
    
    return True


def add_prospect_for_enrichment(prospect, providers=None):
    if not providers:
        providers = config.DEFAULT_ENRICH_PROVIDERS

    try:
        user = prospect.owner
        if not user:
            raise Exception("No user for prospect.id={0}".format(prospect.id))

        credits_amount = user.get_credits()
        if credits_amount <= 0:
            raise Exception("NOT ENOUGH CREDITS: Can't launch enrich for user.id={0} credits_amount={1}".format(user.id, credits_amount))

        EnrichController.add_prospect(owner_id=user.id,
                                        prospect_id=prospect.id,
                                        input_data=prospect.get_data(),
                                        providers=providers)
    except Exception as e:
        app.logger.error(".....add_prospect_for_enrichment Exception:{0}".format(str(e)))
        traceback.print_exc()
        return False
    
    return True


def launch_prospects_enrich(owner_id, leads_list_id, providers=None):
    if not providers:
        providers = config.DEFAULT_ENRICH_PROVIDERS

    try:
        user = models.User.objects(id=owner_id).first()
        if not user:
            raise Exception("There is no such user.id={0}".format(owner_id))
        
        credits_amount = user.get_credits()
        if credits_amount <= 0:
            raise Exception("NOT ENOUGH CREDITS: Can't launch enrich for user.id={0} credits_amount={1}".format(user.id, credits_amount))

        prospects = models.Prospects.get_from_list(owner_id=user.id, list_id=leads_list_id)
        if not prospects:
            raise Exception("Zero prospects for user.id={0} and leads_list_id={1} NOT found".format(owner_id, leads_list_id))

        EnrichController.launch(user=user, prospects=prospects, providers=providers)
    except Exception as e:
        app.logger.error(".....launch_prospects_enrich Exception:{0}".format(str(e)))
        traceback.print_exc()
        return False
    
    return True

@celery.task
def check_enriched_action(task_id):
    result_data = {
        'if_true' : False,
        'code' : -1,
        'error' : 'Unknown Error'
    }
    status = FAILED

    task = None
    try:
        task = shared.TaskQueue.lock(task_id)
        if not task:
            print("CONCURRENCY in check_enriched_action attempt")
            return 
        
        prospect_id = task.prospect_id
        prospect = models.Prospects.objects(id=prospect_id).first()
        if not prospect:
            raise Exception("NEVER HAPPENED: check_enriched_action there is no prospect for task.id={0}".format(task.id))
        
        prospect_data = prospect.get_data()
        email = prospect_data.get('email', None)
        if email:
            #We have a email - don't need to enrich
            result_data = {
                'if_true' : True,
                'code' : 1,
            }
            status = READY
            return

        prospect.add_tag(title='no_email')
        result_data = {
            'if_true' : False,
            'code' : 2,
        }
        status = READY
    except Exception as e:
        print(e)
        traceback.print_exc()

        status = FAILED
        code = -1
        raw = ''
        if (type(e) == ErrorCodeException):
            code = e.error_code
            raw = e.message

        result_data = {
            'error' : str(e),
            'code' : code,
            'raw' : raw
        }
            
    finally:
        if task:
            unlocked = shared.TaskQueue.unlock(task_id=task_id, result_data=result_data, status=status)
            if not unlocked:
                raise Exception("Can't unlock check_enriched_action")
        
        return result_data

    return result_data


@celery.task
def enrich_action(task_id):
    result_data = {
        'if_true' : False,
        'code' : -1,
        'error' : 'Unknown Error'
    }
    status = FAILED

    task = None
    try:
        task = shared.TaskQueue.lock(task_id)
        if not task:
            print("CONCURRENCY in enrich_action attempt")
            return 
        
        prospect_id = task.prospect_id
        prospect = models.Prospects.objects(id=prospect_id).first()
        if not prospect:
            raise Exception("NEVER HAPPENED: enrich_action there is no prospect for task.id={0}".format(task.id))
        
        prospect_data = prospect.get_data()
        email = prospect_data.get('email', None)
        if email:
            #We have a email - don't need to enrich
            result_data = {
                'if_true' : True,
                'code' : 1,
            }
            status = READY
            return

        add_prospect_for_enrichment(prospect)

        result_data = {
            'if_true' : False,
            'code' : 2,
        }
        status = READY
    except Exception as e:
        print(e)
        traceback.print_exc()

        status = FAILED
        code = -1
        raw = ''
        if (type(e) == ErrorCodeException):
            code = e.error_code
            raw = e.message

        result_data = {
            'error' : str(e),
            'code' : code,
            'raw' : raw
        }
            
    finally:
        if task:
            unlocked = shared.TaskQueue.unlock(task_id=task_id, result_data=result_data, status=status)
            if not unlocked:
                raise Exception("Can't unlock enrich_action")
        
        return result_data

    return result_data


@celery.task(name='emit_enricher')
def emit_enricher():
    controller = None
    try:
        controller = EnrichController.lock()
        if not controller:
            print("emit_enricher concurrence attempt")
            return {"status": True}

        #execute current tasks in EnrichTaskQueue  
        controller.execute()

        #move enriched prospects to User's storage 
        controller.enrich()
    
    except Exception as e:
        app.logger.error(".....emit_enricher Exception:{0}".format(str(e)))
        traceback.print_exc()
        return {"status": False}

    finally:
        if controller:
            controller.unlock()

    return {"status": True}
