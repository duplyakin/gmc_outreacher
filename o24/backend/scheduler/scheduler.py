from backend import db
from backend import app

class Scheduler():
    def __init__(self, db, app):
        self.db = db
        self.app = app
    
    
