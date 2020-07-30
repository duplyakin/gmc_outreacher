from datetime import datetime
import traceback
import o24.backend.dashboard.models as models
import o24.backend.models.shared as shared
from bson.json_util import dumps as bson_dumps

from o24.globals import *
import o24.config as config

class CampaignProvider():
    def __init__(self, campaign_id, campaign=None):
        if campaign:
            self.campaign = campaign
        elif campaign_id:
            campaign = models.Campaign.obejcts(id=campaign_id).get()
            if not campaign:
                raise Exception("No such campaign id={0}".format(campaign_id))
            self.campaign = campaign
        else:
            raise Exception("Pass campaign or campaign_id")
    
    @classmethod
    def list_outreach_campaigns(cls, owner_id, page, per_page=config.CAMPAIGNS_PER_PAGE):
        if page and page <= 1:
            page = 1

        cls._cache_outreach_campaigns(owner_id=owner_id, 
                                    page=page, 
                                    per_page=per_page)

        db_query = models.Campaign.objects(owner=owner_id, 
                                            campaign_type__in=OUTREACH_CAMPAIGNS)

        total = db_query.count()


        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "credentials",
                "localField" : "credentials",
                "foreignField" : "_id",
                "as" : "credentials"
            }},
            {"$lookup" : {
                "from" : "funnel",
                "localField" : "funnel",
                "foreignField" : "_id",
                "as" : "funnel"
            }},
            { "$unwind" : { "path" : "$funnel", "preserveNullAndEmptyArrays": True }},
            
            #Fields that we need to show
            { "$project" : { 
                'title' : 1,
                'status' : 1,
                'funnel' : 1,
                'message' : 1,
                'cache' : 1,

                'data' : 1,
                'credentials' : 1,
                'campaign_type' : 1
            }}
        ]

        campaigns = []
        if page is not None:
            campaigns = list(db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').aggregate(*pipeline))
        else:
            campaigns = list(db_query.order_by('-created').aggregate(*pipeline))

        results = bson_dumps(campaigns)

        return (total, results)


    @classmethod
    def list_enrichment_campaigns(cls, owner_id, page, per_page=config.CAMPAIGNS_PER_PAGE):
        if page and page <= 1:
            page = 1

        cls._cache_enrichment_campaigns(owner_id=owner_id, 
                                    page=page, 
                                    per_page=per_page)

        db_query = models.Campaign.objects(owner=owner_id, 
                                            campaign_type__in=ENRICHMENT_CAMPAIGNS)

        total = db_query.count()


        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "funnel",
                "localField" : "funnel",
                "foreignField" : "_id",
                "as" : "funnel"
            }},
            { "$unwind" : { "path" : "$funnel", "preserveNullAndEmptyArrays": True }},
            
            #Fields that we need to show
            { "$project" : { 
                'title' : 1,
                'status' : 1,
                'funnel' : 1,
                'message' : 1,
                'cache' : 1,

                'data' : 1,
                'campaign_type' : 1
            }}
        ]

        campaigns = []
        if page is not None:
            campaigns = list(db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').aggregate(*pipeline))
        else:
            campaigns = list(db_query.order_by('-created').aggregate(*pipeline))

        results = bson_dumps(campaigns)

        return (total, results)
    

    def update_status(self, status, message):
        pass

    def start_campaign(self):
        pass

    def pause_campaign(self):
        pass

    def assign_new_prospects_by_list_id(self, list_id):
        pass

    def assign_prospects_by_id(self, ids):
        pass

    def assign_prospects_by_list_id(self, list_id):
        pass

    
    def unassign_prospects_by_id(self, ids):
        pass

    def unassign_prospects_by_list_id(self, list_id):
        pass


    def _commit(self):
        pass

    def _resume_campaing(self):
        pass

    @classmethod
    def _cache_outreach_campaigns(cls, owner_id, page, per_page=config.CAMPAIGNS_PER_PAGE):
        campaigns = []
        if page is not None:
            campaigns = models.Campaign.objects(owner=owner_id, 
                                            campaign_type__in=OUTREACH_CAMPAIGNS).skip(per_page * (page-1)).limit(per_page).order_by('-created')
        else:
            campaigns = models.Campaign.objects(owner=owner_id, 
                                            campaign_type__in=OUTREACH_CAMPAIGNS)


        for c in campaigns:
            cache = {
                'leads_total' : 0
            }

            leads = models.Prospects.objects(assign_to=c.id)
            if leads:
                cache['leads_total'] = leads.count()

            proceed = shared.TaskQueue.objects(campaign_id=c.id,
                                                proceed__ne=0)
            if proceed:
                cache['leads_proceed'] = proceed.count()

            c.cache = cache
            c._commit()

    @classmethod
    def _cache_enrichment_campaigns(cls, owner_id, page, per_page=config.CAMPAIGNS_PER_PAGE):
        campaigns = []
        if page is not None:
            campaigns = models.Campaign.objects(owner=owner_id, 
                                            campaign_type__in=ENRICHMENT_CAMPAIGNS).skip(per_page * (page-1)).limit(per_page).order_by('-created')
        else:
            campaigns = models.Campaign.objects(owner=owner_id, 
                                            campaign_type__in=ENRICHMENT_CAMPAIGNS)


        for c in campaigns:
            cache = {}

            leads = models.Prospects.objects(assign_to=c.id)
            if leads:
                cache['leads_total'] = leads.count()

            proceed = shared.TaskQueue.objects(campaign_id=c.id,
                                                proceed__ne=0)
            if proceed:
                cache['leads_proceed'] = proceed.count()

            c.cache = cache
            c._commit()
