from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views
from flasgger.utils import swag_from  # type: ignore


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/states/get_states.yml', methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all(State)
    return jsonify([state.to_dict() for state in all_states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/states/get_state.yml', methods=['GET'])
def get_state(state_id):
    """Retrieves a specific State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/states/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a specific State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/states/post_state.yml', methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/states/put_state.yml', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
