#!/usr/bin/python3
""" Module states - handles states objects for RestfulAPI """
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views
from functools import wraps

def validate_json(f):
    """ Decorator to check if incoming request is JSON """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.get_json():
            abort(400, description="Not a JSON")
        return f(*args, **kwargs)
    return wrapper

def validate_state(f):
    """ Decorator to check if state exists and load it """
    @wraps(f)
    def wrapper(state_id, *args, **kwargs):
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return f(state, *args, **kwargs)
    return wrapper

@app_views.route('/states', methods=['GET'], strict_slashes=False, endpoint='get_states')
def get_states():
    """ Retrieves list of all state objects """
    all_states = storage.all(State)
    return jsonify([state.to_dict() for state in all_states.values()])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False, endpoint='get_state')
@validate_state
def get_state(state):
    """ Retrieves a specific state by id """
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False, endpoint='delete_state')
@validate_state
def delete_state(state):
    """ Deletes a state object """
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/', methods=['POST'], strict_slashes=False, endpoint='post_state')
@validate_json
def post_state():
    """ Creates a new state object """
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>',
                    methods=['PUT'], strict_slashes=False, endpoint='put_state')
@validate_json
@validate_state
def put_state(state):
    """ Updates an existing state object """
    data = request.get_json()
    ignore_fields = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_fields:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
