from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.states import *
# Include other imports similarly if there are more view files
