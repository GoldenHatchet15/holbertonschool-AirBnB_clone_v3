from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flasgger import swag_from  # type: ignore

@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/cities/get_cities.yml', methods=['GET'])
def list_cities_in_state(state_id):
    """ Retrieves the list of all City objects of a specific State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/cities/get_city.yml', methods=['GET'])
def show_city(city_id):
    """ Retrieves a specific City by its ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/cities/post_city.yml', methods=['POST'])
def create_city_in_state(state_id):
    """ Creates a new City in a given State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_info = request.get_json()
    if not city_info:
        abort(400, description="Not a JSON")
    if 'name' not in city_info:
        abort(400, description="Missing name")
    new_city = City(**city_info, state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/cities/delete_city.yml', methods=['DELETE'])
def remove_city(city_id):
    """ Deletes a City based on its ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/cities/put_city.yml', methods=['PUT'])
def update_city(city_id):
    """ Updates a City's details """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    updates = request.get_json()
    if not updates:
        abort(400, description="Not a JSON")
    skip_updates = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in updates.items():
        if key not in skip_updates:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
