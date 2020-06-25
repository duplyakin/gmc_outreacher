
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel
from o24.backend.google.models import GoogleAppSetting

def drop_database():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

    with app.app_context():
        db.connection.drop_database(db_name)
        print("****** HAS DROPED DATABASE")
        db.connection.close()   


def drop_database_production():
    print("GOING TO DROP PRODUCTION DATABASE ARE YOU SURE - the uncomment")
    #exit(0)

    env = os.environ.get('APP_ENV', None)
    assert env == "Production", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-prod", "ERROR: db_name. db_name={0}".format(db_name)

    with app.app_context():
        db.connection.drop_database(db_name)
        print("****** HAS DROPED DATABASE")
        db.connection.close()   
