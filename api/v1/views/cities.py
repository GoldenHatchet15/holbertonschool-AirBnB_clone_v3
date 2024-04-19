#!/usr/bin/python3
"""Module states - handles state and city objects for RestfulAPI"""
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views

def validate_city(city_id):
    """Decorator to validate a city by ID."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            city = storage.get(City, city_id)
            if not city:
                abort(404)
            return func(city, *args, **kwargs)
        return wrapper
    return decorator

def validate_state(state_id):
    """Decorator to validate a state by ID."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            return func(state, *args, **kwargs)
        return wrapper
    return decorator

def validate_json(func):
    """Decorator to ensure request data is JSON."""
    def wrapper(*args, **kwargs):
        if not request.get_json():
            abort(400, description="Not a JSON")
        return func(*args, **kwargs)
    return wrapper

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
@validate_state
def get_cities(state):
    """Retrieves list of city objects by state."""
    return jsonify([city.to_dict() for city in state.cities])

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@validate_city
def get_city(city):
    """Retrieves specific city."""
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@validate_city
def delete_city(city):
    """Deletes city object."""
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
@validate_state
@validate_json
def post_city(state):
    """Creates city object in the given state."""
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    city = City(**data, state_id=state.id)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@validate_city
@validate_json
def put_city(city):
    """Updates city object."""
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
