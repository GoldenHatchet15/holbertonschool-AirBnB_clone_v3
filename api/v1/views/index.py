#!/usr/bin/python3
"""API endpoints for checking system status and getting statistics on stored entities."""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route("/status", methods=["GET"])
def status_page():
    """Returns a JSON response indicating the API is operational."""
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=["GET"])
def stats_page():
    """Returns a JSON response with the count of each
        type of model in the database.
        The counts are for the following
        models: amenities, cities, places, reviews, states,
        and users.
    """
    cls_to_plural = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    cls_count_dict = {key: storage.count(cls) for key, cls in cls_to_plural.items()}
    return jsonify(cls_count_dict)
