from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from .states import *
# Include other imports similarly if there are more view files
