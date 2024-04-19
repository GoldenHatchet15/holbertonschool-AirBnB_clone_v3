#!/usr/bin/env python3
import logging
from models import storage
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views
from werkzeug.security import generate_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)

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
        logging.error(f'User with ID {user_id} not found')
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        logging.error(f'Attempted to delete non-existent user with ID {user_id}')
        abort(404)
    storage.delete(user)
    storage.save()
    logging.info(f'User with ID {user_id} deleted successfully')
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    user_data = request.get_json(silent=True)
    if not user_data:
        logging.error('Failed to create user: No JSON data found')
        abort(400, description="Not a JSON")
    if 'email' not in user_data:
        logging.error('Failed to create user: Missing email')
        abort(400, description="Missing email")
    if 'password' not in user_data:
        logging.error('Failed to create user: Missing password')
        abort(400, description="Missing password")
    user_data['password'] = generate_password_hash(user_data['password'])  # Hashing the password
    new_user = User(**user_data)
    new_user.save()
    logging.info(f'New user created with ID {new_user.id}')
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        logging.error(f'Attempt to update non-existent user with ID {user_id}')
        abort(404)
    updates = request.get_json(silent=True)
    if not updates:
        logging.error('Failed to update user: No JSON data found')
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in updates.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    logging.info(f'User with ID {user_id} updated successfully')
    return jsonify(user.to_dict()), 200
