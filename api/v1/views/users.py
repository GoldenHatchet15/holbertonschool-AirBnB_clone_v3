# api/v1/views/users.py
from models import storage
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific User"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    user_data = request.get_json(silent=True)  # Use silent=True to handle error internally
    if not user_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in user_data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in user_data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    updates = request.get_json()
    if not updates:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in updates.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
