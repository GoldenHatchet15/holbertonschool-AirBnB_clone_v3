#!/usr/bin/python3
"""This module instantiates an instance of the Storage will be used"""

from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()

# Importing models
from .amenity import Amenity
from .city import City
from .place import Place
from .review import Review
from .state import State
from .user import User
