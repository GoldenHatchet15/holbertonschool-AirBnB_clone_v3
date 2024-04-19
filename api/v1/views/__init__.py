#!/usr/bin/python3
""" Creates the app_views template"""
from flask import Blueprint

# Creates a Blueprint which the rest of our pages will run through
app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

# Must import individual files below so as not to circular import

from .states import *  # This imports the states module
from .index import *   # Assume you have some basic routes in index.py
from .cities import *  # This imports the cities module
<<<<<<< HEAD
from .amenities import *  # This imports the amenities module
from .users import *  # This imports the users module
=======
from .amenities import *

>>>>>>> 5dfb2c18c0c5a4266136785a033824051026240b
