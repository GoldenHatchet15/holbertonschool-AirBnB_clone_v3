#!/usr/bin/python3
"""Module cities - handles City objects for RESTful API"""
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves list of cities in a given State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a specific City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a specific City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a new City object in a given State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_info = request.get_json()
    if city_info is None:
        abort(400, description="Not a JSON")
    if 'name' not in city_info:
        abort(400, description="Missing name")
    city_info['state_id'] = state_id
    new_city = City(**city_info)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a specific City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    updates = request.get_json()
    if updates is None:
        abort(400, description="Not a JSON")
    skip_updates = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in updates.items():
        if key not in skip_updates:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
