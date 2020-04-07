import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel, TaskQueue
from o24.backend.utils.funnel import construct_funnel
import o24.backend.scheduler.scheduler as SCHEDULER
from mongoengine.queryset.visitor import Q
from o24.globals import *
from o24.exceptions.exception_with_code import ErrorCodeException
from o24.exceptions.error_codes import *

from celery import shared_task, group, chord


CAMPAIGNS_TO_START = [
    {
        'title' : 'campaign-1'
    },
    {
        'title' : 'campaign-2'
    },

]

PROSPECTS_TO_APPEND = [
    {
        'owner' : '1@email.com',
        'amount' : 5,
        'assign_to' : 'campaign-1'
    },
    {
        'owner' : '3@email.com',
        'amount' : 10,
        'assign_to' : 'campaign-2'
    },
]


class TestScheduler(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_start_campaign(self):        
        campaigns_to_start = CAMPAIGNS_TO_START

        campaigns = []
        for c in campaigns_to_start:
            title = c.get('title')

            campaign = Campaign.get_campaign(title=title)
            self.assertTrue(campaign is not None, "There is no such campaign title:{0}".format(title))
            campaigns.append(campaign)
        
        scheduler = SCHEDULER.Scheduler()

        # campaign changed status to IN_PROGRESS
        # prospects changed status to IN_PROGRESS
        # all prospects changed status
        # All ids appeared in TaskQueue with status NEW
        for campaign in campaigns:
            prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
            ids_before = [prospect.id for prospect in prospects]
            count_before = len(prospects)
            self.assertTrue(count_before > 0, "There is no prospects for campaign_title:{0} count_before={1}".format(campaign.title, count_before))

            scheduler.start_campaign(campaign)

            prospects = Prospects.get_prospects(status=IN_PROGRESS, campaign_id=campaign.id)
            count_after = len(prospects)
            ids_after = [prospect.id for prospect in prospects]

            self.assertTrue(set(ids_before) == set(ids_after), "not all prospects updates campaign_title:{0} count_before={1} count_after={2}".format(campaign.title, count_before, count_after))

            campaign.reload()
            self.assertTrue(campaign.status == IN_PROGRESS, "campaing status change error campaign_title:{0}".format(campaign.title))

            #ids_in_queue =[p.get('prospect_id') for p in TaskQueue.objects(Q(status=NEW) & 
            #                                Q(prospect_id__in=ids_after)).only('prospect_id').all().as_pymongo()]
            
            ids_in_queue = TaskQueue.objects(Q(status=NEW) & Q(prospect_id__in=ids_after)).distinct('prospect_id')
            count_queue = len(ids_in_queue)
            self.assertTrue(set(ids_in_queue) == set(ids_before), "not all prospects appeared in TaskQueue campaign_title:{0} count_before={1} count_queue={2}".format(campaign.title, count_before, count_queue))



    def test_2_pause_campaign(self):
        campaigns_to_pause = CAMPAIGNS_TO_START
        
        campaigns = []
        for c in campaigns_to_pause:
            title = c.get('title')

            campaign = Campaign.get_campaign(title=title)
            self.assertTrue(campaign is not None, "There is no such campaign title:{0}".format(title))
            campaigns.append(campaign)
        
        scheduler = SCHEDULER.Scheduler()

        # campaign changed status to PAUSED
        # All prospects in TaskQueue change status to PAUSED
        for campaign in campaigns:
            prospects = Prospects.get_prospects(status=IN_PROGRESS, campaign_id=campaign.id)
            count_before = len(prospects)
            ids_before = [prospect.id for prospect in prospects]
            self.assertTrue(count_before > 0, "There is no prospects for campaign_title:{0} count_before={1}".format(campaign.title, count_before))

            scheduler.pause_campaign(campaign)

            campaign.reload()
            self.assertTrue(campaign.status == PAUSED, "campaing status change error campaign_title:{0}".format(campaign.title))

            #ids_in_queue =[p.get('prospect_id') for p in TaskQueue.objects(Q(status=NEW) & 
            #                                Q(prospect_id__in=ids_before)).only('prospect_id').all().as_pymongo()]
            ids_in_queue = TaskQueue.objects(Q(status=NEW) & Q(prospect_id__in=ids_before)).distinct('prospect_id')
            count_queue = len(ids_in_queue)
            self.assertTrue(set(ids_in_queue) == set(ids_before), "status changed in TaskQueue campaign_title:{0} count_before={1} count_queue={2}".format(campaign.title, count_before, count_queue))


    def test_3_start_paused_campaign(self): 
        campaigns_to_start = CAMPAIGNS_TO_START

        campaigns = []
        for c in campaigns_to_start:
            title = c.get('title')

            campaign = Campaign.get_campaign(title=title)
            self.assertTrue(campaign is not None, "There is no such campaign title:{0}".format(title))
            campaigns.append(campaign)
        
        scheduler = SCHEDULER.Scheduler()

        for campaign in campaigns:
            with self.assertRaises(Exception) as context:
                scheduler.start_campaign(campaign)

            the_exception = context.exception
            self.assertEqual(the_exception.error_code, START_CAMPAIGN_ERROR)

    def test_4_resume_campaign(self): 
        campaigns_to_resume = CAMPAIGNS_TO_START
        
        campaigns = []
        for c in campaigns_to_resume:
            title = c.get('title')

            campaign = Campaign.get_campaign(title=title)
            self.assertTrue(campaign is not None, "There is no such campaign title:{0}".format(title))
            campaigns.append(campaign)
        
        scheduler = SCHEDULER.Scheduler()

        # campaign changed status to IN_PROGRESS
        # All prospects in TaskQueue change status to IN_PROGRESS
        for campaign in campaigns:
            self.assertTrue(campaign.status == PAUSED, "campaing is not PAUSED campaign_title:{0} status:{1}".format(campaign.title, campaign.status))
            #ids_before = [p.get('prospect_id') for p in TaskQueue.objects(Q(status=NEW) &  Q(campaign_id=campaign.id)).only('prospect_id').all().as_pymongo()]
            
            ids_before = TaskQueue.objects(Q(status=NEW) &  Q(campaign_id=campaign.id)).distinct('prospect_id')

            count_before = len(ids_before)
            self.assertTrue(count_before > 0, "There is no prospects in TaskQueue for campaign_title:{0} count_before={1}".format(campaign.title, count_before))

            scheduler.resume_campaign(campaign)

            campaign.reload()
            self.assertTrue(campaign.status == IN_PROGRESS, "campaing status change error campaign_title:{0}".format(campaign.title))

            #ids_in_queue =[p.get('prospect_id') for p in TaskQueue.objects(Q(status=NEW) & Q(prospect_id__in=ids_before)).only('prospect_id').all().as_pymongo()]

            ids_in_queue = TaskQueue.objects(Q(status=NEW) & Q(prospect_id__in=ids_before)).distinct('prospect_id')
            
            count_queue = len(ids_in_queue)
            self.assertTrue(set(ids_in_queue) == set(ids_before), "status changed for prospects in TaskQueue campaign_title:{0} count_before={1} count_queue={2}".format(campaign.title, count_before, count_queue))

    def test_5_resume_with_new_prospects(self): 
        campaigns_to_resume = CAMPAIGNS_TO_START
        
        scheduler = SCHEDULER.Scheduler()
 
        campaigns = []
        for c in campaigns_to_resume:
            title = c.get('title')

            campaign = Campaign.get_campaign(title=title)
            self.assertTrue(campaign is not None, "There is no such campaign title:{0}".format(title))

            self.assertTrue(campaign.status == IN_PROGRESS, "campaign not IN_PROGRESS status:{0}".format(campaign.status))
            
            scheduler.pause_campaign(campaign)
            
            campaign.reload()
            self.assertTrue(campaign.status == PAUSED, "campaign pause error title:{0} status:{1}".format(campaign.title, campaign.status))

            campaigns.append(campaign)
        
        #Append random prospects
        prospects = PROSPECTS_TO_APPEND
        for prospect in prospects:
            owner = User.get_user(prospect.get('owner'))
            self.assertTrue(owner is not None, "No such user")

            campaign = Campaign.get_campaign(title=prospect.get('assign_to'))
            self.assertTrue(campaign is not None, "No such campaign")

            amount = prospect.get('amount')
            for p in range(amount):
                new_prospect = Prospects.create_prospect(owner_id=owner.id,
                                                        campaign_id=campaign.id)
                self.assertTrue(new_prospect is not None, "Can't create prospect")

        # campaign changed status to IN_PROGRESS
        # New prospects are added to TaskQueue
        for campaign in campaigns:
            self.assertTrue(campaign.status == PAUSED, "campaing is not PAUSED campaign_title:{0} status:{1}".format(campaign.title, campaign.status))

            new_prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
            new_prospect_ids = [prospect.id for prospect in new_prospects]
            new_count_before = len(new_prospect_ids)
            self.assertTrue(new_count_before > 0, "new prospects not created for campaign_title:{0} status:{1}".format(campaign.title, campaign.status))

            old_prospects = Prospects.get_prospects(status=IN_PROGRESS, campaign_id=campaign.id)
            old_prospects_ids = [prospect.id for prospect in old_prospects]
            old_count_before = len(old_prospects_ids)
            self.assertTrue(old_count_before > 0, "Not previous IN_PROGRESS prospects found for campaign_title:{0}".format(campaign.title))
            self.assertTrue(set(old_prospects_ids) != set(new_prospect_ids), "new and old prospects can't be similar campaign_title:{0}".format(campaign.title))

            scheduler.resume_campaign(campaign)

            campaign.reload()
            self.assertTrue(campaign.status == IN_PROGRESS, "campaign resume error campaign_title:{0}".format(campaign.title))

            all_ids = new_prospect_ids + old_prospects_ids
            all_count = len(all_ids)
           
            #ids_in_queue =[p.get('prospect_id') for p in TaskQueue.objects(Q(status=NEW) &  Q(prospect_id__in=all_ids)).only('prospect_id').all().as_pymongo()]

            ids_in_queue = TaskQueue.objects(Q(status=NEW) &  Q(prospect_id__in=all_ids)).distinct('prospect_id')

            count_queue = len(ids_in_queue)
            self.assertTrue(set(ids_in_queue) == set(all_ids), "not all prospects added to TaskQueue campaign_title:{0} all_count={1} count_queue={2}".format(campaign.title, all_count, count_queue))

    def test_6_add_new_prospects_to_active_campaign(self):
        campaigns_active = CAMPAIGNS_TO_START
         
        campaigns = []
        for c in campaigns_active:
            title = c.get('title')

            campaign = Campaign.get_campaign(title=title)
            self.assertTrue(campaign is not None, "There is no such campaign title:{0}".format(title))

            self.assertTrue(campaign.status == IN_PROGRESS, "campaign not IN_PROGRESS status:{0}".format(campaign.status))
            
            campaigns.append(campaign)

        #Append random prospects
        prospects = PROSPECTS_TO_APPEND
        for prospect in prospects:
            owner = User.get_user(prospect.get('owner'))
            self.assertTrue(owner is not None, "No such user")

            campaign = Campaign.get_campaign(title=prospect.get('assign_to'))
            self.assertTrue(campaign is not None, "No such campaign")

            amount = prospect.get('amount')
            for p in range(amount):
                new_prospect = Prospects.create_prospect(owner_id=owner.id,
                                                        campaign_id=campaign.id)
                self.assertTrue(new_prospect is not None, "Can't create prospect")

        scheduler = SCHEDULER.Scheduler()

        # APPEND NEW Prospects to working queue
        # campaign changed status to IN_PROGRESS
        # New prospects are added to TaskQueue
        for campaign in campaigns:
            self.assertTrue(campaign.status == IN_PROGRESS, "campaing is not IN_PROGRESS campaign_title:{0} status:{1}".format(campaign.title, campaign.status))

            new_prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
            new_prospect_ids = [prospect.id for prospect in new_prospects]
            new_count_before = len(new_prospect_ids)
            self.assertTrue(new_count_before > 0, "new prospects not created for campaign_title:{0} status:{1}".format(campaign.title, campaign.status))

            old_prospects = Prospects.get_prospects(status=IN_PROGRESS, campaign_id=campaign.id)
            old_prospects_ids = [prospect.id for prospect in old_prospects]
            old_count_before = len(old_prospects_ids)
            self.assertTrue(old_count_before > 0, "Not previous IN_PROGRESS prospects found for campaign_title:{0}".format(campaign.title))
            self.assertTrue(set(old_prospects_ids) != set(new_prospect_ids), "new and old prospects can't be similar campaign_title:{0}".format(campaign.title))

            scheduler.add_prospects(campaign, new_prospects)

            campaign.reload()
            self.assertTrue(campaign.status == IN_PROGRESS, "campaign resume error campaign_title:{0}".format(campaign.title))

            #status_changed_ids = [p.get('_id') for p in Prospects.objects(Q(status=IN_PROGRESS) & Q(id__in=new_prospect_ids)).only('id').all().as_pymongo()]

            status_changed_ids = Prospects.objects(Q(status=IN_PROGRESS) & Q(id__in=new_prospect_ids)).distinct('id')

            self.assertTrue(set(new_prospect_ids) == set(status_changed_ids), "new prospects don't change status to IN_PROGRESS campaign_title:{0}".format(campaign.title))
           
            #ids_in_queue =[p.get('prospect_id') for p in TaskQueue.objects(Q(status=NEW) & Q(prospect_id__in=new_prospect_ids)).only('prospect_id').all().as_pymongo()]
            ids_in_queue = TaskQueue.objects(Q(status=NEW) & Q(prospect_id__in=new_prospect_ids)).distinct('prospect_id')

            count_queue = len(ids_in_queue)
            self.assertTrue(set(ids_in_queue) == set(new_prospect_ids), "new prospects don't added to TaskQueue campaign_title:{0} count_queue={1}".format(campaign.title, count_queue))



def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()