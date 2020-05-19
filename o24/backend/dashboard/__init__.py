from flask import Blueprint

bp_dashboard = Blueprint('dashboard', 
__name__, 
url_prefix='/',
template_folder='templates',
static_folder='static'
)

from o24.backend.dashboard.controllers import settings, \
                                        prospects, credentials, campaigns, lists, users, admin, \
                                        linkedin_enrichment

