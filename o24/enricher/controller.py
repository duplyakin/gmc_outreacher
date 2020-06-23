from o24.enricher.models import AuthData, EnrichTaskQueue, DataStorage, EnrichTaskQueueLock
import o24.config as config
import requests
import json
from datetime import datetime  
from datetime import timedelta  
from pytz import timezone
import pytz
import traceback
from o24.globals import *
import o24.backend.dashboard.models as models
from mongoengine.errors import NotUniqueError
from o24.enricher.providers.snovio import SnovioProvider
import o24.backend.scheduler.models as scheduler_models

PROVIDER_MAP = {
    1 : SnovioProvider
}

class EnrichController():
    def __init__(self):
        pass

    @classmethod
    def lock(cls):
        try:
            locked = EnrichTaskQueueLock.objects(lock_key=ENRICH_TASK_QUEUE_LOCK, ack=0).update_one(upsert=True, ack=1)
            if not locked:
                return None
            
            total = EnrichTaskQueueLock.objects(lock_key=ENRICH_TASK_QUEUE_LOCK).count()
            if total > 1:
                raise Exception("...NEVER HAPPENED EnrichController.lock create more than 1 instance")

            controller = cls()
            return controller
        except Exception as e:
            if type(e) == NotUniqueError:
                return None
                
            print(str(e))
            traceback.print_exc()
        
        return None

    def unlock(self):
        return EnrichTaskQueueLock.objects(lock_key=ENRICH_TASK_QUEUE_LOCK).update_one(upsert=False, ack=0)

    @classmethod
    def restart_prospect(cls, owner_id, prospect_id, input_data, providers={}):
        EnrichTaskQueue.restart_task(owner_id=owner_id, 
                                    prospect_id=prospect_id, 
                                    input_data=input_data,
                                    providers=providers)


    @classmethod
    def add_prospect(cls, owner_id, prospect_id, input_data, providers={}):
        EnrichTaskQueue.create_task(owner_id=owner_id, 
                                    prospect_id=prospect_id, 
                                    input_data=input_data,
                                    providers=providers)

    @classmethod
    def launch(cls, user, prospects, providers={}):
        for prospect in prospects:
            try:
                EnrichTaskQueue.create_task(owner_id=user.id, 
                                            prospect_id=prospect.id, 
                                            input_data=prospect.get_data(),
                                            providers=providers)
            except Exception as e:
                print(".... launch error for prospect.id={0}".format(prospect.id))                
                print(e)
                traceback.print_exc()
  
    def enrich(self):
        tasks = EnrichTaskQueue.get_enriched_tasks()

        for task in tasks:
            try:
                DataStorage.add_data(data=task.result_data)

                data = task.result_data.get('data')
                prospect_id = task.prospect_id

                success = models.Prospects.enrich_prospect(owner_id=task.owner,
                                                            prospect_id=prospect_id, 
                                                            prospect_data=data)
                
                description = 'models.Prospects.enrich_prospect success=True'
                if not success:
                    description = 'models.Prospects.enrich_prospect success=False'
                
                scheduler_models.ActionLog.log_enricher(task=task, 
                                                            step='enrich-controller-enrich', 
                                                            description=description)

                if success:
                    task.update_status(status=ENRICH_MOVED)
            except Exception as e:
                print(".... EnrichController enrich error for task.id={0}".format(task.id))                
                print(e)
                traceback.print_exc()
                scheduler_models.ActionLog.log_enricher(task=task, 
                                            step='enrich-controller-enrich', 
                                            description=str(e))
                

    def execute(self):
        tasks = EnrichTaskQueue.get_execute_tasks()

        for task in tasks:
            Provider = PROVIDER_MAP.get(task.current_enricher, 0)
            if not Provider:
                print("There is no Provider for current_enricher={0} task.id={1}".format(task.current_enricher, task.id))
                continue
            
            description = 'next tick success'
            try:
                #CHECK CREDITS
                credits_amount = self.check_credits(task=task)
                if credits_amount <= 0:
                    task.status = ENRICH_OUT_OF_CREDITS
                    task._commit()

                    scheduler_models.ActionLog.log_enricher(task=task, 
                                                            step='enrich-controller-execute', 
                                                            description='enrich_out_of_credits')
                    continue
                
                #TICK TASK
                provider = Provider()
                status = provider.tick(task=task)
                if status == ENRICH_TRIED_ALL and task.status != ENRICH_SUCCESS:
                    task.status = ENRICH_FAILED_TO_FOUND
                    task._commit()

                #Spent credits
                credits_spent = task.last_spent
                if credits_spent > 0:
                    self.withdraw_credits(task, amount=credits_spent)

            except Exception as e:
                print(".... EnrichController execute error for task.id={0}".format(task.id))                
                print(e)
                traceback.print_exc()
                description = str(e)
            
            scheduler_models.ActionLog.log_enricher(task=task, 
                                                    step='enrich-controller-execute', 
                                                    description=description)

    def withdraw_credits(self, task, amount):
        owner_id = task.owner

        user = models.User.objects(id=owner_id).first()
        if not user:
            message = "User not found owner_id:{0}".format(owner_id)
            raise Exception(message)

        return user.withdraw_credits(amount=amount)

    def check_credits(self, task):
        owner_id = task.owner

        user = models.User.objects(id=owner_id).first()
        if not user:
            message = "User not found owner_id:{0}".format(owner_id)
            raise Exception(message)

        return user.get_credits()

    def _check_storage(self):
        pass
