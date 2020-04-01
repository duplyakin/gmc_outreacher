from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Campaign, Prospects
from o24.globals import *

class Scheduler():
    def __init__(self, db, app):
        self.db = db
        self.app = app

    def plan_campaign(self, campaign):
        if campaign.inprogress():
            raise Exception("Campaign already in progress, title={0}".format(campaign.title))
        
        prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
        


    def plan_prospect(self, prospect):


    
