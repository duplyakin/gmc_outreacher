import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects
from o24.backend.scheduler.models import Priority
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel, TaskQueue
from o24.backend.utils.funnel import construct_funnel
import o24.backend.scheduler.scheduler as SCHEDULER
from mongoengine.queryset.visitor import Q
from o24.globals import *
from o24.exceptions.exception_with_code import ErrorCodeException
from o24.exceptions.error_codes import *
import time
from celery import shared_task, group, chord
from datetime import datetime
import pytz

class TestSchedulerLoop(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_scheduler_loop(self):
        scheduler = SCHEDULER.Scheduler()
        
        #show stats before starting loops
        campaigns_total = Campaign.objects().count()
        campaigns_in_progress = Campaign.objects(status=IN_PROGRESS).count()
        prospects_total = Prospects.objects().count()
        tasks_total = TaskQueue.objects().count()
        print("******Before starting schedule loop*****")
        print("*** campaigns_total={0} campaigns_in_progress={1}".format(campaigns_total, campaigns_in_progress))
        print("*** prospects_total={0} tasks_total={1}".format(prospects_total, tasks_total))

        while True:        
            tasks_before_plan = TaskQueue.get_ready()
            tasks_ids_before = [t.id for t in tasks_before_plan]
            count_tasks_ids_before = len(tasks_ids_before)
            
            scheduler.plan()

            #check plan phase
            if tasks_before_plan:
                print("*** There are COUNT={0} tasks on planning phase".format(len(tasks_before_plan)))
                #check switch of the funnel phase
                tasks_after_plan = TaskQueue.objects(Q(id__in=tasks_ids_before) & Q(status=NEW)).all()
                tasks_ids_after = [t.id for t in tasks_after_plan]
                count_tasks_ids_after = len(tasks_ids_after)
                self.assertTrue(set(tasks_ids_before) == set(tasks_ids_after), "Plan error not all tasks switched")

                #Check that all nodes are switched correctly
                chain_checked = False
                for task_after in tasks_after_plan:
                    found = False
                    for task_before in tasks_before_plan:
                        if task_before.id == task_after.id:
                            found = True
                            chain_checked = True
                            node_before = task_before.current_node
                            result_before = task_before.result_data

                            node_after = task_after.current_node

                            if node_before.check_true(result_before):
                                self.assertTrue(node_before.if_true == task_after.id, 
                                        "if_true: Node switch error for task_before.id:{0}".format(task_before.id))
                            else:
                                self.assertTrue(node_before.if_false == task_after.id, 
                                        "if_false: Node switch error for task_before.id:{0}".format(task_before.id))

                            break
                    self.assertTrue(found, "Can't find task_before for task_after")

                #It means that funnel is broken - check that there is no duplicate keys
                if (len(tasks_after_plan)):
                    self.assertTrue(chain_checked, "Chain checked loop didn't start, It means that funnel is broken - check that there is no duplicate keys tasks_ids_before:{0} tasks_ids_after:{1}".format(tasks_ids_before, tasks_ids_after))

            else:
                print("*** There are no tasks on planning phase")

            #EXECUTING PHASE
            current_priority = Priority.get_priority()
            do_next= current_priority.do_next
            followup_level = current_priority.followup_level
            now = pytz.utc.localize(datetime.utcnow())
            
            print("**** Current time:{0}".format(now))
            tasks_before_execute = TaskQueue.get_execute_tasks(do_next=do_next, followup_level=followup_level, now=now)
            tasks_before_execute_ids = [t.id for t in tasks_before_execute]
            count_tasks_before_execute = len(tasks_before_execute_ids)

            jobs = scheduler.execute(now=now)

            STATUSES_AFTER = [IN_PROGRESS, READY, FINISHED]
            if tasks_before_execute:
                print("*** There are COUNT={0} tasks on executing phase".format(len(tasks_before_execute)))
                tasks_after_execute = TaskQueue.objects(Q(id__in=tasks_before_execute_ids) & Q(status__in=STATUSES_AFTER)).all()
                tasks_after_execute_ids = [t.id for t in tasks_after_execute]
                count_tasks_after_execute = len(tasks_after_execute_ids)
                self.assertTrue(set(tasks_before_execute_ids) == set(tasks_after_execute_ids), "Execute error not all tasks IN_PROGRESS count_before={0} count_after={1} ids={2}".format(count_tasks_before_execute, count_tasks_after_execute, tasks_before_execute_ids))
                print("***Executed tasks:{0}".format(tasks_after_execute_ids))

            else:
                print("*** There are no tasks on executing phase")

            group_jobs = group(jobs)
            
            group_jobs.apply_async()
            #time.sleep(0.5)
             
            tasks_finished = TaskQueue.objects(status=FINISHED).count()
            print("**** tasks_finished:{0}  tasks_total:{1}".format(tasks_finished, tasks_total))
            if tasks_finished == tasks_total:
                print("** SUCCESS: all tasks in queue finished")
                break


def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()