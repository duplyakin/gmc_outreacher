from flask import Blueprint

bp_scheduler = Blueprint('scheduler', 
__name__, 
url_prefix='/scheduler',
template_folder='templates',
static_folder='static'
)

