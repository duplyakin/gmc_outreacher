from o24.backend import db
from o24.backend import app

class Scheduler():
    def __init__(self, db, app):
        self.db = db
        self.app = app
    
    
