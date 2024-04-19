from . import app_views
from flask import jsonify
from models import storage, Amenity, City, Place, Review, State, User


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON object with the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each object by type."""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    counts = {cls: storage.count(cls_model) for cls, cls_model in classes.items()}
    return jsonify(counts)
